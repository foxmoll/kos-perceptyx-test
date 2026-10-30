# Services OS (SOS)

La plataforma interna de operaciones de Customer Value: **un solo lugar para las herramientas, scripts y
workflows** que llevan a un cliente por su programa de surveys. Es el destino de la consolidación que
está haciendo el equipo (📣 Ignacio, 06/10/2026: jails, Querious y los crons pasan a SOS).

Relacionado: [[Perceptyx/plataforma|plataforma]] · [[Perceptyx/procedimientos|procedimientos]] ·
[[Perceptyx/cultivate-360|cultivate-360]]

> **Fuente: ✅ Confluence *Services OS — User Guide*** (espacio COE), exportada por Ignacio el **06/10/2026**
> y re-exportada el **08/10/2026** (**versión 27** de la página; la versión del 06/10 no consta). La guía
> cita un *SOS Cheat sheet* (*Tool Overview*, *Use Cases By Role*: dos planillas de Google embebidas, que el
> export no trae) y **grabaciones de office hours** por módulo, no incorporados. **SOS es role-aware**: si un módulo no aparece, probablemente tu rol no lo
> necesita (y se puede pedir por *Feedback*). Qué ve Ignacio con su rol: sin registrar.

---

## Entrar

1. **VPN** (SOS corre en la red interna; problemas → **#it_help**).
2. Okta → tile **Services OS**.
3. Elegir rol (**PM, WTC**, …).

## Cómo está organizado

Alrededor del **recorrido del cliente**, no como lista de herramientas: *Dashboard*, *Customer Hub* y
*Support* en los extremos, y en el medio **cinco fases del evento** (*Event Journey*). ✅ En pantalla (23/09): **Dashboard · [cliente] · Support** y las fases **Initiation → Design & Build →
Launch → Reporting → Close**. El cliente elegido aparece como `EU-<cliente>` con insignia de región.

| Pieza | Para qué |
|---|---|
| **Dashboard** | Home: comunicados, tours, clientes guardados, launches programados |
| **Customer Hub** | **Elegir el cliente una vez antes de empezar**: los módulos (la guía nombra Customizations, Branching y UDS User Health) se ajustan solos a ese cliente. Sin cliente elegido se puede entrar a casi todo, pero con menos (ej. cargar un archivo pide cliente) — 📣 Jackie, 21/09. ✅ **Abrir los reportes de un survey sin password de MAC** (tip de SOS, captura del 26/10/2026): en el Customer Hub, **Reporting** en la tarjeta del survey, o clic derecho › *Open reporting in a new window*. Entra por Okta y Platform y queda registrado en el audit log. Sirve también para EU, cuando no se tiene la URL de MAC EU |
| **Event Journey** | Los módulos de cada fase del evento |
| **Toolbox** | Scripts e IT Tools |
| **Files** | Hub de archivos (lo que generan los scripts, lo que subís, lo que compartís) |
| **BMS** (cerebro, barra superior) | *Be More Smarter*: tours guiados **con datos ficticios** (práctica segura), guías y videos por módulo, y avisos de *what's new* |
| **Campana** | Alertas de feedback, crons y archivos |
| **Feedback** | Bugs y pedidos (*bug* o *suggestion*; captura de pantalla y contexto se adjuntan solos); es el backlog de SOS, el equipo lo triagea y responde dentro de SOS. Antes de pedir algo, buscar si existe y votarlo (*Admin › Feedback › Upvote Suggestions*) |

### Lectura o escritura, módulo por módulo

✅ El export del 08/10 etiqueta cada módulo:

| | Módulos |
|---|---|
| **READ ONLY** | Compare DBs · Branching · Survey Comms · Reporting Comms · Launch Dashboard · Peace Room · Email Monitor · Database Tools · BMS |
| **READ & WRITE** | Reset Survey · Reset Password · UDS User Health · Event Service Sync · Advanced Troubleshooting · DOC · Translations · **Customizations** · Launch Audit / V2 · Cron Manager · Benchmarks · Trend Mapping · Menus · Files · Perl / Python Scripts · IT Tools · Feedback |

🔍 Cómo se concilia con lo que dijo Ignacio el 06/10 (*"lo único de solo lectura son las queries a las
bases"*): los demás READ ONLY son **visores por diseño** (comparar, previsualizar, monitorear); Database
Tools es **el único que reemplaza a una herramienta que escribía** (Querious) y no escribe. Lectura propia,
no confirmada.

✅ **Database Tools escribe (23/10/2026, captura de Ignacio, app EU):** la pantalla tiene *Select · Insert · Update ·
Delete · Table*, con el banner *"EU production — reads use the replica, changes go to the primary"* y *"Runs on the
primary. You preview it once; SOS backs up every row it touches, runs big changes in waves you can pause, and keeps an
Undo."* Un `INSERT` de 3 filas en `prefill_data` entró con *Preview change* cuando Querious daba `INSERT command denied`.
*Insert* también ofrece cargar un archivo (CSV o tab, primera fila = nombres de columna); *Preview load* no hizo nada.
✅ **Update en uso (27/10/2026):** *Preview change* muestra las filas que van a cambiar y el backup que va a crear
(`sos_dbtool_<tabla>_<AAAAMMDD_hhmmss>`), y corre en tandas. **Con muchas filas pide escribir el nombre de la tabla**
para confirmar. Si el `WHERE` no encuentra nada, no deja correr (*"matches 0 rows"*). En `resp_list` avisa que
**reconstruye el *survey setup file*** después del cambio.
Lo de *"solo lectura"* de abajo queda `SUPERSEDED (23/10/2026)` para escrituras: 🔍 no se sabe desde cuándo.
✅ **Límites de *Update* vistos el 29/10/2026** (app LEB EU, tarea de usuarios manager —
[[Perceptyx/procedimientos#Cómo se resolvió el 29–30/10 (tarea 827284 — status con nombre propio, SSO = emp_id, sin `get-mgr-counts`)|procedimientos § 827284]]):
- **Una tabla por sentencia:** un `UPDATE … JOIN` da *"Unsupported statement. DB Tools runs SELECT, INSERT, UPDATE,
  DELETE, CREATE TABLE, ALTER TABLE and DROP TABLE — one table at a time."* (`CREATE TABLE` sí figura: lo de Jackie
  del 08/10, abajo, quedó viejo en eso).
- **No lee el escape con barra** (`\'`, el que genera `QUOTE()`): da *"couldn't read this query (an unclosed
  quote?)"*. Escapar duplicando el apóstrofo (`''`).
- **No actualiza `users`** cuando otra tabla tiene una clave foránea hacia ella con `ON UPDATE CASCADE` (en ese app,
  `user_privileges`): *"DB Tools backs up and undoes only users itself, so it won't run this. Ask an engineer."* Lo
  bloquea aunque el `UPDATE` no toque la columna referenciada.
- La pestaña de consultas acepta solo sentencias que empiezan con `SELECT` (un `WITH … SELECT` se rechaza).

✅ **Database Tools en uso (call de Jackie, 08/10):** un `CREATE TABLE` devuelve ***"Only select queries
are permitted in this interface"***; devuelve **como máximo 10.000 filas** (una tabla de ~12.000 llegó
cortada) y avisa *"query likely to be slow"* sin `WHERE`; `LIKE` no le funcionó (*"vamos a mandar un
bug"*); el snippet de backup de Text Expander todavía no anda ahí. Jackie tiene un acceso especial de
prueba con escritura (*"US insert"*): **la escritura viene, todavía no está**. Para backups, tablas
completas y `UPDATE`, Querious.

---

## Qué reemplaza a qué

Lo que más importa para leer el resto del vault: **varios procedimientos de Confluence describen la
herramienta vieja**. 🔍 Los cruces son lectura propia salvo donde la guía dice *"replaces"*.

| Antes | En SOS | Notas |
|---|---|---|
| Querious (consultas) | **Toolbox › Database Tools** | ⚠️ **Solo lectura** (réplicas US/EU) — **lo único de SOS que es solo lectura** al 06/10 (📣 Ignacio; matiz del 08/10 en § Lectura o escritura). ~~**Al 06/10 las escrituras siguen en Querious** hasta que SOS habilite escritura (📣 Ignacio)~~ SUPERSEDED (29/10/2026): 📣 Ignacio, Database Tools escribe en EU y US; Querious queda de solo lectura para él |
| Jail + git + `mac.cron_scripts` | **Launch › Cron Manager** | Dashboard de errores, *Cron Builder* con plantillas, *Cron Review*, *Scheduler* (horario + rerun), *Script Editor*. *Burndown* (próximamente): pasar crons custom a **sensores de lifecycle de LEB** |
| MAC trend setup + `trend_custom_linkages` a mano | **Reporting › Trend Mapping** | ✅ *"replaces mac trend setup"*: apps trendeadas, preguntas, demos y opciones en una herramienta, con sugerencias y mapeos custom; exporta el documento de trend |
| Tablas `new_menus` / `new_menu_options` | **Reporting › Menus** | ✅ Reemplazo explícito; drag & drop, versiones, permisos por rol |
| ~5 herramientas de ops de benchmarks | **Reporting › Benchmarks** | ✅ Reemplazo explícito |
| Pedido de Launch Audit al equipo CVOps | **Launch › Launch Audit (V2)** | ✅ Reemplazo explícito. **CVOps = ex SPT** |
| Mail semanal de launches programados | **Launch › Launch Dashboard** | ✅ Reemplazo explícito |
| Auto ticket de SFTP, Transmit para PGP | **Toolbox › IT Tools** | Crear usuario SFTP, clave pública, reset de password, descifrar PGP/GPG (hasta 10) |
| Troubleshooting de UDS a mano (binlog, divergentes, sso_id) | **Support › UDS User Health** | Ver abajo |
| Data Specs Audit script | **Design & Build › DOC** | 🔍 *Data Operations Center*: recibir, auditar y exportar archivos de datos del cliente |
| Perl scripts en SOS (training) | **Toolbox › Perl / Python Scripts** | Lo mismo que se usó en el training, con sus últimos cinco a mano |

---

## Módulos

### Support — ayuda post-lanzamiento

- **Reset Survey** · **Reset Password** (plataforma o reportes).
- **UDS User Health** — chequeo de identidad de **un** respondente: con emp_id, email o username +
  cliente, consulta **UDS, Okta y la base MySQL (SOT, fuente de verdad) en paralelo** y los cruza.
  - Tres tarjetas (UDS, OKTA, SOT) + mappings (*Surveys* y *Reporting*): verde = ok, **ámbar = falta**,
    azul = sobra. Problemas como tarjetas con código (`UH-001`…).
  - **El campo resaltado en verde es el atributo de match de SSO: si difiere entre UDS y Okta, ahí está
    el SSO roto.**
  - ✎ en la tarjeta UDS: editar emp_id, username, email, nombres, sso_id (**todo queda auditado**).
  - **Activar un mapping faltante:** clic en la tarjeta ámbar → dispara un sync de binlog → refrescar
    hasta que quede verde. Si sigue ámbar: *Ops Tools › Binlog Status*.
  - Refresco por tarjeta (↻), mucho más rápido que el de la página.
  - Casos: no puede entrar, le falta un survey, Okta y UDS no coinciden. Es la versión herramienta del
    troubleshooting de [[Perceptyx/procedimientos|procedimientos]] § Sincronización con UDS.
- **Compare DBs** (solo lectura) — dos bases de survey lado a lado: toggles y tablas comunes.
- **Event Service Sync** — empuja datos del app a la API de eventos para actualizar el evento en la
  plataforma.
- **Advanced Troubleshooting** — abrir un caso, traer logs (Okta / Splunk), causas probables rankeadas y
  registrar qué resultó ser.

### Design & Build — diseño y configuración

- **DOC** — *Data Operations Center*. ✅ Captura del 23/09: *"Send it to the DOC — drop a file, DOC
  audits, maps, and builds the **LEB-ready file** for you"* (referencia: spec *Build the Data File*).
  - Tres pasos: **Load File** (activo; inicial o final, **DOC detecta cuál**; audita, mapea y arma el
    archivo para LEB) · **Configure Demographics** (V2: agregar, sacar, renombrar, **reordenar** y
    configurar opciones) · **Verify Data** (V3: confirmar que la carga llegó — prefill, linkage, tablas
    resp, `all_data`). 🔍 V2/V3 parecen versiones próximas.
  - Se elige el survey por app ID o nombre; acepta **CSV, TXT, TSV, XLS, XLSX**; muestra *Recent runs*.
  - ✅ **Audit de archivo final visto de punta a punta** (tarea real, 26/10/2026, capturas; app EU, ~72k filas, xlsx de
    ~40 MB, ~115 columnas):
    - **El audit de DOC es el del data spec**: *Data spec v3.1 · always latest*. Resuelve la versión cuando la tarea
      dice "unknown". *Audit type* sale solo de la industria (*Standard* para non-healthcare).
    - El **primer *Build*** (y la detección del CEO) dio **HTTP 502**. El segundo funcionó y tardó ~7 min
      (436 s). 🔍 Parece un timeout con archivos grandes: reintentar una vez antes de cambiar de vía.
    - *Hierarchy root*: sin jerarquía queda *"No hierarchy root — set manually"* y el build sigue igual (igual genera el
      *managers-tree sidecar*, que no se usa).
    - Resultado en cuatro bloques: **archivo LEB construido** (descargas: LEB file, Audit report, Managers hierarchy,
      managers_tree) · ***Fix first — recommends holding*** (*"doesn't block the build"*) · **PASS/FAILED** con *Why this
      failed* · ***Rows to correct*** (ej. `mgr_id` que no existe como `emp_id`) · *Columns by category* (Required,
      Auto-generated, Optional).
    - **Fallas duras vistas:** *File exceeds column limit of 99* (la que quedó). *Missing required fields: Employee ID,
      Email Address* apareció **solo cuando no se había aplicado el mapeo** de las 5 columnas (*Required 0/5*). Con
      *Column mapping › View changes › Looks right* aplicado, desapareció. ~~🔍 El audit parece leer los encabezados
      crudos, no el mapeo~~ **SUPERSEDED 26/10/2026** (Ignacio, segundo build): era el mapeo sin aplicar.
      Hay que **confirmar el mapeo antes de cada build**.
    - **Qué traen las descargas** (✅ 26/10/2026): ***Export findings*** es un PDF de una página, ***Data File Review***,
      **escrito para el cliente** (*"Prepared for <cliente>"*, firmado con el nombre y el mail del DM). Lista los
      hallazgos con *What to do* y el número de review. El ***Audit report*** es un xlsx con **una fila por empleado** y una
      columna por chequeo. Con un archivo de spec viejo, todas las filas dicen *"column missing in the file"* para los
      campos nuevos de v3.1 (*Nudge Eligible*, *AI Coach Eligible*): es ruido y no suma para el PM. Ignacio, 26/10:
      *"no aporta nada enviárselos"* → al PM le alcanza con el resumen y el número de run.
    - **Que el build salga no quiere decir que se pueda cargar.** Si la tarea dice *"upon audit pass, load"*, un FAILED
      va al PM (§ Data specs en [[Perceptyx/procedimientos|procedimientos]]).
  - **Uso real visto (Jackie, 23/09):** pasar un archivo de emp / manager para que **deduzca la raíz del
    árbol de managers** y devuelva el archivo del árbol y los audit reports.
  - 🔍 Cuando *Configure Demographics* y *Verify Data* estén, reemplazan el reordenamiento por Excel + SQL
    y los verify scripts del training.
- **Translations** — frases en inglés, traducción con el proveedor, edición, links de revisión. ⚠️ No anda
  para eventos **Mosaic**.
- **Branching** (solo lectura) — las reglas de branching de **todas las fuentes** lado a lado, marcando
  *drift*. Responde *"¿se publicó?"* y *"¿en qué motor está?"*. Cada tarjeta tiene borde de color y una
  etiqueta de estado (pasar el mouse da el motivo): verde *match / sole source* = coinciden o hay una sola
  fuente · **rojo *drift*** = diferencia real · ámbar *unexpected* = contenido donde no debería haber
  (edición manual o resto) · **naranja *unpublished*** = cambios hechos sin publicar · gris *empty / N/A* =
  sin cambios o no aplica a ese motor. Caso típico: un cambio en LEB a un survey
  Mosaic que no está vivo → tarjeta *DC vNext* naranja → hay que hacer *Settings / Preview / Make Survey
  Active* en LEB (lo mismo que dice la regla 10 de procedimientos, desde el otro lado).
- **Survey Comms** (solo lectura) — previsualizar comunicaciones como un destinatario, exportarlas a Excel
  para el cliente, tamaño del mail, **errores de merge fields** (rojo = campo conocido mal escrito, ej.
  espacios en `[ First Name ]`; amarillo = campo desconocido, puede ser un prefill válido).
- **Customizations** (~~solo lectura, v1~~ **SUPERSEDED 06/10**: se edita y publica, ver abajo; ✅ el export
  del 08/10 ya lo etiqueta **READ & WRITE**) — qué archivos de plantilla están customizados en un survey
  contra los defaults del *apps-repo*, *"so **PFS** no longer greps the repo by hand"* (PFS = Delivery Ops,
  [[Perceptyx/plataforma|plataforma]] § Glosario): tres capas (**default** = base sin tocar, **overlay** =
  archivo customizado para ese survey, **db_override** = plantilla de DC editada en la base del survey) con
  diff. El árbol marca los archivos con insignias *OVERLAY* / *DB OVERRIDE*; la barra de metadata da último
  autor, SHA del commit, fecha y **qué otros surveys comparten el mismo overlay**. Un survey sin
  customizaciones es normal.
  - ✅ **Lo que mostró Jackie el 21/09** (📣, *"bastante nuevo, lo estamos probando"*; confirmado por Ignacio el
    06/10: en SOS **lo único de solo lectura son las queries a las bases**): desde
    acá **se edita y se publica**. Se busca el archivo base entre las plantillas, se arma un ***subclass
    file*** (recodificar una parte chica para un cliente, ej. una **página de PIN** custom) y SOS hace el
    push → aparece en Slack, en el flujo ***collab GitLab flow*** → lo **aprueba** alguien habilitado
    (Jackie, Edwin, los dos Jack, gente de engineering; **Raphael** cubre la noche de EE.UU.) → **deploys en
    tanda, 10:00 y 15:00 hora Central**. En temporada alta de launches hay ***code freeze***: se evitan estos
    cambios. Antes: editar en el jail local con git y mandar el link. Política: **tratar de no hacer
    subclasses** y resolver dentro del estándar.
  - La guía describía la **v1 de solo lectura**; la edición llegó después. Al 08/10 el cuerpo del texto
    todavía dice *"(Read-only in v1)"* bajo la etiqueta READ & WRITE: la guía se actualizó a medias.
  - ✅ **Captura 21/09** (`#customizations`, en *Design & Build*): *"Browse and edit a survey's file overlays
    against **`apps @ master`** — **push changes as a merge request**"*. Confirma edición + merge request en
    **GitLab** (repo `apps`, rama `master`).
    - **Cuatro tipos de archivo** (leyenda de colores): 🔴 ***Custom code*** · 🟣 ***Template overlay*** · 🟡
      ***DB override*** · 🔵 ***Data***. 🔍 La guía hablaba de tres capas (*default*, *overlay*,
      *db_override*); el *default* es la base contra la que se compara, y *custom code* y *data* son tipos
      que la guía no nombraba.
    - Tres paneles: ***File Tree*** (`apps @ master`; *+ New file*, *Upload file*, *Upload folder*) ·
      ***Viewer*** (*"los template overlays muestran un diff contra la base; custom code y data muestran su
      contenido"*) · ***File Metadata***. Arriba: *← Surveys*, el survey elegido, ***Import***, y una línea
      técnica del escaneo (tiempo, llamadas a GitLab).
    - Un survey sin customizaciones dice *"No customizations for this survey"*: lo normal.

### Launch — que el survey salga bien

- ✅ Captura 21/09: la fase dice *"Survey launch, email delivery, and cron scheduling"*; tiles **Launch
  Dashboard**, **Launch Audit** (*New*), **Peace Room** (*Live*), **Cron Manager** (*New*) y, aparte, **Survey
  Launch Audit v2** (*New*).
- **Launch Dashboard** — launches programados en tiempo real, de todos los surveys. Por ahora **solo
  launches programados** (*"will change as more are added"*).
- **Launch Audit / V2** — auditoría de salud de datos del launch (UDS + MySQL) antes y después; limpiar
  caché de plataforma (`emerge` o `users`); en V2, índice y caché prelanzamiento.
  - 📣 **Visto en uso (Jackie, 21/09):** es la tarea *"launch audit"* de la línea de tiempo. Modo **`emerge`**
    (respondentes, antes del survey) o **`users`** (reporting, antes del launch de reportes). **Reporta y
    arregla**: *bad / missing mappings*, *Okta connectivity*, ***divergent identity*** (la más común: mismo
    email, otro emp ID), *meta mismatches*, *SSO hygiene*, *missing in UDS*, *weird characters* (los limpia
    solo), *active state drift*. Reemplazó a los scripts Python + planillas: *"el 99% se hace ahí"*. V2 ese
    día recién aparecía, a medio construir. Detalle en [[Perceptyx/procedimientos|procedimientos]] § Emails,
    traducciones y chequeos del app.
- **Peace Room** (solo lectura) — día del launch: que salgan los mails y que las respuestas lleguen a
  `all_data`. Detecta problemas temprano *"without having to ask Delivery Ops, SPT"*: 🔍 es una consulta
  que antes caía en Delivery Ops.
- **Email Monitor** (solo lectura) — pestaña *Bouncebacks*: la lista de rebotes del evento (las otras
  pestañas, inactivas).
- **Cron Manager** — ver tabla de arriba. Las *Targeted Alerts* de SOS (campana) remiten a los errores del
  dashboard de crons.

### Reporting

- **Benchmarks**, **Reporting Comms** (igual que Survey Comms), **Trend Mapping**, **Menus** — ver tabla de
  arriba.

### Files

- Explorador con nombre, cliente, origen, tamaño, modificado y **vencimiento**: verde / amarillo (<3 días) / rojo (<1 día);
  punto rojo = no leído.
- Subir: arrastrar a la zona de la barra derecha o *Browse Files*.
- **TTL de 30 días**: subir o compartir o actualizar → 30 días de nuevo · alertas a las 72 h y a 1 h ·
  vence → papelera (solo admin) · 30 días en papelera → archivo permanente.
- **Compartir**: link seguro con vencimiento, interno o al contacto del cliente (externo según el modelo de
  acceso del cliente: autoacceso de 24 h o pedir permanente). **Truco: para conservar un archivo,
  compartirlo (aunque sea con uno mismo).**
- Se re-escanea cada 24 h; *Refresh* si un script recién generó algo.
- 📣 Jackie, 21/09: ahí caen las **salidas de los scripts** (ej. un ***UDS dump***: todos los usuarios con
  sus accesos —reportes, nudges— en una planilla) y se sueltan los archivos de entrada en la carpeta
  ***script input***. Los archivos de ella aparecían bajo *"no customer"* (*"lo están resolviendo"*). Lo usa
  cada vez menos: el Launch Audit ya no pide armar archivos de *"borrar / actualizar estos usuarios"*.

### Toolbox

- **Perl / Python Scripts** — elegir script, completar inputs, correr, ver la salida en vivo; los
  resultados quedan en *Files*. Dos columnas, *Read* / *Write*, por categoría de script; clic en un
  script → cajón a la derecha con descripción e inputs. La guía dice que están *"los más usados por Delivery
  Ops y CVOps"*.
  - ✅ Captura 21/09 (`#perl`): ***Perl Scripts — 73 scripts registered***, buscador, columna **READ** con
    *Recently used* y *All scripts (A-Z)*, cada uno con descripción y etiqueta ***NOT TESTED***. Ejemplos:
    `get-mgr-counts` (conteos de la jerarquía), `verify-survey-integrity`, `comments-verify-steps`,
    `7p-convert-5p-all-data` (escala de 7 a 5 puntos), `add-comparison-views`, `add-new-demo`,
    `add-new-values`, `all-data-counts` (conteo por opción → Excel), `bootstrap-comments`,
    `build-target-queries`, `cleanup-clone`, `clone-app`, `clone-ss-sub-app`, `create-app`… El script corre
    en una **terminal embebida** (acoplable, *Dock*) y es **interactivo**: pregunta al final (ej. si aprobar
    las alertas).
  - 📣 Jackie, 21/09: **Perl = los scripts *"old school"*** (ej. `verify_survey_integrity`), muchos ya
    reemplazados por herramientas mejores; **Python = los nuevos**, sobre todo para **sincronizar sistemas**
    (mappings del app ↔ UDS), hoy absorbidos en buena parte por el Launch Audit. Es el reemplazo de entrar
    al **jail** por terminal.
- **Database Tools** — explorador **solo lectura** de las bases de survey: *"confirmar qué dicen los datos
  antes de escalar"*.
- **IT Tools** — SFTP (crear usuario y compartir el link de password de un solo uso; agregar la clave
  pública SSH del cliente a una cuenta existente para que suba archivos; reset de password con link de un
  solo uso), descifrar PGP/GPG (hasta 10 archivos a la vez), optimizar imágenes (redimensionar, convertir,
  comprimir) a presets de marca: **banner de email, fondo, logo**.
  - 📣 Jackie, 21/09: el **descifrado** reemplazó al **ticket automático de Jira** que devolvía un link; el
    ***image optimizer*** sirve cuando el cliente manda imágenes de tamaño raro para la página de bienvenida
    o los emails.

---

## Lo que no está claro

- ~~🔍 **Cómo se hace en SOS una escritura que antes era un `UPDATE` en Querious**~~ **Respondida 06/10**
  (📣 Ignacio): **hoy las escrituras se siguen haciendo en Querious**, hasta que SOS habilite lectura y
  escritura. La consolidación está en curso, no terminada. SUPERSEDED (29/10/2026): las escrituras van por SOS ›
  Database Tools en EU y US (📣 Ignacio); en Querious no tiene escritura.
- ~~🔍 **WTC** (un rol) y **Mosaic** / **DC vNext**: sin definir.~~ Resueltos 06/10 (ver
  [[Perceptyx/plataforma|plataforma]] § Glosario y [[Perceptyx/dc-mosaic|dc-mosaic]]).
- ~~**Customizations**: ¿solo lectura o edición + push?~~ ✅ 06/10 (📣 Ignacio): edición + push. **Lo único de solo lectura en SOS son las queries a las bases.**
- **Ops tools → SOS**: Jackie (21/09) espera que todos los *Operations tools* del app pasen a SOS; sin fecha.
- Qué módulos ve Ignacio con su rol.
