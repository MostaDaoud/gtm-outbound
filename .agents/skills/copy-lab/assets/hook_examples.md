# LinkedIn Hook Examples (Annotated Reference)

304 hooks from 26 creators, categorized by format, plus the measured width model.

## How to Use This File

- **See the format in action** with real examples of every hook format that works
- **Understand what makes each work** via the specific writing rule it demonstrates
- **Check mobile readability** using the width model below
- **Match creator voice to your brand** across different tones, industries, and content types

All hooks are exact reproductions from LinkedIn, including line breaks and formatting choices.

### Capture notation

Every entry is marked with how it was observed:

- `[visible-complete]`. the hook finished before "...more". Full text known.
- `[visible-cut]`. the hook was still running when "...more" appeared. Text shown is partial and is recorded exactly as seen, never reconstructed.
- `[both]`. we have the truncated view AND the expanded post. The most valuable entries, because they show what the reader loses.

**A `[visible-cut]` entry is not incomplete data.** The visible portion IS the hook. Everything past "...more" is post body. Treat these as first-class examples.

---

## THE WIDTH MODEL

Letters are not equal widths. The real constraint is pixel width, not character count.

### Width scoring

| Character class | Units |
|---|---|
| Narrow letters (i, l, 1, !, ., ,, ;, :, ', j, f, t, r) | 1.0 |
| Space | 1.2 |
| Common punctuation (-, (, ), ?, $, &, @, ") | 1.5 |
| Uppercase narrow (I, J, L) | 1.5 |
| Regular lowercase and digits | 2.2 |
| Uppercase regular (A-H, K, N-V, X-Z) | 2.6 |
| Wide lowercase (m, w) | 2.8 |
| Uppercase wide (M, W) | 4.0 |
| Emoji | 4.0 |

Ordinary sentence-case prose runs at about **1.75 units per character** (measured range 1.66-1.87 on real wrapped lines, 13% spread). ALL CAPS breaks this badly and must be measured directly.

### Measured budgets

| | Full line | Last visible line |
|---|---|---|
| **Mobile** | **~90 units (~50 chars)** | **~78 units (~45 chars)** |
| iPad | ~120 units | ~100 units |
| Desktop preview tools | ~135-146 units | ~120 units |
| LinkedIn's real feed | ~128 units | ~120 units |

Total mobile hook budget across three visible lines: **~258 units (~147 characters)**.

The last visible line is smaller because "...more" sits on it, taking roughly 12-15 units.

### Two findings that change how you work

**1. No preview tool matches LinkedIn.** Measured across three separate tools, desktop previews render at 135, 145 and 146 units per line. LinkedIn's real feed renders at ~128. A hook can pass in every preview and still wrap in the feed. Compose against mobile; treat previews as decorative.

**2. The cut zone is characters 40 to 70.** Mobile cuts near 42, desktop near 66. You cannot control where inside that range the cut lands, so a trailing line must stay interesting across the whole zone.

### Model validation

The model was validated against Matt Barker's repost hook, observed simultaneously in the real feed and in a preview tool at three widths:

`Last month I copy and pasted a few of my best posts from last year and reposted them. 2 of them did over 249,000 impressions combined. I'll be honest, I felt a bit dirty doing it.` (179 chars / 309 units)

| Layout | Budget | Predicted | Observed |
|---|---|---|---|
| Mobile | 258u | cut | cut at "I'll be hones" ✓ |
| iPad | 340u | fits | fits ✓ |
| Preview desktop | 404u | fits | fits ✓ |
| LinkedIn real feed | 376u | fits | fits ✓ |

Four for four. This hook reads perfectly on every surface except the one where most people see it. The confession that justifies the whole post sits past the mobile cut.

---

## FORMAT 1: DENSE

Dense hooks pack multiple facts, stakes, and proof into continuous text with no line breaks. Best for technical audiences, data-driven claims, and proof-heavy content.

**Target: 140-160 characters (~245-280 units).** Deliberate cliffhanger variants run shorter, around 130-140 characters, ending on a colon or dangling setup.

### Diandra Escobar

**Hook 1:** `[visible-complete]`
I built an AI agent that catches the latest news in REAL time, drafts a post + delivers it to our team overnight. One client hit 200K impressions from it. And I'm showing you exactly how to build it.
> Rule 4 (specific numbers as credibility anchors) + Rule 2 (promise-then-payoff)

**Hook 2:** `[visible-complete]`
I started YouTube 6 weeks ago. Since then I've had 20k+ views, 803 hours of watch time and gained 1k+ subs. Here's what I've learned:
> Rule 4 (time + metric combo) + Rule 13 (before/after proof in one sentence)

**Hook 3:** `[visible-complete]`
I've been talking about the LinkedIn algorithm changes for MONTHS NOW. But until THIS WEEK, the only real detail came from arXiv research papers published by LinkedIn's AI team.
> Rule 8 (pattern interrupt via capitalization) + Rule 6 (contrast frame)

**Hook 4:** `[visible-complete]`
We work with founders and executives on their LinkedIn content every day. And over the past year, ONE content type has been underperforming across ALL of them.
> Rule 36 (authority via client roster) + Rule 8 (repetition: "ONE" and "ALL")

**Hook 5:** `[visible-complete]`
I went through all 9 pages of LinkedIn's Algorithm research paper so you don't have to. (watch this if your reach dropped)
> Rule 3 (immediate time value) + Parenthetical Type B (reader-pain callout)

**Hook 6:** `[visible-complete]`
Someone paid a LinkedIn "guru" $15k/month. After 3 months of motivational quotes and sunset graphics with zero CTAs… their leads dropped 22%.
> Rule 4 (dollar figure as stakes) + Rule 2 (setup-result structure)

**Hook 7:** `[visible-complete]`
I started posting on LinkedIn at 22 with zero clients and zero proof. The only useful thing I owned was a feed full of people already doing what I wanted.
> Rule 21 (anti-hype origin) + Rule 3 (reader-first: the have-nothing starting point)

**Hook 8:** `[both]`. 142,481 impressions, her strongest hook
My boyfriend wrote a post by hand at the airport. NO WIFI = NO AI. I read it back and said "sounds so much like AI" ... He'd written every word himself.
> 267 units against a 266 mobile ceiling. Fills the visible space almost exactly.
> Rule 39 (scene-setting) + Rule 12 (reframe: the accusation lands on the human)

**Hook 9:** `[visible-complete]`
A LinkedIn post with 100 reactions gets cited by AI at the SAME RATE as one with 10,000. Followers don't matter. 3 things do, and one almost nobody does.
> Rule 2 (counterintuitive data lead) + Rule 7 (tension: names the count, withholds the items)

**Hook 10:** `[visible-complete]`
I spent my birthday in Medellín with people who drank ginger shots to make me feel loved. Nine hours, no alcohol, and the best conversations of my year.
> Rule 39 (scene-setting) + specific sensory detail over sentiment

**Hook 11:** `[visible-complete]`
The most impressive thing AI has done for me isn't writing... It's letting someone non technical like me build the thing in my head, even without code.
> Rule 25 (identity disclaimer flip) + Rule 12 (reframe)

**Hook 12:** `[both]`. measured across Kleo mobile/tablet/desktop
My LinkedIn stack has one job: turn content into pipeline. Here's what I run. & the one tool I found that connects the ORGANIC side to the PAID side.
> 263 units against a 266 ceiling. Teaching example for filling the mobile budget.

**Hook 13:** `[visible-cut]`
Someone with less credentials than you is becoming the name everyone in your industry knows. The only difference is they post and you
> Rule 3 (reader-first sting) + trailing mode: cut lands on "and you", pronoun awaiting its verb

**Hook 14:** `[visible-cut]`
3 weeks of LinkedIn posts. That's all it took before this client's exact buyers started signing up to the product they launched a few
> Rule 4 (compressed timeframe) + trailing mode

**Hook 15:** `[both]`. measured across a preview tool at three widths
I built a free Claude skill (I ACTUALLY USE EVERY DAY) that writes your LinkedIn hook in 4 proven formats, flags the hookable lines already sitting inside your draft, and checks it fits above see more on mobile
> 370 units. Overruns every layout. Included as a counter-example: still reached 23,642, but the reader never sees the third benefit.

**Hook 16:** `[visible-complete]`
Call LinkedIn cringe all you want. But when I see people like Neza Lupsina, I think LinkedIn is fckn cool.
> Rule 12 (reframe) + tagged mention drawing the eye

**Hook 17:** `[visible-complete]`
We were sold the idea that posting is the only thing standing between us and winning on LinkedIn. But posting is just ONE link in a chain.
> Rule 12 (reframe) + Rule 8 (single capped word)

**Hook 18:** `[visible-complete]`
A client of ours pulled 824k impressions from 4 LinkedIn posts in 3 months. There's a reason I won't shut up about the 4 buckets, and this is it:
> Rule 4 + deliberate colon cliffhanger

**Hook 19:** `[visible-complete]`
Marketers' new moral stance is never gating content. I gated every resource I have, and 2 months later my newsletter sits at 3,8k subscribers, 43% open rate and 8.9% click rate.
> 311 units, overruns mobile. Rule 6 (contrarian) but the proof lands past the cut.

**Hook 20:** `[visible-complete]`
Business class to China. 103th floor hotel suite in one of the tallest towers on earth. Speaking to a mastermind of 7 to 9-figure founders... But 3 years ago:
> 269 units. Rule 42 (inline before/after) + colon cliffhanger

**Hook 21:** `[visible-complete]`
The longer I work in high-stress industries, the more I obsess over one thing: my environment. After 9+ countries in 6 months, I'm convinced your surroundings shape your output more than your discipline
> 358 units, overruns badly. Counter-example: still reached 20,955, but the claim is invisible on mobile.

### Adam Robinson

**Hook 22:** `[visible-complete]`
Worst ways to build wealth- thinking a $100M valuation means you have $100M
> Rule 4 (large numbers) + myth-busting frame

**Hook 23:** `[visible-complete]`
Dharmesh (Founder + CTO of Hubspot) is right  -  nobody's going to vibe code Hubspot. Want to know why SaaS stocks are getting smoked? I'll tell you why.
> Rule 36 (authority name-drop) + Rule 18 (question then promise)

**Hook 24:** `[visible-complete]`
Last week I was at an 8-person founder breakfast in Aspen. Guy goes around the table and asks everyone how they're using AI day-to-day. I was super embarrassed to answer the question, but I did.
> Rule 39 (scene-setting) + Rule 21 (vulnerability)

**Hook 25:** `[visible-complete]`
I want to be crystal clear: the advice I give on LinkedIn is NOT for founders who think they're creating unicorns, decacorns, or the next Anthropic.
> Rule 24 (audience segmentation via exclusion)

**Hook 26:** `[visible-complete]`
This is the only cold email I answered in the last 12 months. Here's why it worked on me:
> Rule 4 (superlative + timeframe) + colon promise

**Hook 27:** `[visible-cut]`
It pisses me off when founders act like the fact that I am running my business to make money is some kind of low brow pursuit. Making money is the point! You don't need to change the world. The goal is
> Rule 6 (contrarian) + trailing mode

**Hook 28:** `[visible-cut]`
$10M ARR is the FU MONEY of SaaS. At $10M ARR bootstrapped, you and your co-founder clear
> Rule 4 (specific milestone) + trailing mode, verb awaiting its object

**Hook 29:** `[visible-cut]`
After the founder of Twitch (Justin Kan) sold his company to Amazon for $1 billion, an interviewer asked him, "Don't you think you won the lottery?" His answer was the best description of being a founder
> Rule 36 (name-drop) + Rule 39 (narrative setup)

### Alicia Teltz

**Hook 30:** `[visible-complete]`
Your impressions dropped because LinkedIn is thinking 10 years into the future. As an ex-LinkedIn employee, here's my prediction:
> Rule 36 (insider credential) + Rule 3 (reader pain first, credential second)

### Anthony Pierri

**Hook 31:** `[visible-complete]`
You'll know your positioning is working if all your sales calls start sounding the same.
> Rule 20 (outcome signal: tests rather than teaches)

**Hook 32:** `[visible-complete]`
Hot Take: most startups should only use one GTM channel until they're making at least $2m ARR.
> Rule 17 (label opener) + Rule 4 (specific milestone)

**Hook 33:** `[visible-complete]`
AI can get you 80%-90% of the way there but it's that last ten percent of full control that makes the difference.
> Rule 4 (percentage breakdown) + Rule 12 (reframe)

**Hook 34:** `[visible-complete]`
If I had a dollar for every hour I've spent thinking about "use cases," I'd have at least $1000
> Rule 21 (self-deprecating) + familiar phrase twisted

**Hook 35:** `[visible-cut]`
Why do we pay copywriters in our agency when we could just use AI? Because AI still cannot…
> Rule 18 (question then incomplete answer). The reader's brain completes the sentence.

### Cam Trew

**Hook 36:** `[visible-cut]`
We are staring at the BIGGEST opportunity since ChatGPT and the dot-com era. If you're seeing this right now, you're ahead of 99% of
> Rule 24 (exclusive audience) + Rule 8 (caps) + trailing mode

### Emily Kramer

**Hook 37:** `[visible-complete]`
I did a 90 min Zoom with my dad and his friend (both in their 70s, both ex-software engineers) to show them how I've been using Claude Code. At their request.
> Rule 39 (specific scene + characters) + Parenthetical Type A

**Hook 38:** `[visible-complete]`
I just spent ~100 hours over 2 weeks in Claude Code & writing a 5,000-word Claude Code newsletter.
> Rule 4 (time + word count proof)

**Hook 39:** `[visible-complete]`
I just wrote a newsletter for the 90% of marketers who don't have 15 agents running and aren't living inside Claude Code all day.
> Rule 24 (audience targeting via exclusion)

### Filipa Canelas

**Hook 40:** `[visible-complete]`
UPDATE: LinkedIn's NEW algorithm is out… and it just became the biggest opportunity for B2B marketing.
> Rule 17 (label opener: "UPDATE") + superlative

**Hook 41:** `[visible-complete]`
NEWS: YouTube just overtook Reddit as the #1 source cited by LLMs. LinkedIn's mentions are still growing (sitting at #4 for Google AI Overview).
> Rule 17 (label opener: "NEWS") + Rule 4 (ranked statistics)

### Jake Ward

**Hook 42:** `[visible-complete]`
We lost sleep over ChatGPT stealing SEO traffic, but what if Google is the real threat?
> Rule 12 (the reframe hook: hijacks existing anxiety, redirects it)

**Hook 43:** `[visible-complete]`
I built 13,000+ pages with AI in 3 hours and grew my SEO traffic by +466% 60 days later.
> Rule 4 (scale) + Rule 13 (time + result metric)

**Hook 44:** `[visible-cut]`
I went offline for 3 days, but returned to see my business ALL OVER the LinkedIn feed…
> Rule 8 (caps) + ellipsis cliffhanger

### Kyle Atwater Morley

**Hook 45:** `[visible-complete]`
Someone on Reddit called your product "overpriced" three years ago. That opinion is now showing up in Google AI Overviews as if it's fact. And the thing is: this is happening constantly and most brands have no idea.
> Rule 3 (reader pain) + emerging threat most miss

### Lara Acosta

**Hook 46:** `[visible-complete]`
I'm scared. In less than 3 hours I'm exposing every single "new" LinkedIn algorithm claim LIVE.
> Rule 19 (real-time urgency) + Rule 21 (emotional openness)

### Leigh McKenzie

**Hook 47:** `[visible-complete]`
A lot of AI citation research is being misread right now, and it's costing marketers real strategic clarity.
> Rule 3 (reader pain) + correcting a common mistake

**Hook 48:** `[visible-complete]`
If you're an even slightly technical SEO, you need to be paying attention to WebMCP.
> Rule 24 (niche targeting)

**Hook 49:** `[visible-complete]`
Over two weeks at Backlinko, we reverse-engineered how AI systems decide which brands to recommend. The findings fundamentally changed how I think about SEO.
> Rule 36 (authority credential) + methodology proof

**Hook 50:** `[visible-complete]`
If you're leading SEO in 2026, here's a practical playbook I'm seeing work: simple, repeatable, and measurable.
> Rule 24 (role targeting) + current-year relevance

**Hook 51:** `[visible-complete]`
Over the last two years, the loudest voices in marketing have been confidently wrong about how AI is reshaping search.
> Rule 6 (myth-busting: experts are wrong)

### Liam Fallen

**Hook 52:** `[visible-cut]`
I know this is a small win compared to others on LinkedIn but… 109 people have joined my marketing community in the first 3
> Rule 21 (humility) + Rule 4 (specific number) + trailing mode

### Magali De Reu

**Hook 53:** `[visible-complete]`
12 months of LinkedIn got me 12,189,119 impressions. But the biggest spike didn't come from using "viral templates". It came from this:
> Rule 4 + colon cliffhanger. 231 units, deliberately short.

**Hook 54:** `[visible-complete]`
By 26, I'd been fired 3 times. By 36, I called BS on a toxic founder. On paper, I'm the problem. In reality, the paper's 100% correct:
> Rule 42 (inline age progression) + Rule 41 (self-interrogation)

**Hook 55:** `[visible-complete]`
I NEVER thought I'd meet LinkedIn's top creators and have them all instantly hate me:
> Rule 8 (single capped word) + colon cliffhanger

**Hook 56:** `[visible-complete]`
Last year, nobody knew my damn name. Last WEEK, Lara Acosta invited me to her launch event in London:
> Rule 42 (inline before/after inside Dense) + tagged mention

**Hook 57:** `[visible-complete]`
Last week, 12 solopreneurs paid me $18,496 to join my community. I was LOSING MY MIND. Then I saw who joined and burst into tears:
> Rule 4 (specific dollar figure) + emotional reversal

**Hook 58:** `[visible-complete]`
I REFUSE to build a 7-figure agency. I don't even have a VA. Unscalable? Nah. I'm f*cking irreplaceable:
> Rule 41 (self-interrogation: raises the objection and kills it in four words)

**Hook 59:** `[visible-complete]`
365 days ago, I came to LinkedIn to save my business. 478 posts later, I finally see it was ME who needed saving.
> Rule 42 (inline before/after) + Rule 12 (reframe)

**Hook 60:** `[visible-complete]`
I'm 36. A woman, ADHD, and ambitious as f*ck. But I'll NEVER be a mom. I've got something worse to parent:
> Rule 16 (personal specifics) + colon cliffhanger

**Hook 61:** `[visible-complete]`
"Women are too emotional for business", my last boss said to my face. So I sent him the most emotional exit email of his life:
> Sub-variant 2G (quoted ANTAGONIST) + retaliation promise

**Hook 62:** `[visible-complete]`
In 11 months, I've made $480K from LinkedIn. This is where I say 'it's not about the money,' right? Except I'm not full of sh*t:
> Rule 41 (self-interrogation) + meta self-awareness

**Hook 63:** `[visible-complete]`
Holy sh*t, there's 40,000 of you. Best year of my career, easily. So why the hell am I losing all my friends?
> Rule 21 (vulnerability paired with achievement in the same breath)

### Matt Barker

**Hook 64:** `[visible-complete]`
Shout out to everyone posting on LinkedIn with less than 500 followers and no engagement. I know the feeling. I'm in year 4 posting on this beautiful hellhole we call linkedin. 2,600+ posts.
> Rule 33 (acknowledgment) + Rule 4 (massive stat)

**Hook 65:** `[visible-complete]`
I'm a 32 year old founder. I run a solo, $400k/year writing business. But I still don't have it all figured out:
> Rule 4 (revenue proof) + Rule 21 (vulnerability)

**Hook 66:** `[visible-complete]`
Last week I was on Zoom with a software engineer. He posts regularly on LinkedIn. Knows his stuff. But when I asked him what felt hardest about writing he didn't hesitate:
> Rule 39 (scene-setting dialogue) + colon cliffhanger

**Hook 67:** `[both]`. model validation example, see Width Model above
Last month I copy and pasted a few of my best posts from last year and reposted them. 2 of them did over 249,000 impressions combined. I'll be honest, I felt a bit dirty doing it.
> **COUNTER-EXAMPLE.** 179 chars / 309 units. Works on desktop, tablet and the real feed. Fails on mobile, where the confession that justifies the post sits past the cut. Also contains a banned phrase; recorded verbatim as observed data, never to be generated.

**Hook 68:** `[visible-cut]`
Last week I had 4 posts hit 25k+ impressions. I'm actually finding it easier to get impressions than ever right now. Here's what you need to
> Rule 4 + trailing mode

**Hook 69:** `[visible-complete]`
2 weeks ago I watched Obsession. It's probably the best horror movie I've seen in years. But it cost just $750k to make. Here's 4 lessons Obsession teaches us about building an audience with content:
> Rule 39 (unexpected subject) + Rule 4 (cost contrast)

**Hook 70:** `[visible-complete]`
I've closed around $1.5M revenue for my one person business over the last 5 years. But I still do outreach. And I'm shocked at how many people are dismissive or arrogant towards it.
> Rule 36 (result credential) + Rule 6 (contrarian practice)

**Hook 71:** `[visible-complete]`
On December 7th 2025, I predicted that video on LinkedIn will still be shit. So far, 7 months in, I'm right.
> Rule 4 (dated prediction) + verified callback

**Hook 72:** `[visible-complete]`
3 years ago I set up an account with a boring tool called ThriveCart. All it does is take payments. But it's been partly responsible for $432,658.42 in revenue:
> Rule 4 (absurdly precise figure) + "boring" framing lowering expectation before the reveal

**Hook 73:** `[visible-complete]`
I give feedback on 20+ LinkedIn posts every week inside my writing community, Your Next Post. Here's some signs I know a post was cooked up by AI:
> Rule 36 (result credential) + colon promise

**Hook 74:** `[visible-complete]`
I'm 33 years young. I'm in year 5 of running a one person business. Here's where I imagine I'll be in year 10:
> Rule 16 (personal numbers) + forward projection instead of retrospective

**Hook 75:** `[visible-complete]`
I'm 75% English. 25% Irish. Married to Armenian. Live in Cyprus. I'm a girl dad. I run a one person business that made $353k in 2025. It's on pace to hit $300k again this year.
> Staccato identity stack inside Dense. Seven facts, no connectives.

### Ruben Hassid

**Hook 76:** `[visible-complete]`
So I always hated the word "agent". And even if I have 800,000 (!! wtf) people reading my newsletters every week on 'How to AI', I barely use the word.
> Rule 6 (contrarian) + Parenthetical Type A used as a self-interrupting aside

**Hook 77:** `[visible-complete]`
I (literally) spent 1000 hours figuring out Claude the hard way. Here are the guides I wish someone had sent me earlier to read:
> Parenthetical Type A + Rule 4 (hours as proof)

**Hook 78:** `[visible-complete]`
I absolutely hate AI writing. And my entire job is to write about AI. So I keep a file of the new em-dash to recognize AI writing instantly:
> Rule 22 (contrast between two sentences) + colon promise

**Hook 79:** `[visible-cut]`
It's crazy how my entire Linkedin feed is about Claude but no one actually properly explains it. I made this quick note for my team on how to
> Rule 3 (names a shared frustration) + trailing mode

**Hook 80:** `[visible-complete]`
If you are not paying for a Claude subscription, DO NOT use Claude. I know how that sounds coming from me.
> Rule 8 (short caps as alarm) + Rule 31 (pre-empts the skepticism inside the hook)

---

## FORMAT 2: PUNCHY + CONTEXT

Line 1 is a short, high-impact claim. Blank line. Line 2 is the rehook.

**Line 1: ≤50 chars. Line 2: ≤45 chars in landing mode, unlimited in trailing mode subject to the cut-zone test.**

### Diandra Escobar

**Hook 1:** `[visible-complete]`
I BLEW up my boyfriend's content.

(+1M impressions, +2K followers / EVERY MONTH)
> Sub-variant C (strategic caps) + Parenthetical Type C

**Hook 2:** `[visible-complete]`
LinkedIn was booking calls. Then we added two more channels.

Leads went from good to insaneeee.
> Word elongation as tone marker

**Hook 3:** `[visible-cut]`
I never expected a LinkedIn account to CHANGE my life.

And I almost didn't start… I swore I wasn't enough. (I actually only did because I was heartbroken and felt I had nothing left to lose)
> Rule 21 (vulnerability) + trailing mode

**Hook 4:** `[visible-complete]`
If you want true inbound from LinkedIn: EVERY SINGLE post needs a JOB.

This four-bucket funnel is how I build six-figure pipelines from content.
> Rule 8 (caps) + concrete system named

**Hook 5:** `[visible-complete]`
I built an AI agent that helps us write viral LinkedIn posts.

Before you roll your eyes… let me explain.
> Rule 31 (pre-empts the objection inside the hook)

**Hook 6:** `[visible-cut]`
Sara and I will be on stage together for the FIRST TIME.

March 26 at the FullFunnel.io Summit, and we're going in on…
> Rule 19 (event urgency) + trailing mode

**Hook 7:** `[visible-complete]`
Stop telling Claude "write me a LinkedIn post about X."

Build this instead:
> Sub-variant F (negation into prescription). Recorded as published.

**Hook 8:** `[visible-complete]`
POV: You believed in yourself, started posting on LinkedIn.

And went from first podcast in 2022 to keynote speaker in 2026.
> Rule 17 (label opener: POV) + Rule 13 (compressed timeline)

**Hook 9:** `[visible-complete]`
My brand new YouTube channel just hit 4.6k views.

But the views aren't the interesting part…
> Downplaying the metric to create the gap

**Hook 10:** `[visible-complete]`
A $20K/month client found me through LinkedIn.

But not how you think.
> Rule 4 (dollar proof) + expectation subversion in four words

**Hook 11:** `[visible-complete]`
"I REPLACED MY TEAM WITH 40 AI AGENTS" is a scam.

Sara and I have been interviewing top marketers for months.
> Sub-variant 2G (quoted claim as target) + Rule 36 (authority)

**Hook 12:** `[visible-complete]`
361 comments. 214 reposts. 206,834 impressions.

From a founder nobody had heard of 3 months ago.
> Rule 4 (stacked metrics) + Rule 13 (unknown to viral)

**Hook 13:** `[visible-complete]`
Three years ago, nobody knew our names.

Saturday, we were all in one room in London.
> Rule 13 (compression) + concrete place detail

**Hook 14:** `[visible-complete]`
One Instagram post got me to 10k followers.

That's my flex that'll hook you. It's not the number that matters
> `[both]` measured across Kleo at three widths. Trailing mode: line 2 cuts at "It's not the nu" on mobile.

**Hook 15:** `[visible-complete]`
The best LinkedIn tool has ZERO VC money.

Built by people who post here for a living.
> Sub-variant C (strategic caps) + credibility through constraint

**Hook 16:** `[visible-complete]`
The first line of your LinkedIn post is doing all the damage.

(40 writing rules and 131 hooks later, I built a fix.)
> Rule 3 (reader-first diagnosis) + Parenthetical Type C

**Hook 17:** `[visible-complete]`
A $70M founder got single-digit likes posting solo.

Expertise and attention are two COMPLETELY different
> Rule 4 + trailing mode, adjective awaiting its noun

**Hook 18:** `[visible-complete]`
I outranked my country's vice president.

I was getting tagged over the week and went to see what it was.
> Rule 4 (unexpected comparison) + 78,274 impressions

**Hook 19:** `[visible-complete]`
We run LinkedIn for billion dollar executives.

On July 23 I'm showing the AI side, live.
> Rule 36 (result credential) + Rule 19 (dated event)

**Hook 20:** `[visible-complete]`
I run my entire business from a 14-inch laptop.

My small screen opened up a big world.
> Rule 16 (concrete personal detail) + Rule 22 (contrast)

**Hook 21:** `[visible-complete]`
One face in your head is stopping you from posting.

You know exactly who it is.
> Rule 35 (mirror hook). Text-only post, no media.

**Hook 22:** `[visible-complete]`
I broke three teeth in Amsterdam.

And that's the most normal thing that happened all week.
> Rule 7 (tension) + escalation implied, not stated

**Hook 23:** `[visible-complete]`
I cut 6 tools from my content stack.

(Now I publish more, in less time)
> Parenthetical Type C

**Hook 24:** `[visible-complete]`
Your LinkedIn industry field is probably wrong.

And it's deciding who sees your posts.
> Rule 3 (reader-first) + stakes revealed in line 2

**Hook 25:** `[visible-complete]`
You can go viral and still go broke.

Most platforms aren't built to turn followers into paying clients.
> Rule 22 (the period is load-bearing) + Rule 6 (contrarian)

**Hook 26:** `[visible-complete]`
LinkedIn users begged for features for years.

Now they're shipping them like hotcakes. (9 this month.)
> Parenthetical Type B (specificity closing line 2). Published with a leading emoji; recorded without, per default rules.

**Hook 27:** `[visible-complete]`
"I don't know how to grow on LinkedIn anymore"

Start at level 1 of the 2026 LinkedIn game:
> Sub-variant 2G (quoted READER objection) + colon promise

**Hook 28:** `[visible-complete]`
We're HIRING! (share this)

If you live and breathe Instagram, this might be for you.
> Recruitment post type. Parenthetical Type B doing share-request duty.

**Hook 29:** `[visible-complete]`
I can't stop thinking about this Tweet.

On LinkedIn, you're alwaysssss days late.
> **Portable template** (Rule 43). Also used by Cam Trew with a different line 2.

**Hook 30:** `[visible-complete]`
If you're in Amsterdam on July 2nd, this is for you!

One session, ALL on LinkedIn pipeline. I'm live at Unmuted
> Rule 24 (geographic segmentation). Published with a leading pin emoji.

### AJ Eckstein

**Hook 31:** `[visible-complete]`
I flew 11 employees to Texas for our first ever company offsite.

But we treated this like a brand trip over a corporate work trip.
> Rule 4 (scale) + expectation inversion

### Alicia Teltz

**Hook 32:** `[visible-complete]`
I spend $5,766/month to run my business

PLEASE tell me where I'm wasting my money
> Rule 4 (precise figure) + vulnerability as engagement request

**Hook 33:** `[visible-complete]`
I'm ex-LinkedIn, and the algorithm just changed AGAIN.

Here's what you need to know, confirmed by LinkedIn.
> Rule 36 (insider credential) + official confirmation

**Hook 34:** `[visible-complete]`
From invisible to invited by Google...

And it all happened because I got over the CRINGE.
> Rule 13 (compression) + Rule 21 (naming the emotional barrier)

**Hook 35:** `[visible-complete]`
I quit my $250k job at LinkedIn for freedom.

What I actually built was a prison.
> Rule 22 (the period is load-bearing) + Rule 12 (reframe)

### Anthony Pierri

**Hook 36:** `[visible-cut]`
AI "hallucinating" is not the same as humans "making mistakes."

If an employee produces a report with 100% made up...
> Rule 12 (reframe) + trailing mode

**Hook 37:** `[visible-complete]`
You probably have TOO many engineers at your startup.

And your product is probably TOO big.
> Rule 6 (contrarian) + Rule 8 (repeated capped word)

**Hook 38:** `[visible-cut]`
Most positioning problems are caused by undisciplined product strategy.

Adding features can be a great thing…
> Rule 12 (root cause) + ellipsis cliffhanger

**Hook 39:** `[visible-complete]`
Something that should be obvious (but isn't):

People need to know WHAT your product is before they'll want to buy it
> Rule 23 (the "(but isn't)" gap between knowing and doing)

**Hook 40:** `[visible-complete]`
Marketing agencies that follow Fletch, this is for you

(normies, keep scrolling)
> Rule 24 (segmentation) + Parenthetical Type C

**Hook 41:** `[visible-complete]`
We just sent the very first Fletch newsletter ever.

I'm putting it here, so it's likely not a single person will see this
> Rule 21 (anti-hype). The opposite of how launches are usually announced.

### Beatrice Vladut

**Hook 42:** `[visible-complete]`
My high school teacher told me I'd never speak English.

Today I work, think, and dream in English.
> Rule 37 (external prediction + personal override)

### Cam Trew

**Hook 43:** `[visible-complete]`
Anthropic is in DEEP trouble.

(And it's worse than you think)
> **The formula.** Line 1: exactly one capped word. Line 2: parenthetical opening "(And". Observed 8/8 times.

**Hook 44:** `[visible-complete]`
Google just changed the AI agent race forever.

(The OpenClaw vs Claude debate is OVER)
> Same formula, escalating variant

**Hook 45:** `[visible-complete]`
OpenAI is in SERIOUS trouble.

(And they may not come back from this)
> Same formula

**Hook 46:** `[visible-complete]`
This man built the most FAMOUS AI agent on earth.

(And most people don't know who he is)
> Same formula + Rule 6 (contrarian: unknown fame)

**Hook 47:** `[visible-complete]`
Everybody is IGNORING this with OpenClaw vs Claude.

(And I honestly find it hilarious)
> Same formula, personal-reaction variant

**Hook 48:** `[visible-complete]`
Stop calling everything an OpenClaw killer…

NOTHING stands a chance, and here's why:
> Sub-variant F (negation into prescription) + Rule 8

**Hook 49:** `[visible-complete]`
Everybody is talking about Mac Minis with OpenClaw.

(But nobody is explaining why… SO I WILL):
> Formula with "(But" variant

**Hook 50:** `[visible-complete]`
AI companies are LYING to you.

Let me explain:
> Rule 8 (caps) + minimal line 2

**Hook 51:** `[visible-complete]`
You can CLONE your best employee with Claude Skills.

Here's how it works (save this):
> Parenthetical Type B (save instruction)

**Hook 52:** `[visible-complete]`
OpenAI is bleeding billions annually.

(Here's why AI companies make no money)
> Formula, systemic-claim variant

**Hook 53:** `[visible-complete]`
Every business NEEDS to become an AI company.

(And a SHOE brand just proved it)
> Formula. Two capped words across the hook, one per line.

**Hook 54:** `[visible-complete]`
Everybody without an AI agent is falling BEHIND.

(And starting is easier than you think)
> Formula, reassurance variant

**Hook 55:** `[visible-complete]`
Anthropic just dropped something BIG.

(And it's impressive... but I still won't use it)
> Formula, self-undercutting variant. Line 2 contradicts the excitement of line 1.

**Hook 56:** `[visible-complete]`
Anthropic built the most DANGEROUS AI ever made.

(And they're refusing to release it)
> Formula

**Hook 57:** `[visible-complete]`
Releasing my first YouTube video was SCARY.

(But at least it's about my favourite thing)
> Formula applied to personal content rather than news

**Hook 58:** `[visible-complete]`
I used to recommend Claude to everyone.

Now I find myself hating it more every day.
> Rule 34 ("I used to think X. But...") applied to a product. **790 comments**, the highest engagement in the dataset. The format invites argument.

**Hook 59:** `[visible-complete]`
I'm 28 with 2 businesses and no home.

All of this 'happened' in the last year.
> **Portable template** (Rule 43). Jake Ward posted the same structure with 4 businesses.

**Hook 60:** `[visible-complete]`
I ranked 12 AI tools from S to F.

This will upset some of you:
> Tier-list post type + Rule 7 (promised conflict)

**Hook 61:** `[visible-complete]`
I just lived through my worst nightmare.

And that was exactly the point...
> Rule 7 (tension) + ellipsis

**Hook 62:** `[visible-cut]`
5 months ago, I started taking my health seriously.

I'm a computer nerd... so let's just say it was a shock to the
> Rule 21 (self-deprecating) + trailing mode

**Hook 63:** `[visible-complete]`
It's FINALLY happening.

16-hour days for 60 days straight has got us to this point.
> Deliberate asymmetry: 43 units against 100. The short line punches, the long one explains.

**Hook 64:** `[visible-complete]`
I had $150k of LinkedIn training from the top 1%.

And here's what happened:
> Rule 4 (investment as proof) + colon promise

**Hook 65:** `[visible-complete]`
Next month, I'm doing something I said I'd never do.

As a tech nerd it's literally my worst nightmare...
> Rule 7 (self-contradiction as tension)

**Hook 66:** `[visible-complete]`
I tried every major AI agent to see which ones are worth your time.

Here's what I found:
> Reverse asymmetry: 117 units against 35. Long setup, short payoff line.

**Hook 67:** `[visible-complete]`
Yes... AI is making software cheaper than ever.

But it's also doing something else:
> Concession then pivot + colon cliffhanger

**Hook 68:** `[visible-complete]`
POV: you quit your 9-5 Software Engineering job to start a business.

Ten months ago, my life looked completely different.
> Rule 17 (label opener) in second person

**Hook 69:** `[visible-complete]`
Don't cry about Fable 5 getting banned...

Instead, build your own AI brain for free.
> Sub-variant F (negation into prescription)

**Hook 70:** `[visible-complete]`
I have absolutely no idea if this is going to work...

But I'm going to do it anyway. I CHALLENGE you:
> Rule 21 (admitting uncertainty) + direct challenge

**Hook 71:** `[visible-complete]`
The US government banned Claude Fable 5.

And it's so ironic it hurts...
> News lead + withheld irony

**Hook 72:** `[visible-complete]`
Claude Fable 5 is by far the best AI model to ever exist.

But honestly, I've got mixed feelings about it.
> Superlative then immediate qualification

**Hook 73:** `[visible-cut]`
I can't stop thinking about this Tweet.

Everyone's building an AI company. But most don't realise
> **Portable template** (Rule 43), same opener as Diandra Hook 29 with a different line 2. Trailing mode.

**Hook 74:** `[visible-complete]`
I just hit 20,000 followers on LinkedIn.

6 months ago I'd have told you it was impossible.
> Rule 13 (compression) + Rule 21

**Hook 75:** `[both]`. see List Preview note
Okay, let me get this straight...

1. You can build a fully functional web app with Lovable or
> **Sub-variant E (List Preview), trailing mode.** Line 2 is 59 chars, over the landing cap, and works because it is designed to be cut. Passes the cut-zone test at both 42 ("web app w", with what?) and 66 ("or Base44 b", by what?).

### Emily Dunlop

**Hook 76:** `[visible-cut]`
I used to think fear was a warning.

But after nearly two years of building, creating and putting…
> Rule 34 ("I used to think X. But...")

**Hook 77:** `[visible-cut]`
22 months ago I had zero followers and a job I'd fallen out of love with.

Now I run a business helping founders build brands that feel like…
> Rule 13 (zero to business)

**Hook 78:** `[visible-complete]`
You know what's holding you back.

I do too.
> Rule 35 (the mirror hook). Five words, and the reader feels seen.

**Hook 79:** `[visible-complete]`
Everyone's selling you a framework.

I've never followed one.
> Rule 6 (contrarian) + Rule 22

**Hook 80:** `[visible-complete]`
This has been THE most important skill I've built.

And it's not an obvious skill.
> Withholding the subject entirely

**Hook 81:** `[visible-complete]`
Nobody in my family has ever quit a job without another one lined up.

I've done it twice.
> Rule 38 (community norm deviation) + escalation

### Emily Kramer

**Hook 82:** `[visible-cut]`
I just wrote a ~3,000-word newsletter on executive dinners.

Here are 10 things that actually make them high ROI…
> Rule 4 (word count proof) + specific list count

### Jake Ward

**Hook 83:** `[visible-complete]`
What do you notice about this data?

Hardly anyone has realised that ~25% of AI answers now come from LinkedIn and Reddit.
> Sub-variant 4E (data-question opener), chart attached

**Hook 84:** `[visible-complete]`
SEO has been dying since 1997.

Some notable "deaths" include:
> Rule 15 (short bomb earning the right to the detail)

**Hook 85:** `[visible-complete]`
I'm 28 with 4 businesses and (still) no home.

Here's how I got here:
> **Portable template** (Rule 43) + Parenthetical Type A. The "(still)" does more emotional work than the numbers.

**Hook 86:** `[visible-complete]`
I literally live and breathe this SEO framework.

5 years ago, I watched a SaaS company burn through 6 months of content budget.
> Rule 39 (cautionary narrative)

**Hook 87:** `[visible-complete]`
THIS NEEDS TO STOP.

I just watched someone manually typing out a LinkedIn post
> **Rule 8 exception.** Full-caps line at 43 units, functioning as an alarm before a specific complaint. Short enough to work; a longer caps line would not.

**Hook 88:** `[visible-complete]`
"SEO is dead!" But... which one?

The 40 types of SEO:
> Sub-variant 2G (quoted claim) + Rule 9 (question answered immediately by line 2)

**Hook 89:** `[visible-complete]`
Planning SEO content for the 2nd half of 2026?

PLEASE do this first:
> Rule 9 (question with immediate answer). Would have been banned under the old rule.

**Hook 90:** `[visible-cut]`
We're in an AI gold rush and people are complaining?

I can build tools by describing them in English and have a
> Rule 9 (rhetorical question) + trailing mode

**Hook 91:** `[visible-cut]`
I can't believe it took me this long.

3 years, 9 months, and 10 days of posting on LinkedIn without
> Precise duration + trailing mode, preposition awaiting its noun

**Hook 92:** `[visible-complete]`
800K views, #1 on Google, cited by LLMs in 5 days.

One article published on LinkedIn Pulse and X.
> Rule 4 (stacked metrics in line 1, mechanism in line 2)

**Hook 93:** `[visible-complete]`
We're hiring (again). No job description. No CVs.

Here's who I'm trying to find:
> **Recruitment post type.** Announce, add constraint, promise criteria. Same shape as Diandra Hook 28.

**Hook 94:** `[visible-cut]`
I just built SEO strategies for beehiiv and Kleo.

A ~$300M newsletter platform and my own 7-figure SaaS we
> Rule 36 (result credential) + trailing mode

**Hook 95:** `[visible-cut]`
I'm doing something I've never done before.

My first ever live SEO webinar. Just me and Rob sharing what's
> Rule 7 (tension) + trailing mode

**Hook 96:** `[visible-complete]`
August 5th, 2026 was one of the best days of my career.

Me and my best friends watching our startup go viral.
> Dated specificity + scene

### Jasmin Alić

**Hook 97:** `[visible-complete]`
LinkedIn folks may think I'm crazy for this.

20,000+ questions. Answered for free.
> Rule 4 (scale) + generosity as proof

**Hook 98:** `[visible-complete]`
If I had to rebuild my LinkedIn to 373K...

I wouldn't change much. (just a few things)
> **Parenthetical Type B in the closing position**, not as the whole line. Distinct placement.

**Hook 99:** `[visible-complete]`
I'm happy certain things exist on LinkedIn!

(but I wish LinkedIn made them better)
> Parenthetical Type C. Confirms the "(And/(But" formula is portable, not Cam Trew's alone.

**Hook 100:** `[visible-complete]`
"I don't want to sound like I'm bragging"

This sentence is a LinkedIn epidemic.
> Sub-variant 2G (quoted READER objection)

**Hook 101:** `[visible-cut]`
Confession: I don't think LinkedIn is "easy".

I wish more folks spoke about this openly...
> Rule 17 (label opener: "Confession:")

**Hook 102:** `[visible-complete]`
My #1 LinkedIn rule is "never post and ghost".

It's why I deleted my post yesterday...
> Rule stated then immediately self-applied. Published with a trailing emoji.

**Hook 103:** `[visible-complete]`
I just did a 1-hour masterclass on national TV!

But you don't have 1 hour so...
> Rule 3 (reader-first: acknowledges their constraint). Published with a trailing emoji.

**Hook 104:** `[visible-cut]`
17 misconceptions people have about LinkedIn:

1. Links lower reach. 100% incorrect. The mistake you make is
> **Sub-variant E (List Preview), trailing mode.** Line 2 is 61 chars. Passes the cut-zone test: claim AND verdict both land by character 37, leaving "The mistake ___" pending.

**Hook 105:** `[visible-complete]`
Most folks here never share personal stories.

My recent Hajj post was my best post in years!
> Rule 6 (contrarian observation) + personal proof

**Hook 106:** `[visible-complete]`
LinkedIn featured my strategy for 1B users.

I woke up to 10,000+ notifications.
> Rule 36 (credential) + consequence as proof

**Hook 107:** `[visible-complete]`
I understand why people quit LinkedIn. I do.

In 2020, I quit it myself. In 2021, I did it again.
> Rule 27 (validate before correcting) + Rule 21

**Hook 108:** `[visible-complete]`
LinkedIn is "slower" in the summer. Noticed it?

If you're reading this, this is your sign to:
> Rule 9 (question) + colon cliffhanger

**Hook 109:** `[visible-complete]`
I'm often asked about my LinkedIn "early days".

But I rarely get asked this one question:
> Withholding the question itself

**Hook 110:** `[visible-complete]`
I get very unusual questions about LinkedIn.

Here's 7 of my favorite. (with answers)
> Parenthetical Type B (reassurance: answers included)

**Hook 111:** `[visible-complete]`
LinkedIn's Product team asked for feedback.

Topic? Comments. My suggestions?
> Two questions used as compression devices

### Lara Acosta

**Hook 112:** `[visible-complete]`
After investing $20,000 in public speaking coaching...

After dealing with a stutter and being introverted….
> Sub-variant D (After-Stack Setup). Both lines setup, no rehook.

**Hook 113:** `[visible-complete]`
I built my first business by doing everything "wrong".

Turns out… most successful entrepreneurs do this too.
> Rule 14 (the "wrong" framing invites the reader in as collaborator)

**Hook 114:** `[visible-complete]`
pov: inside my London flat during launch week...

3 time zones, 47 different problems, 1 shot at winning.
> Rule 17 (label opener) + Rule 4 (descending number sequence)

**Hook 115:** `[visible-complete]`
This is my no.1 tip to fix your low engagement (fast)

I've been using it for 3 years now!
> Parenthetical Type B (speed reassurance)

**Hook 116:** `[visible-complete]`
I went on my dream podcast, but nearly canceled it.

Felt like an imposter the entire day; I was nervous.
> Rule 21 (imposter syndrome)

**Hook 117:** `[visible-complete]`
5 years ago, I didn't think any of this was possible.

Thank you all. We made history and broke the internet.
> Rule 13 (compression) + community credit

**Hook 118:** `[visible-complete]`
I grew my LinkedIn to 346k followers using this 1 trick.

Never start a post with "How to". Do this instead:
> Rule 36 (result credential) + Sub-variant F

**Hook 119:** `[visible-complete]`
If you've been struggling with focus... this is for you.

Focusing has been my biggest struggle this year.
> Rule 24 (segmentation) + Rule 21 (author shares the problem)

**Hook 120:** `[visible-complete]`
I look pro on stage, but I felt like an imposter all day...

Even after building three businesses.
> Rule 21 (achievement does not remove the feeling)

**Hook 121:** `[visible-cut]`
I built a $2M+ ARR business with these non-negotiables.

1. I don't promote a product; I sell a solution
> **Sub-variant E (List Preview).** Line 2 is the first item at 47 chars.

**Hook 122:** `[visible-complete]`
I (finally) landed a 1:1 meeting with the LinkedIn team.

Here's everything I learnt (Including algo updates):
> Parenthetical Type A in line 1, Type B closing line 2. Two placements in one hook, the observed maximum.

**Hook 123:** `[visible-complete]`
Huge announcement... We're launching Kleo 3.0 (live).

This will be the biggest launch in our company's history.
> Announcement post type + Parenthetical Type A

**Hook 124:** `[visible-complete]`
This "simple" strategy built my first 6-fig business.

It's obvious, but it's dangerously effective (here's how):
> Scare quotes (cf Rule 14) + Parenthetical Type B

**Hook 125:** `[visible-complete]`
If you feel like LinkedIn isn't working for you this is why:

(And it's not because the new algorithm)
> Parenthetical Type C using the "(And" opener. Cross-creator confirmation.

**Hook 126:** `[visible-complete]`
There's 100s of ways to get more followers on LinkedIn.

But this one got me to 300k+ (without burning out).
> Parenthetical Type B (cost reassurance)

**Hook 127:** `[visible-complete]`
I'm leaking my phone number.

(and I'm kinda scared)
> Parenthetical Type C in lowercase, tone-matched

**Hook 128:** `[visible-complete]`
This is by far the most rewarding thing about my job.

Making my dad's dreams come true.
> Withholding then delivering an emotional specific

**Hook 129:** `[visible-cut]`
Last month, Jasmin and I decided to change a few lives.

And decided to give away over $10k+ away (direct access to us
> Tagged mention + trailing mode

**Hook 130:** `[visible-cut]`
August has been a monumental month for my startup.

3M+ organic views for our launch campaign
> `[both]` **Sub-variant E (List Preview).** Line 2 is the first item at 43 chars. Published with an arrow marker.

### Leigh McKenzie

**Hook 131:** `[visible-complete]`
Hot take: Most people are using AI for the wrong parts of SEO.

I've been watching how marketers actually use AI tools, and there's a pattern.
> Rule 17 (label opener) + Rule 6

**Hook 132:** `[visible-complete]`
The AI search industry has a vocabulary problem.

GEO. AEO. AIO. LLMO. AI SEO. AI Visibility.
> Staccato stack in line 2. The chaos is the argument.

### Liam Fallen

**Hook 133:** `[visible-cut]`
I owe an apology to everyone on LinkedIn.

I'm sorry to say this but…
> Rule 7 (tension via withheld apology)

**Hook 134:** `[visible-cut]`
I owe an apology to everyone in marketing.

I'm sorry to say this but…
> Same structure, broader audience

**Hook 135:** `[visible-complete]`
I made $23,000 in 3 nights.

I'm giving the strategy away now for free.
> Rule 4 + generosity lowering the cost of clicking

**Hook 136:** `[visible-complete]`
Marketers: "We're data-driven"

The data:
> Setup and punchline compressed to seven words

### Maja Voje

**Hook 137:** `[visible-cut]`
Most GTM stacks are bloated. Mine is not.

Every time I see a logo bomb GTM post, I chuckle. Not because…
> **Rule 22 (the period is load-bearing).** "Mine is not" reads like a verdict.

**Hook 138:** `[visible-complete]`
Go-To-Market Strategist covers 135 frameworks.

If you forced me to pick 9, I'd pick these.
> Rule 26 (credential + constraint signals taste over volume)

**Hook 139:** `[visible-cut]`
I'm not a developer. I don't write code.

But Claude Code is the most powerful GTM tool I've used in…
> Rule 25 (identity disclaimer flip)

### Matt Barker

**Hook 140:** `[visible-cut]`
4 years ago I was a freelance copywriter earning £1k/month:

- I ate the same £3.50 meal deal every day
> **Sub-variant E (List Preview).** Reclassified from plain Punchy+Context.

**Hook 141:** `[visible-cut]`
Most of my investments this year have zero financial ROI.

1. Learning to speak Armenian (my wife is Armenian)
> **Sub-variant E (List Preview).** Reclassified.

**Hook 142:** `[visible-cut]`
You'll hate reading this. But last year, I:

- grew 54,000 followers
> **Sub-variant E (List Preview).** Reclassified. Rule 31 (pre-empts the objection).

**Hook 143:** `[visible-cut]`
How to (finally) be confident writing on LinkedIn:

- go to your calendar
> **Sub-variant E (List Preview).** Reclassified. Parenthetical Type A.

**Hook 144:** `[visible-cut]`
I hate to say this. But the odds of:

- starting to write on LinkedIn
> **Sub-variant E (List Preview).** Reclassified.

**Hook 145:** `[visible-complete]`
You'll think I'm so dumb for this, but:

It's the simplest way to get LinkedIn post ideas.
> Rule 21 (self-deprecation lowering the stakes)

**Hook 146:** `[visible-complete]`
The answer to this:

Write from your Lived Experience only.
> Minimal line 1. Works only with attached media supplying the question.

**Hook 147:** `[both]`. truncated and expanded views both captured
My life is incredibly boring on paper:

- i work from home most days
> **Sub-variant E (List Preview), landing mode.** The definitive example of why line 2 is a sample, not a rehook. "- i work from home most days" would be a total failure as a rehook. It works because the tension lives in line 1's promise and in the items behind the cut.

**Hook 148:** `[both]`
This year, my little business has done $148,646 with:

- $0 payroll (apart from myself)
> **Sub-variant E (List Preview).** First item is the most surprising of the set, which is the rule.

**Hook 149:** `[both]`
Just another week on LinkedIn

A cool guy named Dustin Cantrell wrote a post recommending my community, Your Next Post, to his audience.
> **The definitive trailing-mode example.** Line 2 is 104 characters, far past any cap, and works. At char 42: "wrote a p" (a what?). At char 66: "recommending my co" (your what?). Every cut point leaves a live question. Published with a trailing emoji in line 1.

### Ruben Hassid

**Hook 150:** `[visible-complete]`
Chatbot. Agent. Bot. Automation.

I don't care about AI agents. But I built one anyway.
> Staccato word-stack as line 1. Four bare nouns naming the category confusion the post resolves.

**Hook 151:** `[visible-complete]`
Nobody has ever explained all of Claude to you.

But everything you've learned (so far) was level one:
> Parenthetical Type A + colon cliffhanger

**Hook 152:** `[visible-complete]`
85-year-old grandmas use ChatGPT now.

That's how you know it's the tip of the iceberg:
> Concrete absurd image as evidence

**Hook 153:** `[visible-complete]`
You don't need an expensive Claude course.

You just need 20 mins a day for 26 days:
> **Sub-variant F (negation into prescription).** Line 1 removes the expensive option, line 2 replaces it with a cheaper one.

**Hook 154:** `[visible-complete]`
Don't make (another) .md file for Claude.

Instead, open Claude Settings, Skills, Create.
> Sub-variant F + Parenthetical Type A. "(another)" implies the reader has already made several.

**Hook 155:** `[visible-complete]`
There are 27 ways to make Claude stupid & dumb.

You found all of them on your own (fix in 60 secs):
> Rule 4 + Parenthetical Type B (effort reassurance)

**Hook 156:** `[visible-complete]`
People think learning Claude takes days. It doesn't.

I wrote 17 free guides that teach it in hours:
> Rule 22 (the period is load-bearing) + myth correction

**Hook 157:** `[visible-complete]`
How to make a font of your own handwriting:

(download the exact Claude skill to do it in 3 mins)
> Parenthetical Type C carrying full rehook duty

**Hook 158:** `[visible-complete]`
If I had to start over with a (fresh) Claude account.

These are the 15 settings I'd switch on right away.
> Parenthetical Type A + Rule 4

**Hook 159:** `[visible-complete]`
Your boss pretends to read your (ugly) Excel.

Give him 15 slides instead. It takes 2 minutes:
> Parenthetical Type A doing comic work + Sub-variant F

**Hook 160:** `[visible-cut]`
I use way less Claude tokens than you.

# 1 - Because you prompt, but I don't:
> **Sub-variant E (List Preview)** with a numbered marker

**Hook 161:** `[visible-complete]`
Claude is (still) not the best way to make slides.

It's Gamma, but only if you use it like this:
> Parenthetical Type A. "(still)" signals the author has re-checked over time.

**Hook 162:** `[visible-complete]`
Don't upgrade to the $100 Claude plan (yet).

These 21 hacks make the $20/month plan enough:
> **The clearest Type A example.** Without "(yet)" this is an order. With it, considered advice.

**Hook 163:** `[visible-complete]`
You're getting (very) good at something useless.

Six things to learn instead (all one-time setups):
> Type A in line 1, Type B closing line 2. The observed maximum of two per hook.

**Hook 164:** `[visible-complete]`
These are the exact Claude Skills I use every day.

I'm giving you the whole library (for free):
> Parenthetical Type B (price reassurance)

**Hook 165:** `[visible-complete]`
Writing emails from scratch in 2026 is embarrassing

Here's what I do instead (only takes 2 minutes):
> Sub-variant F + Type B (time reassurance)

**Hook 166:** `[visible-complete]`
Prompting is dead.

Here's what to actually do instead (in one image):
> Short bomb line 1 + Type B (format reassurance)

**Hook 167:** `[visible-complete]`
You could spend a weekend building this yourself.

Or just download my Drive (for free) in five secs:
> Effort contrast + Type B

**Hook 168:** `[visible-complete]`
Don't post (obvious) AI-written content.

Here are 12 tells to delete & the 11 skills that fix it:
> Type A + problem/solution counts in line 2

**Hook 169:** `[visible-cut]`
How to turn your best prompt into a skill (in 10 min):

1. Don't write the Claude skill manually.
> **Sub-variant E (List Preview)** + Type B in line 1

**Hook 170:** `[visible-complete]`
Don't read this if you only post once a month.

You'll burn $100 & hate me. But if you post weekly:
> Rule 24 (segmentation by exclusion) + honest cost warning

**Hook 171:** `[visible-complete]`
Claude doesn't come with a manual.

So I wrote a simple guide (like IKEA instructions):
> Type B using an analogy rather than a metric

**Hook 172:** `[visible-complete]`
Don't use Claude until you read this:

(then send it to your entire team)
> Parenthetical Type C as an instruction

**Hook 173:** `[visible-complete]`
My 9 (most-used) Claude Skills to write prompts.

Download the whole library for free:
> Type A qualifying the count

**Hook 174:** `[visible-complete]`
I wrote these 6 Claude formulas for my team.

Nobody's allowed to skip them (including you):
> Type B addressing the reader directly

**Hook 175:** `[visible-complete]`
How to master Claude Fable 5 in only 15 steps:

(Send it to your team. They're burning credits)
> Type C carrying two sentences

**Hook 176:** `[visible-complete]`
Stop buying expensive $500 courses to learn AI.

I've already done it for you. With one list:
> Sub-variant F

**Hook 177:** `[visible-cut]`
I made a 16-page PDF to get you Claude-certified.

The certificates are official by Anthropic & free...
> Rule 4 (specific artifact) + credibility transfer

**Hook 178:** `[visible-complete]`
Delete your 33 unread Claude guides bookmarks.

This (stupid simple) roadmap is all you need:
> Type A as a two-word qualifier

**Hook 179:** `[visible-complete]`
My mom asked me, "What the hell is Claude?"

This image did the job, not me:
> **Sub-variant 2G (quoted CIVILIAN).** A non-expert asking the question the audience is embarrassed to ask.

**Hook 180:** `[visible-cut]`
This chart changed how I use Claude (entirely).

Every time I re-explain a task, I just repeat "never explain twice"
> Type A closing line 1 + trailing mode

**Hook 181:** `[visible-complete]`
Don't build (another) file folder in Claude.

Here's the zero-maintenance setup in just 20 mins:
> Sub-variant F + Type A

### Sara Stella Lattanzio

**Hook 182:** `[visible-complete]`
Please don't turn all your content into Q&A-style blogs.

I get why marketing teams obsess over it.
> Rule 27 (soft warning; validates before correcting)

**Hook 183:** `[visible-complete]`
Marketers never controlled how people buy.

It was just easier to fake it when there were fewer options to compare and fewer places to search.
> Rule 12 (reframe: the control was always an illusion)

**Hook 184:** `[visible-cut]`
I'm genuinely excited about this one.

It doesn't happen every day that you get a look behind the curtain of the editorial process of one of the most established search…
> Trailing mode

### Sophie Miller

**Hook 185:** `[visible-complete]`
growing up, I was often called bossy…

(yawn)
> Parenthetical Type C as dismissal. Two syllables doing all the work.

**Hook 186:** `[visible-complete]`
a year ago this was just a note in my phone, tomorrow you can bag a ticket to join us
> Rule 32 (problem-origin announcement). Outperforms "excited to announce."

**Hook 187:** `[visible-complete]`
*insert vague caption teasing biggest announcement ever dropping at 8am tomorrow morning here*
> Rule 30 (the meta-hook mocking its own genre)

**Hook 188:** `[visible-complete]`
3 interesting ways I'm working with brands right now (that aren't just another paid post), as a content creator with 750,000 followers on the internet
> Rule 31 (transparency parenthetical pre-empting skepticism)

**Hook 189:** `[visible-complete]`
every conference I attend feels like it was built for someone more senior than me, so I'm creating one that isn't
> Rule 32 (problem-origin). The logic of the solution is already in the problem.

**Hook 190:** `[visible-complete]`
I've spent the last year going properly deep on video and it's humbled me a bit
> Rule 21 (vulnerability about a learning curve)

### Tycho Luijten

**Hook 191:** `[visible-complete]`
Sales and Marketing have a KPI meeting with their CEO.

It gets awkward fast.
> Rule 39 (scene-setting). Opens the curtain without explaining the play.

**Hook 192:** `[visible-complete]`
We are able to pay 60 salaries from posting on LinkedIn.

So it's fair to say we understand the platform.
> Rule 36 (result credential earning the right to advise)

### Vukasin Vukosavljevic

**Hook 193:** `[visible-complete]`
We went from $15K to $3M ARR in 15 months.

Here are 9 channels that didn't help us get there… and 5 that did.
> Rule 28 (failure-first list is more credible than wins-only)

**Hook 194:** `[visible-complete]`
6 things I like about my CEO.

And 3 things I absolutely don't.
> Rule 29 (the negative number earns the click)

**Hook 195:** `[visible-cut]`
I just wanted to acknowledge people who:

Send 5 sentences as one WhatsApp message instead of
> **Sub-variant E (List Preview), trailing mode.** Rule 33. Line 2 is 51 chars; the absurdity lands by char 40.

---

## FORMAT 3: SINGLE-LINE BOMB

One short, charged sentence. **≤45 characters**, because a one-line hook is the last visible line by definition.

### Adam Robinson

**Hook 1:** `[visible-complete]`
AI is making CEO's delusional.
> Rule 6 (contrarian) + direct accusation

### Alicia Teltz

**Hook 2:** `[visible-complete]`
15 Ways to get HATED on LinkedIn instantly
> Rule 4 (specific count) + Rule 8 (caps) + fear trigger

**Hook 3:** `[visible-complete]`
WHAY THE FCK HAVE I DONE???
> Rule 8 (caps as alarm, 43 units) + typo left in for authenticity

### Cam Trew

**Hook 4:** `[visible-complete]`
I quit my 9-5 software engineer job to start an AI business with my friend from school.
> Over the 45-char guideline. Included as observed data; works because the whole life-change lands in one breath.

**Hook 5:** `[visible-complete]`
The most underrated business decision I've made is caring about where I work from.
> Withholds the decision until the final clause

**Hook 6:** `[visible-complete]`
POV: you just replaced your engineering team with a $1.3M/month OpenAI bill.
> Rule 17 (label opener) + Rule 4

---

## FORMAT 4: STACKED

2-3 short lines creating a pattern the reader wants to see broken or explained.

**Non-final lines ≤50 chars. Final line ≤45 chars in landing mode.**

**Tight vs spaced is a real choice.** Spaced (blank lines between) suits before/after contrast, where the blank line creates the pause. Tight (no blank lines) is required for 3-line stacks, since blank lines would consume the whole visible space.

### Sub-variant A: Before/After Timeline (spaced)

**Hook 1:** Diandra Escobar `[visible-complete]`
2023: Broke Colombian girl living in Medellin

2026: Speaking in CHINA to 9 figure founders
> Rule 13 (compression). Two lines carrying three years.

**Hook 2:** Diandra Escobar `[visible-complete]`
1st time in London: hostel bunk bed, £3 meal deal.

This time: people paid $1k to hear us speak.
> Rule 13. Same place, two lives. The £3 and the $1k do all the work.

**Hook 3:** Diandra Escobar `[visible-complete]`
22 years old. Fired. Living in Colombia. $0.

25 years old. Hired friends. Nomading. $1M
> Four parallel facts per line, identical grammar, three years apart.

**Hook 4:** Cam Trew `[visible-complete]`
2025: Working a 9-5 tech job

2026: 2x AI Founder. First YouTube video recorded.
> Rule 13 + identity shift

**Hook 5:** Lara Acosta `[visible-complete]`
2023: 0 followers. $0 made. Felt invisible.

2026: 317k followers. $2M+ made. Forbes featured me.
> Rule 13. Three years in 22 words. Do not soften the gap.

**Hook 6:** Diandra Escobar `[visible-complete]`
2023: Studying Sara's posts to learn LinkedIn.

2026: With a heavy heart I'm leaving the newsletter we built.
> Before/after with an unexpectedly sad second beat. Tagged mention in line 1.

### Sub-variant B: Countdown Stack (tight, no blank lines)

The best-evidenced new format in the dataset. Three creators, three time units, all independently landing on the same construction. **The interval shrinks toward the present**, which creates the acceleration. Match the line widths closely.

**Hook 7:** Cam Trew `[visible-complete]`. 94 / 97 / 93 units, spread of 4
365 days ago: I quit my 9-5 software engineering job.
334 days ago: Started a business with my best friends.
2 days ago: We re-launched it and broke all records.
> 365 to 334 is a month. 334 to 2 is nearly a year of silence before everything lands.

**Hook 8:** Jake Ward `[visible-complete]`. 77 / 84 / 83 units, spread of 7
10 years ago, I was trying to figure out SEO.
7 years ago, I went solo as an SEO consultant.
4 years ago, I published my first LinkedIn post.
> Same construction in years rather than days

**Hook 9:** Lara Acosta `[visible-complete]`. 90 / 88 / 83 units, spread of 8
At 21 I got diagnosed with high-functioning anxiety.
At 22 I got diagnosed with depression and PTSD.
By 23 I had a collection of labels I hid behind.
> Same construction in ages. The switch from "At" to "By" on the final line marks the summation.

### Sub-variant C: Parallel Regret Stack (tight)

**Hook 10:** Lara Acosta `[visible-complete]`
I didn't promote myself for 1 year. Felt embarrassed.
I didn't launch my business for months. Feared failure.
I didn't pitch dream clients for 2 years. Felt unqualified.
> Rule 21. Identical structure, escalating cost.

### Sub-variant D: Anaphora Stack (tight)

**Hook 11:** Lara Acosta `[visible-complete]`. 87 / 84 / 89 units
This was my first LinkedIn post. I still cringe at it.
That same cringe post landed me my first client.
That same cringe post got me my first 4k followers.
> The repeated phrase is the hook. Tight stacking makes the three lines read as one thought.

**Hook 12:** Diandra Escobar `[visible-complete]`
"Use storytelling"

"Just be consistent and comment 300 times"

"Why aren't we going viral yet, we've posted 3 times."
> Stacked quotes. The absurdity escalates across the three, and the third exposes the contradiction.

**Hook 13:** Alicia Teltz `[visible-complete]`
1 follower is your start.

100 followers is validation.

1,000 followers is momentum.
> Milestone framework with multiplying numbers

**Hook 14:** Matt Barker `[visible-complete]`
2022: Hit 40,000 followers.

2023: Hit 100,000 followers.

2026: Will hit 200,000 followers.
> The third line is a prediction, not a record, which is what earns the click.

**Hook 15:** Diandra Escobar `[visible-complete]`
X wants you to pick a fight.

TikTok wants you to dance.

Instagram wants a magazine spread.
> Three platforms, three verbs, one implied fourth. The reader supplies LinkedIn themselves.

### Sub-variant F: Quiz Opener

**Hook 16:** Diandra Escobar `[visible-complete]`
Which LinkedIn posts does AI search cite?

a) Viral b) 20 reactions.
> Question plus multiple choice, infographic attached. The reader clicks to check their answer.

### Sub-variant G: Stacked Jargon Repetition (cut-off)

**Hook 17:** Tycho Luijten `[visible-cut]`
Somebody liking your post doesn't make them TOFU.

Somebody reading your blog doesn't make them MOFU.

Somebody downloading your ebook definitely doesn't make them…
> Rule 40. In-group terminology signals a knowledgeable audience; the cut-off forces completion.

### Sub-variant H: Problem-Cost-Twist

**Hook 18:** `[visible-complete]`
Your brand style guide has 50+ rules.

Your team remembers maybe 3 of them.

We built a system that checks ALL of them.
> Problem, cost, reveal. Best for product posts; worst for personal narrative.

### Sub-variant I: Greentext Stack (tight)

**Hook 19:** Jake Ward `[visible-cut]`
> Be me or Lara Acosta
> Met on LinkedIn in October 2022
> Had less than 10,000 followers each
> Chan-style markers compressing an origin story. Deliberately lo-fi.

### Sub-variant J: Tight Two-Line

Two lines, no blank line between. Distinct from Punchy+Context: without the blank line, line 2 is not a rehook but an emotional or explanatory completion, and can run notably longer.

**Hook 20:** Alicia Teltz `[visible-complete]`. 91 / 143 units
Today, exactly 4 years ago, I was made redundant.
You don't realise how DEVASTATING that moment is until you're the one living it.
> Line 2 at 143 units would be absurd as a rehook. It works as completion.

**Hook 21:** Alicia Teltz `[visible-complete]`. 108 / 69 units
As an ex-LinkedIn employee, I reviewed hundreds of profiles.
Here's the #1 mistake killing your reach:
> Credential then promise, read as one block.

**Hook 22:** Matt Barker `[visible-complete]`
4 years ago I was a freelance copywriter earning £1k/month:
- I ate the same £3.50 meal deal every day
> Cross-listed with Format 2 Sub-variant E.

---

## Portable Templates

Structures observed independently across unrelated creators. If a structure works for three creators in three niches, it will work in a fourth.

**1. The parenthetical rehook**: Cam Trew, Lara Acosta, Jasmin Alić, Ruben Hassid
`[Claim with one capped word.]` / `(And/But [escalation or undercut])`

**2. "I'm [age] with [N] businesses and no home"**: Jake Ward (4), Cam Trew (2)

**3. "I can't stop thinking about this Tweet."**: Cam Trew, Diandra Escobar, different line 2 each

**4. The countdown stack**: Cam Trew (days), Jake Ward (years), Lara Acosta (ages)

**5. Recruitment: announce, constrain, promise**: Diandra Escobar, Jake Ward

---

## File Info

Version: 2.0
Total hooks: 304 (Format 1: 80 | Format 2: 195 | Format 3: 6 | Format 4: 22, some cross-listed)
Creators represented: 26
Width model: measured across 3 preview tools and LinkedIn's live feed, validated against a post observed simultaneously on all four surfaces
Last updated: 2026-08-15
