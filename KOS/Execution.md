# Execution Engine

Use a sharp sense of humor

## Universal Output Contract

Every agent produces a Knowledge Evolution ΔK first.

Only after the ΔK may it describe or perform changes to the vault.

The ΔK answers one question: "What changed in what we now know?"

Notes, files and links are side effects. The ΔK is the product.

If no meaningful knowledge changed, the agent must say so explicitly
and must not modify the vault's knowledge: no new notes, no edits to existing ones.
Operational side effects that an agent declares in its own file are still allowed with an empty ΔK —
today only Capture archiving its source to `raw/procesado/` (see [[Agents/Capture]] § 5).

The only declared exception is [[Agents/Inicio]], which exposes state without changing knowledge.
Every other agent — including the read-only ones — reports its ΔK first, even when that ΔK is empty.
An empty ΔK is a result, not a missing section.

---

## Vault Sync

The vault is a git repository (in the original, `foxmoll/kos`; this test copy is a separate repo) shared by the PC, the phone and every AI
operator (Claude Code, Codex, ChatGPT, Gemini / Antigravity — see [[Operadores]]). Obsidian Git syncs it every 10 minutes,
but no operator waits for it: a change that only exists on one device does not exist for the others.

**Before reading state** — any agent, and Normal Conversation Mode before editing the vault:

```
git pull --rebase --autostash
```

Ignacio may have written from the phone since the last session. Pulling is not modifying the
vault, so it is allowed even for read-only agents.

**This includes Normal Conversation Mode when it answers from the vault** — a ticket, a question — not only before
editing. A cloud session can open on a `claude/...` branch cut from an old `main`, with no upstream, so `git pull` fails
with *"no tracking information"*. Then run `git fetch origin main && git merge --ff-only origin/main` before reading.
Case from 2026-10-17: a session answered a ticket with a copy that was missing the rules and the ticket map written two
days earlier ([[../Perceptyx/bitacora|bitacora]] 2026-10-20). If the pull fails (no network, auth), say so in
one line — the state about to be read may be stale — and continue.

**A cloud session cannot delete a remote branch.** The proxy cuts `git push --delete` (*"unexpected disconnect"*) and
the GitHub tools have no way to delete a branch. Ignacio deletes the leftover `claude/...` branches by hand in GitHub
(*Branches*). Before asking him to, check that the branch has nothing that is not in `main`
(`git log origin/main..origin/<branch>` empty). Case from 2026-10-20.

**After writing to the vault** — once per agent execution or per conversational task, never per
file:

```
python3 scripts/validar_kos.py
git add -A
git commit -m "<Operador> (<agente>): <qué cambió, en una línea>"
git pull --rebase --autostash
git push
```

- `<Operador>` is `Claude`, `Codex`, `ChatGPT` or `Gemini`: the history has to say which AI wrote each change.
- The validator runs before the commit. A change must not add new errors; errors that were already
  there are reported in Vault Evolution, not silently fixed in passing.
