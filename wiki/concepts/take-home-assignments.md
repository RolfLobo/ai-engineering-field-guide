# Take-Home Assignments

What AI engineering take-homes ask for, how they are graded, and what gets offers. Sources: [interview/questions/06-home-assignments.md](../../interview/questions/06-home-assignments.md) (primary), [webinar 4](../summaries/webinars.md), [portfolio section](../summaries/portfolio.md).

## Prevalence and format

17 of 51 companies with disclosed processes (33%) use a take-home or asynchronous assignment; 5 more use paid work trials. Typical format: 2-7 day deadline, 2-4 hours of actual intended work, submit code plus writeup, then a 45-90 minute defence round. Companies emphasize decision-making and clarity over cleverness ("not code golf").

AI tool policy is strikingly permissive: one company explicitly allows AI tools in take-homes, zero explicitly ban them - the bans apply to live interviews.

## What companies ask for

From 100+ public GitHub submissions (Q4 2025 - Q2 2026):

- RAG systems - 40%+: document upload, vector DBs, citations, "I don't know" fallbacks
- Agents and tool-calling - 30%+: multi-step reasoning, tool approval gates, PII refusal logic
- Conversational AI - 20%+: chatbots, live-chat agents, voice
- Document processing - 15%: PDF/OCR extraction, marksheets, clinical notes
- LLM-as-judge evaluation - 10%+: build a system, then evaluate it with another LLM
- 2026 additions: legal-document AI (ingest -> grounded retrieval -> cited drafts -> learn from operator edits), workflow engines with loop protection, NL-to-app compilers

## How submissions are graded

Explicit rubrics recur across assignments: functional correctness, code quality and architecture, evaluation methodology, production readiness (caching, monitoring, cost, PII handling), performance targets (<2s p95, 100+ req/s, >40% cache hits), testing (sometimes mandatory, ~80% coverage), documentation, and weighted rubrics (e.g. 30% functionality / 30% challenge / 25% context engineering / 15% code quality).

## What gets offers

- Start with evaluation - build the eval harness before the main logic. YC startups: "red flag if candidate doesn't start with evals"
- Document decisions and trade-offs, not just code
- Include a video walkthrough
- Make it configurable (the PDF-summarizer-CLI-with-config story ended in two competing offers within 72 hours)
- Show production awareness even when not required
- The flip side: skipping evaluation of AI outputs is the single most common reason submissions fail

## The shadow side

AI startups increasingly use take-homes as unpaid product ideation - a French candidate was asked to build a complete LLM agent for financial document analysis (community estimate: 6,000-10,000 EUR of consulting work). Community guidance: decline assignments that constitute a deployable product, and refuse take-homes sent before any human conversation ([interview/05-trends.md](../../interview/05-trends.md)).

## Relation to portfolio strategy

Take-homes double as portfolio material ([portfolio/01](../../portfolio/01-types-of-projects.md)): companies use them to test real work, so a published, well-contextualized take-home demonstrates realistic skills - and practicing on published assignments (implementing them yourself, studying the READMEs rather than the code) is the repo's recommended preparation ([webinar 3](../summaries/webinars.md)).

## Inference (my synthesis)

- The take-home corpus is the closest thing the market has to a public, de facto certification of AI engineering skill: it reveals both what employers value (grounding, refusals, evals, cost) and the gap between intended effort (2-4 hours) and actual expectations
