# LLM Wiki Pattern

A pattern for building personal knowledge bases in which the LLM incrementally builds and maintains a persistent, interlinked wiki instead of re-deriving knowledge at query time. Contrast with RAG: retrieval reassembles fragments from scratch on every question and nothing accumulates; the wiki compiles knowledge once and keeps it current.

- Sources: [LLM Wiki (Karpathy, April 2026)](../summaries/2026-04-karpathy-llm-wiki.md) - local raw copy in [raw/](../raw/2026-04-karpathy-llm-wiki.md)

## Three layers

- Raw sources - curated, immutable source documents; the LLM reads but never modifies them
- The wiki - LLM-generated markdown: summaries, entity and concept pages, overview, synthesis; the human reads it, the LLM writes it
- The schema - a config document (CLAUDE.md / AGENTS.md) defining structure, conventions, and workflows; the discipline layer that separates a wiki maintainer from a generic chatbot

## Three operations

- Ingest - read a new source, write a summary page, update affected concept/entity pages, revise the overview, update the index, append the log; one source can touch 10-15 pages
- Query - answer from the wiki (index first, drill into pages, raw only when needed), cite, and file reusable answers back as new pages so explorations compound
- Lint - periodic health check: contradictions, stale claims, orphans, missing pages, missing cross-references, gaps fillable by web search

## Why it works

The tedious part of a knowledge base is not reading or thinking but bookkeeping, and humans abandon wikis because maintenance grows faster than value. LLMs do not get bored, do not forget cross-references, and can touch 15 files in one pass - maintenance cost drops to near zero. The human keeps the jobs that need a person: curating sources, directing analysis, asking good questions, deciding what it means.

## Applications named in the source

- Personal - goals, health, psychology, fed by journal entries and podcast notes
- Long-running research with an evolving thesis
- Book companions in the style of fan wikis (Tolkien Gateway is the example)
- Team wikis fed by Slack, meeting transcripts, customer calls
- Competitive analysis, due diligence, trip planning, course notes, hobbies

## Relation to other systems

- RAG / NotebookLM / ChatGPT file uploads - retrieve and re-derive per query; no accumulation
- Vannevar Bush's Memex (1945) - personal curated store with associative trails; the unsolved maintenance problem is what the LLM supplies
- This wiki - this directory is an instantiation of the pattern; see the schema in [CLAUDE.md](../CLAUDE.md)
