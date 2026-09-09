# Repo Content Map

Every authored file in the repo and where this wiki covers it, from the 2026-09-09 ingest. Use this page to verify coverage and to find the wiki page for any repo file. Data and code directories are raw research material per the [schema](../CLAUDE.md) - they are referenced by the pages that interpret them, not summarized file by file.

## Root

- [README.md](../../README.md) - [field-guide-readme](../summaries/field-guide-readme.md)
- [CLAUDE.md](../../CLAUDE.md) - [field-guide-readme](../summaries/field-guide-readme.md)
- [STYLING.md](../../STYLING.md) - [field-guide-readme](../summaries/field-guide-readme.md)
- [awesome.md](../../awesome.md) - [awesome](../summaries/awesome.md)

## role/

- [README.md](../../role/README.md), [01-my-vision.md](../../role/01-my-vision.md), [02-skills.md](../../role/02-skills.md), [03-responsibilities.md](../../role/03-responsibilities.md), [04-use-cases.md](../../role/04-use-cases.md), [05-reality-vs-postings.md](../../role/05-reality-vs-postings.md), [06-fde.md](../../role/06-fde.md), [07-trends.md](../../role/07-trends.md), [08-trends-appendix.md](../../role/08-trends-appendix.md) - [role](../summaries/role.md), synthesized in [ai-engineer-role](../concepts/ai-engineer-role.md) and [evaluation-differentiator](../concepts/evaluation-differentiator.md)

## interview/

- [README.md](../../interview/README.md), [01-interview-process.md](../../interview/01-interview-process.md), [02-questions.md](../../interview/02-questions.md), [03-get-hired.md](../../interview/03-get-hired.md), [04-after-the-interview.md](../../interview/04-after-the-interview.md), [05-trends.md](../../interview/05-trends.md) - [interview](../summaries/interview.md), synthesized in [interview-process](../concepts/interview-process.md)
- [questions/01-theory.md](../../interview/questions/01-theory.md), [questions/02-coding.md](../../interview/questions/02-coding.md), [questions/03-project-deep-dive.md](../../interview/questions/03-project-deep-dive.md), [questions/04-ai-system-design.md](../../interview/questions/04-ai-system-design.md), [questions/05-behavioral.md](../../interview/questions/05-behavioral.md), [questions/06-home-assignments.md](../../interview/questions/06-home-assignments.md), [questions/questions.md](../../interview/questions/questions.md) - [interview](../summaries/interview.md); question 06 additionally in [take-home-assignments](../concepts/take-home-assignments.md)
- `data/` (sources, research-exports) and `_internal/` (including the AI-vs-ML scoping reference that defines the guide's inclusion boundary) - raw research material; its link lists and exports are part of what [interview](../summaries/interview.md) synthesizes

## portfolio/

- [README.md](../../portfolio/README.md), [01-types-of-projects.md](../../portfolio/01-types-of-projects.md), [02-how-to-pick-a-project.md](../../portfolio/02-how-to-pick-a-project.md), [03-start-a-project.md](../../portfolio/03-start-a-project.md), [04-polishing.md](../../portfolio/04-polishing.md), [05-present-the-project.md](../../portfolio/05-present-the-project.md), [06-common-mistakes.md](../../portfolio/06-common-mistakes.md), [07-project-ideas.md](../../portfolio/07-project-ideas.md) - [portfolio](../summaries/portfolio.md), synthesized in [portfolio-projects](../concepts/portfolio-projects.md)
- `_internal/` (fetched Reddit posts, discussion notes) - raw research material

## learning-paths/

- [README.md](../../learning-paths/README.md), [from-backend-engineer.md](../../learning-paths/from-backend-engineer.md), [from-data-engineer.md](../../learning-paths/from-data-engineer.md), [from-data-scientist.md](../../learning-paths/from-data-scientist.md), [from-frontend-engineer.md](../../learning-paths/from-frontend-engineer.md), [from-ml-engineer.md](../../learning-paths/from-ml-engineer.md) - [learning-paths](../summaries/learning-paths.md)

## webinars/

- [README.md](../../webinars/README.md), [01-a-day-of-ai-engineer.md](../../webinars/01-a-day-of-ai-engineer.md), [02-defining-the-role.md](../../webinars/02-defining-the-role.md), [03-the-interview-process.md](../../webinars/03-the-interview-process.md), [04-take-home-assignments.md](../../webinars/04-take-home-assignments.md), [05-selecting-a-portfolio-project.md](../../webinars/05-selecting-a-portfolio-project.md) - [webinars](../summaries/webinars.md)
- `slides/` (HTML/PDF decks, `to_pdf.py`) - presentation artifacts, referenced not summarized
- `images/` - assets

## job-market/

- [README.md](../../job-market/README.md), [_internal/PIPELINE.md](../../job-market/_internal/PIPELINE.md), [_internal/extract_process.md](../../job-market/_internal/extract_process.md), [_internal/eval/README.md](../../job-market/_internal/eval/README.md) - [job-market](../summaries/job-market.md)
- [analysis.ipynb](../../job-market/analysis.ipynb) - the quantitative analysis notebook; referenced as the source of all numbers in [role](../summaries/role.md)
- `data_raw/`, `data_structured/`, `data_interview/`, `_internal` scripts, `pyproject.toml`, `uv.lock` - raw data and pipeline code

## Not part of the corpus

- `.tmp/` (fetched article transcripts, scratch), `_work-in-progress/` (scratch), `images/` (repo asset), `.claude/` (agent tooling, e.g. `commands/fetch-jobs.md`) - scratch, assets, and tooling, excluded per the schema
- [market-wiki/](../../market-wiki/README.md) - the sibling generated data-view wiki over `data_structured/`, with its own schema, [generator](../../market-wiki/generate.py), and log
- `wiki/` - this wiki itself

## Counts

Authored files covered: 4 root + 9 role + 13 interview + 8 portfolio + 6 learning-paths + 6 webinars + 4 job-market docs = 50 files, mapped to 8 summary pages, 5 concept pages, and 1 entity page.
