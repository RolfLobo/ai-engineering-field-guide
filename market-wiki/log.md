# Log

Regeneration history. `pages/` and `charts/` are rewritten in full on every run; this log records when and against what data. The generator appends one entry per run day.

## [2026-09-09] first build | 6,964 postings, 8 scrapes (Feb 4, 2026 to Aug 25, 2026)

- Built the market wiki: [generate.py](generate.py) reads every scrape in job-market/data_structured/ and emits 6 pages and 9 SVG charts plus [dashboard.html](charts/dashboard.html)
- Cross-checked against the repo's published analysis: AI-First 70.0% / AI-Support 24.2% / ML-First 4.9% match [role/README.md](../role/README.md); MCP 9.9% to 17.6% and the LangGraph rise match [role/02-skills.md](../role/02-skills.md) and [role/08-trends-appendix.md](../role/08-trends-appendix.md)
- Known approximations: industries and use-case themes are keyword classifiers (flagged on their pages)
