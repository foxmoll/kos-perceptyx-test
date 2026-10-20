# Modelo de datos de un survey

Cómo están conectadas las tablas que Delivery Ops toca todos los días, y por qué las reglas del training
son las que son. La lista de tablas con una línea cada una está en [[Perceptyx/plataforma|plataforma]] §
Tablas de un survey; acá va el **mecanismo**.

Relacionado: [[Perceptyx/procedimientos|procedimientos]] (reglas 3, 4 y 10) ·
[[Perceptyx/cultivate-360|cultivate-360]] · [[Perceptyx/services-os|services-os]]

> **Fuente: ✅ Confluence, páginas de engineering fuera del espacio de Delivery Ops**, exportadas por
> Ignacio el **06/10/2026**: *Attributed Demographics in Sub Apps*, *Attributed Demographics – Next
> Steps* (*"currently in progress"*), *Prefill data table*, *Demographics Data* y *360 Data Management and
> Flows*; y en un segundo envío *Manager Heirarchy Tree*, *Manager Hierarchy Filtering* y *Snowflake
> Integration* (*Demographics Data* vino repetida, idéntica). Los diagramas (Gliffy) no vinieron. Nombres
> de clientes de los ejemplos, reemplazados.
>
> ⚠️ **Todas son de otros equipos (engineering, producto), no de Delivery Ops** (📣 Ignacio, 06/10). Sirven
> para **entender por qué** las cosas funcionan como funcionan; **no son procedimiento**. Si una de estas
> páginas y una de DelOps dicen cosas distintas sobre cómo hacer una tarea, manda la de DelOps.

---

## Las capas de un demográfico — confirmado

El modelo mental que se armó el 06/10 juntando el training (🔍 entonces) **queda confirmado por la
documentación de engineering**, con un detalle que lo explica todo: cómo se guarda el valor.

| Capa | Tabla | Qué guarda |
|---|---|---|
| **Definición** | `resp_questions` | Cada demográfico (pregunta de demo). Los *attributed* tienen forma `02_XX_YY` |
| **Opciones** | `resp_list` | Los valores posibles de cada demo, ordenados por `seq` |
| **Fuente (HRIS)** | `prefill_data` | Los datos del cliente por empleado, una columna por campo |
| **Respuesta / reporte** | `all_data` | Una fila por respondente; una columna por pregunta o demo |
| **Invitados** | `emerge` | Los respondentes invitados; se une con `all_data` por `client_id` |
| **Unión emerge ↔ prefill** | `prefill_linkage_ids` | **Una sola fila** que dice qué columnas unen `emerge` con `prefill_data` (ej. Employee ID ↔ `emp_id`) |
| **Unión demo ↔ columna** | `prefill_linkage` | Qué columna de `prefill_data` alimenta cada `resp_questions` |

### Columnas verificadas en la base (✅ 20/10/2026, Querious, survey LEB EU)

- `resp_questions`: `id` (`02_NN_07`, el ID del demo), `list`, `width`, `required`, `g_id`, `text` (nombre del demo), `text_fmt`, `quid`, `date_hidden`.
- `resp_list`: `seq` (PK), `id` (ID del demo, enlaza con `resp_questions.id`), `text`, `option_order`, `option_id`, `quid_option_id`.
- `prefill_linkage`: `resp_id` (el qid) y `emerge_id`. **Ojo con el nombre:** `emerge_id` es el nombre de la **columna en `prefill_data`**, no la tabla `emerge`.
- `surv_questions_conditional`: `id`, `qid`, `status`, `q_text`, `q_condition`.
- `trend_custom_linkages`: `id`, `cond1`, `trend_app_id`, `cond2` (y el resto de columnas, no revisado).
- `my_queries` (filtros guardados): `id`, `timestamp`, `username`, `name`, `sql_query`, `disp_query`.
- `comparison_views`: `sequence`, `username`, `view_name`, `view`, `view_disp`.

