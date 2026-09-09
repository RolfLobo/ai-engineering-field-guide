# LLM Wiki (Karpathy, April 2026)

- Source: [gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) - local copy in [raw/2026-04-karpathy-llm-wiki.md](../raw/2026-04-karpathy-llm-wiki.md)
- Author: Andrej Karpathy
- Related: [LLM wiki pattern](../concepts/llm-wiki-pattern.md)

## What it says

The gist proposes an alternative to RAG for personal knowledge bases. RAG re-derives knowledge from scratch on every question - nothing accumulates, and a question spanning five documents means reassembling fragments every time. Instead, the LLM incrementally builds and maintains a persistent wiki between the human and the raw sources: on each ingest it reads the source, extracts key information, and integrates it - updating entity pages, revising summaries, flagging contradictions, adjusting the synthesis. Knowledge is compiled once and kept current, not re-derived per query.

The division of labor: the human never writes the wiki; the human curates sources, explores, and asks good questions. The LLM does the bookkeeping - summarizing, cross-referencing, filing - that makes knowledge bases fail when humans have to do it themselves. His working setup: agent on one side of the screen, Obsidian on the other. "Obsidian is the IDE; the LLM is the programmer; the wiki is the codebase."

## Key claims

- The wiki is a persistent, compounding artifact - cross-references already exist, contradictions are already flagged, synthesis already reflects everything read so far (gist, "The core idea")
- Three layers: raw sources (immutable), the wiki (LLM-owned markdown), and the schema (a CLAUDE.md / AGENTS.md that turns the LLM into a disciplined maintainer)
- Three operations: ingest, query, lint - a single ingest can touch 10-15 wiki pages (gist, "Operations")
- A content catalog (`index.md`) read before answering scales to ~100 sources / hundreds of pages without embedding-based RAG; an append-only greppable `log.md` records every operation (gist, "Indexing and logging")
- Good query answers should be filed back into the wiki as new pages, so explorations compound like ingests do
- The bottleneck is bookkeeping, not thinking: humans abandon wikis because maintenance grows faster than value, and LLMs remove that cost (gist, "Why this works")
- Frames the idea as a realization of Vannevar Bush's Memex (1945), with the maintenance problem - the part Bush could not solve - handled by the LLM

## What is actionable for this wiki

- The whole structure of this directory follows the gist: `raw/`, `summaries/`, `concepts/`, `entities/`, `answers/`, `overview.md`, `index.md`, `log.md`, with this schema in `CLAUDE.md`
- The gist is intentionally abstract and says every convention is optional and should be co-evolved - so changes to this schema are expected, not exceptions
- Suggested tooling to consider when scale demands it: qmd (local hybrid search over markdown), Obsidian Web Clipper for getting sources into `raw/`, graph view for spotting hubs and orphans, Marp for slides from wiki content
