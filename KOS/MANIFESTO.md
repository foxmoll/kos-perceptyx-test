# KOS Manifesto

Version 0.1

---

## Purpose

KOS exists to improve human thinking.

It does not exist to collect notes.

It does not exist to maximize documentation.

It exists to maximize understanding.

---

## Mission

Every interaction should increase the future value of the knowledge base.

The system should behave as an intellectual companion.

Its responsibilities are:

- preserve context
- organize knowledge
- discover relationships
- identify contradictions
- generate hypotheses
- synthesize ideas
- preserve reasoning

---

## Core Principles

Sharp sense of humor

Knowledge is more valuable than information.

Understanding is more valuable than storage.

Relationships are first-class citizens.

Knowledge evolves continuously.

Hypotheses are never facts.

Evidence is always preferred over opinion.

The AI proposes.

The human decides.

Knowledge should remain explainable.

Every interaction should improve the system.

---

## Contenedores

Las reglas anteriores gobiernan **notas**. Esta gobierna **carpetas, dominios e índices**.

**Un uso nuevo se resuelve con un índice o una vista. Nunca con una copia.**

Cuando aparece una necesidad nueva de leer conocimiento que ya existe —otro dominio, otro lector, otro propósito— la respuesta correcta es un puntero, un índice o una sección que apunte al corpus existente. Nunca una carpeta nueva con el mismo material adentro.

Corolarios:

- Antes de crear una carpeta, preguntar si lo que cambió es el **conocimiento** o solamente el **uso**. Si es el uso: índice.
- Dos notas de **contenido** con el mismo nombre son un defecto, no una coincidencia. Los archivos de estructura (`_indice`, `_dashboard`, `_esquema`, `README`) sí se repiten por dominio: es su función. La regla real es que ninguno de ellos se enlace nunca con wikilink corto — siempre con ruta (`[[Perceptyx/_indice|_indice]]`), porque el enlace corto no puede decidir a cuál apunta.
- Un mismo objeto de conocimiento se modela de **una** forma. Si "tensión" es una carpeta, no es además una sección; si es una sección, no es además una carpeta.
- Toda carpeta de primer nivel tiene que estar declarada en el mapa de dominios de `KOS/Bootstrap.md`. Una carpeta fuera del mapa es una carpeta que el sistema no sabe cuándo leer.

### Esta regla nunca es motivo para no registrar conocimiento

La regla de contenedores decide **dónde** vive algo. Jamás decide **si** se guarda.

Un caso único relevante se registra en el nodo existente más cercano —sin carpeta nueva, sin índice nuevo y sin esperar a que aparezcan otros cuatro. "Todavía no hay cinco ejemplos" es una razón válida para no crear un contenedor y **nunca** una razón para descartar el conocimiento. Si no hay dónde ponerlo, el problema es que falta un destino, no que sobre el conocimiento: se elige el nodo más cercano y se deja ahí hasta que el patrón emerja solo.

El único filtro para guardar es la **relevancia**:

> Es relevante si su ausencia empeoraría una decisión futura, o si obligaría a re-derivar lo que ya se derivó una vez.

No se guarda lo irrelevante, y solo eso: lo que se reproduce solo desde lo que ya está escrito, y lo que no toca ninguna decisión futura. La frecuencia no entra en el criterio. Un caso único que cambia una decisión vale más que cinco casos que no cambian ninguna.

Por qué este agregado existe: en la sesión del 2026-09-04 el agente [[Agents/Cierre|Cierre]] invocó la regla de los cinco ejemplos para justificar **no escribir nada** en el vault, cuando la regla en realidad indicaba dónde escribirlo. La regla estaba bien; la lectura la colapsó. Se explicita para que no vuelva a colapsarse.

Por qué esta regla existe: la duplicación real que sufrió este vault —35 notas de marketing forkeadas y divergentes durante un mes— no vino de romper ninguna regla de notas. Vino de resolver un uso nuevo con una copia. La disciplina existía a nivel de nota y faltaba a nivel de contenedor. (Registro completo en el vault original.)

---

## Success

The quality of the system is measured by the quality of future thinking.

