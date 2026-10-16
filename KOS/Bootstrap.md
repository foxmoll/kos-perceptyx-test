# KOS Bootstrap

Model-neutral entry point of the vault. Every AI operator (Claude Code, Codex, ChatGPT, or any future
one) loads this file first, through its own thin adapter: `CLAUDE.md`, `AGENTS.md` or `GEMINI.md`. The adapters only say *how* each tool reaches this
file and the launchers; *what* the system is lives here and in the rest of `KOS/`. Full design in
[[KOS/Operadores|KOS/Operadores]].

## Role

Adopt the KOS philosophy before interacting with the vault.

The objective is to improve the user's thinking, not merely answer questions.

---

## Test copy

This repository is a **minimal test copy** of Ignacio Moll's KOS, made on 2026-10-16 to check whether
Google Antigravity (and Gemini) can operate the protocol. It holds only the Perceptyx domain and the
system layer: the personal domains of the original vault were left out on purpose. Nothing here is the
source of truth; the original vault is.

---

## Knowledge Domains

Every top-level folder of the vault is declared here. A folder that is not on this map is a folder
the system does not know when to read — see `KOS/MANIFESTO.md` § Contenedores.

### Operational Domain

Includes:

- `Perceptyx/` — Ignacio's current job (Delivery Operations Manager). Mainly a
  **knowledge base** (Reference regime): procedures, the different ways to resolve each ticket type, and
  why. Operational only to help with the ticket at hand — **no tracking of ticket completion** (Ignacio,
  2026-10-09; `KOS/Reglas.md` § 9). The
  environment changes week to week: every fact carries its date of validity, source and certainty mark,
  and what changes is marked `SUPERSEDED`, never deleted. **No client data**: only processes and ways
  of resolving, tickets recorded as anonymized patterns. Convention in `Perceptyx/_indice.md`.

Characteristics:

- prioritize execution
- prioritize current state
- recommend next actions

---

### System (not a knowledge domain)

- `KOS/` — the protocol itself: this bootstrap, manifesto, execution kernel, agents, working rules,
  operators. Read at bootstrap, not per domain.
- `.claude/commands/` — launchers. Only activation, no reasoning logic. Single location, no domain
  copies. The folder name is Claude's, but the content is model-neutral: Claude Code exposes them as
  skills, every other operator reads `.claude/commands/<name>.md` as a file when asked for `/<name>`.
- `CLAUDE.md`, `AGENTS.md` and `GEMINI.md` (vault root) — operator adapters (Claude Code; Codex and Antigravity; Gemini CLI). They point
  here; they never hold knowledge or rules of their own.
- `raw/` — unprocessed inbox. Entered only via `/procesar-raw`; `raw/procesado/` is the archive.
- `scripts/` and `.github/` — the structural validator (`scripts/validar_kos.py`) and the GitHub
  Action that runs it on every push: broken wikilinks, launchers pointing to missing agents,
  undeclared top-level folders, duplicate content names. It checks structure, never knowledge.

---

## General Workflow

1. Detect the domain.

2. Read only the required indexes.

3. Traverse the graph only as necessary.

4. Integrate knowledge.

5. Answer.

6. If new knowledge emerged:

- enrich existing objects first
- create new objects only if necessary
- create explicit relationships
- preserve reasoning

---

## Permanent Rules

Never claim information doesn't exist without searching the vault first (Grep/Glob at minimum). This applies especially after context compaction: previously-read files are no longer in working memory — re-search, never answer from memory.

Never ask the user for information already available in the current message (attached files, pasted content) or in the vault.

Never create knowledge duplication.

Never resolve a new *use* with a copy. A new way of reading knowledge that already exists is solved
with an index, a pointer or a view — never with a new folder holding the same material. Two files
of *content* with the same name anywhere in the vault are a defect: they make every short wikilink
ambiguous. Structure files (`_indice`, `_dashboard`, `_esquema`, `README`) do repeat per domain —
they must always be linked with their path, never with a short wikilink.
Full rule in `KOS/MANIFESTO.md` § Contenedores.

Never confuse hypotheses with facts.

Never destroy historical reasoning.

Always preserve evidence.

Prefer evolution over accumulation.

Improve the knowledge base whenever appropriate.

The vault, not any operator's local memory, is the source of truth for working rules. They live in
`KOS/Reglas.md`. When Ignacio gives a new correction, write it there (or in the closest domain
node) — never only in memory, which stays on one machine and in one AI product.

## Bootstrap sequence

Before performing any work:

1. Adopt the philosophy described in KOS/MANIFESTO.md.

2. Follow the execution model described in KOS/Execution.md.

3. Apply the working rules in KOS/Reglas.md: § 1–4 always, plus the section of the active domain.

4. Identify the active domain (in this test copy, always Perceptyx).

5. Read only the indexes required for that domain.

6. Execute the appropriate agent if requested.