### El valor en `all_data` es una posición, no un texto ni una clave

⚠️ **El valor de un demo en `all_data` es el *índice* de la opción dentro del grupo de opciones de ese demo
en `resp_list`, en orden de `seq`.** No es una clave foránea ni el texto.

Ejemplo (anonimizado): `resp_list` para `02_04_07` tiene, en orden de `seq`, *(vacío)*, *Empresa A*,
*Empresa B*, *Empresa C*. Un respondente con `2` en `all_data.02_04_07` es de **Empresa B**: el vacío es
la posición 0 (por eso toda lista de opciones empieza con `B_L_A_N_K`), y cuenta desde ahí.

✅ **Confirmado con un caso real (20/10/2026):** en `02_02_07`, por `seq`, las opciones son *(vacío)*, *Needs improvement*,
*Strong*, *Exceptional*. El `all_data` de una persona con *Strong* guarda `2`. Para cinco demos de otra persona, la posición
calculada como `count(*)` de opciones del mismo demo con `seq` menor coincidió con el valor que escribió la sincronización en vivo.
- ⚠️ **`option_id` no es la posición:** queda NULL en opciones que sí se usan. **`option_order`** vino en 0 en todas las opciones
  consultadas. No usar ninguno de los dos para calcular el índice.
- 🔍 Tensión con § Resincronizar: allí se dice que el sistema ordena las opciones alfabéticamente. En este demo el índice siguió
  `seq`, no el orden alfabético. Por confirmar con Jackie.

**Por qué importa — esto explica las reglas del training:**

- **Reordenar opciones cambia el significado de todos los valores ya guardados.** Si *Empresa B* pasa de
  la posición 2 a la 3 y no se reconstruye `all_data`, los respondentes que tenían `2` ahora "son" de otra
  empresa. Por eso reordenar un demo termina siempre con `rebuild all data demo from prefill`.
- Por eso la carga final de un 360 **no vuelve a subir `_resp.html`** si no hay demos nuevos: agregar
  valores al final con `add_new_values.pl` no mueve las posiciones existentes.
- Por eso un trend se rompe cuando cambian las opciones: el índice 2 de este survey no es el índice 2 del
  anterior, y `trend_custom_linkages` es la tabla que traduce.

### Cuándo se llena `all_data`

- Los *attributed demographics* (*prefill demographics*) se copian a `all_data` **cuando el respondente
  entra a la página de bienvenida** (o la primera página). Lo hace **solo la aplicación Data Collector**,
  buscando al respondente en `emerge` por el parámetro `auth` o `ac` y siguiendo las linkages hasta
  `prefill_data`.
- 🔍 **Consecuencia:** cambiar `prefill_data` después de que alguien entró no cambia lo que ya quedó en
  `all_data`. Hace falta el sync o rebuild de `all_data` (los scripts que se vieron en el training).
- El *Builder* de OnDemand arma `all_data`, `resp_questions`, `resp_list` y `prefill_linkage` a partir de
  los datos y la configuración del **master app**.

---

## Cómo lo explica Delivery Ops — sesión *Databases general* (Jackie, 16/09)

> 📣 **Jackie Cech**, primera sesión de training (16/09/2026, tercer día de Ignacio), transcript completo
> pasado por Ignacio el 06/10. Es la versión **de DelOps** del mismo modelo que engineering describe arriba:
> coinciden. Clientes nombrados en la sesión, omitidos.

**Una app por survey.** Cada survey de un cliente es una **aplicación** con **su propia base**, y esa base
alimenta su **reporting site**: `www.perceptyx.com/<app_id>` (EU: `eu.perceptyx.com/<app_id>`). Hay
**apps classic** (la forma de siempre) y la **plataforma**: cada cliente tiene un **master app**
(*self-service app*) en `ondemand(.eu).perceptyx.com`, desde donde se arman los surveys en **LEB** (en uso
desde hace *"un año y un poco"* al 16/09). Al terminar de cargar en LEB, **todo se sincroniza al sub app**
del survey; el master tiene tablas extra que casi nunca hay que tocar.

