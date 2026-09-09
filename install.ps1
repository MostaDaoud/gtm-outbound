<#
.SYNOPSIS
    Installs the gtm-outbound skill set into ~/.claude/skills/.

.DESCRIPTION
    Copies the orchestrator and its eight sub-skills as flat siblings, matching the
    layout already used by the blog, seo, and skill-forge sets on this machine.

    Existing directories are backed up rather than overwritten, so a re-install never
    silently discards local edits.

    Backups go to ~/.claude/.skill-backups/<timestamp>/, NOT alongside the skills. A
    backup left inside ~/.claude/skills/ still contains a SKILL.md, so the harness
    registers it as a real skill — producing a stale duplicate of every skill that
    competes with the live one for activation.

.EXAMPLE
    ./install.ps1
    ./install.ps1 -DestinationRoot "D:\claude-skills" -WhatIf
#>
[CmdletBinding(SupportsShouldProcess = $true)]
param(
    [string]$DestinationRoot = (Join-Path $HOME ".claude/skills")
)

$ErrorActionPreference = 'Stop'

$skills = @(
    'gtm-outbound',
    'gtm-outbound-offer',
    'gtm-outbound-list',
    'gtm-outbound-clay',
    'gtm-outbound-copy',
    'gtm-outbound-math',
    'gtm-outbound-score',
    'gtm-outbound-diagnose',
    'gtm-outbound-reply'
)

$sourceRoot = $PSScriptRoot
$stamp = Get-Date -Format 'yyyyMMdd-HHmmss'
$AgentDest = Join-Path $HOME ".claude/agents"

# Outside ~/.claude/skills on purpose -- see .DESCRIPTION.
$BackupRoot = Join-Path $HOME ".claude/.skill-backups/$stamp"

function Move-ToBackup {
    param([string]$Path, [string]$Label)
    if (-not (Test-Path $BackupRoot)) {
        New-Item -ItemType Directory -Path $BackupRoot -Force | Out-Null
    }
    Move-Item -Path $Path -Destination (Join-Path $BackupRoot (Split-Path $Path -Leaf))
    Write-Host "  backed up existing $Label -> .claude/.skill-backups/$stamp/"
}

if (-not (Test-Path $DestinationRoot)) {
    if ($PSCmdlet.ShouldProcess($DestinationRoot, 'Create skills directory')) {
        New-Item -ItemType Directory -Path $DestinationRoot -Force | Out-Null
    }
}

foreach ($skill in $skills) {
    $source = Join-Path $sourceRoot $skill
    $target = Join-Path $DestinationRoot $skill

    if (-not (Test-Path $source)) {
        Write-Warning "Missing source for '$skill' -- skipped."
        continue
    }

    if (Test-Path $target) {
        if ($PSCmdlet.ShouldProcess($target, "Back up to .claude/.skill-backups/$stamp")) {
            Move-ToBackup -Path $target -Label $skill
        }
    }

    if ($PSCmdlet.ShouldProcess($target, 'Install skill')) {
        Copy-Item -Path $source -Destination $target -Recurse
        Write-Host "  installed $skill"
    }
}

# Agents live in ~/.claude/agents, not alongside the skills.
$agentsSrc = Join-Path $sourceRoot "gtm-outbound/agents"
if (Test-Path $agentsSrc) {
    if (-not (Test-Path $AgentDest)) {
        if ($PSCmdlet.ShouldProcess($AgentDest, 'Create agents directory')) {
            New-Item -ItemType Directory -Path $AgentDest -Force | Out-Null
        }
    }
    foreach ($agent in Get-ChildItem -Path $agentsSrc -Filter *.md) {
        $target = Join-Path $AgentDest $agent.Name
        if (Test-Path $target) {
            if ($PSCmdlet.ShouldProcess($target, 'Back up existing agent')) {
                Move-ToBackup -Path $target -Label "agent $($agent.Name)"
            }
        }
        if ($PSCmdlet.ShouldProcess($target, 'Install agent')) {
            Copy-Item -Path $agent.FullName -Destination $target
            Write-Host "  installed agent $($agent.Name)"
        }
    }
}

Write-Host ""
Write-Host "Done. Installed to $DestinationRoot"
Write-Host "Restart Claude Code (or start a new session) to pick up the new skills."
Write-Host ""
Write-Host "Verify with:  /gtm-outbound math"