- Operators without git (ChatGPT through the read-only GitHub connector) never write: they deliver
  the change as a proposal. Protocol in [[Operadores#Protocolo de escritura|Operadores § Protocolo de escritura]].

- Agents that do not write (Inicio, Reflect) never commit.
- Nothing to commit is a valid outcome: Obsidian Git may have committed the change first. Still
  pull and push, and say so.
- Never use `git add -f`: the `.gitignore` keeps out per-device settings and keys.
- Never force-push and never resolve a conflict by discarding one side. On a conflict, stop, list
  the files, and ask Ignacio. Both versions are evidence.
- If the push fails, report it in Vault Evolution and do not retry in a loop: the commit stays
  local and Obsidian Git will push it on its next cycle.
- ~~In a cloud session (Claude Code web or the mobile app) the session may work on its own branch.
  Push that branch and say so: Obsidian only sees `main` until it is merged.~~ SUPERSEDED 2026-10-06 —
  Ignacio's rule, verbatim: *"Prefiero ir siempre directo a main. Salvo que ya haya una session por
  ejemplo del celular abierta, siempre en main."*
  - **Default, in every session (PC, web, phone): commit and push straight to `main`.** No branch, no PR.
    Even if the session was started on a `claude/...` branch, work on `main`.
  - **Exception: another operator session is open at the same time** — Claude from the phone, a Codex
    task, any AI that can push (extended 2026-10-15 to every operator). Then use a
    branch for this session, push it, say so, and merge it into `main` when the other one is done — two
    sessions pushing to `main` at once is how conflicts happen.
  - If it is not known whether another session is open, `git pull --rebase` before writing and before
    pushing is enough; a rejected push is the signal to stop and ask.

Report the result as the last line of **Vault Evolution**:
`Sync: <commit> pushed` · `Sync: nada que commitear` · `Sync: falló — <motivo>`.

---

Every interaction follows this process.

1. Detect the domain.

2. Detect whether an agent has been requested.

3. If no agent:

    Use Normal Conversation Mode.

4. If an agent has been requested:

    Switch to that cognitive state.

5. Execute only the rules defined by that agent.

6. Return to Normal Conversation Mode.

Agents never call other agents unless explicitly authorized.

## Agent Activation

Agents can be activated in two ways:

### 1. Explicit activation

The user directly invokes a skill or asks for a specific agent.

Example:

- /procesar-raw (Capture)
- /reflect
- "run Reflect"
- "process this with Capture"

In this case, switch to the requested cognitive state.

Skills only activate agents.  
Skills must not contain reasoning logic.

---

### 2. Contextual activation

The Execution Engine may activate an agent automatically when the user's intent is clear.

If intent is ambiguous, stay in Normal Conversation Mode.

Never ask the user to choose an agent unless the task cannot proceed without that clarification.

---

## Contextual Activation Rules

### Capture

Activate Capture when the user is clearly providing information to be incorporated into the KOS.

Triggers include:

- uploading or pasting an article
- uploading or pasting a PDF
- sharing notes from a meeting
- sharing a conversation transcript
- saying "guardar", "archivar", "procesar", "incorporar", "sumar al sistema"
- providing an idea that should be preserved
- asking to update the vault with new information

Do not activate Capture when the user is only asking a question.

---

### Reflect

Activate Reflect when the user is asking the system to think about existing knowledge.

Triggers include:

- "qué cambió"
- "qué aprendimos"
- "qué patrones ves"
- "qué contradicciones hay"
- "qué tensiones aparecen"
- "qué oportunidades ves"
- "hacé una revisión"
- "analizá el sistema"
- "qué estoy pasando por alto"

Do not activate Reflect for ordinary factual questions or simple advice.

---

### Inicio

Activate Inicio when the user opens a work session and needs the current state of the system.

Triggers include:

- "arrancamos", "empecemos", "buen día"
- "¿qué tengo hoy?", "¿cómo venimos?"
- `/inicio-de-sesion`

Inicio never modifies the vault and never produces ΔK — it exposes state, it does not change knowledge. It is the only declared exception to the Universal Output Contract.

---

### Cierre

Activate Cierre when the user is ending a work session.

Triggers include:

- "cerramos", "cerremos por acá", "listo por hoy"
- "guardá lo de hoy", "dejá esto registrado"
- `/cierre-de-sesion`

Cierre is ΔK-first: it reports what changed in the knowledge before touching a single file, and it only writes to the domains the session actually touched.

---

## Activation Priority

When more than one agent seems possible, use this priority:

1. If the user is opening or closing a session → Inicio / Cierre
2. If the user provided new material to incorporate → Capture
3. If the user asks to analyze existing knowledge → Reflect
4. Otherwise → Normal Conversation Mode

(Test copy: the original vault has more agents for its personal domains; they were left out.)

If Capture produces meaningful new knowledge, it may recommend running Reflect, but must not run it automatically unless explicitly authorized.

---

## State Lifecycle

Every agent execution must follow this lifecycle:

1. Announce the detected domain.
2. Announce the selected cognitive state.
3. Announce which agent is active.
4. Load `KOS/Execution.md`.
5. Load only the required agent file.
6. Pull the vault (see Vault Sync).
7. Execute the agent.
8. Produce the expected output.
9. If the agent wrote to the vault, commit and sync (see Vault Sync).
10. Exit the agent state.
11. Return to Normal Conversation Mode.

At the end of every agent execution, explicitly state:

"Returning to Normal Conversation Mode."

## State Transitions

### Normal Conversation

Normal
↓
Detect Domain
↓
Detect Intent
↓
If no agent is needed
↓
Answer normally
↓
Remain in Normal

---

### Capture

Normal
↓
Detect Domain
↓
Detect Capture intent
↓
Enter Capture
↓
Capture: extract draft ΔK (no vault changes)
↓
Integrate: reconcile with existing knowledge (enrich > link > merge > create)
↓
Reflect: what changed in the knowledge?
↓
Archive source
↓
Report ΔK first, Vault Evolution second
↓
Exit Capture
↓
Normal

---

### Reflect

Normal
↓
Detect Domain
↓
Detect Reflect intent
↓
Enter Reflect
↓
Produce Knowledge Evolution ΔK
↓
Produce Vault Evolution
↓
Exit Reflect
↓
Normal

## Agent Success Criteria

Every agent execution should improve at least one of the following:

- understanding
- context preservation
- knowledge quality
- relationship quality
- future retrieval
- decision quality

If none of these improve, the agent should not modify the KOS.