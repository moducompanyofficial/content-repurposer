# Content Repurposer

![License: MIT](https://img.shields.io/badge/License-MIT-1b4dff.svg) ![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-1b4dff) ![Runs offline](https://img.shields.io/badge/runs-offline-2ea44f) ![No API key](https://img.shields.io/badge/no-API%20key-2ea44f) ![MCP server](https://img.shields.io/badge/MCP-server%20included-8A2BE2)

**Drop in one article. Get a week of platform-ready posts back in a few seconds — offline, no API key, no signup.**

Built for marketing and content agencies that publish a lot and lose hours every week turning each piece into "now make it a thread, a LinkedIn post, an IG caption, a newsletter…". This is the free, single-file tool that does the first draft of all of it.

---

## One input → six outputs

Feed it one `.md` or `.txt` (a blog post, a webinar transcript, a voice-note dump). You get a folder containing:

- 🧵 **X/Twitter thread** — auto-split to tweet length, numbered
- 💼 **LinkedIn post** — hook → key points → CTA
- 📸 **Instagram caption** + hashtags
- ✉️ **Newsletter blurb**
- 🔎 **SEO title + meta description** — length-checked
- 🗓️ **7-day posting calendar** (CSV) you can hand to anyone

No accounts, no upload — the file never leaves your machine.

---

## Before → after (real output)

**You give it this article** (`sample_input.md`, abridged):

> **Why Most Marketing Agencies Lose 15 Hours a Week to Manual Reporting**
> Marketing agencies live and die by client reporting, yet most teams still build reports by hand every single month. An account manager opens five dashboards, copies numbers into a slide deck, writes a short commentary, and repeats this for every client. For an agency with ten clients, that's easily fifteen hours of skilled labor a week spent on copy-paste work that creates no new value… *(full article continues)*

**You get back this** (straight from `example_output/`):

`linkedin_post.txt`
```
Why Most Marketing Agencies Lose 15 Hours a Week to Manual Reporting

Most teams get this wrong. Here's what actually works:

→ Marketing agencies live and die by client reporting, yet most teams still build
  reports by hand every single month.
→ For an agency with ten clients, that's easily fifteen hours of skilled labor a week
  spent on copy-paste work that creates no new value.
→ Agencies that automate reporting typically reclaim ten to fifteen hours a week,
  reduce errors to near zero, and deliver insight faster.

Which of these are you missing? Reply below.

#Reporting #Client #Hours #Agencies
```

`twitter_thread.txt` (first lines)
```
1/8  Why Most Marketing Agencies Lose 15 Hours a Week to Manual Reporting
     A thread 🧵👇
2/8  Marketing agencies live and die by client reporting, yet most teams still build
     reports by hand every single month.
3/8  An account manager opens five different dashboards, copies numbers into a slide
     deck, writes a short commentary, and repeats this for every client.
```

`posting_calendar.csv`
```
Date,Day,Time,Piece,Asset file,Status
2026-06-24,Wed,09:00,X/Twitter thread,twitter_thread.txt,Draft
2026-06-25,Thu,08:30,LinkedIn post,linkedin_post.txt,Draft
2026-06-26,Fri,12:00,Instagram caption,instagram_caption.txt,Draft
2026-06-27,Sat,07:00,Newsletter,newsletter.txt,Draft
```

That's a structured first draft for a full week — something you edit in a couple of minutes instead of writing from scratch. Want it sharper than template-shaped? Add `--llm` (below) and it rewrites each piece properly.

---

## Quick start

```bash
python repurpose.py your_article.md --out output_folder
```

Requires Python 3.9+. **No dependencies for offline mode.** Output lands in `output_folder/`.

Try it on the included sample:
```bash
python repurpose.py sample_input.md --out demo
```

Optional higher-quality rewrite (uses Anthropic's API, needs a key):
```bash
pip install anthropic
export ANTHROPIC_API_KEY=...        # your key
python repurpose.py your_article.md --out output_folder --llm
```

**Offline vs `--llm`, honestly:** offline mode reshapes your existing sentences into each platform's format — fast, deterministic, your content stays local, and you tidy it up. `--llm` rewrites each post for tone and flow, so it reads less mechanical. Start offline; reach for `--llm` when a piece is going out as-is.

---

## Free vs. done-for-you (PRO)

The free tool is the manual, single-file version — run it yourself, one file at a time. **PRO** is for teams that want it to match each client's voice and feed their scheduler automatically.

| | Free (this repo) | PRO |
|---|---|---|
| Platforms | 5 | **9** (+ YouTube, Reddit, Threads, Facebook) |
| Brand voice | generic | **learns each client's voice** from past posts |
| Batch | one file at a time | **a whole folder at once** |
| Scheduler | calendar CSV | **Buffer/Publer CSV + `.ics` import** |
| Reuse | — | **saved brand profiles** (`brand_profile.json`) |
| Price | **Free, MIT** | **Solo $49 · Agency $149 · Done-for-you $499** |

One-time pricing, self-serve, no calls:
- **Solo — $49** · the PRO tool + brand profiles
- **Agency — $149** · multi-brand profiles + scheduler exports + lifetime updates
- **Done-for-you — $499** · I wire it into your CMS + scheduler and train it on your top client's voice (async, 30-day support)

→ **PRO:** https://moduofficial.gumroad.com/l/loaysb

---

## Two ways to start

1. **Use the free tool now** — clone this repo, run the command above, keep it forever. No email required.
2. **Get a free AI automation audit** — if repurposing (or reporting, or any other copy-paste grind) is eating your team's week, I'll map your top 3 automation opportunities with rough ROI, in writing, no call. If nothing's worth automating, I'll tell you straight.
   → **5-min form:** https://moducompanyofficial.github.io/ai-audit/

---

MIT licensed — fork it, ship it, keep it.

— Modu Company · moducompanyofficial@gmail.com
