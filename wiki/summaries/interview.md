# Interview Section (repo: interview/)

- Sources: [interview/](../../interview/) - synthesis of 1,765 job descriptions with disclosed-process data from 51 companies, plus 100+ candidate reports (Reddit, X, blogs, YouTube)
- Related: [interview process concept](../concepts/interview-process.md), [take-home assignments](../concepts/take-home-assignments.md), [portfolio](portfolio.md), [awesome.md reading list](awesome.md)

## What the section says

A data-driven map of how AI engineering hiring actually works: a typical process of 3-6 rounds over 2-6 weeks (median 4 steps), six question categories, what separates candidates (evaluation skills, cost/latency reasoning, trade-off fluency, honesty), and 2026 trends (AI cheating, AI-proctored rounds, in-person rounds returning, no standardization).

## Files covered

- [interview/README.md](../../interview/README.md) - section index and data sources (1,500+ JDs, 100+ Reddit threads, 60+ HN threads, 35+ blogs, 700+ URLs)
- [interview/01-interview-process.md](../../interview/01-interview-process.md) - only ~4.5% of 1,765 JDs disclose a process (51 companies). Median 4 steps, range 2-7. The recurring steps: recruiter screen, technical interview, hiring manager, behavioral, take-home, panel, CEO/founder. Ten company walkthroughs (Doctolib, PostHog, FlowFuse, Microsoft, Amazon, Eightfold, LangChain, IBM, Mistral, Databricks) with sources
- [interview/02-questions.md](../../interview/02-questions.md) - index into the six question categories below; consolidated from 100+ sources
- [interview/questions/01-theory.md](../../interview/questions/01-theory.md) - actual asked questions by topic: LLM practice, RAG, agents/tool use, testing/evaluation, monitoring, cost/latency, safety. Specialized topics (fine-tuning, transformer internals) come up only when the JD requires them. Preparation advice: practice over theory - build RAG end-to-end, know when NOT to use agents, be able to describe golden datasets
- [interview/questions/02-coding.md](../../interview/questions/02-coding.md) - two round formats: implementation rounds (45-90 min, progressive multi-level problems: crawler, key-value store, refactoring) vs algorithm rounds (LeetCode-style). Preparation: 75+ easy/medium problems, build projects that mirror progressive problems, narrate reasoning - interviewers watch how you use AI tools, not whether you do
- [interview/questions/03-project-deep-dive.md](../../interview/questions/03-project-deep-dive.md) - the deep dive tests ownership, judgment, depth: 30-60 min, conversational or prepared presentation (Anthropic: 25 min + 15-20 min questions). The follow-up probe taxonomy (business context, decisions/trade-offs, debugging, evaluation, reflection) and what interviewers evaluate. Key signal: frame around impact, not tool names
- [interview/questions/04-ai-system-design.md](../../interview/questions/04-ai-system-design.md) - AI system design as an emerging distinct category: orchestrating pre-trained models instead of designing training pipelines. Typical questions (design a chatbot, RAG doc QA, Perplexity-like search), the five-step answer structure, four repeatable patterns (RAG, feedback loops, hallucination mitigation, cost/scalability), and how AI design differs from ML and traditional design across seven dimensions (data focus, output, determinism, evaluation, cost model, failure modes, iteration speed)
- [interview/questions/05-behavioral.md](../../interview/questions/05-behavioral.md) - behavioral question bank (AI-specific, conflict, leadership, decision-making, failure, values, motivation). Preparation: map 2-3 STAR stories per company value; Amazon Leadership Principles as the generic template
- [interview/questions/06-home-assignments.md](../../interview/questions/06-home-assignments.md) - 17 of 51 companies (33%) use take-homes, 5 more use paid trials. From 100+ GitHub submissions: RAG 40%+, agents 30%+, conversational AI 20%+, document processing 15%, LLM-as-judge 10%+. Explicit evaluation rubrics, dozens of linked real assignments, and what makes submissions get offers (start with evals - "red flag if candidate doesn't"). Covered in depth in [take-home assignments](../concepts/take-home-assignments.md)
- [interview/questions/questions.md](../../interview/questions/questions.md) - the full consolidated question bank (782 lines) merging all six categories with source footnotes
- [interview/03-get-hired.md](../../interview/03-get-hired.md) - what interviewers actually test vs what postings list; what separates candidates (50+ interviews reports: first 5 minutes decide, cost awareness is a superpower, honesty beats bluffing); the 90/10 rule; before-you-apply requirements some companies have; common mistakes in interviews and job search; prep playbooks from Mimansa Jaiswal (12 weeks, 150+ NeetCode), Yuan Meng (domain expertise as advantage, SAIL format), Janvi Kalra (46 companies, hackathons > courses); an 8-12 week timeline; negotiation data (total comp benchmarking, competing offers as leverage, 2025-2026 US comp ranges)
- [interview/04-after-the-interview.md](../../interview/04-after-the-interview.md) - short and practical: retrospectives on rejections, finish other interviews before accepting, the two approaches to the salary-expectations question
- [interview/05-trends.md](../../interview/05-trends.md) - the trends file: AI-native roles +240% in early 2025, LLM questions tripled since 2023; LeetCode declining but not dead (~70% of senior interviews had none); "no whiteboard" companies; framework bias (rejected for not knowing LangChain); real-time AI cheating and company policies; AI-proctored early rounds (Eightfold, Coinbase); the "no AI tools" irony (Wolters Kluwer paradox); companies allowing AI in live coding (OpenAI, Microsoft's split-round design); exploitative take-homes; new round types (code review, AI-delta assessment); junior-vs-senior divergence; "knowledge is free - judgment isn't"

## Key claims

- Interviews lack standardization because the role itself is still being defined - Janvi Kalra's "all over the place" finding (interview/05-trends.md)
- The interview is shifting from "can you code" to "can you reason with the AI that codes with you" - but DSA rounds persist at big tech and frontier labs (interview/05-trends.md, questions/02-coding.md)
- Evaluation skill is the strongest cross-source signal for getting hired (interview/03-get-hired.md; cross-confirmed in [role](role.md) and [home assignments](../concepts/take-home-assignments.md))
- In-person rounds rose from 24% (2022) to 38% (2025), driven by AI cheating concerns (interview/05-trends.md)

## What is actionable

- The 8-12 week prep timeline in interview/03-get-hired.md is the section's distilled roadmap
- Treat take-homes like a mini job: clarify, eval-first, document decisions, record a walkthrough video
- Prepare distinct STAR stories per company value; vary them across rounds
