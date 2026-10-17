# KOS Perceptyx — copia de prueba para Antigravity

Copia **mínima y descartable** del KOS de Ignacio Moll, armada el 2026-10-16 para probar si Google
Antigravity (Gemini) puede operar el protocolo. Tiene solo:

- `KOS/` recortado: Bootstrap con el dominio Perceptyx, MANIFESTO, Execution, Reglas (§ 1, 2, 4, 9),
  Operadores y cuatro agentes (Inicio, Capture, Reflect, Cierre).
- `Perceptyx/` tal como está en el vault original al 16/10, sin las referencias al proceso de selección.
- Adaptadores `AGENTS.md`, `GEMINI.md` y `CLAUDE.md`, cada uno con un **marcador**: la respuesta empieza
  con `[AGENTS.md cargado]`, `[GEMINI.md cargado]` o `[CLAUDE.md cargado]` según cuál leyó la herramienta.
- El validador (`scripts/validar_kos.py`) y su GitHub Action.

No es fuente de verdad: lo que se aprenda acá vuelve al vault original a mano.

## Plan de prueba

1. **Carga del adaptador.** Sin contexto: *"What are your instructions for this repository? Which files
   did you load before answering?"* → ¿aparece algún marcador?
2. **Protocolo de lectura.** *"Ayudame con un ticket de late adds en Perceptyx: primero las herramientas con
   URL, después los pasos con SQL listo para copiar."* → ¿respeta `KOS/Reglas.md` § 9 y las marcas ✅ 📣 🔍?
3. **Agente.** *"/inicio-de-sesion"* y después *"/reflect"* sobre Perceptyx → ¿abre el lanzador, carga el
   agente y da el ΔK primero?
4. **Escritura sin commit.** *"Agregá a Perceptyx/bitacora.md una entrada fechada que diga que probaste este
   vault desde Antigravity, siguiendo las reglas del vault. Corré python3 scripts/validar_kos.py. No hagas
   commit."* → ¿escribe en castellano, en el formato de la bitácora (la más reciente arriba) y corre el validador?
5. **Ticket sin procedimiento escrito** (reglas del 17/10, `KOS/Reglas.md` § 1 y § 9). En una **conversación nueva**, pegar
   un ticket real que el vault no cubra. → ¿hace **una sola pregunta por mensaje**, en el orden app ID → LEB/Classic →
   activo/cerrado → paso a paso o completa, salteando lo que ya vino en el pedido? ¿Evita inventar nombres de columnas u
   opciones de menú y marca 🔍 lo que deduce?
6. **Quién opera** (`KOS/Reglas.md` § 10, ficha en `equipo/`). En una conversación nueva, saludar o pegar un ticket. →
   ¿corre `git config user.email`? ¿Te encuentra por nombre en `equipo/ignacio.md` y te pide confirmar antes de agregar
   el email? Para probar el onboarding, cambiar el nombre de git en el clon (`git config user.name "Prueba"`) → ¿pregunta
   de a una, en el camino, sin frenar el ticket, y muestra la ficha antes de escribirla?
