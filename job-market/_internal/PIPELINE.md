# Job Scraping Pipeline

## Overview

```
Built In listing pages
  │
  ├─ scrape_builtin_requests.py  (requests + DataImpulse proxy)
  │   └─ jobs/builtin/{site}_{YYYYMMDD}.json    (per-location)
  │   └─ data/scrapes/{YYYY-MM-DD}/all_jobs.csv
  │
  ├─ clean_dedup.py
  │   └─ data/scrapes/{YYYY-MM-DD}/all_jobs_dedup.csv
  │   └─ data/all_jobs_dedup.csv                (global, all months, with scraped_date)
  │
  ├─ download_all_html.py  (requests + DataImpulse, 8 threads)
  │   └─ jobs/raw/{YYYY-MM-DD}/{title}_{job_id}.html
  │
  ├─ extract_from_html.py
  │   └─ data_raw/{YYYY-MM-DD}/{job_id}_{company}_{title}.yaml
  │
  └─ extract_llm.py  (Z.ai / GLM-4.7)
      └─ data_structured/{YYYY-MM-DD}/{job_id}_{company}_{title}.yaml
```

## Environment Variables

Proxy settings live in `job-market/_internal/scrapers/proxy_config.py`, which
uses the same proxy as the fetch-youtube skill: DataImpulse first, Oxylabs
as fallback. Credentials resolve from already-exported env vars, then the
project-root `.env`, then `~/.config/youtube/.env` (the youtube skill's
machine-local config, mode `600` — no need to duplicate them here):

| Variable | Description |
|----------|-------------|
| `DATAIMPULSE_USER` / `DATAIMPULSE_PASSWORD` | DataImpulse login (preferred proxy) |
| `DATAIMPULSE_ENDPOINT` (or `DATAIMPULSE_HOST` + `DATAIMPULSE_PORT`) | Proxy endpoint (default: `gw.dataimpulse.com:823`) |
| `OXYLABS_USER` / `OXYLABS_PASSWORD` / `OXYLABS_ENDPOINT` | Oxylabs fallback (default endpoint `pr.oxylabs.io:7777`) |
| `ZAI_API_KEY` | Z.ai API key (Anthropic-compatible) |

## Directory Structure

```
job-market/
├── _internal/                    # Pipeline scripts and intermediate data
│   ├── scrapers/
│   │   ├── scrape_builtin_requests.py   # Step 1: Scrape listings
│   │   ├── download_all_html.py         # Step 3: Download job pages
│   │   ├── extract_from_html.py         # Step 4: HTML → YAML
│   │   └── pagination/                  # Legacy Playwright scraper
│   │   ├── clean_dedup.py               # Step 2: Deduplication
│   ├── data/
│   │   ├── all_jobs_dedup.csv           # Global dedup CSV (all months, with scraped_date)
│   │   └── scrapes/{YYYY-MM-DD}/
│   │       ├── all_jobs.csv             # Raw combined listings for one scrape
│   │       └── all_jobs_dedup.csv       # Deduplicated new jobs for one scrape
│   ├── extract_llm.py                   # Step 5: LLM enrichment
│   ├── backfill_location.py             # Repatch location fields from stored HTML
│   └── jobs/
│       ├── builtin/                     # Per-site JSON files
│       └── raw/{YYYY-MM-DD}/            # Downloaded HTML pages grouped by scrape date
├── data_raw/{YYYY-MM-DD}/        # Extracted YAML grouped by scrape date
├── data_structured/{YYYY-MM-DD}/ # LLM-enriched YAML grouped by scrape date
└── analysis.ipynb                # Analysis notebook
```

## Steps

### Step 1: Scrape Listings

```bash
cd job-market/_internal
python scrapers/scrape_builtin_requests.py
```

- Scrapes all 5 Built In locations (LA, Berlin, London, Amsterdam, New York)
- Saves per-location JSONs: `jobs/builtin/{site}_{YYYYMMDD}.json`
- Combines into: `data/scrapes/{YYYY-MM-DD}/all_jobs.csv`
- Pass site names to scrape specific locations: `python scrapers/scrape_builtin_requests.py la berlin`
- Pass `--date 2026-03-15` to override date stamp

If requests fails (Built In requires JS rendering), fall back to the Playwright scraper in `scrapers/pagination/scrape_builtin_cards.py`.

### Step 2: Deduplicate

```bash
python scrapers/clean_dedup.py data/scrapes/{YYYY-MM-DD}/all_jobs.csv
```

- Removes spam companies (Alignerr)
- Deduplicates within the scrape by (title, company)
- Removes IDs already in global `data/all_jobs_dedup.csv`
- Saves date-specific: `data/scrapes/{YYYY-MM-DD}/all_jobs_dedup.csv`
- Appends new jobs to global: `data/all_jobs_dedup.csv` (with `scraped_date` column)

### Step 3: Download HTML

```bash
python scrapers/download_all_html.py --csv data/scrapes/{YYYY-MM-DD}/all_jobs_dedup.csv
```

