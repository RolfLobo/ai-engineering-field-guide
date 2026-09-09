# AI Engineering Interview Process

How AI engineering hiring works in practice. Sources: [interview section](../summaries/interview.md) (primary), [webinar 3](../summaries/webinars.md).

## Structure

From 1,765 job descriptions, only ~4.5% (51 companies) disclose a process - but those plus hundreds of candidate reports converge on a typical shape: 3-6 rounds over 2-6 weeks, median 4 steps, up to 7:

1. CV screening
2. Recruiter call (15-30 min)
3. Hiring manager interview - project deep dive plus theory
4. Technical interview - coding with a senior engineer
5. Behavioral interview
6. Take-home assignment + defence round
7. Final panel / CEO-founder round

Not every company uses every step; lean processes have 2 (including one company that runs a single call plus a paid trial day).

## The round types

- Theory - rarely standalone; woven into other rounds. Core topics: RAG, agents, evaluation, monitoring, cost/latency, safety. Fine-tuning and transformer internals only when the JD names them
- Coding - two formats: implementation rounds (45-90 min progressive problems) and algorithm rounds (LeetCode-style; declining but alive: ~70% of senior interviews had none in 2025-2026 reports, yet frontier labs and big tech still run them)
- Project deep dive - 30-60 minutes on one project; the most reliable seniority signal. Tests ownership, decision reasoning, depth under probing
- AI system design - an emerging distinct category: orchestrating pre-trained models, not designing training pipelines. Mostly senior+; four repeatable patterns (RAG, feedback loops, hallucination mitigation, cost/scalability)
- Behavioral - STAR stories mapped to company values; Amazon's Leadership Principles as the generic template
- Take-home - 33% of disclosed processes; see [take-home assignments](take-home-assignments.md)

## What interviewers actually test

What separates candidates ([interview/03-get-hired.md](../../interview/03-get-hired.md)): evaluation frameworks over model building, cost and latency reasoning, trade-off fluency ("when would you NOT use RAG?"), systems thinking in loops, observability, safety awareness, AI fluency with coding tools, Python depth, DSA fundamentals at labs, and honest uncertainty. The first five minutes decide a lot; impact framing beats tool names; "I need a hint" outperforms bluffing.

## AI inside the hiring process itself

The 2026 twist - AI on both sides of the table ([interview/05-trends.md](../../interview/05-trends.md)):

- AI cheating: real-time transcription-and-answer tools; company responses range from bans (Wolters Kluwer, Hudson River Trading) to the Wolters Kluwer paradox - AI tools are mandatory skills for the job but banned in the interview
- AI-proctored rounds: Eightfold.ai and Coinbase use AI agents to conduct first-round technical screens
- AI-allowed rounds: OpenAI allows AI during coding ("they're watching for reasoning and judgment"); Microsoft runs an explicit split - AI-assisted round then raw-coding round
- Consequences: in-person rounds back up from 24% (2022) to 38% (2025); anti-cheating tooling; new round types (code review of AI-generated code, "AI delta" assessment)
- The market has no standardization - "the market is trying to move away from LeetCode but still asks LeetCode" (Janvi Kalra, 46 companies)

## Inference (my synthesis)

- The process is best understood as two filters: a standardized-looking filter (coding, system design) that varies wildly by company, and a consistent signal layer underneath - ownership narratives, evaluation thinking, and production awareness - which the repo argues is what actually decides offers
- Preparation strategy follows from the data: build 2-3 real projects with evals, practice explaining trade-offs aloud, grind just enough DSA for target companies, and prepare honest failure stories