**Tres niveles de servicio:** *self-service* (el cliente arma todo), *guided* (el cliente arma con ayuda del
equipo de PMs) y ***managed*** (lo arma Perceptyx; **lo más común para DelOps**).

**Pasos de LEB** (*Content*): **PIN page** (~95 % entra por link único en un mail o por SSO; algunos
clientes usan PIN), **consent** (si no consiente, no se guarda nada), **welcome**, **demographic page**
(preguntar demos en el survey; raro, casi siempre vienen en el archivo), **questions**, **thank you**;
después *Styling* y ***Invite*** (donde se carga la data).

### Tabla por tabla

| Tabla | Qué es (Jackie) |
|---|---|
| `prefill_data` | Todos los demográficos de cada persona. **Obligatorios: emp ID, email, nombre y apellido**; **manager ID** casi siempre (para el árbol); **SSO ID** si usan SSO. Las primeras ~30 columnas suelen ser el data spec estándar, después lo propio de cada cliente. Las columnas **`pyx_…`** las **genera Perceptyx**: región / región detallada / región extendida a partir del país (para **benchmarks**), y age band, generación y tenure |
| `emerge` | Los mismos registros, pero es la tabla **de invitaciones**: se une con `prefill_data` por **emp ID** (o por **auth code** cuando una persona recibe varios surveys, ej. onboarding a 7, 30 y 90 días). Guarda **fecha de envío, primera y última respuesta, survey completado y cerrado** |
| `resp_questions` | Los demos **por los que se puede filtrar** (no nombre, SSO ID ni teléfono) y de qué columna de `prefill_data` sale cada uno |
| `resp_list` | Todas las opciones posibles de cada demo, **con su índice** |
| `all_data` | Una fila por respondente: entra **en la welcome page** (o después del consent), con `client_id` (de `emerge`), fecha de la **última** actividad, idioma y, por cada demo, **el índice** de la opción |
| `surv_questions` | Las preguntas: QID, **Q type** (ej. **`R249` = escala de favorabilidad**, de *strongly agree* a *strongly disagree*, *"99 % de las veces"*), texto y branching codificado (en LEB se ve legible: *ciudad = X*) |
| `surv_options` | Opciones de preguntas **con escala propia** o de selección única custom; una **multi-select** genera **una columna por opción** en `all_data` |

### Cómo leer un QID ✅

- **Demos:** `PP_SS_07`.
  - **`PP` = origen:** **`02` = armado en la plataforma (LEB)**; **`01` = classic**. Al llegar a 99 en la
    secuencia, pasa al siguiente (`03`…).
  - **`SS` = secuencia** (01–99).
  - **`07` = demográfico que viene del archivo de datos** (casi siempre; `08` y `09` eran cosas viejas que
    ya no se usan).
- **Preguntas:** cuatro dígitos; **los dos primeros son la página** (`00` = primera, `01` = segunda…) y los
  otros dos la posición.
- Que `02_02_07` sea el demo *active* es **propio de ese cliente**, no una regla.

### Las columnas de `prefill_data` — el data spec estándar en la práctica ✅

Capturas de Querious del 16/09: `prefill_data` del **survey de prueba de Jackie** (375 registros
`sample…@pyx.com`, datos falsos). Columnas en orden (falta un tramo entre *years_in_r…* y *…service* que no
entró en pantalla):

- **Sistema / identidad:** `sequence`, `pyx_internal_source` (ej. `data_import`), **`emp_id`**,
  **`email`**, **`first_name`**, **`last_name`**, **`auth`** (código de acceso), `pyx_pin`, **`mgr_id`**,
  `full_name`, **`sso_id`**, `phone_number`, `personal_email_address`, `employee_language` (ej. `en-us`).
