"""Transcribe long audio/video files into resumable, citable WebVTT.

The script decodes one bounded span at a time, so multi-hour audiobooks do not
need to fit in memory. Completed spans are checkpointed in ``progress.jsonl``;
rerunning the same command resumes from the first unfinished span.

Requires a separate environment containing ``faster-whisper`` and PyAV.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


def file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def atomic_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(text, encoding="utf-8")
    temporary.replace(path)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def slug(value: str) -> str:
    cleaned = re.sub(r"[^a-z0-9]+", "-", value.casefold()).strip("-")
    return cleaned or "transcript"


def media_layout(path: Path, maximum_span: float) -> tuple[float, list[dict]]:
    import av

    with av.open(str(path), metadata_errors="ignore") as container:
        if not container.streams.audio:
            raise ValueError(f"media has no audio stream: {path}")
        duration = float(container.duration / av.time_base)
        chapters = list(container.chapters())

    boundaries: list[dict] = []
    if chapters:
        for chapter_number, chapter in enumerate(chapters, start=1):
            base = float(chapter["time_base"])
            start = float(chapter["start"] * base)
            end = min(duration, float(chapter["end"] * base))
            title = str(chapter.get("metadata", {}).get("title") or chapter_number)
            boundaries.append(
                {"chapter": chapter_number, "chapter_title": title, "start": start, "end": end}
            )
    else:
        boundaries.append({"chapter": 1, "chapter_title": "1", "start": 0.0, "end": duration})

    spans: list[dict] = []
    index = 0
    for boundary in boundaries:
        start = boundary["start"]
        while start < boundary["end"] - 0.01:
            end = min(boundary["end"], start + maximum_span)
            spans.append({"index": index, **boundary, "start": start, "end": end})
            index += 1
            start = end
    return duration, spans


def decode_span(path: Path, start: float, end: float, sampling_rate: int = 16000):
    import av
    import numpy as np

    chunks = []
    with av.open(str(path), metadata_errors="ignore") as container:
        stream = container.streams.audio[0]
        seek_at = max(0.0, start - 1.0)
        container.seek(int(seek_at / float(stream.time_base)), stream=stream, backward=True)
        resampler = av.audio.resampler.AudioResampler(
            format="s16", layout="mono", rate=sampling_rate
        )
        for frame in container.decode(stream):
            if frame.pts is None:
                continue
            frame_start = float(frame.pts * frame.time_base)
            frame_end = frame_start + frame.samples / frame.sample_rate
            if frame_end <= start:
                continue
            if frame_start >= end:
                break
            for output in resampler.resample(frame):
                output_start = (
                    float(output.pts * output.time_base)
                    if output.pts is not None
                    else frame_start
                )
                left = max(0, int(round((start - output_start) * sampling_rate)))
                right = min(output.samples, int(round((end - output_start) * sampling_rate)))
                if right > left:
                    chunks.append(output.to_ndarray().reshape(-1)[left:right])
    if not chunks:
        return np.empty(0, dtype=np.float32)
    return np.concatenate(chunks).astype(np.float32) / 32768.0


def read_progress(
    path: Path, source_sha256: str, model: str, spans: list[dict]
) -> dict[int, dict]:
    completed: dict[int, dict] = {}
    expected = {int(span["index"]): span for span in spans}
    if not path.is_file():
        return completed
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        try:
            item = json.loads(line)
        except ValueError:
            continue
        if item.get("source_sha256") != source_sha256 or item.get("model") != model:
            continue
        index = int(item["span_index"])
        span = expected.get(index)
        if not span:
            continue
        if abs(float(item.get("start", -1)) - float(span["start"])) > 0.01:
            continue
        if abs(float(item.get("end", -1)) - float(span["end"])) > 0.01:
            continue
        completed[index] = item
    return completed


def write_progress(path: Path, completed: dict[int, dict]) -> None:
    payload = "".join(
        json.dumps(completed[index], ensure_ascii=False, sort_keys=True) + "\n"
        for index in sorted(completed)
    )
    atomic_text(path, payload)


def vtt_clock(seconds: float) -> str:
    millis = max(0, int(round(seconds * 1000)))
    hours, millis = divmod(millis, 3_600_000)
    minutes, millis = divmod(millis, 60_000)
    secs, millis = divmod(millis, 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}.{millis:03d}"


def cues_from_segments(segments: list[dict], target_words: int = 18) -> list[dict]:
    cues: list[dict] = []
    for segment in segments:
        words = segment["text"].strip().split()
        if not words:
            continue
        parts = max(1, math.ceil(len(words) / target_words))
        duration = max(0.01, segment["end"] - segment["start"])
        for part in range(parts):
            left = part * len(words) // parts
            right = (part + 1) * len(words) // parts
            cues.append(
                {
                    "start": segment["start"] + duration * part / parts,
                    "end": segment["start"] + duration * (part + 1) / parts,
                    "text": " ".join(words[left:right]),
                }
            )
    return cues


def write_vtt(path: Path, segments: list[dict]) -> None:
    lines = ["WEBVTT", ""]
    for number, cue in enumerate(cues_from_segments(segments), start=1):
        lines.extend(
            [
                str(number),
                f"{vtt_clock(cue['start'])} --> {vtt_clock(cue['end'])}",
                cue["text"],
                "",
            ]
        )
    atomic_text(path, "\n".join(lines))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("source", type=Path)
    parser.add_argument("--model", type=Path, required=True, help="Local CTranslate2 model")
    parser.add_argument("--out-dir", type=Path, default=None)
    parser.add_argument("--device", default="cuda")
    parser.add_argument("--compute-type", default="float16")
    parser.add_argument("--language", default="en")
    parser.add_argument("--chunk-seconds", type=float, default=900.0)
    parser.add_argument("--batch-size", type=int, default=8)
    parser.add_argument("--beam-size", type=int, default=5)
    parser.add_argument("--initial-prompt", default=None)
    args = parser.parse_args(argv)

    try:
        from faster_whisper import BatchedInferencePipeline, WhisperModel
    except ImportError:
        print("error: install faster-whisper in the active Python environment", file=sys.stderr)
        return 2

    source = args.source.expanduser().resolve()
    model_path = args.model.expanduser().resolve()
    if not source.is_file() or not model_path.is_dir():
        print("error: source file or local model directory is missing", file=sys.stderr)
        return 2
    output = (
        args.out_dir.expanduser().resolve()
        if args.out_dir
        else source.parent / ".linkedin-lab-data" / "transcription" / slug(source.stem)
    )
    output.mkdir(parents=True, exist_ok=True)
    progress_path = output / "progress.jsonl"
    transcript_path = output / "transcript.vtt"
    manifest_path = output / "transcription_manifest.json"

    source_sha256 = file_hash(source)
    model_id = str(model_path)
    duration, spans = media_layout(source, args.chunk_seconds)
    completed = read_progress(progress_path, source_sha256, model_id, spans)
    manifest = {
        "schema_version": 1,
        "status": "in_progress",
        "source_path": str(source),
        "source_sha256": source_sha256,
        "duration_seconds": duration,
        "model": model_id,
        "device": args.device,
        "compute_type": args.compute_type,
        "language": args.language,
        "batch_size": args.batch_size,
        "beam_size": args.beam_size,
        "chunk_seconds": args.chunk_seconds,
        "total_spans": len(spans),
        "completed_spans": len(completed),
        "updated_utc": utc_now(),
    }
    atomic_text(manifest_path, json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")

    model = WhisperModel(model_id, device=args.device, compute_type=args.compute_type)
    pipeline = BatchedInferencePipeline(model=model)
    for span in spans:
        index = span["index"]
        if index in completed:
            continue
        print(
            f"span {index + 1}/{len(spans)} chapter {span['chapter']} "
            f"{vtt_clock(span['start'])}–{vtt_clock(span['end'])}",
            flush=True,
        )
        audio = decode_span(source, span["start"], span["end"])
        generated, _ = pipeline.transcribe(
            audio,
            language=args.language,
            batch_size=args.batch_size,
            beam_size=args.beam_size,
            temperature=0,
            condition_on_previous_text=False,
            vad_filter=True,
            without_timestamps=False,
            initial_prompt=args.initial_prompt,
        )
        segments = [
            {
                "start": span["start"] + float(segment.start),
                "end": span["start"] + float(segment.end),
                "text": segment.text.strip(),
            }
            for segment in generated
            if segment.text.strip()
        ]
        completed[index] = {
            "source_sha256": source_sha256,
            "model": model_id,
            "span_index": index,
            "chapter": span["chapter"],
            "chapter_title": span["chapter_title"],
            "start": span["start"],
            "end": span["end"],
            "segments": segments,
            "completed_utc": utc_now(),
        }
        write_progress(progress_path, completed)
        all_segments = [
            segment
            for span_index in sorted(completed)
            for segment in completed[span_index]["segments"]
        ]
        write_vtt(transcript_path, all_segments)
        manifest["completed_spans"] = len(completed)
        manifest["segments"] = len(all_segments)
        manifest["updated_utc"] = utc_now()
        atomic_text(manifest_path, json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")

    all_segments = [
        segment
        for span_index in sorted(completed)
        for segment in completed[span_index]["segments"]
    ]
    write_vtt(transcript_path, all_segments)
    manifest.update(
        {
            "status": "complete",
            "completed_spans": len(completed),
            "segments": len(all_segments),
            "transcript_path": str(transcript_path),
            "transcript_sha256": file_hash(transcript_path),
            "completed_utc": utc_now(),
            "updated_utc": utc_now(),
        }
    )
    atomic_text(manifest_path, json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps(manifest, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
