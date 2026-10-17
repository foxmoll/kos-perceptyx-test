# Equipo — esquema de las fichas por persona

Una ficha por persona que opera el KOS: `equipo/<usuario>.md`, donde `<usuario>` es el nombre en minúsculas, sin
acentos ni espacios (`ignacio.md`, `ana-perez.md`). Regla completa: [[KOS/Reglas|Reglas]] § 10.

**Para qué sirve:** que cualquier IA, en cualquier herramienta, trabaje con cada persona como esa persona prefiere, sin
que tenga que repetirlo. Va en el repo y no en la configuración de una herramienta porque así viaja entre operadores
([[KOS/Operadores|Operadores]] § Principio).

**Qué entra:** preferencias de **forma** (idioma, modo de guía, nivel de detalle) y el contexto de trabajo que cambia
cómo explicar (equipo, experiencia, herramientas).

**Qué no entra:**
- reglas que pisen las del equipo. Verificar, marcas ✅ 📣 🔍, sin datos de clientes, preguntar lo que falta y de a una:
  eso vale para todos y una ficha no lo cambia;
- evaluaciones, opiniones sobre la persona ni nada que no quiera que vea el resto. La ficha la lee todo el equipo.

## Campos

```
# <Nombre>

| Campo | Valor | Fuente |
|---|---|---|
| Emails de git | los de `git config user.email` con que opera | ✅ git / 📣 la persona, fecha |
| Rol / equipo de PM | … | 📣 la persona, fecha |
| Idioma de respuesta | … | 📣 / 🔍 deducido de cómo escribe, fecha |
| Modo de guía por defecto | preguntar cada vez · paso a paso · completa | 📣, fecha |
| Nivel de detalle | básico (explicar el porqué de cada paso) · intermedio · experto (solo comandos) | 📣, fecha |
| Herramientas con acceso | Querious, SOS, Transmit, LEB… | 📣, fecha |

## Notas
Preferencias que no entran en la tabla, cada una con fecha. Lo que cambia se marca `SUPERSEDED (fecha)`, no se borra.
```

Las preferencias **deducidas** se marcan 🔍 y se confirman la próxima vez que vengan al caso.