- **Estado:** **`active`** (True/False), `absent`.
- **Fechas y antigüedad:** `birth_date`, `years_in_r…` (🔍 *years_in_role*), … `…service` (🔍 *years of
  service*), `original_hire_date`, `hire_type`, `termination_date`, `termination_type`.
- **Organización:** `gender`, `division`, `business_unit`, `department`, `cost_center`,
  `merger_and_acquisition`, **`work_country`**, `us_state_or_ca_province`, `city`… (siguen más a la derecha).

🔍 Coincide con lo que dijo Jackie (*"los primeros ~30 campos se parecen en todos los clientes"*) y con el
DOS (44 demos estándar). Que `active` sea una columna estándar explica por qué el 23/09 se pudo filtrar
invitados por `active = true`. Los usuarios de prueba con `@pyx.com` son, además, los que el binlog **no**
manda a UDS (§ `prefill_data` y UDS).

**Otras tablas visibles en la misma base** (lista parcial, orden alfabético): `action_plans`, `admin_text`,
`admin_toggles`, `all_data`, **`all_data_<número>`** y **`all_data_febupdates`** (🔍 **backups de
`all_data`**: con marca de tiempo o con un nombre descriptivo — así se ven los backups de la regla 1),
`all_data_annex`, `all_data_poll`, `bench_qid_match`, `benchmark_data`, `benchmarks`, `categories`,
`category_action_plan_items`, `progress`…

**Otras cosas de la sesión:** en *Operations tools* hay una herramienta para **agregar respuestas falsas**
(se usa mucho para armar los reportes antes del lanzamiento); el snippet **`;rowcount`** devuelve los
índices de una lista; en el reporting site, ***Functions › Survey Setup*** (`rm=admin`, *Survey Admin Links*;
detalle en [[Perceptyx/plataforma|plataforma]]) junta la configuración (vista de
`prefill_data`, *users* = usuarios de reportes, operations tools, *survey launch* = la forma vieja de los
mails, con `emerge` como *survey respondents*). Los **run modes** (`rm=`) son atajos a esas pantallas.

---

## `prefill_data` y UDS (binlog)

Complementa [[Perceptyx/procedimientos|procedimientos]] § Sincronización con UDS.

- **Encender binlog para `prefill_data`:** agregar `"prefill_data"` a `app.uds_binlog_config` en la tabla
  `settings` del app (es lo que hace el toggle *Which tables can transact with UDS via binlog*).
- **Reglas de lo que se ignora:**
  - eventos de apps **`ss_master`**;
  - usuarios con email **`@pyx.com`**, o de otra compañía con email **`@perceptyx.com`** (los usuarios
    internos de prueba no viajan);
  - clientes con **ingesta habilitada (`uds_active = 3`)** — esos alimentan UDS por *Data Hub*, no por
    binlog;
  - ⚠️ **`DELETE` y `TRUNCATE` se saltean.** 🔍 Borrar un registro de `prefill_data` **no lo borra de UDS**.
    Para un pedido de borrado de PII, el borrado en la base no alcanza; es de suponer que el *Execution
    Checklist* cubre UDS.
- Si cambia la columna **`sequence`**, el update se trata como **insert** (alta nueva).
- **Email vacío** pero con compañía y emp_id → se genera un email automático con dominio
  `autogen.pyx-no-email.com`.

**Valores de `uds_active`** que aparecieron: `2` (el que se pone en el alta de cliente) y `3` (cliente con
ingesta por Data Hub).

---

## La jerarquía de managers

### Legacy: `managers_tree` (lo que toca DelOps)

✅ *Manager Hierarchy Filtering*. Una tabla por app, `<app_id>.managers_tree`:

