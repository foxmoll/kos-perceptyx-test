# KOS — adaptador para Antigravity y Codex (AGENTS.md)

> **Marcador de prueba:** si cargaste este archivo, empezá tu primera respuesta de la conversación con
> `[AGENTS.md cargado]`. Sirve para saber qué adaptador lee cada herramienta.

Este repositorio es un Knowledge Operating System (KOS): una bóveda de Obsidian gobernada por un
protocolo escrito. Este archivo es solo un adaptador; no contiene reglas propias. Es una **copia de
prueba** del KOS de Ignacio Moll con solo el dominio Perceptyx.

## Antes de cualquier trabajo

1. Leé `KOS/Bootstrap.md` completo: mapa de dominios, reglas permanentes, secuencia de arranque.
2. Seguí la secuencia de arranque de `KOS/Bootstrap.md` (MANIFESTO, Execution, Reglas, dominio activo,
   solo los índices necesarios).
3. Sincronizá antes de leer estado: `git pull --rebase --autostash` (`KOS/Execution.md` § Vault Sync).

## Activar un agente

Los lanzadores viven en `.claude/commands/`. La carpeta lleva el nombre de Claude, pero el contenido
es neutral. Cuando Ignacio pida `/<nombre>` o "corré <Agente>":

1. Abrí `.claude/commands/<nombre>.md` (por ejemplo `/reflect` → `.claude/commands/reflect.md`).
2. Seguí sus pasos al pie de la letra: cargan `KOS/Execution.md` y `KOS/Agents/<Agente>.md`.
3. Respetá el Output Contract del agente: ΔK primero, cambios al vault después.

Disponibles en esta copia: `/inicio-de-sesion`, `/procesar-raw`, `/reflect`, `/cierre-de-sesion`.

## Escribir en el vault

Protocolo común de escritura: `KOS/Operadores.md` § Protocolo de escritura. En corto:

- Prefijo de commit: `Gemini (<agente>): …` si sos Gemini / Antigravity; `Codex (<agente>): …` si sos Codex.
- Antes de commitear: `python3 scripts/validar_kos.py`. No introducir errores nuevos.
- **En esta copia de prueba no hagas commit ni push salvo que Ignacio lo pida explícitamente.**
- Ante un conflicto: parar, listar archivos, preguntar. Nunca descartar un lado ni forzar el push.
