# Market Wiki

A data-view wiki built from the job-description dataset in [job-market/data_structured/](../job-market/data_structured/): 6,964 postings from builtin.com, scraped monthly. Where the main [wiki/](../wiki/) summarizes the repo's documents, this one aggregates the raw postings themselves - skills, use cases, industries, companies, locations, and month-over-month trends - with SVG charts and a one-page [dashboard](charts/dashboard.html).

Start at [pages/index.md](pages/index.md), or open [charts/dashboard.html](charts/dashboard.html) in a browser for the visual version.

## How it is built

Everything under `pages/` and `charts/` is generated in full by [generate.py](generate.py) - a deterministic, stdlib-plus-PyYAML script (no LLM calls, no matplotlib). Rerunning it always produces the same output for the same data, so diffs after an update show exactly what changed in the market.

Two views are keyword-classified approximations, marked as such on their pages:

- industries - matched from company focus text, then company name, then job title (the dataset has no industry field); about 15% of postings stay unclassified
- use-case themes - keyword matching over the extracted use-case sentences; one posting can carry several themes

## How to update it

When a new monthly scrape lands in `job-market/data_structured/<date>/` (via the `fetch-jobs` command and the [pipeline](../job-market/_internal/PIPELINE.md)):

1. Regenerate: `job-market/.venv/bin/python market-wiki/generate.py`
2. Review the diff - pages and charts are rewritten in full, so `git diff` shows every number that moved
3. Note anything notable in [log.md](log.md) and, if a trend is significant, update the main [wiki/](../wiki/) synthesis pages (e.g. the role trends) to match

No configuration needed: the script picks up every scrape directory present, so new months flow through automatically.

## Layout

- `generate.py` - the generator; the only thing that writes `pages/` and `charts/`
- `pages/` - generated markdown views (index, skills, use cases, industries, companies and locations, trends)
- `charts/` - generated SVG charts plus `dashboard.html`
- `log.md` - regeneration history, one entry per run day