| Campo | Qué es |
|---|---|
| `emp_id` | Único. **La raíz (CEO) es una fila con `emp_id = 0`**, sin `mgr_id` ni `tree_path`, `deepness = 0` |
| `mgr_id` | El manager directo |
| `tree_path` | **El camino completo desde la raíz**, emp_ids separados por punto: `ceo.vp.dir.empleado` |
| `deepness` | Nivel en el árbol (1 = reporta a la raíz) |
| `trend_emp_id` | A quién equivale este manager en el survey anterior (trends) |
| `redundant_id`, `revision`, `position` | Internos |

- **Filtrar por manager:** `mgr_id` da solo los reportes **directos**; `tree_path LIKE '%.<emp_id>.%'` da
  **toda la organización debajo** (directos e indirectos). Los filtros de reporte combinan varios
  `tree_path LIKE '<camino>.%'` con `OR` sobre `emerge` unido a `managers_tree`.
- 🔍 **Esto explica dos cosas del training y de los trends:**
  - el *"quitar el 0 de la fila del CEO"* del rebuild del 30/09: la raíz es `0`, y el archivo de carga no
    tiene que traerla como empleado;
  - por qué **cambiar un manager ID obliga a rebuild del árbol**: `tree_path` es un camino precalculado;
    si cambia un eslabón, todos los caminos de debajo quedan mal;
  - el bloque `MGR_HIER` de `trend_custom_linkages` es exactamente este `tree_path LIKE`.

### Nueva: árboles como *snapshot* en UDS

✅ *Manager Heirarchy Tree*. En la arquitectura nueva la jerarquía se arma **en UDS**, a partir de los
`manager id` de los usuarios:

- **Para qué existe:** reporting. Define **qué parte de los resultados ve cada manager o admin**. *"Tiene
  menos que ver con la estructura de la organización del cliente que con los datos que le hacemos
  disponibles en reportes."*
- **Cada árbol es un *snapshot***: guarda los datos de los usuarios al momento de crearlo. Se crea desde
  *user management* con filtros (o con todos), se elige la raíz (puede haber más de una), se mueven o
  colapsan posiciones **solo dentro del árbol** — **los usuarios de UDS no cambian**.
- Estados: **Draft** (agregar y quitar) → **Live** al lanzar el survey (solo agregar) → **Closed** al
  cerrar (nada). Un draft se puede borrar y empezar de nuevo.
- Tablas: *Tree Catalog* (compañía → colección), *User Trees* (metadatos del árbol y criterios), *Tree*
  (los datos inmutables de cada usuario en ese momento).
- El snapshot se asocia al survey (ASK/SDS) y sirve como lista de invitados: cada usuario, participante o
  admin.
- ⚠️ **Regla que se repite en la página:** si el árbol tiene **muchos nodos desconectados** (usuarios sin
  manager), el problema está en los datos del HRIS — **se corrige en el sistema de RR.HH. del cliente y
  se reimporta, no en UDS**. Es la misma lógica de "lo que manda es la fuente".

---

## Comentarios de Dialogue → Snowflake

✅ *Snowflake Integration*. Para entender el circuito de comentarios del lado de **Dialogue** (no es el
workaround del modelo léxico que hace DelOps en surveys clásicos, que vive en
[[Perceptyx/procedimientos|procedimientos]]):

- **Dialogue** empuja preguntas abiertas y sus respuestas a Snowflake para el **pipeline de NLP** de
  Perceptyx. **Una sola dirección**: Dialogue escribe, no lee.
- Solo se sincroniza si la cuenta pertenece a una organización con **`pyx_company_id`** válido; si no, **se
  saltea en silencio** (sin error, sin fila).
- Dos tablas: `QUESTIONS` y `COMMENTS`, etiquetadas con `CLIENT_ID` (= `pyx_company_id`) y `APP_ID`
  (`DIALOGUE_<TITULO>_<AA>_<id>`). Los borrados son **lógicos** (`SNOWFLAKE_DELETED_AT`): nada se borra de
  Snowflake.
- Para engineering hay scripts de chequeo (`rake snowflake:check`, que distingue 404 = cuenta mal / 401 =
  token rechazado) y de **backfill** (dry run por defecto). Detalle de valor general: el chequeo de
  integración estándar **solo verifica que existan las variables de entorno** y da OK aunque Snowflake esté
  rechazando todo.
