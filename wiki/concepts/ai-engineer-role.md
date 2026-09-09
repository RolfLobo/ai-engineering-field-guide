# AI Engineer Role

What "AI engineer" actually denotes in the 2026 job market, synthesized across the repo's data sections. Sources: [role section](../summaries/role.md) (primary), [webinars 1-2](../summaries/webinars.md), [learning paths](../summaries/learning-paths.md), [field guide overview](../summaries/field-guide-readme.md).

## The definition

An AI engineer integrates AI into the product. The model already exists - work happens through provider APIs (OpenAI, Anthropic) - so the job is engineering: prompt design and versioning, RAG, agents, evaluation, deployment, monitoring. "An AI engineer is first and foremost an engineer. The AI part comes second." ([role/01-my-vision.md](../../role/01-my-vision.md), [learning-paths/from-backend-engineer.md](../../learning-paths/from-backend-engineer.md))

## The three role types under one title

From 6,964 postings, Feb-Aug 2026 ([role/02-skills.md](../../role/02-skills.md)):

- AI-First - 70.0%: works ON AI (RAG systems, agents, LLM features)
- AI-Support - 24.2%: works NEAR AI (platforms, infrastructure, tooling, UIs for AI products)
- ML - 4.9%: traditional ML rebranded with the AI title

The test: does the role work on AI systems or near them? Titles are unreliable - "AI Engineer" is the most trustworthy title (92% AI-First) while "AI Platform Engineer" is a coin flip. Candidate reports confirm the confusion from the other side ([role/05-reality-vs-postings.md](../../role/05-reality-vs-postings.md)).

## Full-stack and applied

- 86.8% of AI-First roles need skills beyond GenAI; 70.6% combine GenAI with production/ops (Docker, Kubernetes, CI/CD); only 3.9% expect pure GenAI work
- 97.1% of roles are applied/production, not research
- Python is mandatory (70.8%); one cloud (AWS 40.3% > Azure 29.6% > GCP 27.4%) is the norm

## What the work actually is

- RAG (39.8% of all jobs) and agents (55.4%) are the two dominant patterns, usually asked together
- The #1 use case is automating manual workflows (23.9% of mentions, 69.0% of jobs) - unglamorous reduction of repetitive work at scale; enterprise internal operations is #2
- Five role archetypes from clustering ([role/07-trends.md](../../role/07-trends.md)): agent builder 28.6%, RAG app builder 25.3%, cloud/ML platform 18.0%, DevOps/full-stack 13.3%, ML trainer/researcher 8.2%

## The directional shift

The strongest signal in the dataset (Feb -> Aug 2026): within AI-First roles the integrator stack (RAG/agents/APIs) rose from 80.0% to 88.0% while the trainer stack (PyTorch/TensorFlow/fine-tuning/CUDA) fell from 37.5% to 30.4%. Fine-tuning is a specialization, not core: 84.6% of AI-First roles never mention it. The dedicated "AI infra engineer" has not emerged - inference/serving work halved and stays inside platform roles. Meanwhile the FDE variant - customer-facing production deployers - is the fastest-growing title (4.2x in six months).

## Comparison with adjacent roles

- ML engineer - owns model weights; AI engineer calls APIs. "Replace a call to a locally hosted model with a call to OpenAI - the rest is the same." Easiest transition into the role
- Data scientist - owns model creation and experiments; AI engineers do no real modeling. DS bring evaluation mindset (their advantage) and must add engineering
- Software engineer - the base identity; adds AI-specific skills: prompt engineering/versioning, RAG, agents, LLM-specific evaluation and monitoring

## Inference (my synthesis, not a source claim)

- Reading the repo together: the role is consolidating around "software engineer who ships reliable LLM systems" - every section independently converges on evaluation plus production skills as what separates candidates, while model-training skills fade
- The junior market being pinned near 1% of postings all eight months, combined with full-stack expectations, suggests the role is hired as a second specialization, not an entry point - consistent with the [learning paths](../summaries/learning-paths.md) premise that you transition from an adjacent role
