# Learning Paths Section (repo: learning-paths/)

- Sources: [learning-paths/](../../learning-paths/) - what to learn and in what order, based on skill demand from the job-market data and the From RAG to Agents Buildcamp curriculum
- Related: [AI engineer role](../concepts/ai-engineer-role.md), [webinars](webinars.md) (the Q&As answer the same transition questions), [role section](role.md)

## What the section says

There is a core 20% of skills that covers 80% of the work: LLM fundamentals (APIs, structured output, prompts), RAG and search, agents and tool use, testing, monitoring, evaluation, production. Everything else (web dev, cloud, databases, ML fundamentals, data engineering) depends on where you start from. The five transition guides share one thesis: start from engineering strength and add what's missing - and for every path, evaluation is the key new skill.

## Files covered

- [learning-paths/README.md](../../learning-paths/README.md) - the core curriculum (LLM fundamentals, RAG, agents, testing, monitoring, evaluation, production), the supporting skills by demand, the typical AI engineering stack (application / orchestration / LLM APIs / vector DBs / infrastructure / monitoring / evaluation), and skills by priority: must-have (Python, prompt engineering, RAG, one cloud, Docker), high-value (framework, TypeScript, FastAPI, Kubernetes, CI/CD, PyTorch basics), differentiators (agent frameworks, fine-tuning, evaluation frameworks, vector DBs, multi-agent patterns)
- [learning-paths/from-backend-engineer.md](../../learning-paths/from-backend-engineer.md) - 2-3 months. "An AI engineer is first and foremost an engineer. The AI part comes second." Add: LLM APIs, prompt engineering, RAG, agents, evaluation (the hardest new one), AI-specific monitoring, basic ML
- [learning-paths/from-data-engineer.md](../../learning-paths/from-data-engineer.md) - 3-4 months, one of the smoothest transitions: RAG needs a search engine, which needs an ingestion pipeline - a data engineer's career skill. Entry point: join an AI team through the data side, then shift toward AI work
- [learning-paths/from-data-scientist.md](../../learning-paths/from-data-scientist.md) - evaluation is your superpower; the gap is engineering rigor (tests, CI/CD, deployment, Docker). The hard truth: DS who never leave notebooks have been struggling for a while - a gpt-4o-mini call replaces many traditional modeling tasks; full-stack generalists stay fine
- [learning-paths/from-frontend-engineer.md](../../learning-paths/from-frontend-engineer.md) - backend first (TypeScript path or Python path, both viable; Python for AI depth), then AI. Unique advantage: closing the full stack end-to-end - often the best first AI-team hire at startups. Explicitly recommends starting with an AI assistant (Cursor, Claude Code) while learning backend
- [learning-paths/from-ml-engineer.md](../../learning-paths/from-ml-engineer.md) - the easiest transition: replace a call to a locally hosted model with a call to OpenAI; the rest (serving, monitoring, CI/CD) carries over. New: prompt versioning, LLM-specific evaluation (hallucination, answer quality, tool-use correctness), frameworks. Advantage: can reason about why a model underperforms, and can self-host when privacy/latency/cost demands it

## Key claims

- Every path converges on the same shortlist: LLM APIs, RAG, agents, evaluation - with evaluation named "the most important" in four of the six files
- Transition difficulty ranking (easiest to hardest): ML engineer, backend, data engineer, data scientist, frontend (longest only because backend comes first)

## What is actionable

- Pick the file matching your current role and follow its numbered path; all paths end at build-RAG -> learn-evaluation -> build-agent
- For career changers without an engineering background, the [webinars](webinars.md) Q&A adds: learn Python and testing first, apply for jobs while learning