- 🔍 Dos patrones que se repiten en todo el sistema: **"si no cumple, se saltea sin avisar"** (igual que
  el binlog con usuarios internos o `DELETE`) y **"una lectura vacía no prueba que no haya nada"** (la
  página lo advierte: un error y un "no hay filas" devuelven lo mismo). Antes de concluir que algo no
  existe, confirmar que la consulta funcionó.

---

## Dos arquitecturas conviviendo

Lo que Delivery Ops toca hoy (MySQL, una base por survey) es **la arquitectura vieja**. La nueva ya existe
para algunos productos.

| | Legacy — "PYX-led" | Nueva — "Self-led" / vNext |
|---|---|---|
| **Base** | **MySQL**, **una base por evento** (survey), compartida por varios servicios | **PostgreSQL**, **una base para todos los eventos** (360vNext) |
| **Migraciones de esquema** | **Manuales, por un DBA** | Como código, automáticas en cada deploy |
| **Reporting** | Advanced Reporting, sobre `all_data` | **Snowflake** (Self-led 360 Reporting) |
| **Datos del cliente** | `prefill_data` con **una columna por campo**, distinta por cliente y por survey | *Event Builder*: `ss_app_invitees` con una **columna JSON** para el esquema variable |
| **Ingesta de usuarios** | Archivo → `prefill_data(_all)` → binlog → UDS | **Data Hub** conectado a la fuente del cliente → UDS (`uds_active = 3`) |
| **Data Collector** | El clásico (Perl) | **DC Mosaic** (= DC vNext): toma el survey de LEB y **escribe en MySQL Classic por un adaptador** — ver [[Perceptyx/dc-mosaic|dc-mosaic]] |

- **360:** *PYX-led 360* = lo de [[Perceptyx/cultivate-360|cultivate-360]] (360v2, MySQL). *Self-led 360* =
  **360vNext** (PostgreSQL + Snowflake), otra cosa.
- *Demographics Data* describe la arquitectura nueva por dominios: ingesta a UDS por Data Hub, armado del
  survey tomando demos y respondentes de UDS por API (`/users`, `/companies/:id/profile`, `/surveys`,
  `/surveys/:id/respondents`…) e importación de demos al dominio de Reporting.

### El problema abierto de engineering (*Attributed Demographics – Next Steps*)

- **Rendimiento:** clientes grandes con **75–100+ categorías demográficas** (un caso real: 109 categorías,
  algunas con **58.000 opciones**) hacen que ciertas acciones tarden minutos — **~1 segundo por
  demográfico** en algunos procesos.
- Como cada cliente y cada survey tiene su propio esquema, **no se pueden usar índices ni columnas
  virtuales** de MySQL para acelerar.
- **La raíz:** Advanced Reporting y todo lo que no es DC vNext **exigen que `prefill_data` tenga una
  columna por demográfico**.
- Propuestas en discusión: cambiar el modelo de datos para aprovechar índices; usar SSE o feedback en vivo
  para las acciones lentas.
- Contexto que da la página: casi no hay demos estándar (la mayoría los define el cliente); las opciones
  cambian con el tiempo; a veces un demo es casi único por persona (por diseño o por error); y los datos
  del cliente llegan sucios, el equipo de ingesta limpia lo razonable.

🔍 **Lectura para el puesto:** muchas tareas de Delivery Ops (reordenar demos, rebuilds, trend
mismatch, columnas de más de 200 caracteres, el límite de 100 columnas en la carga del 360) son
**consecuencias operativas de este modelo de "una columna por demo, una base por survey"**. Cuando la
arquitectura nueva absorba más productos, parte de esas tareas debería desaparecer, y otras nuevas (Data
Hub, UDS, PostgreSQL) van a ocupar su lugar.
