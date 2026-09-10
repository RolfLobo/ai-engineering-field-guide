# Wiki

An LLM-maintained knowledge wiki for AI engineering topics, following [Karpathy's LLM Wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f): the human curates sources and asks questions; the LLM writes, cross-references, and maintains every page.

The first corpus is this repo itself: every authored file of the field guide is summarized and cross-referenced here - see [answers/repo-content-map.md](answers/repo-content-map.md) for the file-by-file mapping.

## How to use it

- Ingest - drop a source document into `raw/` (or hand the agent a URL) and ask it to process it; it will summarize, update related pages, and log the change
- Query - ask questions; answers cite wiki pages, and reusable answers get filed into `answers/`
- Lint - periodically ask for a health check (contradictions, stale claims, orphans, missing pages)

## Where to look

- [overview.md](overview.md) - main threads and open questions
- [index.md](index.md) - catalog of every page
- [log.md](log.md) - chronological record of everything done to the wiki
- [CLAUDE.md](CLAUDE.md) - the schema: structure, conventions, and the agent's operating manual

## Browsing it

Run `python3 serve_wiki.py` from the repo root and open http://127.0.0.1:8000 - it renders markdown pages as HTML (wiki, market wiki, and the repo docs they cite) and serves charts and the dashboard as-is. Use `--port` to change the port; pass `?raw=1` on any page to see the markdown source.

`raw/` holds the immutable source documents - the source of truth; nothing else in here is ever edited by hand.
