# Role Section (repo: role/)

- Sources: [role/](../../role/) - analysis of the AI engineer role from 6,964 job descriptions scraped from builtin.com in eight monthly scrapes, Feb 4 - Aug 25, 2026 ([dataset](../../job-market/README.md))
- Related: [AI engineer role](../concepts/ai-engineer-role.md), [evaluation as the differentiator](../concepts/evaluation-differentiator.md), [job-market pipeline](job-market.md), [learning paths](learning-paths.md)

## What the section says

The role section is the analytical core of the field guide. Its headline: "AI Engineer" in 2026 is a new, distinct, mostly full-stack role built on integrating pre-trained models (RAG, agents, orchestration), not training them. Three role types hide under one title: AI-First 70.0%, AI-Support 24.2%, ML rebranded 4.9% (role/README.md). 86.8% of AI-First roles need skills beyond GenAI; only 3.9% expect pure GenAI work. Evaluation skills are explicitly required by 59.7% of AI-First roles - the differentiator in a market where RAG and agents are baseline.

## Files covered

- [role/README.md](../../role/README.md) - section overview and key takeaways; the numbers above come from here
- [role/01-my-vision.md](../../role/01-my-vision.md) - Alexey Grigorev's personal definition: AI engineers integrate AI into the product via provider APIs, starting from a real user problem. Progressive complexity: plain LLM call, RAG (~5x harder), agents (~10x harder). Ten professional-practice steps beyond "just call the API" (prompt testing, eval dataset, A/B rollout, monitoring, logs, human annotators, model-update regression checks, prompt versioning, feedback loops). vs ML engineer: MLE owns model weights, AI engineer calls APIs - easiest transition. vs data scientist: no real modeling, most effort goes to prompt tuning; DS must add engineering, MLE must add evaluation
- [role/02-skills.md](../../role/02-skills.md) - the skills analysis over all 6,964 jobs: Python 70.8%, LLMs 62.2%, agents (any) 55.4%, RAG 39.8%, prompt engineering 34.7%, AWS 40.3% > Azure 29.6% > GCP 27.4%. Framework ecosystem travels together (LangChain 22.0%, LangGraph 13.8%, LlamaIndex 8.3%). Fine-tuning: 27.3% of AI-First postings mention it, but only 3.6% have it as primary responsibility and 84.6% don't mention it at all - a specialization, not core. 54.0% of AI-First roles need some ML (practical: fine-tuning 24.8%, embeddings 22.9%, PyTorch 19.5%). Research roles are 2.9% of the market. Title analysis: "AI Engineer" is the most reliable title (92% AI-First); "platform"/"data" titles are coin flips. MCP is the clearest steady riser: 9.9% (Feb) to 17.6% (Aug)
- [role/03-responsibilities.md](../../role/03-responsibilities.md) - 33,957 responsibilities from 4,894 jobs (Feb-Jun scrapes), categorized with AI assistance (methodology note inside). Building AI systems appears in 98.1% of jobs; productionizing (deploy 78.3%, monitoring 64.3%), evaluation and quality 68.5%, API integration 62.4%. Self-hosting models is rare (2.5%) - the market uses provider APIs. Feb vs Jun shift: agents +13.1 points into the majority (54.8%), research -13.1, security +9.4
- [role/04-use-cases.md](../../role/04-use-cases.md) - 24,502 use cases from 4,894 jobs. Automating manual workflows is #1 (23.9% of mentions, 69.0% of jobs); internal enterprise operations next (21.3%); agentic systems 15.5%; RAG/knowledge access 12.6%. Domains: finance 9.5%, healthcare 7.3%, legal 4.5%, cybersecurity 4.2%. Feb vs Jun: automation +10.6, enterprise ops +13.6, personalization -9.4 - the center of gravity moves from consumer features to internal automation
- [role/05-reality-vs-postings.md](../../role/05-reality-vs-postings.md) - qualitative counterweight from Reddit/X discussions: job descriptions describe ambition, not the day job ("80% prompt engineering + glue code + monitoring"). Three actual work types: orchestrators ~50%, evals specialists ~40%, efficiency wrappers ~10%. Titles are broken; combo roles (3 roles in 1) are a common complaint
- [role/06-fde.md](../../role/06-fde.md) - Forward Deployed Engineer analysis: 28 live FDE listings (Feb 2026) to 118 (Jul), 4.2x growth vs 2.3x for the whole market. 146 unique roles from 94 companies. The profile: production ownership (90%) plus direct customer work (88%); Python 91%, prompt engineering 55%, RAG 52%. Not entry level - zero junior titles
- [role/07-trends.md](../../role/07-trends.md) - month-over-month trends across all eight scrapes: the integrator stack (RAG/agents/APIs) rose 80.0% to 88.0% within AI-First while the trainer stack (PyTorch/TensorFlow/fine-tuning/CUDA) fell 37.5% to 30.4% - the strongest directional signal in the dataset. Five role archetypes from k-means clustering: agent builder 28.6% (now largest), RAG app builder 25.3%, cloud/ML platform 18.0%, DevOps/full-stack 13.3%, ML trainer/researcher 8.2%. Staff+ share nearly halved (18.5% to 11.0%); junior stays pinned near 1%. The dedicated "AI infra engineer" still has not emerged (inference/serving halved to 9.9%)
- [role/08-trends-appendix.md](../../role/08-trends-appendix.md) - methodology and full tables: scrape sizes, cluster signatures with lift values, monthly mix tables, agent-framework churn (LangGraph 37.7% to 61.4% among framework users; DSPy the one outright loser), extraction model/prompt fingerprinting (glm-5.2, fixed prompt_sha)

## Key claims

- The role is full-stack applied engineering: 97.1% applied vs research, 70.6% of AI-First roles combine GenAI with production/ops skills (role/README.md, role/02-skills.md)
- RAG + agents together cover most of the work: agents 55.4% of all jobs, RAG 39.8%, both listed together in 2,213 jobs (role/02-skills.md)
- Evaluation is the differentiator; RAG and agents are baseline (role/README.md; cross-confirmed by [interview](interview.md) and [home assignments](../concepts/take-home-assignments.md))
- Fine-tuning is overhyped relative to demand (role/02-skills.md) - the wiki carries this as a flagged tension with [interview](interview.md) prep sources that still teach LoRA/transformer implementation for frontier-lab coding rounds; both are true for different role segments
- The market data describes postings, not day jobs; candidate reports show a gap (role/05-reality-vs-postings.md)

## What is actionable

- Learn RAG and agents deeply first; add evaluation as the differentiator; treat fine-tuning as an optional specialization (role/02-skills.md bottom lines)
- Read "AI Platform Engineer" and "AI Data Engineer" postings carefully - the title predicts the stack badly (role/02-skills.md)
- Domain selection for projects should start from the use-case data: finance, healthcare, legal, cybersecurity ([portfolio](portfolio.md) uses exactly this)
