# Procedimientos — tareas de Delivery Ops

Cómo se resuelve cada tipo de tarea, tal como se enseñó en el training. Una sección por tipo, la regla
general primero. Sin datos de clientes: los ejemplos están anonimizados
([[Perceptyx/_indice|_indice]] § Qué entra y qué no).

Relacionado: [[Perceptyx/plataforma|plataforma]] (herramientas y tablas) ·
[[Perceptyx/equipo-delops|equipo-delops]] · [[Perceptyx/bitacora|bitacora]]

> **Fuente de todo lo de esta nota, salvo que diga otra cosa:** demostraciones de **Emily Zobel** en
> las sesiones de training del 28/09, 30/09 y 01/10/2026, conocidas por las **notas automáticas de
> Gemini** (Google Meet). Marca por defecto: 📣 Emily, vía Gemini. Las notas de Gemini recuperan la
> reunión, no la establecen: deforman nombres (ver [[Perceptyx/plataforma#Glosario|plataforma §
> Glosario]]) y pueden omitir pasos. **Vigente al 2026-10-01.** Lo que se confirme haciendo una tarea
> real pasa a ✅.
>
> **Revisión del 06/10 (cierre):** los nombres de tabla que venían deformados por Gemini se
> **normalizaron a los reales** confirmados después en Confluence (`prefill_data`, `resp_questions`,
> `all_data`, `trend_custom_linkages`, `managers_tree`, `prefill_linkage`). La forma original está en
> [[Perceptyx/plataforma#Deformaciones de Gemini|plataforma § Deformaciones]]. Lo que el training llamaba
> **"LE app" / "LE data file builder" es LEB** y su Data File Builder (ver § Data file load).

---

## Mapa: tipo de ticket → sección

Para encontrar la sección antes de armar pasos. **Si el ticket no está en el mapa, no hay procedimiento
escrito**: se aplica [[KOS/Reglas|Reglas]] § 1 (*si no está en el vault, se pregunta*) y se arma con las
compuertas de abajo, marcando 🔍 cada paso que no salga de una sección.

| Pedido | Sección |
|---|---|
| Reordenar las opciones de un demo (bandas de edad, tenure, generación) | § Reordenar las opciones de un demográfico |
| Demo nuevo, incluido uno calculado a partir de otro campo | § Agregar un demográfico nuevo |
| Corregir demos, manager IDs o árbol con el survey cerrado | § Actualizaciones después del cierre del survey |
| Sumar participantes con el survey en vivo | § Late adds |
| Cargar el archivo final de un survey de LEB | § Carga del archivo final en un survey de LEB |
| Archivo de participantes con LE / Data File Builder | § Data file load |
| Trends que no cruzan | § Trend mismatch |
| Usuarios Manager / Manager Below Threshold | § Usuarios Manager |
| Emails, traducciones, chequeo de integridad, Launch Audit | § Emails, traducciones y chequeos del app |
| Alta de cliente, SSO, API, borrado de PII | sus secciones, por nombre |
| **Bandas calculadas de edad o tenure** (crearlas o cambiar sus cortes) | § Agregar un demográfico nuevo › *Demo calculado desde una fecha* (✅ 27/10/2026). ~~Sin procedimiento escrito~~ SUPERSEDED 27/10 |
| **User setup con varios status: empleados con la vista de su manager, umbral distinto por país, "replicar el survey anterior"** | **Sin procedimiento escrito** (§ Pendientes). Lo más cercano: § Usuarios Manager, solo para los status de manager |

## Compuertas antes de cualquier tarea que toque demográficos

Se revisan **antes de dar el primer paso** y el resultado se dice en la guía, una línea por compuerta.
Si una da rojo, no se da el paso 1: se dice qué la destraba. Cada una es una regla de la sección
siguiente; acá están juntas para que no se salteen.

| Compuerta | Rojo si… | Qué se hace | Regla |
|---|---|---|---|
| ¿Survey cerrado? | Está en vivo y la tarea no es un late add | No se desactiva: se espera el cierre o se consulta al PM | 2 |
| ¿LEB? | Se armó en LEB con *Use LEB Data Collector* encendido | Apagar el toggle y avisar al PM antes de escribir por fuera | 10 |
| ¿Hay respuestas? | `all_data` ya tiene respuestas para ese demo | Cambiar texto u orden de `resp_list` cambia el significado de las respuestas (el valor es una **posición**): reordenar con rebuild, nunca reescribir textos | [[Perceptyx/modelo-de-datos\|modelo-de-datos]] |
| ¿Quién depende del demo? | Aparece en branching, filtros, comparison views o trends | Se rehace después del cambio | 3 |
| ¿Hay backup? | Todavía no | Backup de cada tabla que se va a tocar | 1 |

🔍 Armadas el 19/10/2026 a partir de la prueba de Antigravity con un ticket real ([[KOS/Operadores|Operadores]] §
Antigravity): el operador conocía las reglas, pero propuso desactivar un survey vivo y no vio la regla 10 ni la de
posiciones. No agregan reglas: juntan las que ya estaban.

---

## Reglas que valen para toda tarea

1. **Backup antes de tocar nada.** Se respaldan las tablas que la tarea va a modificar. Nombre del
   backup: **fecha + iniciales**. Dos caminos: el script de backup del Text Expander (SQL), o
   **Operations Tools › Utilities › Backup table** en la app, que sirve de alternativa cuando el SQL da
   `create command denied` (caso 01/10). ✅ **El script de Text Expander es `mac.create_backup`**
   (captura de Ignacio, 16/10: snippet ***Backup Table***, abreviatura **`;bck`**, grupo *Organization / DM
   Snippets*, solo lectura). La abreviatura pide *Database* (= app ID) y *Table* y expande a
   `CALL mac.create_backup('<app>', '<tabla>', @results); SELECT @results;`. Se corre en la conexión RW
   (Elena lo usó el 16/10) y crea `<tabla>_AAAAMMDDhhmmss` en la base del app. Respalda **una tabla por
   llamada**. 🟡 El nombre lo arma el procedimiento **con fecha y hora, sin iniciales**: el *"fecha +
   iniciales"* de arriba (Emily vía Gemini) sería para un backup con nombre a mano, o un detalle que Gemini
   deformó. *"Backing up tables ensures any mistakes can be corrected"* —
   es la red que permite trabajar tareas reales sin miedo.
   ✅ **Observado 20/10/2026:** `mac.create_backup` dio `execute command denied` desde la conexión de solo lectura. La app
   (*Operations Tools › Utilities › Backup table*, en la URL del survey) hizo el backup y verificó filas (entrada = salida).
   La app devuelve el nombre de la tabla: `<tabla>_backup_AAAAMMDD_hhmmss_NNNNNN`. Anotar ese nombre: sirve de referencia
   para la verificación posterior.
   **Tercera vía, a mano por SQL** (📣 Ignacio, 19/10/2026: *"es válido, lo he visto con otros DM"*): una
   tabla nueva con la misma estructura y una copia de los datos, con nombre **fecha + iniciales**, que es el
   formato del párrafo de arriba:
   `CREATE TABLE <tabla>_AAAAMMDD_<iniciales> LIKE <tabla>;`
   `INSERT INTO <tabla>_AAAAMMDD_<iniciales> SELECT * FROM <tabla>;`
   🔍 Necesita permiso de `CREATE`: si da `create command denied`, queda la vía de Operations Tools.
2. **El survey tiene que estar cerrado** antes de tocar demográficos. Se verifica en *Survey Setup ›
   Survey Configurations*: **Deactivation** tildado. Tocar `all_data` con el survey vivo puede romper
   respuestas de participantes.
   **Es una condición que se verifica, no un paso que se ejecuta.** Si el survey está en vivo, no se
   tilda *Deactivation* para poder trabajar: cortarlo deja afuera a quienes están respondiendo y esa
   decisión no es de Delivery Ops. El ticket **se trabaja después del cierre** o se consulta con el PM
   (regla 8). (📣 Ignacio, 19/10/2026: ticket de cambio de bandas con el survey vivo, *"hay que
   trabajarlo después de que cierre la encuesta"*.) La excepción escrita son los **late adds**, que
   solo suman valores con el survey vivo (§ Late adds).
3. **Antes de cambiar un demo, buscar quién depende de él**: branching (`surv_questions_conditional`; Gemini lo había transcripto *"Q condition"*), filtros
   guardados por usuarios, comparison views, y **`trend_custom_linkages`** (trends contra surveys
   anteriores). Si hay dependencias, se rehacen después del cambio.
4. **Toda escritura que cambia un demo se propaga**: se actualiza `prefill_data` y después se
   sincroniza hacia `all_data` (sync / rebuild). Un cambio que queda solo en prefilled no se ve en
   reportes.
5. **Scripts Perl: primero en modo test, después live.**
6. **Si un script pregunta si agregar entradas "as approved" → siempre `no`.**
7. **Cerrar con verificación**: *Verify survey integrity* (en SOS, columna *read*) o el *data
   integrity verify script*.
8. **Lo raro se le devuelve al program manager.** Faltantes o discrepancias en los datos del cliente
   (managers que no aparecen, registros que no están en prefilled) son del PM, que habla con el
   cliente. Delivery Ops le entrega el **audit file** y le avisa; no adivina.
9. **Cierre de la tarea en Salesforce**: estado → *Complete*, iniciales en el comentario con el atajo
   `;me` (Text Expander).
10. **Si el survey se arma en LEB, LEB pisa lo que se cambió por fuera.** Con el toggle *Use LEB Data
    Collector* encendido (lo normal), **previsualizar el survey, hacer *Next: Settings* o activarlo**
    reescribe desde LEB `surv_groups`, `resp_groups`, `surv_questions`, `surv_options`,
    `resp_questions`, `resp_list`, `prefill_linkage`, `all_data`, `progress` y dc settings. Un cambio
    hecho por SQL u Operations Tools sobrevive solo hasta que alguien toque uno de esos botones. ✅
    Confluence *PFS LEB Learnings* — detalle en § LEB.

🔍 **Modelo mental que sale de juntar las cinco sesiones** (inferido, no lo dijo nadie así): un
demográfico vive en tres capas — su **definición** (`resp_questions`, 🔍 en realidad `resp_questions`:
ID del demo, opciones e índices),
el **valor por participante** (`prefill_data`) y la **copia de reporte** (`all_data`). Casi todas las
tareas son cambiar una capa y propagar a las otras, sin romper lo que cuelga del demo (branching,
filtros, trends). Si el modelo está mal, las reglas 3 y 4 son las que lo van a desmentir. **Y hay una
cuarta capa por encima** (regla 10, 06/10): si el survey vive en LEB, LEB es la fuente de la estructura y
puede pisar las otras tres. ✅ **Confirmado y explicado el 06/10** por la documentación de engineering:
[[Perceptyx/modelo-de-datos|modelo-de-datos]] — el valor en `all_data` es la **posición** de la opción en
`resp_list`, por eso reordenar obliga a reconstruir.

---

## Cola de tareas y escalación (Project Turbo+)

> ✅ Confluence *Team Partnership Model – Project Turbo+*; escalación actualizada el **02/12/2025**.
> Equipos y nombres en [[Perceptyx/equipo-delops|equipo-delops]].

- **Delivery Ops (PFS) es dueño de la Team Task Queue** de cada equipo de PM. Los 2–3 partners del equipo
  revisan las tareas nuevas, acuerdan prioridad y capacidad, y **se reparten el trabajo entre ellos**.
- **Aclarar requerimientos con el PM temprano**, antes de que se vuelvan bloqueo.

**Escalación, en orden:**

1. 🟢 **Dentro del equipo (primera parada).** PM + partners resuelven bloqueos, dudas y prioridades:
   comunicación, realineación o **mover la fecha**. La mayoría se resuelve acá.
2. 🟡 **Columna *Assist* — "Support Welcome".** Ayuda liviana opcional: la tarea queda visible para que
   otro partner la tome si tiene capacidad; **el equipo sigue siendo dueño hasta que se reasigne**. Sin
   notificación. Ej.: podés hacerla pero tenés cosas más prioritarias; o es de CRON/automatización y no
   urgente (Automation mira esta columna). Cualquiera puede tomar una tarea sin flag, **avisando antes al
   equipo dueño**.
3. 🔴 **Team Assist workflow — "Support Required".** Equipo sin capacidad, sin cobertura o sin la
   habilidad necesaria → alerta a todo PFS (incluido Automation) y a los managers, **con notificación de
   Slack**. Ej.: no llegás a la fecha; necesita automatización o skills avanzados (marcar *"Automation
   Task Handoff"*).
4. 🚨 **Urgent Support — solo PMs.** Impacto en vivo, de cara al cliente, que no se resolvió en los
   pasos anteriores → **#ps_task_escalation**.

Para visibilidad amplia o discusión entre equipos: ~~#pfs_support~~ **`#do_support`** (abierto a todos; el doc usa el nombre viejo).

**Dónde se ve la cola en Salesforce** (✅ captura del video *9.23.2026 task walkthrough*, visto el 06/10;
el resto del video sin transcribir todavía): pestaña **DelOps Workspace** de *Perceptyx PSA*.
- *Quick Links* → **DelOps Task Dashboard**.
- ***Task Workspaces*** **uno por PM** (Adam, Bill, **Kim**, Mindy, Pam, Steve) más *Implementation
  Workspace*: es la Team Task Queue de cada equipo. **El de Ignacio es el de Kim.**
- Listas: **My Current Tasks**, **Open Tasks – All DelOps** y **Open Tasks – Cron/Automation – All
  DelOps** (la de Automation).
- **Cómo se toma una tarea** (📣 Jackie, mismo video, transcript completo): entrar al workspace del
  equipo → arriba lo ya asignado, abajo **lo del equipo sin asignar**. Sin entrar a ningún workspace se ven
  **todas las abiertas de DelOps** (con filtro por *project group*). En la tarea, ✎ en ***Resource*** →
  tu nombre → **Save** (si no, no aparece) → queda en ***My Tasks***. El botón **Assist** manda el aviso
  al canal de Slack para que otro la tome.
- Después: abrirla y marcarla **In Progress** (§ Carga del archivo final, paso 1).
- Asignación de la cohorte (✅ 16/09 y 23/09): **Ignacio → Kim**; **Andrea → Bill y Steve** (cada equipo
  tiene un solo partner: Emily en Bill, Tim en Steve); **Guillermo → onboarding / implementación** (sin
  equipo fijo, con JT; *Implementation Workspace*).

**Cuándo una tarea aparece en la cola** (📣 Jackie, 16/09): los PM trabajan sobre la **plantilla de proyecto**
de Certinia — un cronograma estándar de tareas (vista **Gantt**) con cada tarea asignada a un equipo; las de
DelOps todavía dicen **PFS / Platform Services** (*"wherever you see PFS, that's us"*). Ejemplos: datos
históricos de otro proveedor, cargar o crear archivos de datos, **armar jerarquías de managers**, armar
mails. Una tarea llega al workspace **solo si**: estado **Ready to Start** (en *Not Started* no aparece),
tiene **fecha de vencimiento**, y en la asignación el **resource role** es Platform Services. Algunos PM
hacen solos parte de las tareas (ej. la carga inicial) y piden la final.

**Estados:** Not Started → **Ready to Start** → **In Progress** → (**Info Needed** con nota al PM ↔ **Info
Provided**) → **Complete**. **Una tarea, una persona** (se pasa a otro solo si hay PTO o algo urgente).

**Qué mirar en la tarea:** fechas de inicio y vencimiento, descripción, **servidor** (`www` / `EU` / `gov`
— *gov* lo hacen pocas personas y va a desaparecer; ver la regla FedRAMP en Reglas § 9), **prioridad**
(*urgent* = aunque sea corta, va ya; suelen avisar por Slack), **tipo de trabajo** (*custom* = no esperar
al día del vencimiento, planificar), PM que la pidió y **survey ID**.

**Cerrar:** comentario con todo lo hecho (*"I probably comment more than I need to"*) — el cuadro se
**vacía** al guardar y queda en el **Comments History** con autor y hora — y las **horas reales** en la
tarea, **en múltiplos de 0,25**.

### La plantilla de proyecto: *2026 LEB Project Timeline* (✅ capturas, video del 16/09)

Plantilla de Certinia **"ZTemplate – 2026 LEB Project Timeline – DO NOT EDIT"** (vista Gantt). Cada
proyecto nuevo se crea a partir de ella. **Cómo leer los nombres de las tareas** (el prefijo dice quién la
hace):

| Prefijo | Quién |
|---|---|
| **`PFS:`** / **`QA:`** (resource *Platform Services*) | **Delivery Ops** |
| `PM:` | Program manager |
| `DLV (PM)` · `DLV (C)` · `DLV (WTC)` · `DLV (EX OPS)` | Entregable de PM, **cliente**, consultor WTC o EX Ops |
| `EX OPS:` | EX Ops (arman el survey en LEB con el consultor) |
| `PROGRAM CALL:` | Llamada con el cliente |
| *(sin prefijo)* | Hito (*… Complete*) |

**Fases y tareas que tocan a Delivery Ops** (lo que se ve hasta el inicio de *Final Data File*; las fases de
lanzamiento, reporting y cierre no entraron en las capturas):

1. **Program Initiation** — kickoff, materiales, aprobación del cronograma, **`PM: Event Creation | Clone`**,
   mail de *LEB Build Readiness* a EX Ops. **Nada de DelOps.**
2. **Survey Design**
   - *Stakeholder Interviews* (opcional) — WTC.
   - ***Historical Content*** (opcional): el cliente manda datos de surveys anteriores → `PM: Create App(s)
     in MAC` → **`PFS: Upload Historical Survey Data`** → **`QA: Review Historical Survey Data`** →
     aprobación del cliente.
   - *Survey Content*: EX Ops arma el survey en LEB, export del diseño, working session, ajustes y
     benchmarks, aprobación, comunicaciones y branding.
3. **Survey Build**
   - ***Initial Data File***: el cliente manda el archivo → `PM: Load Initial Data File` y `PM: Build
     Manager Hierarchy Tree in LEB` → **`PFS: Load Initial Data File – OPTIONAL`** y **`PFS: Create
     Manager Hierarchy Tree – OPTIONAL`** → audit al cliente → revisión del árbol por el cliente →
     **`PFS: Manager Tree Hierarchy Data File…`** → **`QA: Review Initial Data File For Launch –
     OPTIONAL`**.
   - ***Initial Survey Build***: `PM: Complete After-Build Checklist`, **`PFS: Build Survey – OPTIONAL`**,
     `PM: Build email templates, branding & comms`, **`PFS: Build email templates – OPTIONAL`**, **`QA:
     Review English Survey & Communications – OPTIONAL`**.
   - *Initial Survey Build Adjustments*: revisión del cliente y ajustes del PM.
   - ***Survey Translations***: `PM: Populate Survey Languages`, **`PFS: Add Translation Tags –
     OPTIONAL`**, envío a traducción (**machine o human**, con duración distinta), aprobación, **`QA:
     Review Survey Translations`**.
   - ***Final Data File + Manager Hierarchy Tree***: el cliente manda el final → `PM: Load Final Data
     File` → … (sigue fuera de la captura).

🔍 **Lo que muestra la plantilla:** en el modelo LEB **el PM hace por defecto** las cargas, el árbol y el
armado; **las tareas `PFS:` son casi todas *OPTIONAL*** — el PM las activa (*Ready to Start*) cuando no
puede o no quiere hacerlas. Las que son de DelOps sin alternativa son los **QA** y el **histórico**.
Explica el *"algunos PM lo hacen solos, otros piden ayuda"* de Jackie, y que la sesión del 02/10 haya sido
QA. La barra de Salesforce también muestra **DO Dash** y **DO %** (DO = Delivery Ops).

**Canales:** cada equipo de PM tiene **su canal de Slack** (el de Ignacio: el de Kim); para urgencias del
PM, **`#do_support`**, el canal de Slack de Delivery Ops (📣 Ignacio, 06/10): lo ve todo el equipo y lo
toma el primero que puede. Las referencias a *#pfs_support* en documentación vieja se leen como `#do_support` (📣 Ignacio, 06/10: probablemente se llamaba así antes).

🔍 **Cómo encaja con lo del training:** el consejo de Emily del 30/09 (*"si estás desbordado, pedile al
PM pasarla al día siguiente o escalala a otro"*) es el paso 1 y el paso 3 de este esquema. Y el *"task
pool"* que describió Melanie en la selección es **lo que este modelo reemplazó** — ver
[[Perceptyx/_indice|_indice]].

---

## Integraciones de datos (Push / Pull)

> ✅ Confluence *Data Integrations*, exportada 06/10/2026.

**Cliente nuevo:** el equipo de **Platform Onboarding** (Kevin Carlson) hace la conversación inicial
(beneficios, overview, Perceptyx Academy, tech specs, *push vs pull*), junta requerimientos y después
**pasa la propiedad a PFS**:

- **Pull** → tarea *"Data Integration Setup – Pull"* al **Automation Team**.
- **Push (SFTP)** → tarea *"Data Integration Setup – Push (SFTP)"* al **equipo PFS del PM asignado**.
- ⚠️ **Al tomar una de estas tareas, avisarle a Kevin**: él manda el mail al cliente presentándote.

**Cliente existente sin automatización** (o sin automatización en su self-service app): tarea *"Data
Integration – Begin Integration Process"* → Automation Team, que revisa lo que hay, define push/pull con
el cliente y convierte la tarea.

**Burn Down – Push (SFTP)** — tuya si sos el partner del equipo:

1. Si el cliente ya tiene alguna automatización: revisar sus archivos y automatizaciones actuales, y
   **chequear el archivo contra los data specs**.
2. Recomendar cambios **mínimos**, para no romper sus *lifecycles* activos.
3. Trabajar con el cliente los hallazgos del audit y las modificaciones.
4. **Escalar a Automation (conversión a cron)** si el cliente rehace sus archivos según specs, o si hay
   lifecycles de candidatos, hiring managers, aniversarios o muy complejos.
5. Con el archivo final: crear la **self service automation** y coordinar la puesta en marcha con el
   cliente.

**Burn Down – Pull** → Automation Team. Las integraciones Pull siguen el **Standard HRIS Integration
Playbook** (no incorporado).

**Cierre (las dos):** actualizar el proyecto *Overall* del cliente en **Certinia** con el estado de la
integración y de los data specs.

🔍 Es el terreno más cercano a lo que Ignacio hacía en UKG: archivo del cliente contra especificación,
auditoría y cambios mínimos sin romper lo que está corriendo.

---

## LEB (Listening Event Builder): toggles, archivos finales, clonado

> ✅ Confluence *PFS LEB Learnings*, exportada 06/10/2026.

**Toggles de sincronización** — por defecto los tres de arriba encendidos y los tres de abajo apagados:

| Toggle | Qué pisa | Cuándo |
|---|---|---|
| **Use LEB Data Collector** | Contenido del survey y demográficos: `surv_groups`, `resp_groups`, `surv_questions`, `surv_options`, `resp_questions`, `resp_list`, `prefill_linkage`, `all_data`, `progress`, dc settings | Al previsualizar, *Next: Settings* (desde invite) o activar el survey |
| **Use LEB Filestorage** | Tabla `filestorage` (contenido de bienvenida y agradecimiento) | Ídem |
| **Use LEB Categories** | `categories` y `category_qid` — **solo si Data Collector también está encendido** | Ídem |
| ~~Reporting Content / Translations / User Status Content~~ | — | ~~*"Coming in the future"*~~ **SUPERSEDED 27/10/2026** (✅ captura): ya existen, apagados por defecto |
| **Use LEB Reporting Content** | Toolkit, benchmarks, comentarios (`lexical_keywords`) y visibilidad de reportes (`runmodes`) | Ídem |
| **Use LEB Translations** | `languages`, `translated_phrases`, `localized_email_content` | Ídem |
| **Use LEB User Status Content** | `statuses`, `status_privileges` | Ídem |

✅ **Dónde están (27/10/2026):** master app › *My Surveys* › **Actions › View Survey** › **Managed Settings**
(`…/<master_app>/app/#/builder/<n>/managed_settings`). Arriba está el toggle *Enable DC Mosaic* (apagado = DC Amsterdam,
el default de los managed). Los seis de sincronización están más abajo, en la sección desplegable **Sync Settings**.

- **Data Collector debería estar siempre encendido**, salvo que hayas hecho cambios fuera de LEB que no
  querés perder. Encendido no pisa nada por sí solo: pisa cuando alguien previsualiza, hace *Next:
  Settings* o activa.
- 🔍 Consecuencia práctica: después de un `UPDATE` por fuera en un survey de LEB, **avisarle al PM** que
  previsualizar o activar puede deshacerlo, o apagar el toggle. 📣 Ignacio (06/10, a confirmar): la
  práctica es **las dos cosas — apagar el toggle y avisar al PM**.

**Archivo final cargado por fuera de LEB:**

- Mover `pyx_internal_source`, `added_at` y `sequence` **al final** de la tabla `prefill_data`.
- **Todos los registros con email único.**

**Clonar un survey *managed*** (con el toggle *managed* encendido):

- Los toggles de LEB quedan **deshabilitados** en el clon.
- **No se copian** (quedan vacías): `all_data`, `progress`, `emerge`, `prefill_data`,
  `survey_launch_batches`, `survey_launch_emails`, `dc_info`, `emerge_group`, `emerge_group_rel`,
  `survey_launch_batched_group_rel`.
- Clones anteriores a este resguardo pueden traer basura: si `resp_questions` o `all_data` tienen valores
  tipo `01_01_07`, **puede hacer falta limpiar los datos del clon**.

---

## Data file load (carga de archivo de participantes con LE)

Sesión 28/09/2026. Caso: carga de un archivo de cliente, sin manager tree.

1. Permisos y **backup** de las tablas que cambia el data file load (script del Text Expander; Emily
   quedó en agregarle las *rest questions*).
2. Pasar el archivo del cliente por el **LE data file builder** (= Data File Builder para LEB; ✅ el camino normal, que ya controla nombres de columna reservados), con banding (generación, tenure en
   bandas de 10 años, edad).
   - Errores típicos: **fila vacía** (→ borrarla), **formato de fecha** (→ el builder ofrece *fix
     dates*), columna **manager ID** innecesaria cuando no se arma manager tree (→ sacarla).
   - Se reinicia con el archivo corregido y se descarga el LE file.
3. **Antes de cargar: revisar branching.** Cargar un archivo nuevo cambia demográficos y deja el
   branching existente incorrecto. Branching simple se rehace; complejo se carga por *advanced
   reporting*.
4. **LE app (= LEB) › invite list › Bring Your Own List** → seleccionar el LE file. ⚠️ Es la misma pantalla de la carga directa de § Columnas reservadas: acá es segura porque el archivo ya pasó por el builder.
5. **Selección de demográficos: destildar** lo que no debe ser demo — fechas, nombre completo, manager
   ID, fecha de ingreso original, SSO ID, fecha de terminación. Motivo: identifican a la persona o no
   sirven para filtrar. ⚠️ Avisa que **borra los demográficos existentes**; se confirma, *save* e
   *import*.
6. *Settings* → **sync records to SQL**.
7. **Data collector verification script.** Si marca algo (en el caso: *termination type* vacío), se
   inspecciona con un `SELECT DISTINCT` sobre la columna para ver si la alerta es real.
8. Ordenar las bandas (edad, generación, tenure) con la helper formula y mover el **audit report** →
   tarea completa.

**Manager tree:** los clientes suelen quererlo, pero se arma solo si el PM lo pide. En el caso, el PM
dijo explícitamente que no.

---

## Sacar bajas anteriores a una fecha de corte (snippet `;terms`)

> ✅ Snippet ***;terms*** del grupo *DM Snippets* de Text Expander (captura de Ignacio, 16/10/2026; solo
> lectura). No se vio usarlo en una tarea: el **cuándo** es 🔍.

Pide *Database* (app ID) y *Cutoff Date*. Hace, en este orden:

```sql
CALL mac.create_backup('<app>', 'prefill_data', @results); SELECT @results;
CALL mac.create_backup('<app>', 'emerge', @results);       SELECT @results;

delete from emerge where emp_id in
  (select emp_id from prefill_data where termination_date < '<fecha de corte>');
delete from prefill_data where termination_date < '<fecha de corte>';
```

- **`emerge` va primero** porque encuentra a quién borrar a través de `prefill_data`: al revés, el segundo
  `DELETE` no encontraría a nadie.
- 🔍 Sirve cuando el archivo del cliente trae **bajas** (gente con `termination_date`) que no deben
  invitarse. Es la versión SQL de destildar inactivos en LEB (§ Carga del archivo final, paso 4.6).
- 🔍 **No toca `all_data`**: si la persona ya respondió, su respuesta queda. Para eso existe *Operations
  tools › Remove Ineligible Participants* (borra respuestas de no elegibles / bajas, ver § Emails,
  traducciones y chequeos). Hay otro snippet, *Datafile - Remove Terms* (`;dmtterm`), cuyo contenido no se vio.
- 🔍 Compara `termination_date` como **texto**: funciona si el formato es `AAAA-MM-DD`. Con otro formato,
  el `<` compara mal sin dar error.

---

## Actualizaciones después del cierre del survey (manager IDs, manager tree, demos)

Sesión 30/09/2026. Disparador: el PM avisa de antemano que al cerrar el survey hay una tarea del mismo
día (en el caso ya se había hecho una de *after-close comments*).

1. Bajar el archivo de correcciones del cliente desde **Transmit** (carpeta *incoming* de la tarea) a
   la carpeta propia. Las filas resaltadas son los empleados a corregir.
2. **Backup**: `prefill_data`, `managers_tree`, `all_data`, listas y `resp_questions`.
3. **Manager IDs** — viven en **dos** lugares: `prefill_data` y `managers_tree`. Se generan los
   `UPDATE` con una fórmula de Excel (set manager ID where ID del registro = …) y se corren en las dos
   tablas. Emily tiene las fórmulas armadas y quedó en compartirlas.
4. **Rebuild del manager tree** — después de cambiar IDs el *path* del árbol queda mal:
   - Sacar los datos (email en blanco), formatear como texto en Excel, **quitar el 0 de la fila del CEO
     y la fila placeholder de arriba** (si no, falla la carga).
   - Correr el **data file builder** de *Survey Setup › Operations tools* con el file ID del CEO.
   - Mover los audit files viejos a otra carpeta (conflicto de nombres), abrir el audit en el editor y
     subir los managers nuevos.
   - Managers faltantes → al PM con el audit file (regla 8).
5. **Data integrity verify script.**
6. **Demográficos** (columnas con valores): generar `UPDATE`s, o más rápido por *Operations tools ›
   participant data*, matcheando por ID y "update to blank if blank". Registros que no están en
   prefilled se saltean.
7. Si el verify script dice que falta una opción de demo → *Operations tools* › agregar opciones de
   demo faltantes desde participant data.
8. **Sync reporting demographics from participant data** para las columnas tocadas → `all_data`.
9. Audit report al PM.

---

## Agregar un demográfico nuevo

Sesión 01/10/2026 (demo updates). Caso: el cliente pide, ya cerrado el survey, un demo calculado a
partir de la ubicación de trabajo.

1. **Backup** (en el caso, desde Querious).
2. Extraer ID de participante + campo origen de `prefill_data` a Excel y armar el archivo de
   configuración con las etiquetas nuevas (ej.: agrupar ubicaciones en 3 categorías).
3. **App operations › add/update demographics**: elegir el archivo, **matchear por el ID único del
   participante**, todos los estados, **correr test**, después cargar.
4. **Verification script.**

**Alternativas** (pregunta de Ignacio): el script Perl **`add new demo`** agrega el campo en todas las
tablas y después se actualiza `prefill_data` por SQL; o a mano tabla por tabla (`resp_questions`,
`prefill_linkage`, `prefill_data`). Las dos funcionan; la app o el script reducen el riesgo de
olvidar un paso.

---

### Demo calculado desde una fecha: Age Band / Tenure Band (tarea real, 27/10/2026)

> ✅ App EU de LEB, **cerrado**, ~15.800 participantes y ~13.800 respuestas. Paso a paso con Ignacio. Cliente omitido.

1. **¿Existe el demo?** Listar todos: `select l.resp_id, l.emerge_id, q.text from prefill_linkage l left join
   resp_questions q on q.id = l.resp_id`. Ojo con los nombres engañosos: `band` es la banda de puesto, y
   `manager_employee_id` aparece en un `LIKE '%age%'`. Si no existe, el pedido de *"update"* es **crear** dos demos.
2. **Fechas en `AAAA-MM-DD`** (`regexp '^[0-9]{4}-[0-9]{2}-[0-9]{2}'`). Las vacías suelen ser late adds incompletos:
   completarlas antes de calcular.
3. **Fecha de corte:** la del lanzamiento (`min(sent_date)` de `emerge`). 🔍 Elegida por Claude (la tarea no la
   daba). Se informa a la PM.
4. **Previsualizar** con `timestampdiff(year, <fecha>, '<corte>')` + `CASE` agrupado: las bandas tienen que sumar el
   total, sin menores de 18, ingresos futuros ni fechas vacías.
5. **Exportar** `emp_id` + `Age Band` + `Tenure Band` (textos exactos del pedido) a CSV desde Querious.
6. ***Operations Tools › Participant Data › Add / Update Demographics***: *Action* = **Add New Demographics**,
   *Match Field* = `emp_id`, ***Statuses with access* es obligatorio** (si no, frena con *"Please select statuses
   with access"*). Mirar `statuses.blocked_demos`: por defecto todos ven todo salvo lo bloqueado, así que se tildaron
   todos. **Test Mode = Yes** primero.
   - El test lista *"Clean up different case"* para todas las filas: no es error.
   - ✅ **Crea la columna en `prefill_data`, el demo en `resp_questions` y las opciones, y *reconstruye `resp_list` y
     `all_data`***: las respuestas ya existentes quedaron con su banda, sin sync aparte.
7. **Orden:** las opciones quedan **alfabéticas**. La edad (`18-24`…`65+`) coincide con el orden lógico; la
   antigüedad no. Se reescriben los textos en las posiciones (`UPDATE resp_list SET text = CASE seq …`) y enseguida
   ***Sync reporting demographics*** de ese demo (test: todas las respuestas aparecen como discrepancia; después en
   vivo). Verificado contando `all_data` por posición contra `prefill_data`.
8. **Q&I** al final.

## Reordenar las opciones de un demográfico

Sesiones 01/10/2026 (demo y práctica). Es la tarea que practicaron Ignacio, Andrea y Guillermo.

1. Verificar que el survey esté **desactivado** (regla 2). Desactivar el demo y correr el **demo
   backup script** (tablas principales: `resp_questions` y `all_data`).
2. **Encontrar el ID del demo** en `resp_questions` (Querious). Si no se sabe el ID, búsqueda con
   comodín: `LIKE '%leadership%'`. Los IDs suelen empezar con `02`, pero no siempre.
3. **Buscar dependencias** (regla 3), en modo solo lectura: el ID en `surv_questions_conditional` (✅ 23/09; antes anotado como *"Q condition"*), filtros,
   comparison views y `trend_custom_linkages`. Emily tiene una query armada (`select *` + filtro por el
   demo) y snippets para chequear que no se use en otro lado ni tenga *trend mismatch*.
4. **Excel + helper formula**: exportar opciones e índices (al importar: origen **Unicode UTF-8**,
   delimitador coma), pegar desde la **fila 22** de la helper formula, ordenar de menor a mayor
   (ej.: <18, 25, 35…; <1 año, 1, 1–3…). Opciones tipo *"not participating"* al final — **si no está
   claro dónde va, se le pregunta al PM**.
5. **Correr los `UPDATE`** en la base (conexión **read-write**). El índice de cada opción se registra en
   `all_data`: cambiar el orden cambia los índices.
6. Verificar el nuevo orden con un `SELECT` del ID.
7. **Rebuild**: SOS (ícono de llave) › *Perl scripts* › `rebuild all data demo from prefill`, con el ID
   del demo — **test primero, después live**; *blank prefill* = yes; *add as approved* = **no**. Se
   puede hacer un demo por vez o todos juntos.
   Alternativa sin script (📣 Jackie, 21/09): *Operations tools › Data › **Sync reporting demographics from
   participant data***, por demo (§ Emails, traducciones y chequeos del app).
8. **Si el demo estaba en trends**: bajar el *trend mismatch report* del reporting site, borrar las
   linkages viejas en `trend_custom_linkages` y regenerarlas con fórmulas. Procedimiento escrito completo en § Trend mismatch.
9. **Verify survey integrity** (SOS, columna *read*). En surveys grandes tarda. Versión con interfaz:
   *Operations tools › Utilities › **Quality and integrity checks*** — marca justamente el desfasaje
   `prefill_data` / `all_data` que deja un reordenamiento sin resincronizar (📣 Jackie, 21/09).
10. Cerrar la tarea (regla 9).

**Para los PM, dicho por Emily:** deberían revisar el orden de los demos al cargar el archivo; reordenar
después es retrabajo evitable.

---

## Comentarios con modelo léxico (workaround de bug)

Sesión 01/10/2026 (demo updates) y huddle del mismo día.

**El bug:** los comentarios que se procesan con el **modelo léxico** se pierden o quedan mal tematizados
en Snowflake. Los surveys con **modelo supervisado** no tienen el problema.

**Cómo saber si un survey está afectado:** ✅ (captura del 20/10/2026) *Report Editor › Configuration*, con los
campos **Filter** y **Bucket** (la casilla *Show Active Toggles Only* oculta lo apagado). Filter `Snowflake` →
*"Enables automated comments processing (Snowflake)"*: si está activo, hay procesamiento automático. Filter
`Themes matching` → *"usage of machine learning level"* (valor *Level 0: … lexical keyword matching* = léxico) y
*"supervised: machine learning models"* (activo = supervisado). 📣 Antes el procedimiento decía *Survey Setup ›
Survey Configurations*: esa pantalla no muestra estos toggles. 🔍 Pendiente confirmar la ruta con Jackie.
✅ **30/10/2026 (capturas, survey EU):** la pantalla es `rm=configure` (`https://ondemand[.eu].perceptyx.com/<app_id>/index.cgi?rm=configure`).
En la misma pantalla, Filter `deactivate` → ***Deactivate Survey?*** (bucket *Data Collector, Key Features, LEB*): sirve
para la compuerta de survey cerrado sin ir a *Survey Configurations*. Filter `lexic` muestra además ***Only show themes
of selected models*** (activo, valor *Custom Themes (Lexical model)*): qué modelos muestra el reporte de comentarios.
Aviso de la pantalla: *"Disabled toggles can be configured in event builder"* (en LEB, los toggles apagados se cambian desde LEB).

**Workaround manual** (surveys con modelo léxico):

1. Script **`comments verify steps`** con el survey ID y step `2` (post-cierre). Dentro: paso 1
   (nombres duplicados), hacer visibles los temas, paso 3 (chequeo del procesamiento).
2. **Backup de `comments theme matches`**, vaciarla y repoblarla; **reinsertar los temas supervisados**
   (`model ID = 10`) desde el backup.
3. Verificar que el conteo de temas cambió, **rebuild y flush del comments report**.
4. En **EU** es igual, en el entorno EU (la VPN de US sirve para los dos — 📣 Ignacio).
5. Variante de Edwin: el mismo script desde **SOS** (IT / Python / Perl scripts).
6. ✅ **Observado 20/10/2026:** el paso 2 del script **escribe** en `comments theme matches` (hacer visibles los temas). Si el paso 3 responde `mismatches in comment qid counts` con la automatización de Snowflake en curso, la salida pide esperar o volver a correr. **Volver a correr solo el paso 3, no el 2:** repetir el paso 2 vuelve a escribir sobre lo ya escrito.
   ✅ **30/10/2026, otro estado de la automatización:** *"Current automation status: extra client IDs in Snowflake"*, con
   el mismo pedido (*"allow Snowflake automation to complete or re-run the process"*). Después el paso 3 sigue con los
   conteos (*Supervised / Lexically / Orphaned / Improperly modeled themed comments*); si dan bien, *"There are no
   issues with comments_themes_matches or lexical themes"*, y pasa a *comments processing*.
   ⚠️ **30/10/2026, falla en SOS en *comments processing*:** después de *"Comment QIDs:"* el script corta con
   `FATAL … Cannot create directory /usr/home//script_output/: No such file or directory at …/comments_verify_steps.pl
   line 312`. La doble barra indica que el usuario o el `$HOME` llega vacío al correr desde SOS: el script quiere
   escribir un archivo de salida en el home de quien lo corre y en el runner de SOS no hay home. Es **del entorno, no de los
   datos**: corta en el `mkdir`, antes de escribir, y lo que va hasta ahí (duplicados, visibilidad, conteos de
   `comments_themes_matches`) ya corrió. Recordar que los scripts de SOS figuran como *NOT TESTED*
   ([[Perceptyx/services-os|services-os]]). 🔍 Cómo se completa la verificación de *comments processing*: pendiente de
   quien mantiene SOS o de Jackie. ✅ Se repite igual al volver a correr solo el paso 3 (mismo día, 3 minutos después): no es
   intermitente. ✅ **Pasa también con otro app** (30/10, 14:08): no es del survey. 🔍 Puede ser de SOS en general o del usuario de
   Ignacio, que tampoco tiene armado el entorno en `pms.eu`. Elena lo corrió desde su home en `pms`, no desde SOS, así que
   eso no lo resuelve. Ignacio lo reportó por **IT Help**, junto con el alta del entorno (30/10). Mientras no se arregle, la parte
   *Comment QIDs* la tiene que correr alguien con el entorno de `pms` armado.
   📣 **Elena Khaletskaya, 30/10/2026 (Slack), sobre *"extra client IDs in Snowflake"*:** *"If we have matching number of
   comments I think we are good"*. El criterio es que coincidan los conteos de comentarios, no que el aviso desaparezca.
   🔍 Falta saber qué conteos tienen que coincidir: lo más probable es la comparación de *Comment QIDs* (app ↔ Snowflake),
   que es justo la parte que corta en SOS.
   ✅ **Cómo se completó (30/10/2026):** en el host de scripts (`pms.eu.perceptyx.com`) tampoco le anduvo a Ignacio, que todavía no tiene el entorno armado: *Can't locate DBI.pm*, `proot` inexistente ([[Perceptyx/plataforma|plataforma]], fila *Jail*). Lo corrió **Elena desde
   su entorno**, con home propio, y ahí *Comment QIDs* lista cada pregunta abierta con *"All comments processed for QID
   …"*, deja el detalle de lo no procesado en `/usr/home/<usuario>/script_output/<app_id>_unprocessed_comments.txt` y
   termina con *"If all comments have processed, you are good to proceed."* Con todas las QID procesadas, el aviso
   *extra client IDs in Snowflake* **no bloquea**: es el criterio de Elena. Mientras SOS no se arregle, la vía es
   pedirle a alguien con jail que funcione que corra la parte post-cierre del paso 3.
7. ✅ **Backup de `comments_themes_matches` (30/10/2026, app LEB EU, tarea *PFS: Verify Comments Processed (Survey Closed)*):**
   la tabla **no aparece** en el desplegable de *Operations Tools › Utilities › Backup table* (🔍 no se sabe por qué; las
   tablas `comment_*` y `comments_processed*` sí). Se respaldó por **SOS › Database Tools** con `CREATE TABLE
   comments_themes_matches_AAAAMMDD_<iniciales> LIKE comments_themes_matches;` y después `INSERT INTO … SELECT * FROM
   comments_themes_matches;` (regla 1, tercera vía; Database Tools aceptó el `INSERT … SELECT` aunque nombra dos tablas) y se verificó el conteo en Querious
   (entrada = salida). El nombre real de la tabla es `comments_themes_matches` (✅ `SHOW TABLES`).
8. ✅ **`model_id = 10` con el supervisado apagado (30/10/2026):** en ese survey (léxico, *supervised* apagado),
   `comments_themes_matches` tenía 67.007 filas con `model_id = 10` y 31.318 con `NULL`. El paso 3 del script las cuenta
   como *Supervised themed comments: 66994* y *Lexically themed comments: 31312*: **`10` = supervisado se confirma**, y
   hay temas supervisados aunque el toggle esté apagado (🔍 los generaría Snowflake igual; el toggle *Only show themes of
   selected models = Custom Themes (Lexical model)* decidiría cuáles se muestran). Si hubiera que repoblar, la
   reinserción de `model_id = 10` sí tiene filas que restaurar.
9. 🔍 **Backups automáticos el día del cierre:** el mismo 30/10, antes de abrirse la tarea, ya existían
   `comments_themes_matches_partial_removal_<fecha>_0416…` y `…_terms_removal_<fecha>_0422…` (y lo mismo para
   `comment_sentiments*` y `comments_processed*`). Igual que el 20/10. Patrón: algo corre al cierre y deja esos backups
   (🔍 probablemente la automatización de Snowflake); los `…_clr_data_…` son de los clearouts previos al lanzamiento.

**Estado al 01/10/2026** (✅ decisión registrada en el huddle, por Jackie Cech): engineering dice que
está arreglado, pero **el script manual se sigue corriendo** hasta que los chequeos automáticos entren
en el *survey launch audit*. Si aparecen temas léxicos mal o comentarios viejos/falsos que vuelven
después del clearout previo al lanzamiento → avisarle a Jackie **con los backups de las tablas** para
comparar. Documentación: Confluence (*snowflake comments*).

---

## Alta de un cliente en la plataforma (Platform Configuration, US y EU)

> **Fuente: ✅ Confluence, *(Temp) Platform Configuration (US)* y *(Temp) Platform Configuration (EU)***,
> exportadas por Ignacio el **06/10/2026** (.doc). **Son la versión vigente**: *Platform Technical
> Setup* (PDF) se creó en febrero y es anterior (📣 Ignacio, 06/10). Lo que solo tenía el PDF, en §
> Qué versión manda.
> Ejemplos de nombres de cliente reemplazados por uno genérico; usuarios de ejemplo omitidos.
>
> **Quién:** el documento marca cada bloque con su dueño. **PFS = Delivery Ops** (nombre anterior, 📣
> Ignacio 06/10). Los bloques **PFS** son tuyos; los **PM** son del program manager.

**La cadena:** Certinia → **UDS** (compañía) → **Okta** (proveedor de identidad SSO + Group UUID) →
**MAC** (cliente + *master app*) → **binlog** (qué tablas se sincronizan con UDS) → cierre cruzando IDs.
Después, la parte del PM: usuarios admin, SFTP, permisos de administrador y envío de accesos.

**Dónde se rompe** (🔍 lectura propia): un **duplicado** por no buscar antes (UDS, Okta, MAC); el
**nombre** que no es idéntico en todos lados, pasa los 30 caracteres o le falta el `EU-`; el **Customer ID
provisorio** que queda sin reemplazar; y en EU, el `uds_invite_type` que se deja en `invitation`.

**Diferencias US / EU de un vistazo:**

| | US | EU |
|---|---|---|
| Nombre del cliente (UDS, Okta, MAC) | `Cliente` | **`EU-Cliente`** — obligatorio |
| Login a UDS | `go.perceptyx.com/login` → *Login Now* | Okta › *My Apps* › chicklet **People Insights Platform (EU)** |
| `uds_invite_type` en MAC | `invitation` | **`sso`** |
| URL del master app | `ondemand.perceptyx.com/<app_id>` | `ondemand.eu.perceptyx.com/<app_id>` |
| Entrar a la compañía en UDS | *Shadow company* | *Switch to company* |
| Buscar el grupo en Okta | por nombre | empezando por `EU-` |

### 1. Datos del cliente en Certinia — PFS

Salesforce → buscar el cliente → proyecto. Copiar **Account** y **Account 18 Digit SF ID**.

### 2. Crear la compañía en UDS — PFS

- **Antes: buscar si ya existe.** Una sola instancia por cliente.
- Login (ver tabla US/EU) → *Administrator Portal* → *PYX Admin › Create Company*.
- **Name** y **Description**: idénticos entre sí y al nombre en MAC; se puede acortar el de Certinia;
  **máx. 30 caracteres**. En EU, con prefijo `EU-`.
- **Customer ID**: número **provisorio** único (chequear que no esté usado). **Se reemplaza en el paso 7.**
- Subdomain = `app` · Activation/Invite Method = **Invitation** · Master App ID (el de MAC) · Salesforce ID.
- *Create Company*.
- SSO después: cuando el cliente está configurado y listo para probar, el PM pide en Slack
  **#product_support** pasar los usuarios a SSO.

### 3. Crear el proveedor de identidad en Okta (metadata) — PFS

Se usa también si el cliente pide **nuestro** metadata primero. Requiere **Okta Verify** configurado (si
aparecen dos códigos, usar el de `login.perceptyx.com`). Casi todo viene precargado; se cambia lo marcado
en verde.

1. Okta admin › *Security › Identity Providers*. **Buscar antes que no exista.**
2. *+ Add Identity Provider* → **SAML 2.0**.
3. *General Settings*:
   - Name = `<Cliente> SSO` (EU: `EU-<Cliente> SSO`)
   - IdP Usage = SSO Only · IdP Username = `idpuser.subjectNameId` · Match against = Custom SSO ID
   - Account Link Policy = Automatic · Auto-Link Restrictions = None · If no match = Redirect to Okta
     sign-in page
   - SAML: Issuer URI = `test` · SSO URL = `https://URL` · **Signature Certificate = el certificado
     "falso"** del documento (se guarda y se reutiliza; se reemplaza cuando llega el metadata real del
     cliente)
   - Request Binding = HTTP Post · ☑ Sign SAML Authentication Requests · Request Signature = SHA-256 ·
     Response Signature Verification = Response or Assertion · Response Signature = SHA-256 ·
     Destination = `https://URL` · ACS URL = Trust-specific
4. *Finish* → **Download Metadata** (va al cliente en el *Platform Setup recap email*).
5. *Directory › Groups* → buscar el cliente (la búsqueda es quisquillosa: por la primera palabra del
   nombre, no por una del medio) → **copiar el Group UUID de 36 caracteres.** ✅ **Eso es el
   `uds_company_id` del paso 4.**

### 4. Crear el cliente en MAC — PFS

- **Antes: buscar en *Customers Table*** (columna `masterapp_app_id`, última a la derecha). Un master
  app por cliente. **Si existe, saltear los pasos 4 y 5.**
- *Functions › Create New App › Add New Customer*:
  - `company_name` = `company_nickname` = el nombre de UDS, **exacto** (EU: con `EU-`)
  - `active = 1` · `sfdcid` = Account 18 Digit SF ID · `uds_active = 2`
  - `uds_invite_type` = `invitation` (US) / `sso` (EU)
  - `uds_company_id` = **Group UUID de Okta** (paso 3.5)

### 5. Crear la Self Service Master Application en MAC — PFS

- *Functions › Create New App*: **Application ID** = DB name de *Company Details* en UDS, sin guion bajo
  inicial, **máx. 30 caracteres** (US: minúsculas, sin espacios; ej. `acme_corp`) · Name/Description =
  `<Cliente> Self Service Master Application` · Type = *Master Self Service Application* · Prefix = 2–3
  letras · Master_app = `mac` · Customer = el del paso 4.
- *Create new application in production* → URL según tabla US/EU.
- Entrar → engranaje › *Configuration* → toggle **Which tables can transact with UDS via binlog** (paso 6).

### 6. Tablas que transaccionan con UDS (binlog) — PFS / PM

- **Cliente nuevo:** lo hace Delivery Ops (PFS) acá.
- **Cliente existente:** el PM pide antes a **Special Projects** (vía tarea PFS) migrar al cliente a
  **binlog listeners**, obligatorio aunque no usara Listening Home ni triggers. Tarea: *Workstream:
  Listening Home · Category: UDS · Sub-Category: Listening Home*.
- En la aplicación: `rm=configure` → bucket *Admin* → *Which tables can transact with UDS via binlog*:

| Tabla | Cuándo |
|---|---|
| **Users** | Logins de PIP/resultados. **Inmediatamente al configurar.** Todas las apps |
| **Emerge** | Al lanzar |
| **Survey Respondents** | Al lanzar — ⚠️ desde ahí **los links del survey quedan accesibles** |
| **Prefill_data** | Solo si hay empleados del survey fuera del master app, o no hay automatización de datos |
| **Prefill_data_all** | Lista completa del data file; típicamente solo en el master app (con automatización) |

- Típico: *Users* al principio, *Emerge* al lanzar. Cada aplicación se configura por separado. Al crear
  *statuses*, definir también *status_groups*.

### 7. User Set-up: cierre — PFS

1. MAC › *Customers Table* → editar el cliente → `master_app_id` = nombre del master app.
2. Copiar el **Customer ID** de MAC → UDS → compañía → campo **Classic customer ID** (pisa el
   provisorio) → *Save Changes*.

### 8. Platform Admin Set-up — PM

- En el master app: *Application Settings › User Management › + Add New User* con los usuarios de prueba
  que identificó el cliente (username, nombre, email y Employee ID **únicos**, Role = Admin o Creator) →
  *Save*; *Send Invite* cuando corresponda. Verificar que aparezcan en UDS con el mapeo correcto.
- **SFTP:** auto ticket en el service desk de Atlassian › *Auto Tickets › Create SFTP User* (**sin
  guiones bajos ni espacios** en el username). Después: login al SFTP (SFTP, `sftp.perceptyx.com`, puerto
  22, carpeta `incoming`), mail al cliente y confirmar con él la carpeta.

### 9. System Admin set-up — PM

Da acceso al *Administrator Portal* de PIP a los admins del cliente (que después no pueden agregar otros).
UDS › *Administrator Portal* › *Pyx Admin* → buscar compañía → *Shadow / Switch to company* →
*Employees* → buscar → *Actions › User Details* → *Edit Account* si hace falta → *Edit Roles*:
**platform_administrator = Company Read-only Admin** y verificar **ondemand = Admin** (hace aparecer la
pestaña *Listen*) → *Save*. Avisar en el canal de Slack del cliente (hasta que Gainsight tenga un flag).

⚠️ No usar otras opciones por ahora (no todas las automigraciones están y lo editado ahí no persiste).
**Limitar a 2–5 Platform Admins por cliente.**

### 10. Customer Access — PM

- Master app › *User Management* › engranaje del usuario › *Send invite* → repetir para cada admin.
- EU, si usa usuario/password: en UDS, el estado **"Activating"** = recibió el mail y todavía no hizo
  clic.
- La plataforma desloguea tras **60 minutos** sin interacción.
- Volver al *Platform Setup recap email*.
- US: para usar la **URL de SSO en el Listening Event Builder** hacen falta (1) feed automatizado a
  `master_app.prefill_data_all`, (2) binlog configurado y (3) SSO de PIP (Okta) funcionando.

### FAQ del binlog — y por qué importa para las tareas de datos

- **Fuente de verdad: `master_app.prefill_data_all`**, automatizada; ahí va el binlog listener. Si no
  existe, el `prefill_data` más reciente (último censo o el próximo).
- **`master_app.users` siempre con binlog** (es la lista de usuarios de ondemand); todas las apps con
  binlog en `users`. Las tablas `emerge` de ASK self-service ya lo tienen.
- ⚠️ **Cambiar emp_id, nombre, email o sso_id en `users` o `emerge` NO cambia UDS.** La "meta"
  información del usuario se cambia **en la fuente: `prefill_data(_all)`**. Así el cliente se hace cargo
  de sus datos y Perceptyx deja de parchearlos.
- Binlog es más rápido y completo que los triggers viejos.

🔍 **Conexión con lo del training:** es la misma regla que [[#Reglas que valen para toda tarea|regla 4]]
desde el otro lado — el dato vive en prefill y desde ahí se propaga. Un `UPDATE` en la tabla equivocada
"funciona" en la base y no llega a la plataforma.

### Qué versión manda

~~**No se sabe con certeza cuál es la vigente.**~~ SUPERSEDED 06/10: 📣 Ignacio vio en Confluence que
***Platform Technical Setup* (el PDF) se creó en febrero** → es la anterior. **Manda *(Temp) Platform
Configuration*.** Matiz: *creado* no es *última edición*; si el PDF se siguió editando después, alguna
diferencia podría ser más nueva que (Temp). Año de creación no anotado. La evidencia previa, que apunta en
el mismo sentido:

- Las páginas *(Temp)* tienen capturas fechadas hasta el **28/04/2026** → se editaron por lo menos ese
  día. El PDF no trae fechas.
- 🔍 **Indicio de que *(Temp)* es posterior:** en la página EU, el paso del master app conserva el texto
  *"Update the below toggles to match the contract of Users"* —el del PDF, que listaba los máximos de
  usuarios— pero debajo ya muestra el toggle de binlog con la captura del 28/04. Parece texto viejo
  editado a medias.
- *"(Temp)"* en el título sugiere una página de transición. 🔍 Puede ser la versión nueva en
  construcción o una provisoria.

**Lo que tenía *Platform Technical Setup* (PDF) y no aparece en (Temp)** — se conserva por si sigue
siendo necesario:

- En UDS: *Shadow Company › Company Details › Edit Information* → toggle **Platform 2.0 Experience**, y el
  PM avisa al manager que actualiza el indicador **PIP** en Salesforce.
- En el master app: *Configuration* → **Maximum # of Active Admin Users** y **Maximum # of Active Creator
  Users** según contrato (si hay duda, AE/CSM).
- No tenía: Okta, Platform Admin, SFTP, System Admin, Customer Access ni FAQ.

➡️ Sigue abierto solo esto: **¿el toggle *Platform 2.0 Experience* y los máximos de usuarios
admin/creator ya no hacen falta, o (Temp) los omitió?** (ver
[[Perceptyx/_indice#Preguntas abiertas para el equipo|_indice § Preguntas abiertas]]).

---

## Sincronización con UDS (binlog): cómo decide y por qué no llega un cambio

> ✅ Confluence *UDS*, exportada 06/10/2026. Complementa § Alta de un cliente › FAQ del binlog.

**Qué escucha UDS en cada aplicación** (solo si la tabla está tildada en *Which tables can transact with
UDS via binlog* **antes** del cambio):

| Tabla | Qué dispara en UDS |
|---|---|
| `prefill_data` / `prefill_data_all` | **Fuente de verdad del usuario**: agrega o actualiza el usuario |
| `emerge` (respondentes) | Migración de *mapping* cuando el survey se pone disponible |
| `users` (usuarios de reportes) | Migración de *mapping* cuando el usuario se activa |

**Árbol de decisión:**

- 🟢 **Binlog encendido:**
  - Email **y** emp_id no existen en UDS → se crea **usuario + mapping**.
  - Email **o** emp_id ya existe → se agrega **solo el mapping**. Cada combinación emp_id + email es un
    usuario; un usuario puede tener muchos mappings (surveys y reportes a los que tiene acceso).
- 🔴 **Binlog apagado:** **no pasa nada en UDS.** Hay que encenderlo y **repetir el cambio**.

**Lo que hay que tener presente:**

- Binlog se enciende solo en las tablas de usuarios nuevas y en `emerge` y `users` de las apps
  self-service. **En el resto, confirmar que esté encendido antes de cargar datos.**
- ⚠️ **Los clones copian la configuración de binlog del original**: revisarla.
- ⚠️ **Si el cliente tiene feed diario, el feed pisa cualquier cambio manual** al refrescar. Un arreglo a
  mano en una tabla con feed dura un día.
- **SSO ID:** solo entra a UDS desde `prefill_data` o `prefill_data_all`, y **la columna tiene que
  llamarse `sso_id`**. Sin integración de datos: confirmar binlog en el `prefill_data` del app actual
  **antes** de cargar.

**Troubleshooting — el cambio no aparece en UDS** (🆕 06/10: en SOS, **Support › UDS User Health** hace
este cruce para un respondente — UDS, Okta y la base — y permite activar un mapping faltante; ver
[[Perceptyx/services-os|services-os]]):

1. ¿Binlog encendido (antes del cambio)?
2. **Binlog drift** (demora): ver el *PM Dashboard* en la página de SPT en Confluence.
3. **Caracteres especiales** en nombre o apellido *classic* → el registro se saltea.
4. **Usuarios divergentes**: dos registros en UDS para la misma persona (uno por email, otro por emp_id)
   → borrar uno y volver a disparar el cambio.
5. **sso_id duplicado**: si ya existe en UDS, el registro no migra.

---

## Borrado de registros y remoción de PII (pedido del cliente)

> ✅ Confluence *Customer Survey Data Management & Record Removal Policy* y *Certinia Request Process –
> Record Deletion | PII Removal*, exportadas 06/10/2026. **Delivery Operations es quien revisa, ejecuta y
> documenta.** No incorporados todavía: el *Request Form* y el ***Execution Checklist*** (el paso a paso
> técnico de la ejecución).

**Dos opciones, nada más.** Si el pedido no encaja en ninguna, el PM consulta a Delivery Ops antes de
seguir.

| | Opción 1 — **Record Deletion** | Opción 2 — **Participant Identifier Removal** |
|---|---|---|
| Qué hace | Borra del survey app: participante, respuestas, comentarios, demográficos | Reemplaza emp_id, nombre, apellido y email por valores no identificatorios |
| Queda | Nada de ese registro | Respuestas y demográficos |
| Se pierde | Todo; **no se puede restaurar** | **Comentarios y jerarquía de managers** |
| Reportes | Sin reporte, trend, benchmark ni comparación histórica | Respuestas, demográficos y trends siguen; comentarios y reportes por manager no |

**El flujo (Certinia):**

1. **PM/CSM** recibe el pedido y define el tipo.
2. **PM/CSM + cliente** completan el *Customer Data Deletion & Participant Identifier Removal Request
   Form*: tipo, impactos entendidos, aprobación. **Sin formulario completo no empieza el trabajo** — es la
   autorización oficial y el respaldo de auditoría.
3. **PM/CSM** crea la tarea en Certinia (*Data – Record Deletion* o *Data – Participant Identifier
   Removal*) con el formulario adjunto.
4. **Delivery Ops revisa**: alcance, factibilidad técnica, impacto en reportes. Si hace falta, consulta a
   Engineering, Product, InfoSec, Privacy o Legal. **Anota el resultado en la tarea.**
5. **Delivery Ops ejecuta** con el *Execution Checklist*, **verifica**, adjunta el checklist completo a la
   tarea y documenta notas o excepciones.
6. **PM/CSM** revisa, avisa al cliente, confirma que todo esté adjunto y cierra la tarea.

**Lo que no se borra y conviene saber antes de prometer nada:**

- **Backups:** diarios ~12–13 días, semanales ~12 semanas, mensuales ~12 meses; máximo un año. Lo borrado
  sigue existiendo en backups hasta que expiran.
- **Audit logs:** inmutables; no se tocan por pedido del cliente.
- 🔍 **Si el cliente no lo saca de su fuente, vuelve.** La política lo pone a cargo del cliente: tiene que
  borrar el registro de sus sistemas y de sus integraciones automáticas. Con un feed diario y binlog
  encendido (§ Sincronización con UDS), un registro borrado reaparece al día siguiente.

---

## Habilitar la API estándar para un cliente

> ✅ Confluence *Perceptyx API Setup Process*, exportada 06/10/2026.

**Qué entrega la API estándar:** datos de respuesta **a nivel de registro**, para BI, reportes internos o
data warehouse. **No aplican los umbrales de anonimato de los reportes.** Identificadores de empleado
apagados por defecto, habilitables por survey; ⚠️ **habilitar PII en un survey también lo habilita para
cualquiera del cliente que pueda bajar flat files del reporting site.** Alcance: **todos los surveys del
entorno**, sin restricción por survey.

🔍 **Esto explica el patrón del huddle del 01/10** (cliente que pide API y sus propios stakeholders de
privacidad la bloquean): la API estándar es exactamente datos crudos sin umbral de anonimato y sin poder
limitarla a un survey. La salida que encontró el equipo —reporting o extracción agregada por script— es
lo que la API estándar no ofrece.

1. **Requisitos:** **DRA** firmado (los contratos nuevos lo traen) · Technical Contact confirmado con el
   CSM.
2. **Acuse del cliente** sobre datos y alcance **antes de dar credenciales**: mail con el snippet
   **`;apiconfirm`**. Guardar el acuse.
3. **Habilitar:** plataforma (US `app.perceptyx.com` / EU `app.eu.perceptyx.com`) → engranaje → *Pyx
   Admin* → compañía → *Shadow Company* → *Platform Settings › Integrations* → *Perceptyx API › Enable*.
4. **Crear la aplicación:** *Data Management › API Tokens › + Create Application* → guardar **Client ID**
   y **Client Secret** (**el secret se muestra una sola vez**).
   - Si ya existe una aplicación: **antes de revocarla, confirmar que ninguna integración activa la
     use** (revocar invalida las credenciales en el acto). Alternativa: recuperar el secret desde Okta.
5. **Probar en Postman** — workspace *Platform Services* › *Collections › Developer Portal API Access ›
   External*; entorno *Production US* o *EU*:
   - *INT Get CC Token* (Basic Auth: Client ID / Client Secret) → 200 + token.
   - *Get Survey List* → 200 + lista; copiar un `app_id`.
   - *StartResponseExport* + `app_id` → 200 + request ID. **Acá la conectividad ya está validada.**
   - (Opcional) *Get Response Export* + request ID → URL de descarga → JSON con las respuestas.
6. **Entregar credenciales por 1Password**, vault *Customer API*: ítems con nombre y Customer ID del
   cliente → *share link* **restringido al email del Technical Owner**, **vence en 1–7 días** → mail con
   snippet **`;apicredentials`**. ⚠️ **Nunca** el Client ID ni el Secret en mail, Slack, tickets, capturas
   o documentación.
7. **Documentar:** acuse del cliente en su carpeta del SFTP **DM Task (US/EU)**. (Actualizar
   Certinia/SOS con API habilitada + Technical Owner: *paso futuro, todavía no disponible*.)

---

## Datos de prueba para un 360

~~Conversión automática incompleta de *360 Survey Test Leader & Raters Setup Guide*.~~ SUPERSEDED
06/10: llegó la página real (*360 Survey Test Leader & Raters Setup*). Todo lo de 360 vive ahora en
[[Perceptyx/cultivate-360|cultivate-360]] § Usuarios de prueba. Lo único que traía la versión fallida y
sigue valiendo (prefijo consistente en los nombres de prueba, un leader por escenario) está implícito en
la real.

---

## SSO del cliente (después del alta)

> ✅ Confluence *SSO Team Process (US & EU)*, *SSO – OKTA Configuration (US)*, *SSO – OKTA Configuration
> (EU) NEW* y *SSO Helper Script*, exportadas 06/10/2026. Las páginas de Okta tienen capturas de
> **febrero de 2024**. Recursos citados y no incorporados: *Okta Runbook*, *Overview of SSO Implementation
> and Support*, *Perceptyx SSO Connection Form*, el script `Extract_SAML.py` y su readme.
>
> **Dueños:** la página del proceso dice *Owner: PM, SSO Team · Team: PFS*. 🔍 No está claro si el **SSO
> Team** (`pyx_sso@perceptyx.com`) es parte de Delivery Ops o un equipo aparte — la configuración en Okta
> está escrita para quien la ejecuta, y cita *"PFS CRON task"*.

**Requisitos:** alta de plataforma completa (§ Alta de un cliente), con el identity provider ya creado en
Okta con el certificado "falso" y el metadata de Perceptyx descargado.

**El flujo:**

1. **PM → cliente:** mail *"[Cliente] | Perceptyx Platform SSO Setup"* (o el del paso 3 del Platform
   Setup) **con copia a `pyx_sso@perceptyx.com`**, adjuntando el **metadata de Perceptyx** de ese cliente,
   el **SSO Connection Form** y la Quickstart Guide. El cliente completa el formulario (*Create a new SSO
   Connection*): identity provider (Okta, Azure…), **valor de autenticación**, **1–5 usuarios de prueba**,
   y responde con **su metadata**.
   - Valor de autenticación recomendado: **Employee ID u otro identificador que no sea nombre ni email**.
     Tiene que venir en la columna **SSO ID** del archivo de datos.
2. **Configuración en Okta** (abajo) con el metadata del cliente.
3. **SSO Team → cliente** (PM en copia): *"SSO Connection Ready To Test"* con la URL; los usuarios de
   prueba entran y mandan captura de página completa.
4. SSO completo → el SSO Team avisa al PM, que sigue con el armado del programa.

**Soporte posterior:** problemas con un SSO existente → *Issue/Bug/Task* en **#product_support**; clientes
complejos → *General Questions/Collaboration Needed* en el mismo canal.

### Cambiar una URL en los emails del survey (snippet `;updatesso`)

> ✅ Snippet ***;updatesso*** del grupo *DM Snippets* (captura de Ignacio, 16/10/2026). 🔍 Por el nombre, se
> usa cuando cambia la URL de acceso del survey, por ejemplo al pasar el cliente a SSO. No se vio usarlo.

Pide *app_id*, *old_url* y *new_url*. Primero respalda las tres tablas que toca:

```sql
CALL mac.create_backup('<app>', 'survey_launch_bodies', @results); SELECT @results;
CALL mac.create_backup('<app>', 'need_translation', @results);     SELECT @results;
CALL mac.create_backup('<app>', 'translated_phrases', @results);   SELECT @results;

update <app>.survey_launch_bodies set body_text = replace(body_text, '<old_url>', '<new_url>');
update <app>.need_translation   set english_value = replace(english_value, '<old_url>', '<new_url>');
update <app>.translated_phrases set translated_value = replace(translated_value, '<old_url>', '<new_url>');
update <app>.filestorage set content = replace(content, '<old_url>', '<new_url>')
  where filename like '/email_reminders/%%.json';
-- la captura corta acá: puede haber más líneas
```

- **Dónde vive una URL de los emails** (✅ por el snippet): el cuerpo de los mails de *Survey Launch*
  (`survey_launch_bodies`), las frases para traducir y las traducidas, y los JSON de recordatorios en
  `filestorage`. Si se cambia en un solo lado, el inglés y las traducciones quedan distintos.
- ⚠️ Sobre `filestorage` **no hay backup** en la parte visible del snippet.

### Configuración en Okta

**Requisitos:** el cliente existe en MAC y UDS, tiene su identity provider en Okta, mandó su metadata y
**confirmó su valor de autenticación**.

1. **Certificado:** abrir el metadata (XML) del cliente en **BBEdit** y correr el **SSO Helper Script**
   (`Extract_SAML.py`, recomendado). Genera, en la misma carpeta del XML:
   - `extracted_cert.crt` — el certificado x509 ya formateado para Okta;
   - `extraction_log.txt` — el **EntityID** (= *IdP Issuer URI*) y el **Location** (= *IdP Single Sign-On
     URL* y *Destination*), más errores si los hay.
   - Instalación, una vez: guardar el script en la carpeta de scripts de BBEdit (*ícono de pergamino ›
     Open Scripts Folder*) y darle permiso de ejecución con `chmod +x`. Se le puede asignar un atajo de
     teclado (*Window › Palettes › Scripts › Set Shortcut*).
   - Método manual (legacy): copiar el bloque `X509Certificate`, agregar `-----BEGIN CERTIFICATE-----` /
     `-----END CERTIFICATE-----`, guardar como `.crt` y pasarlo por `fold -w 64`. Si Okta lo rechaza, está
     mal formado. ⚠️ **Si el metadata trae dos certificados distintos, preguntar al cliente cuál usar**
     (por defecto, el primero).
2. **Actualizar el identity provider:** Okta › *Security › Identity Providers* → cliente → *Actions ›
   Configure Identity Provider* → *Edit*:
   - **Autenticación por Employee ID u otro valor:** *IdP Username* =
     `String.join(":", "<Group ID del cliente>", idpuser.subjectNameId)` · *Match against* = **Custom SSO
     ID**. Si el valor no es emp_id ni email, **pedir en la tarea CRON de PFS que la columna del valor se
     renombre a `sso_id`**.
   - **Autenticación por email:** *IdP Username* = `idpuser.subjectNameID` · *Match against* = **Okta
     Username or Email**.
   - *SAML Protocol Settings:* Issuer URI y SSO URL desde el `extraction_log.txt` · **reemplazar el
     certificado "falso"** por `extracted_cert.crt` · Destination = la misma URL de Location →
     *Update Identity Provider*.
   - Nota del doc: **las aplicaciones nuevas ya no usan `sso_id` como índice único**; Okta matchea contra
     el valor definido en UDS (employee ID, SSO ID o username/email).
3. **Routing rule:** *Identity Providers › Routing Rules › Add Routing Rule* → nombre `<Cliente> SSO` ·
   IP: Anywhere · dispositivo: Any · aplicación: Any · *User matches* = atributo **`company_ID` starts
   with `<Group ID del cliente>`** · *Use this identity provider* = **User specific IdP(s)** → el IdP del
   cliente, **sacando Okta** (no se permiten varios) → *Create Rule* → **Activate**.
4. **UDS y MAC:**
   - UDS › compañía › *Company Details › Edit Company Information* → **Method = SSO** y **Login URL** =
     la *Assertion Consumer Service URL* del IdP en Okta (es la URL de SSO del cliente; no cambia). ⚠️
     **En EU, a esa URL se le agrega un sufijo fijo `/home/oidc_client/…`** que está en la página EU —
     **es la única diferencia entre US y EU**.
   - MAC › *Customers Table* → cliente → **`uds_invite_type`: `invitation` → `sso`**.
5. **Usuarios no activos:** si en UDS hay usuarios que no figuran *Active* (*staged* o *activating*), el
   PM pide en **#product_support** que los pasen a activos; si no, **no van a poder entrar a PIP**.
6. Volver al Platform Setup: mail de prueba al cliente (paso 3 del flujo).

🔍 **El Group ID de Okta aparece tres veces en el SSO** (IdP Username, routing rule) además de en MAC
(`uds_company_id`): es el hilo que une al cliente entre Okta, MAC y UDS. Un Group ID equivocado en
cualquiera de los tres lugares rompe el login sin un error obvio.

---

## Columnas con nombre reservado (carga directa a LEB)

> ✅ Confluence *Reserved Column Names in Direct LEB Data Loads*, exportada 06/10/2026. Seguimiento de
> engineering: **SPT-721**.

**Regla:** si un archivo se carga **directo en LEB** (*Invite › Bring your own list*, típicamente un
archivo del cliente tal cual) y algún encabezado es una **palabra reservada de MySQL 8.0**, la carga falla
con un error poco claro o queda mal. **Arreglo:** renombrar la columna agregando guion bajo
(`group` → `group_`) y volver a cargar. No distingue mayúsculas.

- **Por el camino normal no pasa:** el *Data Audit Script* y el *Data File Builder* de Operations Tools ya
  controlan esto antes de armar el archivo para LEB (como en el data file load del training, § Data file
  load).
- **Las que más aparecen en archivos de clientes:** `group` (la más común), `key`, `order`, `rank`,
  `lead`, `lag`, `range`, `interval`, `match`, `system`, `usage`, `partition`. La lista completa está en
  la página. Palabras como `status`, `comment`, `level` o `region` **no** son reservadas.
- Por qué: los datos terminan en `prefill_data` (MySQL 8.0) y en la carga directa el SQL generado no pone
  los nombres entre backticks.

---

## Data specs: auditoría del archivo del cliente y excepciones

> ✅ Confluence *Data Specs Process for Healthcare and Non-Healthcare* y *Data Spec Compliance Review
> Process*, exportadas 06/10/2026. Hay un video de entrenamiento (*DataAuditTemplateTraining.mov*) y un
> diagrama del flujo, no incorporados. A pesar del título, la página **no distingue** pasos distintos para
> healthcare y non-healthcare.

**Herramienta:** el **Data Specs Audit script** (`dataspecs_automation`, en los `dm_scripts` de Python del
servidor) — dice si el archivo cumple los data specs o no.

**El flujo:**

1. El cliente tiene su archivo inicial → **el PM hace una primera revisión** y pide una tarea PFS para
   correr el audit.
2. Según el resultado:
   - **El cliente corrige** → tarea *"PFS to audit data file if no updates after PM check"*, **con las
     instrucciones de carga incluidas**: Delivery Ops **carga apenas el archivo pasa el audit**.
   - **El cliente no puede corregir** (a tiempo o nunca) → pedir excepción con la tarea ***Data Spec
     Compliance Review Request***, también con instrucciones de carga: se carga apenas se aprueba.
   - **Apps self-service:** **no se carga al pasar el audit.** Se pide *"PFS Team creates Data
     Automation"* y la carga se hace como parte del armado del cron.

**Un pedido de excepción tiene que traer:** que el archivo **ya falló un audit** (de PFS o del PM) y dónde
está ese audit · si es **por única vez** o **permanente** (las de datos preliminares se aprueban casi
siempre mientras el cliente termina de corregir) · **qué ítems fallaron y por qué el cliente no puede
cumplirlos** · todo lo necesario para cargar.

**No se aceptan como excepción:**

- **xlsx / xls para automatización** (solo para una carga única).
- **Campos con el mismo nombre** para automatización (solo en cargas manuales únicas).
- **Archivos con problemas de delimitador o parseo**: hay que poder abrirlos y revisarlos.
- **Jerarquías custom** (demográficas o de managers que requieren intervención manual fuera de lo que arma
  la herramienta de data ops): tienen que estar en contrato; caso por caso.
- **Archivos encriptados sin extensión `.pgp` o `.gpg`** para automatización.

**Excepciones que se suelen aprobar** — idealmente solo para cargas preliminares o únicas, para empujar
al cliente a cumplir del todo:

- Nombre de archivo distinto de **`customerid_demographic_data_file_YYYY-MM-DD.csv`**
- xlsx para una carga única · encriptado sin `.pgp`/`.gpg` para una carga única
- **emp_ids duplicados**
- Nombres de campo con guion bajo en lugar de espacio
- Nombres de campo duplicados (carga única)
- Un campo que se llama igual que uno autogenerado (se puede renombrar, pero no puede haber dos columnas
  con el mismo nombre)
- **Pipe (`|`) en lugar de coma** como delimitador

✅ **Composición del data spec** (DOS, 2025-09): hasta **94 demográficos = 44 estándar + 10
autogenerados + 40 custom**; el SKU *Additional Demographics* lo amplía hasta 135.
📣 Según el bot Pyxee-CVO (06/10), sin fuente citada para esto: **CSV en UTF-8**, encriptación opcional con
la **clave pública GPG de Perceptyx**, envío a la **raíz del SFTP**, típicamente **nightly**; las
credenciales de SFTP las da el PM o el equipo de onboarding. Coherente con *Automation Setup – 360*
(UTF-8, `.csv`/`.txt`/`.pgp`/`.gpg`).

🔍 Lo que estas listas dicen del data spec, aunque la página del spec en sí no vino: **CSV delimitado por
comas**, nombre de archivo con customer ID y fecha, **emp_id único**, nombres de columna únicos, y
encriptación PGP/GPG si va encriptado.

---

## Trend mismatch: cargar linkages custom de trend

> ⚠️ **06/10: SOS tiene *Trend Mapping*, que según su guía *"replaces mac trend setup"*** (apps trendeadas,
> demos, opciones y mapeos custom en una herramienta). Lo de abajo es el método manual documentado; 🔍
> probablemente en retirada. Ver [[Perceptyx/services-os|services-os]].

> ✅ Confluence *Load Trend Mismatch File*, exportada 06/10/2026 (capturas de **mayo 2025**). Es la versión
> escrita de lo que Emily mostró el 01/10 al reordenar un demo con trends (§ Reordenar las opciones de un
> demográfico, paso 8). Los app IDs de los ejemplos se reemplazaron por genéricos.

**Tarea en Certinia:** *Trend - PFS Add | Edit | Delete Custom Demographic*. **Insumo:** el **Trend
Mismatch Report** (casi siempre `.xlsx`), en el campo *Attachment URL* de la tarea. Si no está, **comentar
en la tarea pidiéndoselo al PM**.

**Qué es:** cuando un demográfico cambia entre un survey y el anterior (opciones nuevas, renombradas,
fusionadas), el trend no sabe qué opción de hoy corresponde a cuál de antes. La tabla
**`trend_custom_linkages`** guarda esas equivalencias: `cond1` (condición en el app actual),
`trend_app_id` (el app anterior) y `cond2` (la condición equivalente en el app anterior).

### Cargar las linkages

1. **Si `trend_custom_linkages` no está vacía, backup.**
2. En la pestaña **Demo Option Mismatch** del reporte, pegar en **F3** la fórmula que está de referencia en
   la columna K y arrastrarla a toda la columna F:
   ```
   =IF(TRIM(E3)="","","insert into trend_custom_linkages (cond1,trend_app_id,cond2) select '"&H3&"="&VLOOKUP(G3&H3&E3,map!A:B,2,0)&"','"&I3&"','"&J3&"="&VLOOKUP(I3&J3&D3,map!A:B,2,0)&"';")
   ```
   Donde hay valores en D y E aparece un `INSERT`. Filtrar F sacando los vacíos.
3. **Si aparece `#N/A`:**
   - El valor de E **no existe en el app actual** → avisar al PM y preguntar: omitirlo o mandar un reporte
     corregido.
   - **Varios valores en una celda de E** (separados por coma o punto y coma) → duplicar la fila una vez
     por valor, dejando uno solo en cada una. Si sigue el `#N/A`, es el caso anterior.
4. Con solo `INSERT`s en F: **correrlos en la instancia read-write**.

### Chequeo obligatorio: sin duplicados de `cond1` + `trend_app_id`

El par `cond1` + `trend_app_id` **no se puede repetir** (`cond2` sí). Si se repite, **se fusionan por
`cond2` con `OR`**: `01_18_07=1` y `01_18_07=3` → una fila con `01_18_07=1 OR 01_18_07=3`.

- Para encontrar duplicados:
  ```sql
  select t1.*, t2.* from trend_custom_linkages t1
  inner join trend_custom_linkages t2 on t1.cond1 = t2.cond1 and t1.trend_app_id = t2.trend_app_id
  where t1.id <> t2.id;
  ```
- **Si son muchos, fusionarlos con una query** (temp table con `GROUP_CONCAT(DISTINCT cond2 ORDER BY cond2
  SEPARATOR ' OR ')` agrupando por `cond1, trend_app_id` → `DELETE` de esos pares → `INSERT` de los
  fusionados; la query completa está en la página). ⚠️ **Probarla primero en el *jail*** y con backup: si
  `cond2` es demasiado chica para el texto fusionado, **se pierde la tabla entera**.

### Extras

- **Con qué apps trendea un app:** MAC › *Functions › Trend Report Systems* → buscar el app ID → columna
  *Apps Included*. MAC permite **hasta 5**; más que eso, por SQL en **`mac.trend_apps`** (`trend_id` = app
  actual, `app_id` = el que se suma, `app_caption` con el mismo estilo que las otras filas).
- **Trendear al manager A contra el manager B:** en `trend_custom_linkages`, `cond1 = MGR_HIER: <emp_id
  A>`, `trend_app_id = <app anterior>`, `cond2 = MGR_HIER: <emp_id B>`; y en **`managers_tree`** del app
  actual, `trend_emp_id` de A = emp_id de B. **Contra varios managers:** emp_ids separados por coma en
  `cond2` y en `trend_emp_id`.
- **Trendear un demográfico contra la jerarquía de managers:** `cond2` lleva un bloque
  `/* MGR_HIER: X */ client_id IN (SELECT E.client_id FROM <app>.emerge E, <app>.managers_tree T WHERE
  E.emp_id = T.emp_id AND T.tree_path LIKE '%.X.%') /* END_MGR_HIER: X */`, con X = emp_id del manager y
  `<app>` = el app de trend. Plantilla exacta en la página.

---

## Standard Forms: lo que el PM tiene que entregar antes de pedir trabajo

> ✅ Confluence *Standard Forms*, exportada 06/10/2026. Los formularios (PDF) no vinieron.

El PM baja el formulario, lo completa entero y **lo sube al FTP de dmtask antes de pedir el trabajo**.
Cada formulario corresponde a una o más **categorías de tarea**:

| Formulario | Para qué | Producto | Categoría de tarea |
|---|---|---|---|
| 360 Feedback Data Import | Cargas automáticas y puntuales de 360 | Cultivate – 360 Feedback | *Automation › New CRON build › 360v2 Data Import* · *… › Automated Comment Processing* · *Participant Data › Data File Processing › 360v2 Data File Upload* |
| Self-Service Automated Data Import | Cargas automáticas de Ask self-service | Ask – Self-Service | *Automation › New CRON build › New Ask (Self-Service) CRON* |
| Lifecycle Event – Candidate | Cargas y lanzamientos para candidatos | Sense – Classic | *… › Lifecycle Event – Candidate* / *Customized Candidate* |
| Lifecycle Event – Exit | Cargas y lanzamientos para egresos | Sense – Classic | *… › Lifecycle Event – Exit* (+ variantes *Customized* y *with Major / Minor Add-On Features*) |
| Lifecycle Event – Onboard | Cargas y lanzamientos para ingresos | Sense – Classic | *… › Lifecycle Event – Onboarding* (mismas variantes) |
| Add-On Major – Email Alerts | Alertas por mail según respuestas a ítems de escala | Sense – Classic | *… › Add-On Major Feature – Email Alerts* |
| Add-On Major – Exit Launch Pad | Cargas para Exit Launch Pad | Sense – Classic | *… › Add-On Major Feature – Exit Launch Pad* |
| Add-On Major – Raw Data Extract | Extracción automática de flat file a FTP | Sense – Classic | *… › Add-On Major Feature – Raw Data Extract* |
| Add-On Minor – Data Anonymization | Borrado automático de datos personales en surveys continuos | Sense – Classic | *… › Add-On Minor Feature – Data Anonymization* |
| Add-On Minor – Demographic Update · Major – Secondary Respondent | *Coming soon* | Sense – Classic | — |

- Hay plantillas **BETA** de Exit y Onboarding y un documento de *Decision Points* (de febrero de 2026),
  no incorporados.
- Si hay dudas con el formulario o la tarea: el manager.
- 🔍 **Lifecycle** = surveys continuos disparados por un evento del empleado (candidato, ingreso, egreso),
  alimentados por un cron. Es lo que *Data Integrations* manda a Automation cuando es complejo.

> *Create Data Automation* también vino en este batch, pero **la página exportada está vacía** (solo el
> título).

---

## Carga del archivo final en un survey de LEB (walkthrough de Jackie, 23/09)

> 📣 **Jackie Cech**, video *9.23.2026 task walkthrough* (Drive de la empresa), **transcript completo**
> pasado por Ignacio el 06/10. Una tarea real de *final data file load* para un cliente EU, hecha en vivo y
> con todo lo que salió mal — Jackie: *"this is a good picture of reality"*. Cliente, PM y empleados del
> ejemplo, omitidos. Es la fuente más completa del dominio sobre **una tarea de punta a punta**, y
> coincide con lo que después documentaron Confluence y engineering.

### 1. Tomar la tarea y abrirla

(Cómo se toma de la cola: § Cola de tareas.) Clic en el **nombre de la tarea** → **marcarla *In Progress***
(*"mark as current status"*). Sirve para que el PM vea que se empezó y para medir el tiempo: el *last
modified* queda con la hora de inicio.

### 1b. Ubicar el archivo (si no está en la tarea)

> 📣 / 🔍 Tarea real del 08/10 (bitácora). No es parte del walkthrough de Jackie.

- Mirar el campo ***Attachment URL*** de la tarea: el PM pone ahí el link al archivo
  (`sftp://sftp.perceptyx.com/incoming/<cliente>/<app ID>/…`).
- Si está vacío: **DM Task** en Transmit → SFTP del cliente → `filename` en `prefill_data_all` del master
  (dice qué archivo cargó el feed) → *SOS › Cron Manager* (de dónde toma y adónde archiva).
- 🔍 **Si hay cron, el archivo no queda en el SFTP del cliente**: lo consume y lo archiva en el **SFTP de
  cronjobs**. Un SFTP del cliente sin archivos recientes es lo esperable.
- Si no aparece: estado **Info Needed** + comentario en la tarea (el 08/10 la PM lo resolvió moviéndolo
  a DM Task).
- `.pgp` / `.gpg` → *SOS › Toolbox › IT Tools › PGP/GPG File Decrypt*. No abrir y guardar el CSV en Excel
  (rompe fechas y ceros a la izquierda, y genera *weird characters*).
- **Audit del data spec antes de cargar** (no confundir con el Launch Audit): ~~🔍 *SOS › Design & Build ›
  DOC › Load File*, sin confirmar que sea el mismo audit.~~ **SUPERSEDED 26/10/2026:** ✅ es el mismo: DOC audita contra
  el **data spec v3.1** (*always latest*). Antes de *Build LEB file*: **aplicar el mapeo de las 5 columnas** y, sin
  jerarquía, dejar *No hierarchy root*. Si el audit da **FAILED**, no se carga: resumen al PM y se cierra la tarea
  (detalle y qué traen las descargas en [[Perceptyx/services-os|services-os]] § DOC).
- **Archivo con muestra** (*"load only records marked YES in column X"*, tarea del 26/10/2026): contar en Excel sin
  guardar `=COUNTIF(<col>:<col>,"Yes")` y `=COUNTIF(<col>:<col>,"No*")`; la suma tiene que dar el total. El audit corre
  sobre el **archivo completo** (lo que mandó el cliente) y el filtro se aplica al cargar en LEB (paso 4.6). 🔍 El
  filtro en LEB no se llegó a probar: el audit falló antes. Las columnas de muestra (`Q3/Q4 SAMPLED`) no son demos.
- **Antes de cargar:** confirmar el binlog de `prefill_data` (§ Sincronización con UDS). El Launch Audit
  lo avisa como *"Prefill→UDS binlog inactive"*.

### 2. Identificar el app y entrar

- El **app ID** está en la tarea. El **servidor** también: `www` (US) o `EU` (hay algunos `gov`, *"que
  se van"*).
- **App ID que empieza con `OD`** → entrar por **`ondemand.perceptyx.com`** o **`ondemand.eu.perceptyx.com`**.
- Entrar también al **master app self-service** del cliente (de ahí sale la data). ~~Credenciales: las de
  **MAC**; ⚠️ a algunos la de **EU es distinta** de la de US (al 23/09 a los nuevos no les andaba EU).~~
  **SUPERSEDED 26/10/2026 (📣 Ignacio): por *SOS › Customer Hub › Reporting*, en US y EU, sin credencial de MAC** ([[KOS/Reglas|Reglas]] § 9).

### 3. Decidir: ¿cargar por LEB o por la vía clásica?

1. En LEB, **ver el survey → *Manage settings*: los toggles de sincronización** (§ LEB). Si están grises,
   el survey ya está **activo**: no se pueden cambiar, pero **se puede cargar igual** (a veces el cliente
   agrega gente con el survey vivo).
   ✅ **Vía más rápida para el estado** (captura del 26/10/2026): el master app abre en ***My Surveys***
   (`ondemand(.eu).perceptyx.com/<master_app>/app/#/surveys`), una lista con **Name, AppID, Created By, Date
   Created y Status** (*Draft*, *Closed*…). Se busca el app ID de la tarea y se lee la columna. Ojo: el sitio de
   reportes del sub app (`…/<app_id>/?rm=dashboard`) **no** muestra LEB ni *Manage settings*.
2. **Comparar columnas** de `prefill_data` del **sub app** contra `prefill_data_all` del **master app**:
   `DESCRIBE` en las dos, pegar en Excel, `COUNTIF`. Diferencias esperables: `filename` (está en el
   master), y los campos que se agregan solos al cargar: `pyx_internal_source` (de dónde vino: import o
   HRIS), `pyx_pin`, el campo de auth code y `added_at`.
3. **Buscar dependencias de los índices actuales** con el snippet de Text Expander (*"check resp…"*). ✅
   Las queries exactas (captura de Querious, 23/09):
   ```sql
   select id, text from resp_questions;   -- los demos
   select * from surv_questions;
   select * from surv_questions_conditional;  -- branching
   select * from popup_definitions;           -- definiciones emergentes (tienen q_condition propia)
   select * from my_queries;                  -- filtros guardados por usuarios
   select * from comparison_views;
   select * from trend_custom_linkages;
   select * from users;                       -- mirar la columna view
   select * from custom_crosstab_options;
   ```
   Se corren en la **conexión de solo lectura** con la base del app (el nombre de la base es el app ID).
   Cualquier tabla con filas que mencionen IDs de demos = dependencia.
4. **La decisión:**
   - **Sin dependencias → cargar por LEB.** Es lo más limpio: reconstruye preguntas de demos, opciones e
     índices, y deja LEB, sub app y master en sincronía.
   - **Con dependencias → vía clásica.** No toca los índices existentes (no rompe branching, vistas ni
     trends), pero no actualiza el master app (no importa: todo corre del sub app) y obliga a **sumar los
     valores nuevos al final** de cada lista.
   - 🔍 Es la regla 3 y la del modelo de datos (el valor es una posición) aplicadas a una decisión real.

### 4. Cargar por LEB (con los datos del HRIS del cliente)

1. **Revert to draft** → **borra las respuestas existentes**. Normalmente son de prueba (pilotos, datos
   falsos; los comentarios en *lorem ipsum* lo delatan). **Si hay duda, preguntar al PM.**
2. **Reset invitee selection** → avisa que borra *display logic* y demos de HRIS (por eso se revisaron
   dependencias antes).
3. *Email distribution – unique links* → **"HRIS data available"**: trae los datos del **master app**. No
   distingue si llegaron por SFTP o por conector; aparece solo si hay feed con datos. (La otra opción es
   *Bring your own list* con un archivo.) → *Start import*.
4. **Elegir demográficos:** destildar PII, identificadores únicos y fechas (ahora LEB ya saca solo
   teléfono y fechas). Renombrar casi nunca hace falta.
5. **Errores:** **emp ID y email tienen que ser únicos.** Con duplicados, ver § 5.
6. **Filtrar** a quién se invita (ej. *active = true*): ⚠️ **filtrar y después *seleccionar todo***; si no,
   no deja avanzar (Ignacio: *"igual que en UKG"*).
7. *Save* → recorrer las pantallas o ***Preview listening event*** para que **sincronice** al sub app.
8. **Comparar conteos** master vs. sub app.

### 4b. Carga por *Bring your own list* con el archivo de DOC (tarea real, 27/10/2026)

> ✅ Archivo final con muestra, app EU, survey en draft y vacío (sin demos ni dependencias). Paso a paso con Ignacio,
> con capturas. Cliente omitido.

- **Archivo:** el **LEB file (XLSX)** que genera DOC (*Recent runs* › descarga), **no el original del cliente**. DOC
  rellena ceros, unifica mayúsculas y ordena las bandas.
- **Ruta:** survey › **Invite** › *Email Distribution – Unique Links* › **Bring your own list**. Es un asistente de tres
  pasos: **Upload → Data Mapping → Review**.
- **`sequence` frena la subida:** *"These column names can't be used: sequence"*. **DOC no la renombra.** Se
  renombra el encabezado a `sequence_` en el xlsx (solo esa celda) y se vuelve a subir (§ Columnas con nombre reservado).
- **Límite de demos:** *"This file has 112 demographic columns. This survey allows up to 99"*. Es un bloqueo duro, no
  un aviso. 📣 **Tim Sams (Slack del equipo, 27/10):** master app › **Configuration** › *Filter* = **`Max Number of
  Demographics - Data Import`** (bucket *Self Service*, `index.cgi?rm=configure&bucket=Self%20Service`) › subirlo por
  encima del número de columnas del archivo. Se usó 120 para 117 columnas. Vale para todo el master app. Anotar el valor
  anterior.
- **Data Mapping:** LEB destilda solo `emp_id`, `email`, `first_name` y `last_name`. El resto viene tildado. Se
  destildan identificadores y datos personales, fechas, columnas de muestra y columnas vacías (`unnamed_*`): 30 de 113
  en el caso. Eso es procedimiento, no elegir demos. Lo que es demo queda (decisión de la PM).
- **Review:** *records found / ready for import / need fixing* (duplicados de emp ID o email). → *Save changes and
  Import* carga **la lista completa**.
- **Select Invitees › Add Filters:** se filtra por cualquier demo tildado (ahí, `q4_sampled` = *Yes*) y muestra *Total
  invitees*. Después *seleccionar todo*. Coincidió con el conteo de Excel (35.464).
- ✅ **El Preview es obligatorio:** después de importar, `prefill_data`, `emerge` y `resp_questions` ya estaban, pero
  **`all_data` no tenía ninguna columna de demo**. El Q&I frena con *"ERROR! UNABLE TO PROCEED… Missing all_data
  column(s)"*. Con **Preview Listening Event** se crearon las 83 (`information_schema.columns` de 0 a 83).
- ✅ **LEB recorta el `0 ` de DOC:** después de la carga, `resp_list` tenía `0` sin espacio en 3 demos, y `prefill_data`
  también en 2 de las 3 columnas (1.398 y 4.002 filas). El Q&I lo marca. Se arregló con `UPDATE … SET <col> = '0 '
  WHERE <col> = '0'` por SOS › Database Tools (en `resp_list` y en `prefill_data`). 🔍 Previsualizar o activar puede
  deshacerlo (regla 10): se avisa al PM que corra el Launch Audit antes de lanzar.
- ✅ **Columnas del spec vacías en el archivo del cliente:** 30 demos sin opciones (`gender`, `work_country`,
  `department`…). Los datos venían en columnas propias del cliente (`gender1`, `country`, `hr_region`,
  `org_unit_name`). *Create demographic options from participant data* saca la alerta *missing a blank option*, pero
  ***does not have any options*** sigue: no hay valor que crear. Se informa al PM. Antes de arreglar, **verificar que
  los valores no estén en otra columna** (`sum(<col> <> '')`).
- 🔍 **`emerge.survey_closed` = 0 en todos después de la carga, con el survey en Draft.** El snippet *"data load"* de
  Jackie (paso 6.3) no está en el vault. Se le preguntó al PM si cerrar.

### 5. Duplicados (lo que no estaba en el guion)

- Encontrarlos (`prefill_data_all`, **conexión de solo lectura**):
  `SELECT email, COUNT(*) FROM prefill_data_all GROUP BY email HAVING COUNT(*) > 1;` y después ver los
  registros completos con `WHERE email IN (…)`. Jackie: **la IA es muy buena escribiendo SQL**, usarla.
- **Causa típica:** el HRIS del cliente **crea un registro nuevo cuando la persona cambia de rol o de
  país**. El viejo suele estar **inactivo**, con ID de otro formato y más antigüedad.
- **Arreglo:** preguntarle al PM (por Slack, para no frenar). En el caso: invitar solo a **activos**; al
  registro viejo de los que seguían duplicados, **email falso** (y también **SSO ID**), con `UPDATE` en la
  **conexión read-write** del **master app**. La herramienta de audit hace algo parecido sola, pero elige
  mal.
- ⚠️ **El feed diario del cliente pisa ese arreglo al día siguiente** (idea 2 de la síntesis). Sirve para
  esta carga, no arregla el dato: hay que decirle al PM que el cliente lo corrija en su HRIS.

### 6. Después de cargar

1. **Orden de las opciones:** `rm=24` (prefill linkage) para ver los IDs → `resp_list` → reordenar **age
   band, generation y tenure** (los demás quedan alfanuméricos) con la fórmula de Excel: `UPDATE
   resp_list SET text = '<nuevo>' WHERE seq = <seq>`. 🔍 Se reescriben los textos en las posiciones
   existentes: es seguro **antes** de que haya respuestas (acá el survey se acababa de pasar a draft); con
   respuestas, cambiaría el significado de los índices.
2. ***Operations tools › Utilities › quality and integrity checks*** — **después de cualquier cambio de
   datos.** Lo que suele marcar y qué hacer:
   - el código con **espacio** (`"0 "`) → snippet *"zero"*;
   - **países sancionados** (Irán, Cuba) en país de trabajo o de ubicación → **avisar al PM**;
   - **SSO ID duplicado** → si se sabe cuál es el viejo, corregirlo;
   - **demos sin valores** (no generan lista) → *Operations tools › Participant Data › **Create demographic
     options from participant data*** con esos demos: crea la opción vacía y deja contento al verify.
     ⚠️ ✅ **El campo *Test Mode* viene en "Yes" por defecto** (*"no updates, just see the issues"*):
     hay que cambiarlo a *No* para que haga algo (le pasó a Jackie);
   - *"requires auth code"* → lo cambia el PM después; no tocar.
   - A veces tarda en refrescar: volver a correr más tarde.
3. **Cerrar los surveys** hasta que el cliente esté listo: en *Survey launch › respondents*, verde =
   cualquiera que entre a la plataforma lo ve → snippet ***"data load"*** (actualiza `emerge` y los cierra).
4. **Árbol de managers** → § Armar un árbol de managers.

### 7. Cerrar la tarea

- **Comentarios en la tarea** con los pasos hechos y los **llamados de atención para el PM** (duplicados,
  jerarquía, verify): quedan *"for posterity"*.
- Si falta algo del cliente: estado **Info Needed** con la pregunta; Jackie prefiere **Slack al PM** para
  resolver en el momento.
- **Horas:** copiar el proyecto de la tarea → *Time entry* (Certinia) → *project* → horas → *Save*. Cada
  semana se puede **copiar la anterior** y borrar lo que sobra.

### Lo que dijo Jackie de paso

- **Ninguna escritura por SOS todavía** (Database Tools sin probar). Alternativa manual para ver o editar
  una tabla desde el app: **`rm=18&tbl=<tabla>`** (✅ `tbl`, captura del 16/09); en SQL es más rápido.
- Las descripciones de las tareas tienen demasiado texto; las limpia con los PM managers (**Bill**, el de
  las plantillas de Certinia).
- En un on-site del equipo (22/09) se habló de *start / stop / continue*; lo que más se quiere es **que
  los clientes manden datos limpios**.
- *"Classic"* = la forma vieja de armar surveys; **LEB** = la nueva, *"really intuitive"*. Estamos en la
  transición. El colector hoy es mayormente **DC Amsterdam**; **Mosaic** es el nuevo.
- Algunos toggles: *Advanced Reporting* nunca se prende (*"es donde lo queremos"*); **traducciones y
  usuarios siguen en Classic**.

---

## Late adds: sumar participantes a un survey que ya está en vivo (Elena, call del 16/10)

> 📣 **Elena Khaletskaya** (Automation Team), call de Zoom con Ignacio del **16/10/2026** (~55 min),
> resolviendo en vivo una tarea *Data – (Late) Add – Live* de un cliente enterprise (survey Ask de
> ~9.500 participantes, app EU; al final entraron **7 personas nuevas**). **Fuente:** grabación de Ignacio,
> transcripta con Whisper y cruzada con capturas del video cada 10 s. Lo que se ve en pantalla es ✅
> (captura del 16/10); lo que Elena dice o recomienda es 📣 Elena; lo que se deduce, 🔍. Cliente,
> personas y app ID: omitidos. **Vigente al 2026-10-16.** Elena aclaró que es *su* forma: *"other
> DelOps might do this differently"*.

**Qué es un late add.** El survey ya está **en vivo** (la gente lo está respondiendo) y el PM manda un
archivo con personas que faltaban. Hay que sumarlas **sin tocar a las que ya están**: no se agregan ni
borran demográficos, **solo se suman valores** (📣 *"we can only add values for live surveys"*). Es lo
contrario de la carga final de § Carga del archivo final, donde se reconstruye todo.

**La regla de la tarea: primero `prefill_data`, después `emerge`, después `managers_tree`.**
📣 Motivo de Elena: si se carga primero `emerge`, la persona puede recibir invitación o recordatorio y
entrar a la plataforma **sin demográficos conectados** → branching mal y otros efectos que no se
quieren. Con los demos ya en `prefill_data`, sumarla a `emerge` es lo que la habilita a responder.

### 1. Mirar el archivo y el app

- ✅ **Resultado del paso 1, 19/10/2026** (`select * from prefill_data limit 10;`, base EU de un late add): las
  columnas coinciden con el esquema verificado. **`emp_id` y `mgr_id` están en minúsculas** (el Data File
  Builder las pasa a minúscula, 📣 Elena). Los IDs de las listas que manda el cliente suelen venir en
  mayúsculas: **comparar siempre en minúsculas** (`lower(emp_id) in (…)` o la lista en minúsculas). Una
  búsqueda en mayúsculas no encuentra nada y hace parecer que los IDs no existen. `manager_employee_id` sí
  viene en mayúsculas: el mismo ID puede aparecer distinto en dos columnas.

- Archivo de la tarea en **Transmit** (SFTP del cliente, carpeta del app) → carpeta propia.
- `select * from prefill_data limit 10;` en el app: ver si la carga inicial vino de LEB, si hay bandas
  calculadas (edad, generación, tenure). En el caso **no había bandas** → nada que calcular, aunque el
  archivo traía fechas de nacimiento e ingreso.
- 📣 **LEB ignora las columnas vacías**: una columna del archivo que no está en `prefill_data`
  probablemente vino vacía en la carga original. No es un error.

### 2. Alinear los encabezados con `prefill_data` (Excel)

- ✅ **Dónde está el archivo** (📣 Ignacio y captura, 19/10/2026): en **Transmit**, servidor EU, carpeta de la
  empresa cliente → carpeta del app (`odtnpees26a`) → el archivo *ten addditional employees* (`.xlsx`, subido el
  15/10). La URL de la tarea (`sftp://…/incoming/…/odtnpees26a/…`) es esa misma ruta. Si el app es US, la ruta
  cambia de servidor, no de estructura.
- ✅ **Resultado del cruce, 19/10/2026** (encabezados del archivo contra las columnas de `prefill_data`, en el
  mismo orden del archivo): 61 columnas. **34 mapean** a `prefill_data`. **27 no mapean**. Entre las que no
  mapean están `SSO ID` (va a `emerge.sso_id`, no a `prefill_data`) y `Phone Number` (el nombre en `emerge` es
  `mobile_number`, no coincide).
- ✅ **`mgr_id` aparece dos veces** (columnas 5 y 11) y **tienen la misma información** (📣 Ignacio, 19/10/2026).
  Se mapea una sola: la **columna 5**, que además queda entre las primeras cinco. La otra se quita antes del
  builder, y así no hay dos columnas que pisen la misma en el import de Querious. 🔍 No verificado contra datos:
  si hay una fila donde difieran, se consulta antes de importar.
- ⚠️ **No borrar las columnas que no mapean sin revisar `emerge`.** La regla de *borrar lo que no mapea* (arriba)
  sirve para `prefill_data`. `SSO ID` no mapea ahí, pero sí es un campo de `emerge`. Antes de descartarlo se
  verifica si el Data File Builder lo lleva a `emerge.txt`.
- 🔍 `prefill_data` tiene columnas que el archivo no trae: `email_1`, `manager_employee_id` (en las filas de
  muestra repiten `email` y `mgr_id`), `auth`, `pyx_pin`, y las de sistema (`sequence`, `pyx_internal_source`,
  `added_at`). No se completan a mano; se verifica qué queda vacío después del import (paso 5).

✅ Las columnas reales del app:

```sql
SELECT column_name FROM information_schema.columns
WHERE table_name = 'prefill_data' AND table_schema = database()
ORDER BY ordinal_position;
```

En Excel (✅ captura): columna A = encabezados del archivo; B = los mismos con `_` en vez de espacios;
C = `BUSCARV` de B contra la lista de columnas de `prefill_data` → el **nombre exacto** que corresponde,
o vacío. Se pega como valores, se reemplaza la fila de encabezados del archivo y **se borran las columnas
que no mapean** (y las vacías). 📣 Elena prefiere hacerlo *antes* del Data File Builder: así el archivo
que sale se importa **uno a uno sin mapear a mano** — *"especially if you have hundreds of columns"*.
La otra vía (la que hizo primero en la call) es mapear columna por columna en el import de Querious.

✅ **Verificado 19/10/2026** (capturas del *Table Reference* de Querious, base del app EU, 📣 Ignacio):
- `prefill_data`: `sequence`, `pyx_internal_source`, `emp_id`, `email`, `first_name`, `last_name`, `auth`,
  `pyx_pin`, `mgr_id`, `full_name`, `email_1`, `manager_employee_id`, `active`, `absent`, `birth_date`,
  `original_hire_date`, `gender`, `termination_date`, `department`, `work_country`, `job_title`, …, `grade`,
  `band`, `added_at` (TIMESTAMP). **No hay columnas de banda de edad ni de tenure** (`band` es la banda de
  puesto, no un demo calculado). Esto sale del esquema, no del paso 1: el paso 1 (`select * from prefill_data
  limit 10;`, origen LEB y bandas en las filas) **sigue pendiente**.
- `emerge`: `sequence`, `survey_closed`, `survey_completed`, `create_date`, `sent_date`, `first_response_date`,
  `last_response_date`, `client_id`, `emp_id`, `middle_init`, `auth`, `first_name`, `last_name`, `theme`,
  `email`, `mobile_number`, `sso_id`, `pyx_pin`.
- 🔍 El orden de columnas de la **tabla** no es el orden que pide el **archivo**: en `prefill_data` la primera
  es `sequence`, no `emp_id`. Por eso la exigencia de que las primeras cinco columnas del archivo sean
  `emp_id, first_name, last_name, email, mgr_id` **no sale de la tabla** y queda abierta (ver *Pendientes*).

~~Lo que el Data File Builder necesita en las primeras columnas: **first name, last name, email, manager
ID** (📣).~~ Corregido el 16/10, releyendo la transcripción: Elena dijo que el archivo *"does have first name, last name,
email, and manager ID as first four columns… five columns"*. ✅ En la captura de Excel las primeras cinco eran
**`emp_id`, `first_name`, `last_name`, `email`, `mgr_id`**. 📣 Lo nombró como la razón de que el builder tomara el
archivo, pero 🔍 no está claro si el builder **exige** ese orden o si alcanza con que estén las columnas.

### 3. Antes de cargar: ¿ya están? (el paso que se olvidó en la call)

📣 *"Oh come on, we should have checked this first. Now we have duplicates."* Los clientes reenvían gente
que ya estaba: en el caso, de los ~20 emp IDs consultados **13 ya estaban** invitados, sin cambios en la
jerarquía.

```sql
select * from prefill_data where emp_id in ("…", "…");
select * from emerge       where emp_id in ("…", "…");
```

- La lista del `IN` se arma con buscar/reemplazar por regex sobre la columna pegada: `^(.*)\n` →
  `"\1",` (✅ el patrón está en la barra de búsqueda de Querious).
- 📣 **Chequear también por email**: a veces emp ID y email no coinciden.
- Los que ya están se **sacan del archivo**. Si ya se importaron, se borran de `prefill_data` por
  `sequence` (los del import tienen `sequence` mayor al último que había).
- ✅ **Decidir por ID, no en bloque** (📣 Ignacio, 19/10/2026: *"hay que verificarlo"*). Cada ID de la lista
  del cliente cae en uno de cuatro casos, según lo que devuelvan las dos consultas:

  | Dónde está el ID | Qué hacer | Por qué | Certeza |
  |---|---|---|---|
  | En `prefill_data` **y** en `emerge` | Sacarlo del archivo. No se toca | Ya está cargado y puede responder | ✅ (procedimiento) |
  | Solo en `prefill_data` | **No** volver a importarlo a `prefill_data` (duplicaría la fila). Consultar a Ignacio cómo sumarlo solo a `emerge` | `prefill_data` acepta duplicados sin avisar | 🔍 el caso no está escrito |
  | Solo en `emerge` | No tocar nada. Consultar a Ignacio antes de decidir | Inconsistencia entre tablas; no hay procedimiento escrito | 🔍 |
  | En ninguna | Entra normal por el archivo | Caso de late add | ✅ |

  🔍 Sacar a todos los IDs del archivo sin correr esto deja afuera a los de la fila 2 sin invitación.
  ✅ **Resultado en un ticket real, 20/10/2026:** los 13 IDs que el cliente marcó como existentes estaban en las
  dos tablas. En 4 de 13, `survey_completed = 0` (invitados, sin responder). Nombre y email aparecían en blanco
  al compartir el resultado porque se **borraron a propósito** (datos personales fuera del chat, 📣 Ignacio,
  20/10/2026). No es un dato faltante. Para compartir resultados: contar, no copiar filas.
  ⚠️ **El chequeo de "ya están" cubre todas las filas que quedan en el archivo, no solo la lista del cliente.**
  En ese caso, la addenda listaba 13 y el archivo traía además 10 nuevos. Los 13 de la addenda se confirmaron
  en las tablas; los 10 nuevos se chequean igual, por ID y por email, antes de importar.
  ✅ **Conteo final de ese caso, 20/10/2026:** el nombre del archivo decía 10 y traía 21 filas. Los 13 de la
  addenda coincidieron 1 a 1 en `prefill_data` y `emerge` y salieron del archivo. Quedan 8 filas (21 − 13).
  Por email, 0 coincidencias. 🔍 Pendiente el chequeo por ID de esas 8 antes del paso 4. **El nombre del archivo
  no sirve para contar las filas a cargar:** se cuenta sobre el contenido.
- 🔍 `emerge` rechazaría el duplicado con error; **`prefill_data` lo acepta sin avisar** (📣) — por eso
  el chequeo va antes.

### 4. Data File Builder (*Operations tools › Participant Data*)

✅ Opciones del diálogo (captura del 16/10) y lo que eligió Elena para un late add:

| Campo | Opciones | Late add |
|---|---|---|
| *Process Data* | *Export Files (for LEB)* · *Export Files* · *Direct Import (drops existing participants)* | **Export Files** |
| *Data Source* | *File* … | *File* |
| *Application Type* | *Ask* … | el del app (*Ask* en el caso, *"normal point-in-time survey"*) |
| *CEO emp id* | — | vacío |
| *Hard Reset Data Tables* | *No* · *Reset all* · *Reset demographic options only* | **No** — 📣 *"we don't want to reset a live survey"* |
| *First row contains* | *Column headers* … | *Column headers* |

⚠️ **Nunca *Direct Import* en un late add**: 📣 *"overrides the current participants and deletes them and
replaces them with the file you load"*. Si se vuelve a correr, **refrescar la página** antes: si no, no
toma el archivo nuevo.

Devuelve cuatro archivos (✅): `<app>_AUDIT.txt`, `<app>_prefill_data.txt`, `<app>_emerge.txt`,
`<app>_resp.html`.

- **AUDIT** — 📣 *"usually audit is needed only to check that all emails are valid"*: emails en blanco,
  inválidos, duplicados; nombres en blanco (los reemplaza por `FIRST_NAME` / `LAST_NAME`). Las
  diferencias de mayúsculas en opciones de demo **ya las unificó** el builder.
- 📣 **El builder pasa los emp IDs (y los manager IDs) a minúscula.** Para SQL da igual; importa para el
  código **Perl** y para que la jerarquía sea consistente.

✅ **Lo que mostró el builder en un late add del 23/10/2026** (app EU armado en LEB):
- **Exige los cinco primeros encabezados con nombre exacto y en orden:** `emp_id`, `first_name`, `last_name`, `email`,
  `mgr_id`. Con `First Name` frena con *"Invalid Required Columns… add them in anyway and you can keep them blank"*.
  Resuelve el 🔍 del paso 2: no alcanza con que estén las columnas.
- **Del sexto encabezado en adelante los copia tal cual.** No los renombra ni los valida: se alinean antes (paso 2).
- **Agrega una columna `emp_id_1`** (copia de `emp_id`) antes de las `pyx_*`. `prefill_data` no la tiene: en el import
  queda en *Unused File Columns*.
- **Nombres de salida:** `<app>_prefill.data` (no `_prefill_data.txt`), `<app>_emerge.txt`, `<app>_AUDIT.txt`,
  `<app>_resp.html`.
- **`emerge.txt` sale sin encabezado y con cuatro columnas** (`emp_id`, nombre, apellido, email): sin `sso_id`.
- **No calcula las `pyx_*`** que LEB puso en la carga inicial (región, tenure, banda de tenure en el puesto). Si
  `prefill_data` las tiene, se derivan de las filas ya cargadas y se agregan al archivo antes del builder (bitácora
  23/10). Una columna que es NULL en toda la tabla se saca del archivo: 🔍 vacía podría entrar como texto vacío.
- 🔍 **No abrir la salida en Excel para editarla:** puede volver a cambiar fechas y el `0 ` con espacio. Si hay que
  tocar los encabezados, se hace en un editor de texto.

### 5. Cargar `prefill_data` (import de Querious)

- 📣 Renombrar `_prefill_data` a `.txt` → Querious, **conexión RW** del servidor (EU en el caso) → *File ›
  Import* → base = **app ID** (✅ la lista no filtra: hay que buscarla a ojo, *"the most annoying
  thing"*) → tabla `prefill_data` → mapeo de columnas (si se alinearon en el paso 2, coincide solo) →
  *Next*. **Agrega** filas; no reemplaza.
- 📣 Cuidado con el mapeo automático cuando no se alinearon columnas: en el caso asignó una columna
  custom a `auth` y un manager ID a `email_1`.
- Verificar los registros nuevos. 📣 *"Interesting that added at also gets populated from Querious — it
  hasn't been the case previously."*
- 🔍 En el caso había columnas `email_1` y `manager_employee_id` que repetían `email` y `mgr_id`; Elena
  las completó por consistencia, sin saber si se usan.
- ✅ **`auth` queda NULL y está bien (23/10/2026):** el import no lo trae y no se completa. Dos altas anteriores con
  `auth` NULL en `prefill_data` respondieron el survey: la entrada se resuelve por `emerge` (bitácora 23/10).
- ✅ **Formato del import (23/10/2026):** *Import as* = **Tab**, *Destination* = base + tabla, y tiene que aparecer
  la pantalla de **Column Mapping**. Si Querious toma el `.txt` como **SQL**, devuelve *"error in your SQL syntax… at
  line 1"* sobre la línea de encabezados, y no escribe nada. Con *Stop if error occurs* activo, un error corta el import.
- ✅ **Permiso:** el import necesita `INSERT` en la conexión RW del servidor del app. El 23/10 dio `INSERT command
  denied` en EU: sin esa escritura no hay otra vía documentada para sumar filas a `prefill_data` (*Direct Import* del
  builder borra a todos). ~~Se pide a Jackie o a un DM con escritura.~~ ✅ **Vía que funcionó el mismo día: SOS ›
  Database Tools › Insert** con un `INSERT … VALUES` (columnas vacías omitidas → NULL), *Preview change* y confirmar.
  SOS respalda las filas que toca. Detalle en [[Perceptyx/services-os|services-os]] § Database Tools.

✅ **Late add del 26/10/2026** (app EU de LEB, 4 personas). Lo que agregó:
- **Comparar formatos de valor, no solo encabezados.** El archivo traía `Active` como `1` / `0`, y la base guarda
  *true* / *false*. El builder lo dejó pasar y el Q&I lo marcó como *Can't find a resp_list entry '1'*. Se corrigió en
  `prefill_data` con un `UPDATE` (`CASE WHEN TRIM(active)='1' THEN 'true' ELSE 'false' END`), **no** sumando opciones a
  `resp_list`. Antes de cargar: `select <col>, count(*) from prefill_data group by 1` en las columnas tipo sí/no.
- **Excel rompe valores sin avisar:** fechas → número de serie (`44620`), y `+4` → `4` (en esa base, `role_tenure_band` =
  `+4` cuando `years_in_role` está vacío). Las fechas van a `AAAA-MM-DD` antes del builder.
- **El `INSERT` armado con fórmulas de Excel falló:** sin paréntesis ni comillas, los vacíos se perdieron y las columnas
  se corrieron. *Preview change* mostró **25 filas para 4 registros**. No se confirmó y no se escribió nada. Funcionó
  armando la sentencia desde el `_prefill.data` **pegado como texto** (vacíos → `NULL`, apóstrofos escapados).
  **Regla: si el *Preview* no muestra exactamente las filas esperadas, no se confirma.**
- **Cálculo de `pyx_*` desde la base** (queries agrupadas, sin datos personales): regiones y función colapsada salen de
  una tabla de búsqueda (`work_country`, `job_function`). `pyx_tenure` sale de `original_hire_date`, y la **fecha de
  corte se deduce** de los `min`/`max` de cada banda (ahí, 18/09/2026). `pyx_role_tenure_band` sale de `years_in_role`
  (0 → <1; 1–2; 3–4; 5–8). Las `pyx` vacías en toda la tabla no se agregan.

### 6. Cargar `emerge` (*Survey Launch*)

- Si en `emerge` no hay **SSO** ni **PIN** poblados, es el caso fácil (📣 *"nothing has been said in the
  task"*). Si los hay, 🔍 habría que poblarlos (*Operations tools › Populate Survey Launch Fields* existe;
  no se usó).
- ✅ ***Populate Survey Launch Fields*** (Help, captura de Ignacio, 23/10/2026): completa campos de `emerge` desde una
  columna de `prefill_data`. Opciones: campo para **SSO ID**, para **PIN** (después hay que poner el toggle *What to ask
  on the Enter PIN page* en `pyx_pin`), para **Theme** (texto exacto de los themes de `rm=110`) y para **Email
  Language** (ids de dos letras de `rm=18&tbl=languages`). En los cuatro, *"duplicates are ignored from being updated"*.
  *Type of Update*: **Blanks Only** (solo registros vacíos) o *Clear and update all*. ⚠️ ***Survey Close Status***
  actualiza **todos** los registros de `emerge` a `survey_closed` = 1 o 0: en un late add no se toca.
  ✅ **Usado el 23/10/2026** en un late add con SSO (`emerge.sso_id` = email en todas las filas): SSO ID = `sso_id`, el
  resto en N/A, *Type of Update* = **Blanks Only**, *Survey Closed Status* en blanco. Sin *Type of Update* frena con
  *"Please select Type of Update and/or Survey Closed Status"* y no hace nada. Con eso: *"Table backed up: emerge"*,
  *"Assigning SSO ID using prefill_data.sso_id field… 3 row(s) updated"*. La carga de *Upload Respondents* ya había
  generado el `auth` en `emerge`; el `sso_id` no.
  ✅ **`emerge` tiene una columna `lang`** (idioma del email; 19 columnas en ese app, no 18 como en la lista verificada del
  paso 2). En ese app `lang` y `theme` estaban en NULL en las 17.788 filas: no hubo nada que completar. Antes de invitar se
  mira cómo está en el resto (`employee_language` × `lang`).
- ✅ **`rm=survey_launch` › subir respondents** → el `<app>_emerge.txt`. Después se ve a la gente en la
  lista de *Survey Launch*.
- ✅ **Dónde y cómo (captura de Ignacio, 23/10/2026):** *Survey Launch* tiene tres pestañas: *Email Creation*, **Survey
  Respondents** y *Launch Schedule*. En *Survey Respondents* están *Add New Respondent*, **Upload Respondents**, las búsquedas
  múltiples por email y por emp ID, y la lista (con *Auth*, *Most Recent Email Sent*, *Survey Complete*). El diálogo de
  *Upload Respondents* pide un archivo **sin encabezado**, con **exactamente 4 columnas separadas por tab** y en este orden:
  Employee ID, First Name, Last Name, Email Address (o vacío). Es justo el formato del `<app>_emerge.txt` del builder. No
  ofrece reemplazar ni enviar. 🔍 Agrega: así se vio en la call de Elena.
- ✅ **Menú *Actions* de cada fila** (captura, 23/10/2026): *Edit Name/Email*, **Send Email**, *Re-Open Survey*, *Set Survey
  Status to Available / Unavailable*, *Clear Survey*, *Assign New Auth Code and Clear Survey*, *Delete Respondent*, *Assign
  New Auth Code* (las que no aplican aparecen grisadas). Debajo de la lista hay otro botón **Actions** que actúa sobre el
  listado filtrado: 🔍 sin filtro serían todos. Para invitar a pocos late adds, *Send Email* fila por fila.
  ✅ *Send Email* pide *"Pick an Email Body version"* con las versiones del survey (*Survey Invitation*, *Survey Reminder
  1/2*, *Final reminder…*, *Final reporting invitation*). Con **Survey Invitation** y fila por fila, `emerge.sent_date`
  quedó con la hora del envío en las 3 (23/10/2026). Antes de invitar conviene mirar ***Launch Schedule › Details*** de
  los envíos pendientes (solo *Details*): muestran población (p. ej. *"Respondents that have not completed survey"* +
  filtro por país) y cuántos reciben. Un late add que entra en esa población recibe ese recordatorio también.

✅ **26/10/2026 — *Blanks Only* alcanza a todo `emerge`:** *Populate Survey Launch Fields* completó **7** SSO, los 4
nuevos y 3 altas anteriores que lo tenían vacío. El backup que crea se llama `emerge_upd_fields_<AAAAMMDD_hhmmss_…>`.
Con un `LEFT JOIN` a ese backup se ve quién cambió. Llenar un vacío desde `prefill_data` no rompe nada, pero se informa
al PM. En este app `emerge` **no tenía columna `lang`**: varía por app.

### 7. Opciones de demo nuevas y *Quality and Integrity Checks*

📣 *"When you add late adds, it could be that they have demographic values that are not part of the
survey."* → correr ***Operations tools › Utilities › Quality and Integrity Checks*** (✅ en la segunda
pasada: *Run Q&I Checks*, *Big Brother report only* = No, checks = *Data Collector / Participant Data*,
el resto en No). ✅ Lo que marcó:

| Alerta (✅ texto del xlsx) | Qué hizo Elena |
|---|---|
| *Verify prefill_data linkage — Can't find a resp_list entry 'X' associated with qid 02_NN_07* | Valores nuevos → ***Operations tools › Participant Data › Add missing demographic options from participant data***, *Test Mode = No*, **un demográfico por vez**. Agrega a `resp_list` lo que falta. 📣 Ella lo hace de una con un script por **terminal (SSH al jail)**, pero *"they don't want us to use that; they want us to get familiar with SOS"*; no supo decir cómo se hace en SOS |
| *prefill_data column `job_title` has multiple entries for 'X' (each with a different case)* | Unificar en `prefill_data`: `select distinct binary job_title, job_title, count(1) from prefill_data where job_title = "X" group by 1,2;` y un `UPDATE` a la forma que ya existía |
| *Demographic question 02_NN_07 has multiple resp_list entries for 'X'* | **No borrar** la opción duplicada de `resp_list` — 📣 *"it will destroy indexes"*: **renombrarla** para que no se use. Si ya tiene respuestas, hay que actualizar también `all_data` |
| *Demographic question 02_NN_07 has a "0" value in resp_list. Please add a space after it or change the value* | `prefill_linkage` para saber qué columna es el qid → `update prefill_data set <col> = "0 " where <col> = "0";` (📣 Perl toma `"0"` como vacío). Es el snippet *"zero"* de Jackie (§ Carga del archivo final, paso 6) |

- Después del arreglo, sincronizar a `all_data` (*Sync reporting demographics from participant data*,
  § Emails, traducciones y chequeos). ✅ En el caso quedaron **6 respondentes** con el valor viejo en
  `all_data` (`Prefill: 0 – All Data: … (Occurrences: 6)`). 🔍 Elena: probablemente respondieron
  **mientras** corría el `UPDATE` — riesgo propio de un survey vivo. Se resolvió volviendo a sincronizar.
- 📣 Esos ceros no suelen importar, **salvo que el demo se use en branching**.
- Al final del Q&I solo deben quedar, del lado de la jerarquía, **los nuevos que faltan en el árbol** (en
  el caso, 7) → paso 8.

### 8. Sumar los nuevos al `managers_tree`

1. ✅ **Backup** (§ Reglas, regla 1):
   ```sql
   CALL mac.create_backup('<app>', 'managers_tree', @results);
   SELECT @results;   -- "Backup <app>.managers_tree_AAAAMMDDhhmmss Created"
   ```
2. ✅ Quiénes faltan: `select * from prefill_data where emp_id not in (select emp_id from managers_tree);`
3. ✅ Armar el archivo completo: el árbol actual **más** los nuevos —
   `select … from managers_tree union all select emp_id, first_name, last_name, mgr_id from prefill_data
   where emp_id not in (select emp_id from managers_tree);` → Excel.
4. ✅ En Excel, `BUSCARV` del `mgr_id` contra `emp_id` → marcar *missing*. **Solo debe faltar el nodo de
   arriba** (el CEO): si falta un manager entre los nuevos, va al PM (regla 8). Al CEO, `mgr_id = 0`.
   Guardar como `managers_tree.txt`.
   ✅ **Por esta vía (*Settings › Upload Managers*), el CEO va en el archivo con `mgr_id = 0`**, como dice
   este procedimiento. 🔍 La regla de *quitar la fila del CEO y la placeholder* (§ Actualizaciones después
   del cierre, 30/09) es de **otra vía** (Data File Builder para el árbol). No se aplica acá. Si la carga
   falla, consultarlo antes de reintentar.
5. ✅ ***Reference Reports › Manager Hierarchy Tree*** (`rm=managers_tree`) **› Settings** → *CEO
   emp_id* + *Choose File* → ***Upload Managers***. Reconstruye el árbol completo.
   ✅ **El archivo va sin encabezado** (27/10/2026): con encabezado, frena con *"Orphaned employee ID: emp_id"* y no
   escribe. Columnas `emp_id, first_name, last_name, mgr_id`, separadas por tab. No incluir la fila `emp_id = 0`, que
   el sistema recrea. Control de huérfanos **con `LEFT JOIN`**, no con `lower(...) NOT IN (subquery)`, que con ~16k
   filas hace *timeout*:
   `select count(*) from managers_tree t left join managers_tree m on m.emp_id = t.mgr_id where t.emp_id <> '0' and
   t.mgr_id <> '0' and m.emp_id is null;`
6. ⚠️ **El rebuild pierde los `trend_emp_id` puestos a mano.** Antes de subir, ver si `managers_tree`
   tiene `trend_emp_id` distinto del natural; en el caso, uno. Después, restaurarlo desde el backup
   (`select * from managers_tree_<fecha> where emp_id = …` → `UPDATE`; con muchos, un `JOIN`).
   ✅ En la vista del árbol: **verde** = trend natural (mismo emp ID en el survey anterior); **amarillo**
   = trend a otro nodo.

✅ ***Build Hierarchy from Loaded Data*** (*Operations Tools › Participant Data*, botón **Download**; Help, captura de
Ignacio, 23/10/2026): *"Builds and downloads a managers tree file from prefill_data"* con `emp_id`, `first_name`,
`last_name`, `mgr_id`. Pide *CEO emp id* y la columna de manager ID. Marca vacíos, managers faltantes y referencias
circulares, y cuelga los nodos afectados de nodos *placeholder*. El archivo (`<app>_tree.txt`) se importa en
`rm=managers_tree`. 🔍 **No escribe**: arma el archivo de los pasos 3–4 de arriba desde `prefill_data` entero. La escritura
sigue siendo *Upload Managers*, con lo que implica (rebuild completo, `trend_emp_id` del paso 6).

✅ **Antes del rebuild, ver si hace falta** (late add del 23/10/2026): los 3 nuevos ya estaban en `managers_tree`, con su
manager, y en toda la base no faltaba nadie (`emp_id NOT IN (SELECT emp_id FROM managers_tree)` = 0). Se compara contra el
backup del paso 1 para saber si ya estaban antes de la carga. ✅ **Resultado:** ya estaban en el backup de las 15:52 (antes
del `INSERT` de las 17:15), con el mismo `mgr_id` y `tree_path`. 🔍 Ese árbol se cargó con la jerarquía completa del
cliente, incluida gente que no estaba en el survey: un late add puede no necesitar paso 8. Se verifica, no se asume.

✅ **26/10/2026 — late add ya en el árbol, pero con otro manager:** los 4 estaban en `managers_tree`, y uno
tenía **otro `mgr_id`** que el del archivo (el árbol se cargó con un dato viejo). Corregirlo exige el rebuild completo
con el survey vivo, así que va al PM y no se hace dentro del late add (regla 8). Para verlo:
`select emp_id, mgr_id from managers_tree where emp_id in (…)` contra el `mgr_id` del archivo.

### Cierre y hábitos de Elena

- **Validación final** que se vio: `emerge` contra `prefill_data` —
  `SELECT * FROM <app>.emerge WHERE emp_id IS NOT NULL AND emp_id NOT IN (SELECT emp_id FROM
  <app>.prefill_data WHERE emp_id IS NOT NULL);` — 🔍 aparecieron dos registros de prueba (*"probably
  some test records"*).
- 📣 **Backup cuando no estás segura**; en este caso solo respaldó `managers_tree` porque lo reconstruía:
  en las otras tablas solo **agregaba** filas. 🔍 Es más laxo que la regla 1 del training (backup de todo
  lo que se toca).
- 📣 **Guarda las queries de cada tarea en Querious** (*Saved Queries*, con el app ID en el nombre): le
  sirven de historial durante años, y se pueden exportar.
- 📣 Ofreció pasar sus snippets, queries y regex para BBEdit / Querious / Text Expander.

---

## Emails, traducciones y chequeos del app (sesión *DelOps Emails*, Jackie, 21/09)

> 📣 **Jackie Cech**, sesión del **21/09/2026** (training, día 6 de Ignacio), **transcript completo** del
> video (0:02 → 54:01) pasado por Ignacio el 06/10. Capturas (✅) de Q&I checks, Perl scripts, Sync
> reporting demographics y Launch Audit; el resto, solo transcript. Clientes
> nombrados: omitidos. Es anterior a todo lo de Emily (28/09 en adelante): Jackie hizo con **ops tools** lo
> que Emily después hizo con **scripts Perl**. **Las dos formas valen igual** (Reglas § 9) — ver § Reordenar,
> pasos 7 y 9.

### Chequeo de integridad del app — *Operations tools › Utilities › Quality and integrity checks*

Es el script **`verify_survey_integrity`** (Perl, en SOS) en versión *"mucho más amigable"*: se eligen los
chequeos con casillas en vez de escribirlos.

- Entrar: cualquier reporting site → run mode **Operations tools** → *Utilities* → *Quality and integrity
  checks* → **survey ID** → *Run*. Jackie usa siempre el botón **pop out** (la salida es chica).
- **El diálogo** (✅ captura 21/09, `rm=operations_tools`):

| Campo | Valor por defecto | Uso |
|---|---|---|
| *Select action* | **Run Q&I Checks** | 🔍 Hay otras acciones en el desplegable; no vistas |
| *Run Big Brother report only?* | No | ⚠️ No explicado en la sesión |
| *Select checks to run* | 0 seleccionados (*Select All / Deselect All*, buscador) | En apps grandes, **por partes**; antes del reporting alcanza con los del **data collector** (estructura y links), sin usuarios |
| *Include previously approved alerts?* | No | Si mostrar también las alertas **ya aprobadas** |
| *Include details?* | No | Jackie: **siempre sí** |
| *Include additional checks?* | No | Jackie: siempre sí |

- **Aprobar una alerta** = darla por buena cuando es intencional (ej. un demo que a propósito se desligó de
  prefill) para que **no vuelva a salir**. En el script Perl de SOS es la pregunta del final: *"Would you
  like to add any of the above entries as 'approved', such that they will not appear again in this
  output (yes or no)?"* (✅ captura) — la misma que Emily contestaba **no** (*add as approved = no*, §
  Reordenar). Jackie lo contó como "approve alerts"; el campo del diálogo es *include previously approved*.
- **Salida real del script** (✅ captura, survey de prueba de Jackie): líneas numeradas tipo *"Username X
  has emp_id 'Y' in their **`emp_id_view`**, however that emp_id is not a manager"* (usuarios de reporting
  restringidos a la vista de alguien que no es manager en el árbol cargado) y *"Verify emerge/prefill
  records are in managers_tree → Found 12 `prefill_data` records / 12 `emerge` records that are not in the
  `managers_tree` table"*. 🔍 `emp_id_view` = la vista de jerarquía asignada a un usuario.
- Vecinos en *Utilities* (✅ captura): *Backup Table*, *Check Bad Email Domains for Users and Participants*,
  *Clear Data*, *Healthcare Data Extract*, ***Index Demographics*** (🔍 lo que el Launch Audit V2 chequea como
  índices), *Manage Quality & Integrity Email Notifications*, *Populate Initial Dummy Translation*,
  ***Translation Export***. Cada herramienta muestra etiquetas y **para qué productos** sirve (*Ask, Sense,
  360*), con *Run* (o *Download*) y *Help*. Debajo, el bloque *Utilities: Product & Technology*.
- Lo que marca, por ejemplo:
  - demo configurado **sin link a un campo de `prefill_data`**, o **sin resp list**;
  - **usuarios** creados antes del launch que **no van a ver nada** (no llegan al mínimo de respuestas), o
    cuyo **árbol de managers no coincide** con el que hay cargado;
  - **`prefill_data` y `all_data` no coinciden** para una persona (ej. género distinto): pasa cuando se
    **reordenó la resp list y no se resincronizó `all_data`** — es el riesgo de § Reordenar.
- 🔍 *"En algún momento todos los ops tools van a pasar a SOS"* (Jackie; los había visto en el entorno de
  test).

### Resincronizar `all_data` después de reordenar — *Operations tools › Data › Sync reporting demographics from participant data*

- El sistema ordena las opciones de un demo **alfabéticamente**; en **banda de edad, antigüedad o
  generación** eso queda mal y se reordena a mano.
- Después de reordenar, esta herramienta, **por demo**, vuelve a poner en `all_data` el **índice correcto**
  según lo que dice `prefill_data`.
- **El diálogo** (✅ captura 21/09): *Select demographics to sync* (varios, *Select All*) · ***Test Mode (no
  updates, just see the issues)*** = **Yes** por defecto → primero test, después con *No* · ***If prefill is
  blank, should we blank out all_data?*** = **No** por defecto (si no, deja `all_data` como está; solo cuenta
  con Test Mode = No). Mismas opciones que el script Perl de Emily (*test primero, después live*; *blank
  prefill*). ⚠️ Emily usaba *blank prefill* = **yes**; acá el default es **no**. Qué conviene depende del
  caso: sin dato no anotado.
- Vecinos en la misma sección (✅ captura): *Add / Update Demographics*, *Add missing demographic options from
  participant data*, ***Build Hierarchy from Loaded Data*** (*Download*), *Create demographic options from
  participant data*, *Data File Builder*, *Participant Count by Demographic Report*, *Populate Survey Launch
  Fields*, ***Remove Ineligible Participants*** (borra respuestas de no elegibles / bajas; Ask), ***Remove
  Partial Responses*** (360, Ask).
- 🔍 Hace lo mismo que el script Perl `rebuild all data demo from prefill` que mostró Emily el 01/10 (§
  Reordenar, paso 7), desde la interfaz.
- ✅ **Qué muestra *Test Mode* y qué no** (20/10/2026): lista solo las discrepancias (demo, persona, valor de prefill, y
  `all_data` vacío o con otro valor). **No muestra el índice que va a escribir.** En vivo, la salida dice
  `Updated N records`: es el contador de registros recorridos, **no de cambios**. Para saber qué cambió, comparar contra
  el backup (solo lectura):

```sql
select count(*) as filas_cambiadas
from all_data a
join <backup> b on b.client_id = a.client_id
where not (a.`02_13_07` <=> b.`02_13_07`)
   or not (a.`02_17_07` <=> b.`02_17_07`);   -- agregar los demos sincronizados
```

  `<=>` compara también los NULL. Si `client_id` estuviera repetido, el join cuenta de más: revisar antes de concluir.

### Launch Audit (SOS › Launch › *Launch Audit*) — la tarea *"launch audit"*

- **Aparece como tarea** en la línea de tiempo del proyecto: verificar, **antes del launch**, que las
  **mappings** estén bien y que cada persona vaya a tener el acceso que necesita.
- Contexto: cuando alguien se agrega a un app como **survey taker** o como **usuario con acceso a
  reportes**, esa mapping se sincroniza a su registro en **UDS** (*"la plataforma"*). Antes se chequeaba
  con scripts Python y planillas; ahora está todo en el Launch Audit — *"uno de mis favoritos"*, *"el 99%
  se hace ahí"*.
- **La pantalla** (✅ captura 21/09): *Launch* en SOS tiene dos tiles, **Launch Audit** y **Survey Launch Audit
  v2**, los dos *New*. La página se llama ***Survey Launch Audit***: *"data health por cliente / survey /
  tabla; los widgets muestran conteos y (en fases siguientes) **arreglos sugeridos**"*. Arriba: cliente,
  buscador de survey (*Copy Survey ID*), **TABLE: `emerge` | `users`**, ***Start Audit***, y tres botones de
  caché: ***Clear Platform cache — survey info***, ***— all users*** y **— usuarios puntuales** (emp_id, email,
  username o UDS ID, uno por línea). *Find user* (emp_id, email, sso_id o nombre). Los widgets van en dos
  columnas, **USER / META** (*Okta Connectivity*, *Divergent Identity*…) y **MAPPINGS** (*Missing
  Mappings*, *Bad Mappings*…), cada uno con su *family* (`okta_connectivity`, `missing_mappings`).
  🔍 El texto de la página promete los arreglos *"en fases siguientes"*, pero Jackie ya los usaba: la
  página va atrás del producto.
- **Dos modos** (se elige el survey primero):
  - **`emerge`** — los **respondentes**: correrlo **antes de que salga el survey**.
  - **`users`** — los **usuarios de reporting**: correrlo **antes del launch de reportes** (cuando se mandan
    los links a quienes tienen acceso). Si todavía no se crearon usuarios, sale limpio sin significar nada.
- **No es solo un reporte: también arregla.** Avisa cuando arreglar una categoría arregla otra; se puede ir
  en orden. Categorías:

| Categoría (*family*, ✅ captura) | Qué es | Qué se hace |
|---|---|---|
| **Bad mappings** (`bad_mappings`; la tarjeta dice *"Independent — fix anytime"*) | Una mapping que está en la plataforma pero ya no existe en el app (se borró y no sincronizó) | Borrarlas |
| **Missing mappings** (`missing_mappings`) | El app dice que la persona puede responder, pero en UDS no figura | Link → lista; agregar de a uno o **add all** |
| **Okta connectivity** (`okta_connectivity`) | La persona no está en Okta | Importa solo si el cliente usa **SSO** |
| **Divergent identity** (`divergent_users`) | **La más frecuente.** El mismo email con **otro emp ID** (ej. de un survey anterior con ceros a la izquierda); dos registros de la misma persona | Muestra los dos y de dónde vino cada uno, sugiere cuál vale; se elige la **fuente de verdad** y *update all* |
| **Meta mismatches** (`different_meta_info`) | Datos que no coinciden, sin chocar con otro registro | 🔍 Corregir hacia el dato vigente |
| **SSO ID hygiene** (también `different_meta_info`) | Si hay `sso_id`, que coincida con lo del sistema | — |
| **Missing in UDS** (`missing_users`) | La persona está en los datos pero no existe en UDS | *Add* |
| **Weird characters** (`name_cleanup`) | Caracteres raros, típicamente porque el cliente **abrió el CSV en Excel** antes de mandarlo; sin limpiar, a veces no se crea la mapping o el registro en UDS | **Los limpia solo** y lista qué cambió |
| **Active-state drift** (`wrong_active_state`) | Activo en el app y todavía no en la plataforma: lag de sync | *Sync all* |

- **Cada tarjeta** (✅ capturas 21/09): contador, *"No issues · 0.00s"* (resultado y tiempo del chequeo),
  botón ***Export*** y, si hay más, *click for details*. Las de USER / META en la columna izquierda; las de
  MAPPINGS a la derecha.
- ⚠️ **Aviso visto en *SSO ID Hygiene*:** *"Prefill→UDS **binlog inactive** — MAC/prefill edits may not reach
  UDS"*. Es decir: con el binlog apagado para ese survey, **lo que se edite en MAC o en `prefill_data` no
  llega a UDS**. Conecta con [[Perceptyx/procedimientos#Sincronización con UDS (binlog): cómo decide y por qué no llega un cambio|§ Sincronización con UDS]]: antes
  de culpar al dato, mirar si el binlog está activo (*Ops Tools › Binlog Status*).
- ⚠️ **No es el "audit" de una tarea de carga** (lección del 08/10): mide lo **ya cargado** contra UDS. Corrido
  antes de cargar el archivo final, describe la población vieja: exportar como foto del "antes", no arreglar.
- **V2** (*Jackie lo vio por primera vez ese día; en construcción*): cubre **survey y reporte** a la vez, en
  cuatro áreas — **estructura, configuración, continuidad de datos y optimización** (incluye **índices**
  sobre demos para que todo corra más rápido). Chequeos vistos: **`prefill_data` vs `emerge`**, **`all_data`
  y `progress`** (`progress` guarda un **timestamp por página**: cuánto tarda cada uno en pasar el survey),
  **jerarquía de managers**, **completitud de `all_data`**.

### Emails del survey: armar y corregir

**Dónde:** *Survey Setup › View/Edit Emails, Respondents and Launch Schedules* (run mode **survey
launch**) → ***Email body*** (la primera página no sirve; Jackie no sabe por qué está).

**La pantalla** (✅ captura 21/09, `rm=survey_launch`):

- Arriba: ***Load Email From Another Survey***; pestañas ***Email Header/Footer*** | ***Email Body***.
- Por email: casilla ***Text Only***, desplegable con la plantilla (*Survey Invite 1*…) y ***Load Body From
  Another Survey*** — 🔍 traer el email de otro survey (ej. el del año anterior) es otra forma de partir de
  algo armado.
- Campos: ***Email Format*** (*Default*), ***Sender Name*** (por defecto *Perceptyx*), ***Sender Email*** (por
  defecto la casilla de soporte de Perceptyx), ***Reply-To Name / Email*** (vacíos), ***Subject*** (por
  defecto *"Take the Survey"*).
- ***Upload*** / ***Remove*** de imágenes: queda listado como **`cid: banner`** + nombre de archivo.
- Editor con barra de formato, desplegable ***Merge Fields***, ***Source*** y pantalla completa.
- En el cuerpo se ve el marcador **`[ Translated Email Links Array ]`**, el banner, y la **sintaxis real del
  translation tag**: **`[%- obj.translate_this("Texto…") %]`** (🔍 cierre inferido; es sintaxis de
  plantillas tipo *Template Toolkit* de Perl). Por eso una `"` dentro del texto cierra el string antes de
  tiempo.

- Todo survey nace con **plantillas de email** armadas. Traen **translation tags** por defecto. A veces el
  PM arma el email y pide que se le **agreguen los translation tags** (tarea `PFS: Add Translation Tags –
  OPTIONAL` de la plantilla); lo más fácil es **partir de la plantilla**.
- La plantilla trae el **array de links traducidos** (*translated email links*): se arma **solo** con los
  idiomas de *Survey Setup › **Selected Languages***. Antes había que escribir cada link a mano.
- **El texto va dentro del translation tag, entre las comillas.** El editor permite negrita, listas y
  links como un procesador de texto.
- Botón **Take survey**: link de **SSO** si el cliente usa SSO, o el link con **auth code** si no.
- ***Merge fields***: lista de **todos los campos de `prefill_data`** del cliente; *"Hola [first name]"* se
  completa solo. Casi siempre solo el nombre; a veces el área o similar.
- **Color del botón**: se cambia con el **hex** del cliente (pasa seguido).
- **Banner**: subir la imagen como archivo con **content ID `banner`** y se toma solo. Si viene con
  tamaño raro: *IT Tools › Image optimizer* de SOS.
- **Source code**: para algo fino, o para el error típico.

**El error típico (emails que arma el PM):** *"el email no sale"* — o sale y se ve mal. Casi siempre son
**comillas dobles dentro del translation tag**: el tag ya está entre comillas dobles y una comilla doble
adentro (en un link, en una cita) rompe la sintaxis. **Arreglo: pasar a comillas simples** las de adentro
(o las otras) en el código fuente.

**Email nuevo:** ***New entry*** desde un email existente crea **otra plantilla** en la lista **copiando
la actual** (formato, colores, banner). Jackie arma primero el *invite* y saca los demás de ahí.

### Probar un email

1. ***Send a test email*** (abajo de todo) → llega a uno mismo, pero **con los translation tags crudos** y
   sin merge fields: sirve para ver el banner y poco más.
2. **La prueba de verdad:** *Survey respondents* → **agregarse como respondente** (en `emerge`), con un emp
   ID propio fácil de encontrar → mandarse, ej., ***survey invite 1***. Llega el email real: merge fields
   completos, links por idioma arriba, botón que entra al survey (si es por auth code, no por SSO).
3. **Borrarse después.**

- Si los links de idioma muestran inglés salvo el botón, es que el app **todavía no tiene traducciones
  cargadas** (el botón es texto estándar ya traducido).
- 📣 Outlook no es obligatorio (Jackie lo usa por costumbre); sirve cualquier cliente de correo.

### Traducciones

**Regla: el survey y los emails tienen que estar terminados y confirmados *en inglés* antes de mandar a
traducir.** Normalmente **lo envía el PM**; DelOps lo ve por troubleshooting o QA (la plantilla tiene
`QA: Review Survey Translations`).

**1. Juntar las frases en inglés — ops tool *Translations for Data Collector (DC)*** (✅ captura 21/09:
*Operations tools*, sección ***Data Collector / Survey***; el buscador de ops tools filtra por nombre, ej.
*"trans"*). Recorre survey y emails, **calcula todas las frases en inglés** y las deja listas para enviar.

| Campo (✅) | Default |
|---|---|
| *Get translations from a previous app(s)* | ninguno (multi-selección) |
| *Get translations for email templates* | ninguno (multi-selección) |
| *Get translations from the Perceptyx core library* | **Yes** |
| *Will customer use vendors (SmartCAT or Microsoft) to complete missing translations* | **Yes** (**No** = traducción del cliente) |
| *Move previously translated text to a separate category* | **Yes** |

Y una nota fija: *"If using Vendor Translations, go to the **Translation Tool** to send text to the
appropriate vendor"* — este paso **no envía**; el envío es en el paso 2. Lo que dijo Jackie de cada opción:

- **traer traducciones de un app anterior** (textos que se repiten año a año);
- **qué emails** traducir;
- **traducciones de la *core library*** — Jackie: *"siempre; no sé por qué no lo haríamos"*;
- **proveedor: SmartCat o Microsoft** (si el cliente usa alguno de los dos);
- **traducciones del cliente**: mete todo en una tabla y se le entrega un archivo con el inglés para que
  complete;
- **separar lo ya traducido** en otro *bucket* (*"esto vino del año pasado, ya está revisado"*).
  ⚠️ **Límite: hay una sola tabla de inglés.** Si hay traducción previa para un idioma pero no para otros,
  la frase **no** va al bucket de "ya traducido": una frase está en un bucket o en el otro, no por idioma.

| Proveedor | Cómo | Tiempo | Costo |
|---|---|---|---|
| **Microsoft** | Automática | Inmediata | *"Menos de un centavo"* por tanda |
| **SmartCat** | Antes, traductores humanos; 🔍 hoy IA + **revisión humana** | **~5 días** | Más caro; mejor resultado |

**2. *Translate Survey Content*** (en *Survey Setup › Translation Functions*, o run mode **translation
tool**: `rm=translation_tool`; por idioma, `&trans_lang=<código>`, ej. `ar`, `nl`).

**La entrada** (✅ captura 21/09): seis acciones — ***Add new English text entry*** · ***Upload English content
that needs to be translated*** · ***Upload completed translations*** · ***Submit English text for translation
to the external provider*** · ***Download Review URLs*** (🔍 los links de revisión para el cliente) · ***Get
Translations from Internal Source*** (core o app anterior) — y la grilla ***Select a language to view / edit
existing translations***. Abajo, *Export* y *Help*.

**Por idioma** (✅ captura, *Translation Tool (<idioma>)*):

- Pestañas ***Client Translations*** | ***Perceptyx Core Translations***; selector de idioma; ***Lock
  translation***; ***Upload content/translations***.
- Filtro ***Show phrases that are***: 🔴 **Untranslated** · 🟡 **Submitted** · 🟢 oscuro **Translated** · 🟢
  claro **Modified**; buscador por texto; ***Submit All for Translation***; ***Refetch all SmartCAT
  translations (n)***.
- Frases agrupadas por **bucket** (ej. ***Survey Emails – Previously Translated***), con *Expand / Collapse
  All*. Columnas: **ID** + *Edit English* · **English text** · **Initial translation** · **Modified
  translation** · **Status** (*Modify translation* + punto de color).
- ✅ El inglés guardado **incluye el HTML** (ej. `<strong>NOTE:</strong> Please do not forward…`): la
  prueba visible de por qué el inglés cargado a mano tiene que coincidir **tags incluidos**.

Lo que contó Jackie:

- Lista de idiomas → al entrar en uno, las frases **por bucket**, con el inglés, la ***initial
  translation*** (la del proveedor) y la ***modified translation*** (si el cliente revisa y quiere otra
  cosa, la escribe ahí; o mueve la frase de bucket).
- **Enviada y no vuelta**: punto **amarillo**; botón ***check status*** con la fecha en que vuelve de
  SmartCat.
- **Carga a mano de inglés** (de a una o por archivo): posible, pero **el inglés tiene que coincidir
  exactamente** con lo programado, **tags de formato incluidos** — si no, la traducción no aparece. Por eso
  **siempre conviene juntar el inglés con el ops tool**, que trae solo lo programado y tal cual.
- **Subir traducciones del cliente**: por idioma o **archivo multi-idioma**, columnas **language ID ·
  English text · translated phrase**. Al cargar: ***insert new phrases*** (agrega el inglés que no esté) o
  ***skip import*** (solo completa donde el inglés coincide).
- Traer de la **core** o de un **app anterior**; enviar lo que falte **por idioma o todo**, o **por
  bucket**; muestra lo **gastado por proveedor**.

**Troubleshooting típico:** *"está la frase pero no sale traducida"* → casi siempre el **inglés cargado a
mano no coincide** con el programado.

**Caso: formato agregado en el editor** (✅ ticket del 29/10/2026, app LEB EU en vivo, DC Amsterdam; [[Perceptyx/bitacora|bitacora]]).
Síntoma: un texto sale en inglés **en todos los idiomas** aunque en el Translation Tool figure 🟢 *Translated*.

- **Cómo se enlaza** (✅): la traducción se busca por el texto **entero** que está dentro de `obj.translate_this('…')`,
  hasheado como `md5(lower(texto))` → `need_translation.english_value_md5`; las traducciones cuelgan de
  `translated_phrases.original_id` = `need_translation.sequence`. Si el texto programado cambia, aunque sea un tag, el
  hash no coincide y sale el inglés.
- **Dónde mirar lo programado:** el agradecimiento de DC Amsterdam está en `filestorage`,
  `filename = '/templates/dc/amsterdam_page_complete.html'`. `content` es BINARY: leerlo con
  `CONVERT(content USING utf8mb4)`.
- **La causa vista:** el párrafo quedó envuelto en `<p style="text-align: left">…</p>` (alineación puesta en LEB) y la
  frase traducida era el texto plano.
- **El Translation Tool no sirve para arreglarlo:** *Edit English* rechaza el atributo `style`.
- **Arreglo usado** (📣 el cliente confirmó que el agradecimiento salió traducido, 29/10): backup de `need_translation` y `translated_phrases`, después por **SOS › Database Tools › Update**:

```sql
UPDATE <app>.need_translation
SET english_value     = '<inglés exacto del tag, con sus tags>',
    english_value_md5 = '<md5(lower(ese texto)), calculado aparte>'
WHERE sequence = <sequence>;
-- verificación
SELECT CHAR_LENGTH(english_value), MD5(LOWER(english_value)) = english_value_md5 AS md5_ok
FROM <app>.need_translation WHERE sequence = <sequence>;
SELECT COUNT(*) FROM <app>.translated_phrases WHERE original_id = <sequence>;
```

- Las traducciones quedan sin el formato (en este caso, sin la alineación). La otra vía es sacar el formato en LEB, pero
  toca contenido del survey y LEB vuelve a publicar (regla 10). 🔍 Si alguien abre después *Edit English* en esa frase, la
  herramienta le pide quitar el `style`: no hay que hacerle caso.
- Snippet ✅ ***Update translation MD5*** (`;md5`): `UPDATE need_translation SET english_value_md5 =
  md5(lower(english_value)); UPDATE translated_phrases SET translated_value_md5 = md5(lower(translated_value));`
  (recalcula **toda** la tabla, sin `WHERE`).

### Lo que dijo Jackie de paso (21/09)

- **Jails:** el de producción y el **local de test** de cada uno; *"geniales cuando andan"*. **Los locales
  ya no se crean y se van a dar de baja**; el reemplazo de esa parte todavía no está. **Para practicar**:
  los surveys de prueba del master app ***LEB enablement*** (los que se armaron en el training) —
  *"mientras no haya datos de clientes, no se puede romper nada"*; el archivo de muestra tiene emails
  falsos.
- **Classic hay que aprenderlo igual**: LEB es *"una interfaz más linda"* sobre lo mismo, y buena parte del
  trabajo de DelOps es **entrar al back end a arreglar**.
- **Postman**: hoy solo para **probar la API** cuando se le configura a un cliente. Se usaba con **Boomi**
  (la ingesta de datos actual), que **se reemplaza por *Merge***. Los **bots de Teams / Slack** para
  clientes los arma **engineering**, no DelOps (se habló de traerlos, no pasó).
- **Transmit**: dos conexiones de equipo, ***DM Task*** y ***DM Task EU*** — el SFTP donde **el PM deja
  los archivos** (*"está en tal ruta, cargalo"*). Jackie pasa las credenciales (no van al vault). Además,
  los **SFTP de los clientes**, con usuario y clave en un **vault aparte de 1Password**: no siempre hacen
  falta; sirven para buscar un archivo que quedó en el SFTP del cliente.
- Al 21/09 la cohorte **no tenía** ese vault de 1Password (solo el de empleado), ni las claves de Transmit;
  Querious esperaba las **SSH keys**. Jackie quedó en gestionarlo.
- Próximo: el 22/09 **Edwin** — **SSO** y la **API de Perceptyx** (con la que el cliente baja sus
  respuestas); desde el 23/09, tareas reales (es el video del 23/09).

---

## QA de branching de un survey (sesión *QA DCT*, 02/10)

> 📣 Emily Zobel, sesión del **02/10/2026**, vía **notas rápidas de Gemini** (solo el resumen; las notas
> completas no vinieron). Es la sesión de las 10:30 que estaba pendiente de volcar.

**La tarea:** verificar que el **branching** de un survey funcione: que cada respondente vea las preguntas
que le corresponden según sus **demográficos precargados** (`prefill_data`) y sus respuestas.

- Se revisan registros de participantes de ejemplo **en modo solo lectura** para ver qué condición de
  branching le toca a cada uno.
- Se hace el **walkthrough del survey** entrando con los códigos de prueba (*"off-codes"* en Gemini; 🔍
  muy probablemente **auth codes / access codes**, el parámetro `ac` con el que se entra al survey — ver
  [[Perceptyx/dc-mosaic|dc-mosaic]] § Glosario) y se anota cada condición que **no muestra** las
  preguntas esperadas.
- **El problema que apareció:** el branching dependía de cuatro demos combinados (país, ubicación,
  subtipo y tipo de trabajo) y daban **135 combinaciones distintas** (cálculo de Ignacio). Probarlas todas a
  mano no escala; Emily frenó el walkthrough para definir con Jackie el proceso más eficiente.

🔍 **Cómo reducir las 135 (criterio general de QA, no de Perceptyx):** lo que hay que cubrir no son las
combinaciones de demos sino los **caminos distintos** del survey. Dos combinaciones que terminan mostrando
exactamente el mismo conjunto de preguntas son el mismo caso de prueba. Entonces:

1. Sacar las **reglas de branching** (qué condición muestra qué pregunta; en la base, `surv_questions_conditional`).
2. Para cada una de las 135 combinaciones, calcular **qué preguntas vería** → agrupar las combinaciones con
   el mismo resultado. Cada grupo es **una** prueba.
3. Probar **un representante por grupo**, más los **bordes**: valores vacíos o que no matchean ninguna
   regla (¿cae en el default o no ve nada?), y una combinación por cada regla que use **varios demos a la
   vez** (son las que más se rompen).

Si las reglas dependen de un solo demo cada una, el número de pruebas suele ser cercano a **la suma** de
opciones relevantes, no al producto.

**Pendientes de la sesión** (📣 Gemini):

- Emily: consultar a Jackie el proceso eficiente de QA de branching y compartir la guía; mandar la lista de
  códigos de prueba marcando las condiciones a validar.
- **Ignacio: analizar las combinaciones con IA y agruparlas** para minimizar las pruebas manuales.
  ⚠️ **Antes de pasarle datos del cliente a una IA, chequear la lista de clientes sin GPT** (Reglas § 9).
  Para agrupar alcanza con **las reglas de branching y la tabla de combinaciones**, sin nombres ni datos de
  personas.
- Todos: walkthrough con los códigos asignados, documentar y reportar lo que falle.
- ⚠️ **No consta** qué se resolvió después (proceso de Jackie, resultado del QA).

---

## Usuarios Manager / Manager Below Threshold (acceso a reportes por jerarquía con umbral)

> **Dos fuentes, una sección (merge del 08/10/2026).** El mismo día, dos sesiones documentaron esta
> tarea por separado: una **desde la tarea real 890116** (lo de arriba hasta *Pasos*) y otra **desde la
> transcripción del shadow del 24/09** (§ Lo que se vio en el shadow del 24/09, abajo). Se juntaron sin
> descartar nada. Cómo se leen juntas:
>
> - **Umbral:** coinciden — *responses* en la tarea = *Responses* / respondents; al PM solo si el pedido
>   se contradice.
> - **Superior de cada `mgrbt`:** dos vías con la misma validez ([[KOS/Reglas|Reglas]] § 9) — la fórmula
>   `TEXTSPLIT` + `XMATCH` sobre `tree_path` (verificada por Ignacio el 08/10) y el **BUSCARV en cadena**
>   de Emily. El shadow dice *"partir el `tree_path` no sirve"* porque los largos varían; la fórmula lo
>   resuelve con `TEXTSPLIT`, así que esa objeción no aplica a ella.
> - ~~**Crear los usuarios (paso 5, pendiente):** 🔍 el shadow muestra una vía que el paso 5 no tenía —
>   ***Manager Hierarchy Tree › Settings › Add Users***, con el umbral ya configurado por el PM. Es la
>   candidata más fuerte para la carga masiva que Jackie mostró; confirmar en la próxima sesión.~~
>   ✅ **Confirmado 09/10** por la call de Jackie (08/10, transcripción + capturas): es esa herramienta,
>   en dos pasadas. Ver § Cómo lo resolvió Jackie, abajo — **es la versión de referencia de esta tarea**.
> - **Backup:** el shadow agrega la tabla de contraseñas temporales y que **los backups no se borran**.
> - **`UPDATE` de status:** con `AND status = <manager>`, por los duplicados permitidos (shadow).
> - **Tercera fuente (09/10):** la call de otro DM con Andrea (§ Cómo lo resolvió otro DM, abajo). Suma
>   otro orden (conteos **antes** de *Add Users*), una tercera vía para el superior (la tabla `users` como
>   oráculo) y el paso de **SSO ID**. ⚠️ **Contradice** que *Add Users* deje los usuarios activos: ver ahí.

> Armado sobre la marcha con la primera tarea de este tipo (08/10/2026, survey de LEB, umbral 5). **En
> curso**: lo que no está marcado ✅ todavía no se vio funcionar. Sin página de Confluence conocida.

**El pedido típico:** *"create Manager users for anyone who hit threshold of 5 or more responses in their
hierarchy; Manager Below Threshold users for anyone below, with access to the next level up that has 5 or
more"*.

**Criterio del umbral — 📣 Ignacio, 08/10:** se cuenta lo que dice el ticket. Si dice ***responses***, es la
columna *Responses*, **no** *Completions*. No se reinterpreta el pedido.

**Las piezas:**

- ✅ **Statuses** ya definidos en `statuses` del app: **`mgr`** (*Manager*) y **`mgrbt`** (*Manager Below
  Threshold*), cada uno con sus `blocked_demos`. 🔍 `mgrbt` bloquea más demos que `mgr` (menos cortes para
  quien ve una jerarquía chica); la columna se vio truncada.
- ✅ **Columnas de `users`:** `username`, `lang_default`, `password`, `last_password_change`,
  `last_email_send`, `last_login_date`, `failed_login_cnt`, `emp_id`, `sso_id`, `mgr_id`, **`emp_id_view`**,
  `username_view`, `first_name`, `last_name`, `email`, `theme`, `status`, **`view`**, `view_disp`,
  `view_name`, `inactive`.
- 🔍 **Dos formas de restringir a un usuario:** por **jerarquía** (`emp_id_view` = el manager cuyo árbol
  ve) o por **demográfico** (`view` = una condición SQL sobre `all_data`, ej. `02_55_07 = '2' OR …`, con
  `view_name` como texto legible). Se vieron las dos en usuarios `mgr` existentes.
- 📣 Ignacio, 08/10: un `mgr` lleva **su propio emp_id** en la vista. 🔍 Por lo tanto un `mgrbt` lleva el del
  superior. Se verifica al final con `verify-survey-integrity` (marca `emp_id_view` que no es manager).
- ✅ Los toggles de LEB **no pisan** `users` ni `statuses` (*User Status Content*: *"coming in the future"*,
  § LEB): un usuario creado por fuera de LEB sobrevive a previsualizar o activar.

**Pasos:**

1. **Árbol cargado:** `select count(*), max(deepness) from managers_tree;` en la conexión de solo lectura.
   Si está vacío, al PM.
2. **Conteos:** *SOS › Toolbox › Perl Scripts* › **`get-mgr-counts`** (input: app ID). ✅ No muestra nada en
   la terminal: deja **`<app_id>_mgr_counts`** en *Files* (*Script output*). Su descripción: *"Does not
   create users — use **Users Upload** or **Users → Manage** with the export."* Marcado *NOT TESTED*.
   - ✅ Columnas (texto separado por tabulaciones): `Employee ID`, nombre, email, `Hierarchy Count` ·
     `Invitees` · `Responses` · `Completions`, y las mismas cuatro para `Direct Reports`.
   - 🔍 *Hierarchy* = toda la organización debajo (directos e indirectos), **sin contar al propio manager**
     (filas sin indirectos: *Hierarchy Count* = *Direct Reports Count*).
   - **Abrir en Excel** como delimitado por tabulaciones, con `Employee ID` como **texto** (ceros a la
     izquierda). En la vista de texto las celdas vacías desalinean las columnas.
3. **Clasificar:** `Hierarchy Responses` ≥ umbral → `mgr`; menor → `mgrbt`.
4. **Superior para cada `mgrbt`:** el ancestro más cercano en `tree_path` con `Hierarchy Responses` ≥
   umbral. ✅ Hecho y verificado por Ignacio el 08/10 (incluidos dos casos subidos a mano):
   - ✅ Formato de `tree_path`: `000042775.000009733` — IDs de **9 dígitos** con ceros, **arranca en el
     CEO** (sin `0.`), **termina en el propio empleado**; `deepness` = cantidad de eslabones (CEO = 1).
   - El export pierde los ceros en Excel: `=TEXT(A2,"000000000")` o importar la columna como texto.
   - Hoja `tree` con `select emp_id, tree_path from managers_tree;` (todo como texto). En la hoja de
     conteos (G = *Hierarchy Responses*):
     - `tree_path`: `=XLOOKUP(A2, tree!A:A, tree!B:B, "NO ESTÁ EN EL ÁRBOL")`
     - `status`: `=IF(G2>=5, "mgr", "mgrbt")`
     - `emp_id_view`:
       ```
       =IF(G2>=5, A2,
         LET(anc, IFERROR(DROP(TEXTSPLIT(M2, "."), , -1), ""),
             r,   XLOOKUP(anc, $A$2:$A$9999, $G$2:$G$9999, 0),
             i,   IFERROR(XMATCH(TRUE, r>=5, 0, -1), 0),
             IF(i=0, "SIN SUPERIOR ≥5", INDEX(anc, i))))
       ```
       `XMATCH(…, -1)` busca de atrás hacia adelante → el ancestro **más cercano** (*"next level up"*).
   - Chequeos: 0 *"NO ESTÁ EN EL ÁRBOL"*, 0 *"SIN SUPERIOR ≥5"* (si no, al PM), dos `mgrbt` subidos a mano.
   - Filas del export **sin email** → separarlas y al PM.
5. **Crear los usuarios:** ~~con *Users Upload* o *Users → Manage*, según la descripción del script.~~
   ~~*(Pendiente: la vía de carga masiva.)*~~ **SUPERSEDED 09/10** → se crean con ***Manager Hierarchy Tree ›
   Settings › Add Users*** (§ Cómo lo resolvió Jackie). 🔍 *Users Upload* / *Users → Manage* de la
   descripción de `get-mgr-counts` no aparecen en ningún lado: nombres viejos o de otra herramienta.
   Backup de `users` antes (regla 1). Lo que se exploró antes de saberlo — el User Editor, útil para
   revisar o tocar usuarios de a uno:
   - ✅ ***Survey Admin › User Administration › View/Edit Users*** = **User Editor** (`rm=users_editor`,
     captura 08/10). Arriba: **Add Record** (de a uno), **Actions** sobre seleccionados (*Activate /
     Deactivate Record*, *Update User Status*, *Reset Password*, *Send Email Notification*, *Delete
     Record*), buscador, ***Search by List of User Information***, *Export*, y el indicador ***Connected to
     People Insights Platform*** (🔍 los cambios van a UDS por binlog).
   - ✅ **Add New User Profile Data** — pestañas: *Personal Info* · ***Data Access: Demographic Based***
     (🔍 = `view`) · ***Data Access: Hierarchy Based*** (🔍 = `emp_id_view`) · ***Data Access: User
     Based*** (🔍 = `username_view`) · *Comparison Views*; al pie, *Summary of Access*. Obligatorios: *Profile
     Username*, *First/Last Name*, *Status*, *Employee ID*, *Theme* (Default), ***Inactive User* — viene
     tildado por defecto**. Opcionales: email, password (*Make Password Permanent*), `sso_id`.
   - 🔍 El `username` de los usuarios existentes **no es la parte local del email** (difieren en letras y
     números): no derivarlo del email sin ver el patrón en usuarios `mgr` existentes.
6. **Verificar:** *Quality and Integrity Checks* (*Include details* = sí) y *Launch Audit* en modo `users`.

### Cómo lo resolvió Jackie (call del 08/10 — la tarea 890116, de punta a punta)

> Fuente: call de Jackie con Ignacio y Andrea, 08/10 (34 min), **transcripción automática + 4 capturas**,
> pasadas por Ignacio el 09/10. Marca por defecto: 📣 Jackie, 08/10; ✅ lo que se ve en las capturas.
> Se hizo **en vivo sobre el app real de la tarea**: la tarea quedó resuelta en la call. Nombres de
> personas y del cliente: omitidos. La transcripción deforma *emp ID* (*"amp ID"*, *"MP ID"*, *"M ID"*).

1. **Backup de `users`** antes de agregar nada: `CREATE TABLE users_<fecha> LIKE users;` +
   `INSERT INTO users_<fecha> SELECT * FROM users;` — *"si necesito revertir lo que agregué, es más
   fácil"*. Mirar de paso qué usuarios hay y con qué status (en el caso: HR, admin y un solo manager de
   prueba del PM).
   - Jackie lo quiso hacer en **SOS › Database Tools** y no se pudo: ***"Only select queries are permitted
     in this interface"***; ella tiene un acceso especial de prueba (*"US insert"*, lo que viene). El
     snippet de Text Expander del backup **todavía no funciona en SOS**. Se hizo en **Querious**.
2. **Crear los Manager** — ✅ app › ***Manager Hierarchy Tree*** (`rm=managers_tree`; pestañas *Hierarchy
   Tree* · *Settings* · *Activity Log*) › ***Settings*** (campo *CEO emp_id*, *Choose File*, botón **Add
   Users**) › **Add Users**:
   | Campo | Valor |
   |---|---|
   | *Which Population?* | **All Managers Who Met Threshold** |
   | *User Status* | **Manager** |
   | *Username Format* | *Employee ID* o **First Letter of First Name + Last Name** |
   | *Based on Completed or Respondents* | lo que diga el pedido (**Respondents** en la 890116) |

   - ✅ **Dónde está en el menú** (captura del 09/10): reporting site (*Advanced Reporting*), menú izquierdo
     ***Reference Reports › Manager Hierarchy Tree***. No está en *Functions › Survey Setup*.
   - ⚠️ ✅ **El diálogo arranca con *Based on…* = *Completed*** (captura del 09/10; los otros tres campos
     vacíos). El pedido suele decir *responses* = **Respondents**: hay que **cambiarlo a mano**. Si se deja
     el default, la población que llega al umbral sale mal **sin ningún aviso**.
   - **Username:** *"siempre inicial + apellido, salvo que digan otra cosa"*. La herramienta **resuelve los
     repetidos sola** (`…williams`, `…williams1`).
   - **Respondents vs. Completions:** *"lo tienen que especificar siempre: 10 respondieron, 3 no apretaron
     submit → 7 completions"*. Confirma la regla de Ignacio de arriba.
   - **Ya existentes:** avisa cuántos hay y deja elegir **no duplicarlos** — sirve para volver a correrla si
     el PM agrega gente después.
   - Resultado del caso: **1.235 creados**, 11 sin email (*"está bien"*). Cada uno con **su propia vista
     de jerarquía** (`emp_id_view` = su emp_id, `view_disp` = su nombre).
3. **Crear los Below Threshold** — la misma pantalla: *All Managers Who **Did Not** Meet Threshold* ·
   status ***Manager Below Threshold*** · mismo formato y base. ⚠️ **Los crea con su propia vista**: falta
   apuntarlos al superior (pasos 4–6). Caso: **868**.
4. **Conteos:** `get-mgr-counts` (§ Parte 2.1). Excel: *importar desde texto* → **delimitado, UTF-8**
   (*"si no, pone caracteres raros"*), tabulación → **todo como Texto**. Solo importa ***Hierarchy
   Responses***; se pasa a número con `NUMBERVALUE` para poder filtrar ≥ 5 / < 5.
   - **Chequeo de Jackie:** los ≥ 5 del archivo = los creados en el paso 2 (1.235) y los < 5 = los del
     paso 3 (868).
   - *Manager of managers* (cuando el PM pide un status distinto para ellos): *Hierarchy Responses −
     Direct Reports Responses* (o lo mismo con *Invitees*) dice si alguien tiene managers abajo.
5. **El superior que llega a 5:** `emp_id` + `mgr_id` de **`managers_tree`** (todo), pegado **como texto**
   (ceros a la izquierda), texto en columnas, **se borra la fila del `0`**. **`INDEX` + `MATCH` en
   cadena**: jefe → respuestas del jefe → si < 5, jefe del jefe → … hasta que todos lleguen (en el caso,
   al segundo nivel ya estaban todos). *"Probablemente haya una forma más inteligente con IA; si la ven,
   me interesa."*
   - ⚠️ **SOS › Database Tools devuelve como máximo 10.000 filas** (`managers_tree` tenía ~12.000 y avisa
     *"query likely to be slow"* sin `WHERE`): para traer la tabla entera, Querious.
   - **Otra vía, la misma validez** (Reglas § 9): la fórmula de una sola celda sobre `tree_path` de los
     pasos 3–4 de arriba (`TEXTSPLIT` + `XMATCH`), verificada por Ignacio el 08/10. Responde la invitación
     de Jackie; no se la mostró todavía.
6. **`view_disp`** = nombre y apellido del superior elegido (concatenar y buscar). *"`view_name` no
   importa; **`view_disp` es lo que el usuario ve al entrar**: de quién son los resultados que mira."*
7. **Actualizar** — dos maneras según la cantidad:
   - **Pocos:** un `UPDATE` por fila generado en Excel (el *helper* de Emily —
     [[Perceptyx/plataforma|plataforma]]), con `… AND status = 'mgrbt'`.
   - **Muchos (868):** planilla con **solo** `emp_id`, `emp_id_view`, `view_disp`, **valores pegados** →
     CSV → Querious › *File › Import* sobre la base del app → **tabla nueva** (todo `VARCHAR`), ej.
     `mgrbtupdates` → **índice en `emp_id`** (snippet de Text Expander) → ✅
     ```sql
     update users u join mgrbtupdates m on m.emp_id = u.emp_id
     set u.emp_id_view = m.emp_id_view, u.view_disp = m.view_disp
     where m.emp_id = u.emp_id and status = 'mgrbt';
     ```
     El `status = 'mgrbt'` es por si alguno tiene **otra cuenta** (admin, HR): esa no se toca. Filas
     afectadas = las esperadas (868). *"Esto va a estar en SOS: elegir el archivo y cargarlo."*
8. **Verificar:** *Operations Tools › **Quality and Integrity Checks*** solo con el check ***Users*** (✅
   captura). Avisos **normales**, que no se tocan:
   - **emails en blanco**;
   - ***"solo ven 6 o 7 preguntas"***: preguntas que menos de 5 de su gente contestó. Solo importa si el
     PM fija un mínimo (*"si ven menos de una o dos…"*);
   - **status con acceso total que no es admin** (HR): sale siempre.

- 📣 Ignacio, 09/10: los usuarios que crea *Add Users* **quedan activos** (a diferencia del alta manual del
  User Editor, que viene con *Inactive User* tildado). ⚠️ **En tensión** con el DM de la call del 09/10
  (*"they're always created inactive"*, con un check a la vista) — § Cómo lo resolvió otro DM › Activos o
  inactivos. Sin resolver.
- **Envío de accesos** (*Send User Accounts*): 📣 Ignacio, 09/10, como supuesto — **lo hace el PM, no
  DelOps**. 🔍 hasta que alguien del equipo lo confirme.

### Cómo lo resolvió otro DM (call del 09/10 — misma tarea, otro orden)

> Fuente: call de un **DM** (sin nombre en la transcripción) con una trainee — 🔍 **Andrea**, que dice haber
> estado *"ayer"* en la call de Jackie con Ignacio, de donde sale también la fecha 🔍 **09/10**.
> **Transcripción automática + 2 capturas** de la pantalla compartida (reloj: **vie 9 oct, 13:05** → ✅
> fecha 09/10), pasadas por Ignacio el 09/10; Ignacio no estaba. Marca por
> defecto: 📣 el DM, 09/10. Deforma *get-mgr-counts* (*"get pearl get manager accounts"*), *inactive*
> (*"in action"*), *emp ID* (*"M ID"*, *"NID"*) y *SSO* (*"SSL"*). Nombres de empleados: omitidos.
> Pedido: dos statuses, *Manager* y *Manager Threshold Not Met*, umbral 5 por respuestas, con SSO ID e
> inactivos. Resultado: **1.102** Manager y **758** below threshold; Q&I sin alertas.

1. **Conteos primero.** `get-mgr-counts` (SOS › Perl) con el app ID. *"Corrémoslo mientras hacemos lo
   demás"*: el script tarda.
2. **Backup mientras corre:** `users` **y la tabla de contraseñas temporales** (como el shadow del 24/09;
   Jackie solo hizo `users`).
3. **Arreglar el archivo:** caracteres raros y columnas corridas (el email caía en otra columna) — el
   mismo problema que Jackie evita importando en **UTF-8**. Filtrar *Hierarchy Responses* < 5 para tener
   **el número esperado** de cada pasada.
   - **Por qué en este orden** (lo dijo el DM, la trainee lo resumió): *"así, cuando creás los managers,
     sabés si el número coincide — no te tenés que acordar después"*. Jackie hizo lo contrario: creó y
     después contó (§ arriba, paso 4). **Las dos valen** (Reglas § 9); el chequeo es el mismo.
4. **Add Users, pasada 1:** *All Managers Who Met Threshold* · status *Manager* · username inicial +
   apellido · *Respondents*.
   - **Formato de username sin especificar en el pedido:** *"no nos dieron el formato, pero siempre es…"*
     — **se mira cómo están armados los managers que ya existen y se copia eso**. Coincide con el default
     de Jackie (inicial + apellido).
   - Chequeo: **1.102 = lo que dice el archivo.**
5. **Add Users, pasada 2:** *All Managers Who Did Not Meet Threshold* · status *Manager Threshold Not Met*
   (el nombre del status cambia por cliente, como ya se sabía) · mismo formato y base. Avisa de los que ya
   existen (los recién creados). **758 = el número del archivo.**
6. **El superior — tercera vía, la tabla `users` como oráculo.** En vez de buscar las respuestas del jefe
   en el archivo de conteos, se pregunta **si el jefe ya tiene cuenta *Manager***: como la pasada 1 creó
   *Manager* solo para los que llegan al umbral, tener esa cuenta **es** llegar.
   ```sql
   select * from users
   where emp_id in (<los mgr_id de los below threshold, sin duplicados>)
     and status = '<status de Manager>';
   ```
   - En el caso: **416** jefes distintos (la lista tenía muchos repetidos: varios de abajo comparten jefe),
     **374** encontrados como *Manager* → 🔍 **42** cuyo jefe también está por debajo: van al segundo
     nivel.
   - Excel: BUSCARV desde los below threshold contra ese resultado → **nuevo `view_disp`** = el `view_disp`
     del jefe; **nuevo `emp_id_view`** = el `mgr_id` (*"para un Manager, emp ID y vista son el mismo"*).
     Los `#N/A` son los que no resuelven en este nivel. Duplicados, con formato condicional.
   - **Segundo nivel:** `tree_path` de `managers_tree` para los que quedaron, y una fórmula para sacar el
     ancestro siguiente. El DM se la pidió a ChatGPT (*"el tercer número de la secuencia"*) y la primera
     **contaba desde el lado equivocado**: el `tree_path` arranca en el CEO, así que el *"next level up"*
     se cuenta **desde el final**. La fórmula `TEXTSPLIT` + `XMATCH(…, -1)` de arriba (paso 4 de *Pasos*)
     ya lo resuelve así y no necesita IA. ⚠️ Antes de pegarle datos de un cliente a una IA, la lista de
     clientes sin GPT (Reglas § 9).
   - 🔍 Lo que esta vía no cubre sola: un jefe con *Manager* que no está en el árbol, o una cuenta *Manager*
     creada a mano que no llega al umbral. En el caso, ningún aviso.
7. **Actualizar:** `UPDATE` por fila generado en Excel (`set view_disp = …, emp_id_view = …`), esta vez
   **con `where username = …`** (🔍 el username es único por cuenta, así que no toca la otra cuenta de la
   misma persona: cumple el papel del `AND status`).
   - ⚠️ **Un apellido con apóstrofo** (tipo *O'Brien*) **rompió la sentencia**: con el valor entre
     comillas simples, el apóstrofo la cierra. Arreglo: valores **entre comillas dobles**, o duplicar el
     apóstrofo (`O''Brien`). Se suma a las **comas** del shadow. Pasa con la fórmula del helper y con
     cualquier `UPDATE` armado en Excel.
8. **SSO ID = email**, para todas las cuentas nuevas juntas, después de las dos pasadas:
   ```sql
   update users set sso_id = email where status in ('<Manager>', '<Manager Threshold Not Met>');
   ```
   - **No está en la versión de Jackie** (su pedido no lo traía). **El valor depende del pedido:** el
     checklist del shadow del 24/09 pedía **SSO ID = emp_id**; este, **email**. Se lee en el pedido, no se
     asume.
   - Hubo filas **sin email**: el `sso_id` les queda vacío. 🔍 Mismo destino que las 11 sin email de Jackie.
   - Que la misma persona tenga **otra cuenta** con otro status (y quizás el mismo `sso_id`) es normal: se
     permiten varias cuentas por persona. No se toca.
9. **Verificar:** *Quality and Integrity Checks*. *"Es cómo chequeo esta parte: si hay problemas con eso,
   aparecen ahí."* **Sin alertas** → se cierra.

#### Activos o inactivos — tensión abierta

- La trainee: el PM pidió los usuarios **inactivos**. El DM: *"siempre se crean inactivos"*, con un **check**
  a la vista (🔍 en *Add Users* o en el usuario creado), *"no hay que hacer nada más"*.
- 📣 Ignacio, 09/10 (§ arriba): los que crea *Add Users* **quedan activos**.
- ✅ **El diálogo *Add Users* no tiene campo de activo/inactivo** (captura del 09/10, a las 13:05: solo
  *Which Population?*, *User Status*, *Username Format* y *Based on Completed or Respondents*). El check que
  vio el DM **no estaba en ese diálogo**. 🔍 Eso le suma peso a la lectura (c): podría ser *Inactive User*
  en el **User Editor**, que viene tildado por defecto (§ Pasos, paso 5). Pero que se tilde ahí al crear a
  mano no dice nada de lo que hace *Add Users*.
- Las dos no pueden ser ciertas para la misma herramienta y la misma versión. 🔍 Lecturas: (a) la
  herramienta cambió; (b) depende del app o de un setting; (c) el check que vio el DM era otro. **Sin
  resolver: se verifica en el app, no se elige.** En la próxima tarea de este tipo, después de las pasadas:
  ```sql
  select status, inactive, count(*) from users
  where status in ('<Manager>', '<Below Threshold>') group by status, inactive;
  ```
  Si el pedido dice inactivos y salen activos: `update users set inactive = 1 where status in (…)`. 🔍 el
  valor exacto de la columna `inactive` (1 / 0) no se vio.
- ✅ **Medido el 29/10/2026** (tarea 827284, § Cómo se resolvió el 29–30/10, abajo): las dos pasadas de *Add
  Users* dejaron las 3.720 cuentas con **`inactive = 1`**. Le da la razón al DM del 09/10, **para ese app y esa
  versión**. 🔍 Lo del 09/10 de Ignacio queda sin explicar (¿otro app, otra versión?). La query de arriba se sigue
  corriendo en cada tarea: es barata y el pedido manda.

### Cómo se resolvió el 29–30/10 (tarea 827284 — status con nombre propio, SSO = emp_id, sin `get-mgr-counts`)

> Fuente: tarea real trabajada paso a paso por Ignacio con Claude, 29–30/10/2026 (survey LEB EU cerrado, ~24.000
> personas, árbol de 3.720 managers y 11 niveles). Marca por defecto ✅ (visto en pantalla o en la base). Cliente y
> personas omitidos. Registro en [[Perceptyx/bitacora|bitacora]].

Pedido: dos status con **nombre propio del cliente** (*Leader* = `mgr`, *Leader below threshold* = `mgr_below_min_n`, no
`mgrbt`), umbral 5 **por responses**, *below* con acceso al nivel de arriba, **duplicados conservados** (quien ya tenía
cuenta HR/exec suma la de manager), **SSO ID = emp_id**, e integridad: **informar** (no borrar) a quien ve menos de 10
preguntas.

Lo nuevo respecto de las versiones de arriba:

1. ***Settings* tiene dos herramientas en la misma pantalla.** *CEO emp_id* + *Choose File* + **Upload Managers**
   reconstruye el árbol (§ Late adds, paso 8). El botón **Add Users**, debajo, es aparte y **no pide CEO ni archivo**.
   El diseño invita a confundirlas (le pasó a Ignacio). La pantalla existe en EU: `ondemand.eu.perceptyx.com/<app>/index.cgi?rm=managers_tree`.
2. **El aviso *Conflict detected* de *Add Users* cuenta por `emp_id_view`**: *"N manager accounts appear to already
   exist, based on the emp_id_view. Skip or Create?"*. Cuenta **cualquier** cuenta cuya vista sea un manager de la
   población, sea de quien sea: en el caso, un `exec` de la misma persona y un `admin2` de otra con su vista. **Skip
   dejaría a esos managers sin su cuenta de manager** → con "retain duplicates", **Create**. Antes de elegir:
   `select username, status, emp_id, emp_id_view from users where emp_id_view is not null and emp_id_view <> '';`.
   🔍 El aviso dijo 4 y la query encontró 2 en la población: no se sabe qué más cuenta.
3. **Las claves van a `temp_passwords`** (creció exactamente lo mismo que `users` en cada pasada; `password_history`
   quedó en 0). Esa es la tabla a respaldar junto con `users`.
4. **Ambas pasadas dejaron todo inactivo** (§ Activos o inactivos, arriba).
5. ⚠️ **`get-mgr-counts` devolvió 115 managers de 3.720** (8 KB contra ~900 KB en otros apps), igual en dos
   corridas. Con ese archivo como "esperado", la pasada 1 parecía mal (2.319 contra 94) y no lo estaba. **Control
   independiente del archivo:** `select count(distinct mgr_id) from managers_tree where mgr_id <> '0';` →
   Leader + Below tiene que dar eso (2.319 + 1.401 = 3.720 exacto). Y el umbral se verifica **por muestreo en el
   borde**, contando respondents en SQL:
   ```sql
   select count(distinct e.emp_id) from managers_tree t join emerge e on e.emp_id = t.emp_id
   where concat('.', t.tree_path, '.') like concat('%.', '<ID>', '.%')
     and t.emp_id <> '<ID>' and e.first_response_date is not null;
   ```
   En el caso: 4 → sin cuenta, 5 → *Leader*. Coincidió con el archivo en managers chicos; en uno grande dio 1.536
   contra 1.369 del script (🔍 el script vería una población recortada).
6. **Cuarta vía para el superior, toda en SQL, sin conteos:** subir por `mgr_id` nivel por nivel y quedarse con el
   **primer ancestro que tiene cuenta *Leader*** (la tabla `users` como referencia, igual que el otro DM, pero sin
   Excel). Joins de igualdad: corre en segundos. La variante con `LIKE` sobre `tree_path` cruzando 1.401 × 2.319 hizo
   *timeout* en Querious (15 s).
   ```sql
   select b.username as below_user, b.emp_id as below_id,
          coalesce(l1.emp_id,l2.emp_id,l3.emp_id,l4.emp_id,l5.emp_id,
                   l6.emp_id,l7.emp_id,l8.emp_id,l9.emp_id,l10.emp_id) as sup_id,
          case when l1.emp_id is not null then l1.view_disp when l2.emp_id is not null then l2.view_disp
               when l3.emp_id is not null then l3.view_disp when l4.emp_id is not null then l4.view_disp
               when l5.emp_id is not null then l5.view_disp when l6.emp_id is not null then l6.view_disp
               when l7.emp_id is not null then l7.view_disp when l8.emp_id is not null then l8.view_disp
               when l9.emp_id is not null then l9.view_disp when l10.emp_id is not null then l10.view_disp end as sup_view_disp
   from users b
   join managers_tree t0 on t0.emp_id = b.emp_id
   left join managers_tree t1  on t1.emp_id  = t0.mgr_id left join users l1  on l1.emp_id  = t1.emp_id  and l1.status  = '<Leader>'
   left join managers_tree t2  on t2.emp_id  = t1.mgr_id left join users l2  on l2.emp_id  = t2.emp_id  and l2.status  = '<Leader>'
   -- … igual hasta t10 / l10 (tantos saltos como max(deepness) − 1)
   where b.status = '<Below>';
   ```
   Control a mano en un caso: con `niveles = 1`, `sup_id` es el **penúltimo** ID del `tree_path`. `view_disp` sale
   de la cuenta *Leader* del superior (sin concatenar nombres ni escapar apóstrofos).
7. **Escritura:** el `UPDATE … JOIN` con esa query adentro (y `DISTINCT` para que MySQL materialice) + `SET
   emp_id_view, view_disp` `WHERE u.status = '<Below>'`; después `UPDATE users SET sso_id = emp_id WHERE status in
   (…) AND emp_id NOT LIKE 'Test%'` (cuentas de prueba del PM, con emp_id no numérico, afuera). **No se pudo correr
   desde DelOps** (§ services-os, *Database Tools* no actualiza `users`; Querious de solo lectura): lo corrió alguien
   del equipo con escritura, a pedido por Slack.
8. **Verificación:** *below* con vista propia = 0; *below* cuya vista no es una cuenta *Leader* = 0; *Leader* con
   vista propia = 2.319; `sso_id = emp_id` = 3.720; total de `users` sin cambios; cuentas de prueba sin tocar.
9. ***Quality and Integrity Checks*, solo *Users*:** *"only has N questions that will be shown"* es la lista de
   **menos de 10 preguntas** (5 *Leader* de equipos chicos, por supresión por pregunta); *"blank email"* = exactamente
   las cuentas sin email del mensaje de *Add Users*. **Antes de informar, clasificar cada alerta por status**: casi
   todas eran de cuentas `hr` / `comprate` preexistentes (vistas armadas a mano a no-managers, 0 preguntas). Esas van
   al PM **aparte**, como FYI, sin tocarlas.

#### Lo que se dijo de paso (09/10)

- **Complejidad:** la trainee, *"la más complicada que vimos"*. El DM: *"hablaron de querer una
  herramienta para esto"*. Emily la había puesto en 6–7/10.
- **Frecuencia:** 🔍 en la call alguien dice *"you see it a lot too"* (no queda claro quién). **Choca** con
  Emily el 24/09 (*"no la vas a ver mucho"*) — y van tres tareas en dos semanas (24/09, 08/10, 09/10).
- La trainee iba a cargar un **demo nuevo por el ops tool con el archivo** (§ Agregar un demográfico nuevo),
  para no tener que pedirle al DM el `UPDATE`.

### Lo que se vio en el shadow del 24/09 (tarea `PFS: Creates Manager Users`)

> Fuente: shadow ***Users set up*** del **24/09** con Emily (Guillermo, Andrea e Ignacio). **Transcripción
> completa** del video, pasada por Ignacio el 08/10; el resumen de Gemini de la misma sesión quedó
> superado (ver al final). Marca por defecto: 📣 Emily, 24/09. Lo que se vio en pantalla se describe,
> pero no hay capturas. La transcripción es automática: deforma nombres (*"Pearl"*, *"FID"*/*"M ID"* =
> emp_id). Ejemplos con nombres de empleados del cliente: omitidos. Primer pedido real de este tipo:
> 08/10 ([[Perceptyx/bitacora|bitacora]]).

**Qué es.** Dos partes:

1. **Crear usuarios Manager** — lo normal, desde el árbol de managers, siguiendo el checklist del PM.
2. **Reasignar a los que no llegan al umbral** — Emily: *"no es una tarea normal, no la vas a ver
   mucho"*. A los managers cuya jerarquía **no llega a 5** no se los mueve ni se los borra: se les
   **cambia el status** y se les da **la vista del primer manager de arriba que sí llega**.

En la tarea del 24/09 **la parte 1 ya estaba hecha** (*"the users are already set up"*); se trabajó solo la
2. 🔍 En la tarea del 08/10 se piden las dos.

**Por qué** (lo explicó Ignacio y Emily lo confirmó): privacidad. Con menos de 5, un manager puede
deducir quién respondió qué. El de abajo pasa a ver **lo mismo que su jefe**: sus reportes, los de sus
pares y los del jefe, agregados. Las respuestas de su gente no se pierden: entran en la vista de arriba.
Emily: el status nuevo tiene **otra configuración de reportes**, armada por el PM (puede tener más
restricciones) — *"no te tenés que preocupar por eso"*.

#### Antes de empezar: ¿5 *qué*?

En la tarea del 24/09 el **título** decía *respondents* y la **descripción** *completions*. Emily le
preguntó al PM por chat: **completions**.

- **Completion** = apretó *submit*, aunque haya dejado preguntas sin contestar. En **`emerge`**:
  `survey_completed = 1`.
- **Respondent** = contestó algo y no envió. En `emerge`: fechas de primera y última respuesta cargadas,
  `survey_completed` en 0. **Sin fechas** = 🔍 nunca entró.
- Para ver qué contestó: **`all_data`**, unido a `emerge` por el ID del participante (*"client ID"*). Las
  columnas que empiezan con **`000000…`** son las **preguntas**; las otras, demográficos.
- Emily: **la creación de usuarios suele hacerse por respondents**. Por eso vale preguntar.
- ✅ **Criterio (Ignacio, 08/10): lo que dice la tarea manda.** *"La task dice responses, así que son
  responses, no completions."* *Responses* = **respondents**: en `get-mgr-counts` se filtra la columna de
  respondents y en *Add Users* la base es respondents. Se pregunta al PM solo si la tarea **se contradice**
  (como el 24/09: título *respondents*, descripción *completions*).

#### Parte 1 — Crear los usuarios Manager (*Manager Hierarchy Tree › Settings › Add Users*)

- Llega un **checklist de usuarios** del PM (una planilla) con lo que quiere el cliente. El que mostró:
  usuarios **según respondents**, **no activos**, **SSO ID = emp_id**, **duplicados permitidos** (si la
  persona ya tiene otra cuenta con otro status, puede tener además la de manager), **username = inicial
  del nombre + apellido**, status manager, umbral 5.
- En la pantalla de *Add Users* (vista en vivo, sin captura): **qué managers** (*"all managers who met
  threshold"*; **el umbral ya lo configuró el PM**) · **status** (el de manager; **el nombre cambia por
  cliente** — en ese era *Direct Supervisor*) · **formato del username** · **base: respondents o
  completed** → ***Save***.
- Resultado: los usuarios en la tabla **`users`** con ese status, y sus claves en la tabla de
  **contraseñas temporales** (✅ `temp_passwords`, medido el 29/10: crece igual que `users` en cada pasada).
- **La vista de cada manager es él mismo**: ve a toda su jerarquía. En la tabla, *view display* = su
  nombre y `emp_id_view` = su emp_id.
- Alternativa del lado del PM: una **planilla de carga de usuarios con demográficos** que suben ellos;
  DelOps casi no la toca.
- ~~🔍 Para el 08/10: los **Below Threshold**, ¿se crean con otra pasada de *Add Users* (otro filtro, otro
  status) o se crean todos como Manager y después se reasignan como el 24/09? En el caso del 24/09 los
  761 de abajo del umbral **ya tenían cuenta de manager**. A confirmar con el PM o en la pantalla.~~
  ✅ **Resuelto 09/10** (Jackie, 08/10): **otra pasada de *Add Users*** con *All Managers Who Did Not Meet
  Threshold* y status *Manager Below Threshold*. Cuando ya tienen cuenta de manager (como el 24/09), el
  camino es el `UPDATE` de status del shadow. Los dos existen.

#### Parte 2.1 — Contar: `get-mgr-counts`

- **Vía terminal** (la que usó Emily): SSH al **jail de PMS** (snippet de Text Expander `pms`) → `cd` a
  la carpeta de los scripts Perl (otro snippet, *"cd root"* en la transcripción) → `ls` lista los
  scripts → `perl get-mgr-counts` → pide el **survey ID** → deja el archivo en la carpeta de **script
  output**.
- **Vía SOS**: el mismo script en *Toolbox › Perl* ([[Perceptyx/services-os|services-os]]). Las dos
  valen.
- `verify-survey-integrity`, del mismo directorio: *"lo corrés prácticamente en cada tarea"*.
- La salida tiene **una fila por manager** con los conteos de toda su jerarquía en **dos columnas
  vecinas**: ***hierarchy responses*** y ***hierarchy completions*** (en la planilla de Emily, la 7.ª y la
  8.ª). Se abre en **Excel como delimitado por tabulaciones** y se filtra la que pida la tarea **< 5**.
- ⚠️ **Error real de la sesión (segunda parte, 📣 Emily):** en el BUSCARV del conteo del jefe puso el
  índice de columna **7 en vez de 8** y trajo *responses* en lugar de *completions*. Lo detectó ella
  misma: trajo la otra columna al lado, comparó las dos y miró las que daban distinto — **todas estaban
  muy por encima de 5**, así que no cambió nada. *"Really easy to accidentally mess things up."*
  **Chequeo que queda:** antes de usar el conteo, confirmar con el encabezado qué columna trajo el
  BUSCARV; si hay duda, traer las dos y comparar.
- Chequeo: que cada uno **tenga cuenta de manager** (por emp_id contra `users`). En el caso: **761**.

#### Parte 2.2 — Backup

**`users` y la tabla de contraseñas temporales**, con las iniciales (§ Reglas que valen para toda
tarea). **No se borran al terminar**: si el PM vuelve semanas después con *"esto no está bien"* o *"no lo
queremos más"*, el backup muestra cómo estaba y permite revertir.

#### Parte 2.3 — Cambiar el status

- Los statuses están en la tabla de **statuses**. El de "siguiente nivel" (en ese cliente, *Manager Next
  Level*) **ya lo había creado el PM**: DelOps solo lo asigna.
- `UPDATE users SET status = <manager next level> WHERE emp_id IN (<los 761>) AND status = <manager>`.
  ⚠️ **El `AND status` es obligatorio**: con duplicados permitidos, la misma persona puede tener otra
  cuenta con otro status, y esa no se toca.
- Verificar el conteo: **761 actualizados**.
- Ignacio dijo que escribir directo en la base le daba miedo. Emily: *"vas a hacer mucho de esto"*; para
  eso está el backup.

#### Parte 2.4 — Encontrar el manager de arriba que llega

- Traer de **`managers_tree`** el `mgr_id` y el **`tree_path`** de los de abajo del umbral. El
  `tree_path` muestra **toda la cadena hacia arriba**: el último es la persona, el anterior su jefe
  directo, y así ([[Perceptyx/modelo-de-datos|modelo-de-datos]] § La jerarquía de managers).
- **Partir el `tree_path` no sirve**: cada uno tiene un largo distinto.
- **Lo que funcionó** (lo propusieron los trainees; Emily: *"good idea"*): **BUSCARV en cadena**.
  1. BUSCARV del `mgr_id` en la salida de `get-mgr-counts` → ¿el jefe llega a 5?
  2. Si llega: listo, esa es la vista.
  3. Si no: BUSCARV del **jefe del jefe** en `managers_tree` y repetir.
  4. Se repite hasta que no quede nadie. Emily: *"apuesto a que en este nivel ya está bien"*; la mayoría
     se resuelve en el **primer nivel**.
- *View display* = **nombre y apellido** del manager elegido, combinados en Excel.
- Emily dijo que quizás le pediría a un chat de IA una query para esto. ⚠️ Revisar antes la lista de
  clientes con los que no se puede usar IA (Reglas § 9).

#### Parte 2.5 — Asignar la vista

- Un `UPDATE` **por fila**, generado con una **fórmula de Excel** (Emily tiene fórmulas guardadas y las
  adapta; Ignacio tiene el **helper formulas** en su equipo de trabajo — [[Perceptyx/plataforma|plataforma]]):
  `UPDATE users SET emp_id_view = '<B>', view_display = '<F>' WHERE emp_id = '<A>' AND status =
  <manager next level>;` 🔍 nombres de columna tal como se oyen en el video.
- ⚠️ **Comas en los nombres** rompen la sentencia: los valores van **entre comillas**.
- Se corre de a tandas: primero los que ya tienen ancestro resuelto, mientras se calcula el siguiente
  nivel de los demás.
- **Segundo nivel** (segunda parte de la grabación): para los que seguían sin vista, otro BUSCARV del
  jefe del jefe, se arma de nuevo el *view display* (nombre + apellido), y **antes de correr se revisa
  que el emp_id del manager elegido coincida con el `mgr_id` de la fila** (*"everything's lining up"*).
  Después, los mismos `UPDATE` de vista con los valores nuevos. Una vez falló la fórmula y hubo que
  corregirla antes de correr.

#### Cierre — no se vio

La sesión se cortó a los 55 minutos por otra reunión; en una **segunda parte** (8 minutos, el mismo día)
Emily resolvió el segundo nivel y dejó los `UPDATE` listos para correr, y ahí terminó. **No se vio
verificación final ni cierre de la tarea.**
🔍 Por lo que ya está en el vault: `verify-survey-integrity` (avisa de `emp_id_view` que no es de un
manager; § Chequeo de integridad) y el **Launch Audit en modo `users`** antes del launch de reportes
(§ Launch Audit). Quién manda los accesos (*Send User Accounts*): sin dato.

**Complejidad:** Emily, 6–7 sobre 10 — *"no es directa: BUSCARV y pensarla"*. Cuántas tareas por día:
*"preguntale a Jackie"*; depende de cada tarea.

**Lo que el resumen de Gemini deformó (SUPERSEDED 08/10):** decía que en la sesión se crearon los
usuarios Manager (ya estaban creados; solo se mostró la pantalla); decía *"basado en completions"* para
la creación (el checklist pedía respondents); y presentaba la búsqueda del ancestro como pendiente sin
método (el método de BUSCARV en cadena sí se armó y se empezó a correr).

---

## Armar un árbol de managers (lo que hay, sin procedimiento oficial)

> ⚠️ **No hay página de DelOps para esto.** Se juntan dos rastros, los dos 📣, ninguno verificado contra un
> documento. Cómo es la tabla por dentro (raíz `0`, `tree_path`): [[Perceptyx/modelo-de-datos|modelo-de-datos]]
> § La jerarquía de managers.

**Camino clásico — el que se vio en el training** (📣 Emily, 30/09, vía Gemini; § Actualizaciones después
del cierre, paso 4): sacar `emp_id` / `mgr_id` / nombres → Excel en texto → **quitar el `0` de la fila del
CEO y la fila placeholder** → **Data File Builder** de *Survey Setup › Operations tools* con el **ID del
CEO** como raíz → mover los audit files viejos → subir → managers faltantes al PM con el audit. El Data
File Builder del 360 también tiene un campo *CEO* y genera un `_tree.txt` (✅ *360 Data Upload Steps*), lo
que es coherente.

**Lo que hizo Jackie el 23/09** (📣, transcript completo — § Carga del archivo final): ✅ **la
herramienta *Build Hierarchy from Loaded Data* existe** (✅ captura: *Operations tools › Participant Data*, botón **Download**, para apps 360 y Ask; descarga un archivo que se sube
al *manager tree*), y es el camino **si toda la empresa está invitada**. Si no (como en su caso, con
inactivos filtrados): `SELECT emp_id, first_name, last_name, email, mgr_id` del **master app** → Data
Builder. **No se sabía quién era el CEO** → lo corrió por **SOS › Design & Build › DOC** (✅ captura), que **deduce la raíz** de las
relaciones emp → manager y devuelve el archivo del árbol y **audit reports** (asignados / faltantes → al
PM). Con datos sucios, SOS **eligió mal la raíz** (nadie reportaba a esa persona) y quedó para
troubleshooting.

**Camino LEB — según el bot Pyxee-CVO** (📣 06/10, citando *LEB FAQ – (Gemini Friendly).pdf*, **archivo al
que Ignacio no tiene acceso**: no se pudo verificar):

- Requisitos: el archivo importado trae un campo de **manager ID**; el equipo de Perceptyx **habilita la
  función *Manager Hierarchy*** (hasta **3 días hábiles**); se hace **antes de crear el evento**; solo para
  clientes con **feed automatizado** alineado al data spec.
- Pasos: ops tool ***Build Hierarchy from Loaded Data*** → armar con **`rm=managers_tree`** → pedir un
  **data file audit a PFS**.
- *"No hace falta que PFS cargue el archivo por la vía clásica: LEB lo resuelve si el manager ID vino en la
  importación."* Instrucciones completas: guía de LEB en Academy.
- 🔍 Por cómo está escrito (pedirle el audit **a PFS**, *"no hace falta PFS"*), es el flujo **del PM o del
  cliente en LEB**, no el de Delivery Ops. El nombre de la herramienta y `rm=managers_tree` encajan con el
  patrón de pantallas `rm=` del app, pero no están vistos. ✅ **09/10: `rm=managers_tree` existe** — es la
  pantalla ***Manager Hierarchy Tree*** del app (captura de la call de Jackie, 08/10). Su *Settings* tiene
  *CEO emp_id* + *Choose File* (🔍 la carga del árbol) y *Add Users* (§ Usuarios Manager / Manager Below
  Threshold).
- **Segunda consulta (06/10)**, pidiendo explícitamente *"for a delivery ops manager"* y *"a link from
  Confluence"*: **la misma respuesta con el título cambiado** (repite la pregunta), la misma fuente, y
  *"no tengo un link de Confluence"*. 🔍 No hay página de Confluence en lo que indexa el bot. Agregó un
  paso nuevo, para el **acceso a reportes**: *Listen › Manage Event › Event Options › Edit Reporting
  Access* → **List View** o **Hierarchy View**.
- 🔍 **Conexión:** ese *Hierarchy View* para dar acceso a reportes es lo que *Manager Heirarchy Tree*
  (engineering) describe como el árbol *snapshot* en UDS asociado al survey para restringir reportes
  ([[Perceptyx/modelo-de-datos|modelo-de-datos]]). Refuerza que el camino LEB es el de la **arquitectura
  nueva**, y el clásico (Data File Builder + `managers_tree`) el de la legacy.
- ⚠️ **Matiz del 08/10:** en un survey **de LEB**, el acceso a reportes por jerarquía (usuarios `mgr` /
  `mgrbt`) se resolvió en la tabla clásica `users` con `emp_id_view`, no por *Edit Reporting Access*
  (§ Usuarios Manager / Manager Below Threshold). La conexión de arriba queda **debilitada**: LEB no
  implica arquitectura nueva para los permisos de reporte.

---

## Pendientes de procedimiento sin cubrir

- **Late add: IDs que están solo en una de las dos tablas** (`prefill_data` o `emerge`). Cómo sumarlos sin
  duplicar. Apareció el 19/10/2026 con el ticket odtnpees26a. Pregunta abierta para Ignacio.
- **Late add: orden de las primeras columnas del archivo.** ¿El Data File Builder exige `emp_id, first_name,
  last_name, email, mgr_id` al inicio, o alcanza con que las columnas existan? Sin resolver (🔍).

- ~~**Cambiar la definición de las bandas de un demo calculado**~~ **SUPERSEDED 27/10/2026**: resuelto como *crear* el demo (§ Agregar un demográfico nuevo › Demo calculado desde una fecha). Queda abierto solo *cambiar los cortes de una banda que ya tiene respuestas*. Texto original: (pedido del cliente con cortes propios de
  edad o tenure, a partir de la fecha de nacimiento o de ingreso). Apareció el 19/10/2026 con el survey en
  vivo → se trabaja después del cierre (📣 Ignacio). Sin ver todavía: si se reescriben las opciones de
  `resp_list` o se crea un demo nuevo; cómo se recalcula la banda de cada participante (¿*Add / Update
  Demographics* con archivo, como § Agregar un demográfico nuevo?); qué pasa con las bandas `pyx_…` que
  genera Perceptyx ([[Perceptyx/modelo-de-datos|modelo-de-datos]]). Al resolverlo, va a sección propia y al
  mapa del principio.

- **User setup con varios status, incluidos empleados** (apareció el 17/10/2026, [[Perceptyx/bitacora|bitacora]]
  2026-10-20): status de empleado que ven los resultados de su manager o del siguiente nivel, y un umbral más alto
  para un país. Sin ver todavía: cómo se crean los usuarios empleado (¿*Add Users* tiene esa población?); qué umbral
  usa *Add Users* cuando hay dos; si un umbral *"de comentarios"* se cuenta en la creación o se configura en el status
  (`get-mgr-counts` no cuenta comentarios); cómo se compara `statuses` con un app de usuarios de prueba aprobado. Al
  resolverlo, va a § Usuarios Manager o a sección propia, y al mapa del principio.

- Qué tablas exactas respalda el script de backup de un data file load (se sabe que depende de la
  tarea).
- *Advanced reporting* para branching complejo: no se vio.
- ~~Cómo se toma una tarea de la cola en Salesforce y cómo se asigna.~~ Cubierto por Confluence el
  06/10: § Cola de tareas y escalación. Falta verlo en la pantalla de Salesforce.
- Activate / Nudge Engine: en nota propia, [[Perceptyx/nudge-engine|nudge-engine]].
- **Execution Checklist** de borrado / remoción de PII y el *Request Form*: nombrados en Confluence, no
  incorporados.
- ~~Procedimiento real de datos de prueba 360.~~ Llegó el 06/10: [[Perceptyx/cultivate-360|cultivate-360]].
- *Create Data Automation*: la página vino vacía. Cómo se arma la automatización **self-service**, sin
  cubrir; la de **360** sí está, en [[Perceptyx/cultivate-360|cultivate-360]] § Automatización por cron.
- La página del **data spec** en sí (formato exigido), los Standard Forms (PDF) y el video del audit.
