# /procesar-raw

Purpose:
Launch the KOS Capture workflow for unprocessed files in `raw/`.

This skill contains no reasoning logic.

Execution:

1. Load `KOS/Execution.md`.
2. Switch cognitive state to `Capture`.
3. Load `KOS/Agents/Capture.md`.
4. Process all unprocessed files in `raw/`, ignoring:
   - `README.md`
   - `procesado/`
5. Follow the Capture agent exactly.
6. Produce output in this order:

## Knowledge Evolution ΔK
- New concepts
- New principles
- New tensions
- New hypotheses
- New relationships
- Confidence changes

## Synthesis (only when genuine)
- One non-obvious idea from crossing the ΔK with the rest of the graph — or state that none emerged. Never force one.

## Vault Evolution
- Objects updated
- Objects created
- Relationships created
- Files archived
- Recommended follow-up actions

7. Archive processed source files only after integration is complete.
8. Commit and sync, as the Capture agent defines.
9. Exit Capture state.
10. Return to Normal Conversation Mode.

Rules:

- Do not decide structure inside this skill.
- Do not create notes based only on this skill.
- Do not summarize files as the final result.
- Always explain what changed in the knowledge before explaining what changed in the vault.
- If no meaningful knowledge changed, say so explicitly.