- Downloads full job pages for each URL in the CSV
- 8 concurrent threads, 3 retries per URL
- Skips already-downloaded files across `jobs/raw/`
- Failed URLs saved to `jobs/queue/failed_urls.txt`

### Step 4: Extract to YAML

```bash
python scrapers/extract_from_html.py --all --csv data/scrapes/{YYYY-MM-DD}/all_jobs_dedup.csv
```

- Parses HTML files and extracts structured job data
- Primary source: JSON-LD structured data
- Fallback: HTML parsing (title, skills, company size)
- Output: `data_raw/{YYYY-MM-DD}/{job_id}_{company}_{title}.yaml`

### Step 5: LLM Enrichment

```bash
python extract_llm.py --all --csv data/scrapes/{YYYY-MM-DD}/all_jobs_dedup.csv
```

- Sends each job description to Z.ai (GLM-4.7)
- Classifies AI type (ai-first, ml-first, ai-support)
- Extracts skills by category, responsibilities, use cases
- Carries the scraped location fields through to `meta` unchanged
- Skips already-processed files
- Output: `data_structured/{YYYY-MM-DD}/{job_id}_{company}_{title}.yaml`

## Location

Locations come from the job page's JSON-LD (`jobLocation`, `jobLocationType`), never from the LLM. Three fields carry through the whole pipeline:

- `location` - primary location as `City, CCC`, or just `CCC` when Built In gives no city
- `locations` - every listed location, primary first; only written for multi-location postings
- `remote` - `true` when the posting is flagged `TELECOMMUTE`; omitted otherwise

Country codes are ISO-3166 alpha-3, plus Built In's own `EUR` pseudo-code for unspecified Europe.

In `data_raw` these sit at the top level. In `data_structured` they sit under `meta`, alongside `job_id`. Read them in analysis code through the helpers in `analysis/common.py`:

- `job_locations(job)` - all locations, primary first
- `primary_location(job)` - the first listed location
- `job_countries(job)` - distinct country codes, primary first
- `split_location(loc)` - `'Bengaluru, IND'` into `('Bengaluru', 'IND')`
- `country_name(code)` - readable country name
- `is_remote(job)` - remote flag

### Backfilling location

```bash
python backfill_location.py --dry-run
python backfill_location.py
```

Re-reads the stored HTML in `jobs/raw/` and patches only the location lines in `data_raw` and `data_structured`, leaving descriptions and every other field byte-identical. Safe to re-run; it is idempotent.

Use it after fixing a location parsing bug, or to fill in months scraped before those fields existed. Jobs whose HTML is no longer on disk keep whatever `data_raw` already holds - re-download their pages first with `download_all_html.py` if you need them re-parsed.

## Deduplication Strategy

1. **Spam removal**: Filter out known spam companies (e.g., Alignerr)
2. **Within-scrape dedup**: `drop_duplicates(subset=['title', 'company'])`
3. **Cross-month dedup**: Remove IDs already in global `data/all_jobs_dedup.csv`

Job IDs are extracted from Built In URLs (last path segment) and are stable across scrapes. The global `data/all_jobs_dedup.csv` is the single source of truth for which jobs have been processed and which dated folder a job belongs to.

## Running for a New Month

```bash
cd job-market/_internal

# 1. Scrape
python scrapers/scrape_builtin_requests.py

# 2. Dedup
python scrapers/clean_dedup.py data/scrapes/{YYYY-MM-DD}/all_jobs.csv

# 3. Download HTML
python scrapers/download_all_html.py --csv data/scrapes/{YYYY-MM-DD}/all_jobs_dedup.csv

# 4. Extract YAML
python scrapers/extract_from_html.py --all --csv data/scrapes/{YYYY-MM-DD}/all_jobs_dedup.csv

# 5. LLM enrichment
python extract_llm.py --all --csv data/scrapes/{YYYY-MM-DD}/all_jobs_dedup.csv

# 6. Canonicalize skill names
python analysis/canonicalize_skills.py

# 7. Re-run analysis.ipynb on combined dataset
```

## Before Changing the Model or the Prompt

Either change silently rewrites what the numbers mean. The `glm-5.1` to
`glm-5.2` switch mid-2026 moved the AI-First share by up to 10 percentage
points and added 6 skills per job, none of it real. Extract to a staging
directory first, never over `data_structured/`, and run the checks in
[eval/](eval/):

```bash
# cheap, no judge, run these on every scrape - not just prompt changes.
# with no argument it checks the current corpus for self-consistency;
# with a git ref it also diffs against that ref's extraction.
eval/run_checks.sh 7e269b34

# the 50-job blind A/B, for a substantive prompt change. use a fresh seed:
# seed 2026 has already been graded and is a regression set, not evidence.
uv run python eval/build_eval.py --baseline /tmp/base --out ./run2 --seed 4242
```

Each extracted record stamps `meta.model` and `meta.prompt_sha`, so a mixed
corpus is visible in the data rather than having to be reconstructed later.

All months' data accumulates under dated folders in `data_raw/` and `data_structured/` — the analysis notebook and helper scripts read those directories recursively.
