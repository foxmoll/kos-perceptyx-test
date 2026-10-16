# Operadores — un KOS, varias IAs

Desde el 2026-10-15 el KOS no es "un sistema operado por Claude": es un protocolo que cualquier IA
puede operar. Origen: una conversación de Ignacio con ChatGPT (2026-10-15) que propuso *un KOS,
varios operadores, cada uno con un adaptador fino*. Este archivo es el registro de ese diseño.

## Principio

**Las reglas de operación nunca dependen de qué IA las lee.**

El vault separa tres capas, y solo la tercera cambia de una IA a otra:

| Capa | Dónde vive | ¿Portable? |
|---|---|---|
| Conocimiento | los dominios (en esta copia, solo `Perceptyx/`) | sí, es Markdown |
| Sistema operativo | `KOS/` — Bootstrap, MANIFESTO, Execution, Reglas, Agents, este archivo | sí, es Markdown |
| Interfaz con la IA | un adaptador por operador | no: cada producto carga instrucciones distinto |

Consecuencias:

- Un adaptador dice **cómo** llega su IA al KOS. Nunca dice **qué** es el KOS. Si una regla aparece
  en un adaptador y no en `KOS/`, es un defecto: los otros operadores no la ven.
- No hay carpeta de conocimiento por IA ni copia de agentes o lanzadores por IA. Eso es la misma
  duplicación que prohíbe [[KOS/MANIFESTO#Contenedores|MANIFESTO § Contenedores]].
- El punto de entrada neutral es `KOS/Bootstrap.md`. Todos los adaptadores apuntan ahí.

## Operadores

| | Claude Code | Codex | ChatGPT |
|---|---|---|---|
| Adaptador | `CLAUDE.md` (importa `KOS/Bootstrap.md`) | `AGENTS.md` | bootstrap pegado en el proyecto de ChatGPT (abajo) |
| Carga las instrucciones | automática | automática (`AGENTS.md`) 📣 | manual: lee los archivos por el conector de GitHub |
| Lanzadores | `.claude/commands/` como skills | lee `.claude/commands/<nombre>.md` como archivo | lee `.claude/commands/<nombre>.md` como archivo |
| Lee el vault | sí, repo clonado | sí, repo clonado | sí, conector de GitHub |
| Escribe en el vault | sí | sí | **no** (hoy): propone, no escribe |
| Commit / push | sí | sí; en Codex cloud puede quedar en rama/PR | no |
| Prefijo de commit | `Claude (<agente>)` | `Codex (<agente>)` | — (lo aplica quien escriba: `ChatGPT vía <Operador> (<agente>)`) |

📣 Capacidades de productos de terceros según OpenAI, citadas en la conversación del 2026-10-15
(Codex descubre `AGENTS.md` solo; el conector de GitHub estándar de ChatGPT es de solo lectura).
No verificadas desde el vault: si algo cambia, se actualiza esta tabla con fecha.

### Claude Code

Sin cambios de comportamiento. `CLAUDE.md` pasó a ser un adaptador de diez líneas que importa
`KOS/Bootstrap.md`; el mapa de dominios y las reglas permanentes se mudaron ahí sin cambiar de
contenido.

### Codex

`AGENTS.md` en la raíz. Le dice a Codex que lea `KOS/Bootstrap.md`, cómo resolver `/<nombre>`
contra `.claude/commands/`, y el protocolo de escritura. Prueba pendiente: abrir una tarea de Codex
sobre el repo, pedir "corré Reflect sobre Perceptyx" y comparar con el resultado de Claude.

## Protocolo de escritura

Común a todos los operadores. Extiende [[KOS/Execution#Vault Sync|Execution § Vault Sync]], no lo
reemplaza.

1. **Base fresca.** `git pull --rebase --autostash` antes de leer el estado que se va a modificar.
2. **Leer** el conocimiento y las reglas relevantes en esa revisión.
3. **Preparar** los cambios contra esa revisión. ΔK primero.
4. **Validar** con `python3 scripts/validar_kos.py`. El cambio no puede agregar errores.
5. **Commit** con el prefijo del operador. `git pull --rebase` otra vez: si la base cambió y el rebase
   es limpio, seguir; si hay conflicto, parar.
6. **Push.** Un push rechazado o un conflicto se reporta, nunca se resuelve descartando un lado ni
   forzando. Las dos versiones son evidencia.

**Operadores sin escritura** (ChatGPT hoy) cortan en el paso 3 y entregan la propuesta:

```
### Propuesta de cambio — base <commit leído, si se conoce>
- `ruta/al/archivo.md`: <crear | reemplazar "texto viejo" por "texto nuevo" | agregar al final de § X>
- Commit sugerido: ChatGPT vía <Operador> (<agente>): <qué cambió>
```

La aplica un operador con escritura, que hace los pasos 1–6 y revisa que la base no haya cambiado
debajo de la propuesta. Si cambió, la propuesta se re-lee contra el estado nuevo; no se pega a ciegas.

## Gemini (planeado, 2026-10-16)

Para el **KOS de equipo de Perceptyx** (repo en el GitHub de la empresa, ver
[[Perceptyx/_indice|Perceptyx/_indice]] § Proyecto: KOS de equipo). Gemini es la IA aprobada para todos en
Perceptyx (📣 Ignacio). Candidato: **Gemini CLI** con un adaptador `GEMINI.md` que lleve a `KOS/Bootstrap.md`,
igual que `CLAUDE.md` y `AGENTS.md`. 🔍 Sin verificar:
- que Gemini CLI esté habilitado para las cuentas de la empresa;
- que escriba y commitee como Claude Code.

Prefijo de commit propuesto: `Gemini (<agente>)`. Hasta probarlo, no tiene fila en la tabla de operadores.

**Segundo candidato: Google Antigravity** (IDE agéntico de Google). 🔍 Según búsqueda web del 16/10, sin abrir
la documentación oficial:
- viene **incluido en Gemini Enterprise** (Standard / Plus) sin licencia aparte y con controles de admin;
- tiene extensiones para VS Code y JetBrains;
- lee archivos `AGENTS.md` y `SKILL.md`. El vault **ya tiene un `AGENTS.md`**: sería el mismo adaptador que usa Codex.

A confirmar antes de elegirlo: si la licencia de Gemini de Perceptyx es Gemini Enterprise o solo Gemini en
Workspace, y si carga `AGENTS.md` solo, como Codex.

## Agregar un operador nuevo

1. Un adaptador fino que lleve a `KOS/Bootstrap.md`, en el formato que esa IA cargue sola.
2. Una fila en la tabla de Operadores y un prefijo de commit.
3. Si escribe: el protocolo de escritura completo. Si no: el formato de propuesta.
4. Nada más. Si hace falta tocar un agente para que funcione con una IA, el agente estaba mal escrito.
