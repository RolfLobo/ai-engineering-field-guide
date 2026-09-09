# Market Wiki Schema

Sibling of [wiki/CLAUDE.md](../wiki/CLAUDE.md), with a different contract: this directory is a generated data view of the job-description dataset, not an LLM-written summary corpus.

## Layers

- `pages/` and `charts/` - generated artifacts. Never hand-edit; change [generate.py](generate.py) and rerun instead.
- `README.md`, this schema, `log.md` - hand/LLM-maintained. Keep them current when the generator's contract changes.
- The dataset in [job-market/data_structured/](../job-market/data_structured/) is the source of truth; `data_raw/` and `_internal/` scripts are upstream of it and out of scope here.

## Rules

1. Regeneration is the update path: `job-market/.venv/bin/python market-wiki/generate.py` after each new scrape. One entry per run day in `log.md` (the script appends it).
2. Generated markdown follows the repo [STYLING.md](../STYLING.md): no bold, no italics, no horizontal rules, blank lines around lists, one H1 per page, one-decimal percentages.
3. Approximations must be flagged on the page that presents them (currently: industries and use-case themes are keyword classifiers).
4. Shares are within-scrape fractions of postings - never describe them as headcount or hiring volume. Cite the scrape window (currently Feb 4 - Aug 25, 2026, eight scrapes).
5. Numbers quoted in the main `wiki/` must come from the repo's own analysis (`role/`), not from this wiki's keyword classifiers, when the two could differ.
