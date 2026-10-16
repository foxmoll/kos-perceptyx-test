# Cultivate – 360 Feedback: datos, demos y automatización

Todo lo de Delivery Ops sobre el producto **360** (Cultivate – 360 Feedback, apps **360v2**): cargar el
archivo del cliente, armar los demográficos propios del 360, preparar usuarios de prueba, el demo oculto
de relaciones combinadas y la automatización por cron.

Relacionado: [[Perceptyx/procedimientos|procedimientos]] (reglas generales, data specs, Standard Forms) ·
[[Perceptyx/plataforma|plataforma]] (tablas, glosario)

> **Fuente: ✅ Confluence**, cinco páginas exportadas por Ignacio el **06/10/2026**: *360v2 Load Data File
> – Cultivate: 360 Feedback*, *360 Data Upload Steps*, *Create 360 Combined Relationship Demo (Hidden
> Demo)*, *360 Survey Test Leader & Raters Setup* y *Automation Setup – Cultivate: 360 Feedback*. Los
> nombres de clientes de los ejemplos (carpetas, scripts de muestra) se reemplazaron por genéricos; un
> hash de password de usuario de prueba que trae la página no se copia.

---

## Cómo es un 360 por dentro

> Lo que opera DelOps es el **Managed 360** (= PYX-Led = Classic 360, apps 360v2). El **Self-Service 360
> (SS360)** lo configura el cliente y vive en la arquitectura nueva. Glosario completo de 360 (nomination,
> report eligible, threshold, cohort, 180) en [[Perceptyx/dc-mosaic|dc-mosaic]] § Glosario.

- Un **leader** (el evaluado, *ratee*) recibe feedback de varios **raters**: él mismo, su manager,
  reportes directos, pares, externos.
- Cuatro demográficos propios del 360, que van **primero** y en este orden (los PM lo prefieren así para
  configurar los reportes):

| Demo ID | Demo | Qué es |
|---|---|---|
| `01_01_07` | **Survey Version** | Versión del cuestionario (opciones las da el PM) |
| `01_02_07` | **Relationship** | Relación rater → leader. **Self siempre = 1**; Direct Manager casi siempre = 2; después reportes, pares, etc. |
| `01_03_07` | **ratee_id** | A quién evalúa ese registro (= `sequence` del leader en `users`) |
| `01_04_07` | **Participant Fullname** | Nombre del leader. Columna **`participant_fullname`** en `prefill_data` |

- `emerge` lleva la relación rater–leader (`ratee_id`, `relationship`, `survey_version`, fechas); el leader
  vive en `users` con status `participant` y su `view` filtrado a su `ratee_id`.
- **Por lo general no se carga `emerge`** desde el archivo del cliente, y el **manager tree solo se arma si
  el PM lo pide**.

---

## Carga del archivo (inicial y final)

> Hay **dos páginas que describen lo mismo y no coinciden en el orden de columnas**. *360 Data Upload
> Steps* es 🔍 probablemente la más nueva (usa `dataspecs_audit_v3.py`, separa carga inicial y final, y
> agrega los demos `Respondent_`); se sigue esa. La diferencia está abajo.

### Carga inicial

1. **Columnas obligatorias:** Employee ID, First Name, Last Name, Email, **Job Title (sin nulos)**.
2. Correr **`dataspecs_audit_v3.py`**: data specs + bandas (edad, tenure, generación).
3. **Largos de campo:** si algún valor pasa los **200 caracteres** (`varchar(200)`), anotarlo; en Excel,
   `=MAX(LEN(A2:A99999))`. Se ajusta después de cargar (paso 7).
4. **Agregar columnas vacías:** Survey Version, Relationship, `ratee_id`, Participant Fullname
   (`participant_fullname`), `filename`.
5. **Primeras 11 columnas, en orden:** `emp_id`, `first_name`, `last_name`, `email`, `mgr_id`, Survey
   Version, Relationship, `ratee_id`, Participant Fullname, Job Title, `filename`.
   - *(La página vieja pone Job Title sexto y Participant Fullname séptimo, y usa el truco de duplicar la
     fila de encabezados para el Data File Builder: segunda fila con los nombres de base, primera fila
     solo con las columnas que serán demos.)*
6. **Demos `Respondent_`** (si los piden): duplicar los demográficos comunes al final con prefijo
   `Respondent_` (ej. `Respondent_Location`). **No** se duplican IDs, nombres, emails, `mgr_id`, los
   cuatro demos de 360 ni fechas.
7. **Generar archivos** con el Data File Builder de Operations Tools (`rm=operations_tools`; CEO en
   blanco; *First Row Contains* = *Demographic Questions*) o `datafile_builder.pl`:
   - `_resp.html` → se usa (demos) · `_prefill.data` → se usa (datos)
   - `_emerge.txt` → **ignorar** en 360 · `_tree.txt` → casi nunca
   - `_AUDIT.txt` → **al que pidió la tarea**, por emails o emp_ids duplicados.
8. **Cargar `_prefill.data`:** app → *Survey Setup › Rebuild Setup* → *View/Edit Prefill Data › Upload
   Prefill Data* (nombre obligatorio `<appid>_prefill.data`; tildar *First row contains Field Names*;
   *Replace Existing Data*). Si hubo campos de más de 200 caracteres: `ALTER TABLE … MODIFY COLUMN …
   varchar(N)` con ~5 % de margen sobre el más largo, y **volver a cargar** (si no, quedan truncados).
9. **Usuarios de prueba en `prefill_data`:** si hay cuentas `sample%` en `emerge`, copiarlas a
   `prefill_data` con `job_title = 'TBD'` y `participant_fullname` = nombre + apellido. Si no hay: §
   Usuarios de prueba.
10. **Limpiar `_resp.html` en BBEdit y subirlo por MAC** (*app › Demographic Questions*, nombre
    `<appid>_resp.html`):
    - los cuatro demos de 360 primero;
    - opciones de Survey Version y Relationship: copiarlas de la base si ya existen, o cargarlas como las
      dio el PM — cada opción en su renglón con `O` + tab, empezando por `B_L_A_N_K`;
    - **sacar demos de fechas, identificadores únicos (SSO_ID), teléfonos, emails**;
    - reordenar bandas (edad, tenure).
    - Tip: con muchos demos, subir solo los demos (sin opciones) y reconstruir `resp_list` con los
      scripts Perl.
11. **Prefill linkage** (`rm=24`, o *Configure Prefill Linkage*): mapear demos a columnas · *Force all
    linkages to occur* · ⚠️ **E-Merge Data Field = Employee ID ↔ Pre-Fill Data Field = `emp_id`**.
12. **Participant Fullname:** `UPDATE prefill_data SET participant_fullname = CONCAT(first_name,' ',
    last_name)` (verificar 0 nulos) → `cleanup_values_with_different_case.pl` y
    `rebuild_resp_list_options.pl` sobre ese demo → `add_new_values.pl` sobre Job Title (por el `TBD` de
    prueba).
13. **Chequeos:** opciones de Survey Version y Relationship en orden en `resp_list` · todos con
    `job_title` y `participant_fullname` · linkage bien mapeado y por `emp_id` · conteo de registros ·
    *Rebuild Setup* (arma los índices) · `verify_survey_integrity.pl` — **la advertencia "records in
    prefill not in emerge" es esperable**.

### Carga final

1. **Backup de lo preliminar:** `prefill_data_prelim`, `resp_questions_prelim`, `resp_list_prelim`
   (`CREATE TABLE … LIKE` + `INSERT … SELECT`).
2. Pasos 1–7 de la inicial.
3. **Mantener la estructura de `prefill_data`** si el archivo final trae los mismos campos (`DESCRIBE
   prefill_data` y alinear en Excel). Importa sobre todo con **más de 100 columnas**: ahí la subida por
   `rm=21` puede fallar y hay que **importar directo a la tabla** (`DELETE FROM prefill_data` → importar →
   chequear conteo, emails y job titles nulos).
4. `participant_fullname` y usuarios de prueba como en la inicial.
5. ⚠️ **Si no hay demos nuevos, no volver a subir `_resp.html`**: correr
   `cleanup_values_with_different_case.pl` y `add_new_values.pl` para sumar valores nuevos a `resp_list`.
   Así **no cambian los Demo ID ni los índices** de opciones de un survey que ya está armado (misma lógica
   que la regla 3 de [[Perceptyx/procedimientos|procedimientos]]).
6. Chequeos de la inicial.

---

## Usuarios de prueba (leaders y raters)

> Esta es la página real. La que vino en el batch 3 (*360 Survey Test Leader & Raters Setup **Guide***)
> era una conversión automática fallida de esta.

- **No hacen falta los 30 usuarios de prueba** con menos de tres versiones: **~10 por versión** alcanza.
- **Plantillas** (`myappid_prefill.data`, `myappid_emerge.txt`, `myappid_resp.html`) en una carpeta de
  Google Drive: reemplazar `myappid` por el app ID (en los nombres de archivo y en el prefijo de los
  emails).

**Parte 1 — Archivos.**
- Si **todavía no se cargó** el archivo inicial: ajustar las opciones de Survey Version y Relationship en
  el `_resp.html` según el PM, subir los tres archivos, configurar linkage (`rm=24`, Employee ID ↔
  `emp_id`).
- Si **ya se cargó** (los demos existen): subir **solo los usuarios de prueba** del `_emerge.txt` a
  `emerge`, copiarlos a `prefill_data` (`sample%`, `job_title = 'TBD'`, `participant_fullname`) y sumar
  los valores nuevos con `add_new_values.pl`.

**Parte 2 — Tabla de retención** `prefill_data_360internalusers` (emp_id como clave, más nombres, email,
job_title, participant_fullname) con los `sample%`, para que **sobrevivan a las cargas automáticas**.

**Parte 3 — Leaders de prueba.**
- Que exista el status `participant` en `statuses` (si no, insertarlo).
- Un leader por versión: `INSERT INTO users (…)` desde `prefill_data` (ej. `sample01`), username tipo
  `participanttest_v1`, status `participant`, `approval_status = 'pending'`. El password va con el valor
  que trae la página.
- Su `ratee_id` = su `sequence` en `users` → `UPDATE users SET view = "01_03_07 = '<sequence>'"`.

**Parte 4 — `emerge`.**
- Para el rango de raters de ese leader: `ratee_id`, `participant_fullname`, `survey_version`,
  `survey_starts` = hoy, `survey_ends` = **2–3 semanas** después.
- Relaciones con `UPDATE … LIMIT n`: **Self = 1** (el propio `sample01`), Manager = 2 (uno), reportes = 3
  (tres), pares = 4 (tres), el resto según el proyecto. Chequear con un `SELECT` ordenado por `ratee_id`,
  `relationship`.
- Después: probar con *auth* y pasarle al PM los links de prueba por relación.

---

## Demo oculto de relaciones combinadas

Para reportar, por ejemplo, **Self / Manager / Others Combined** respetando umbrales mínimos. Va en
**`custom_queries`** y **`custom_query_options`** — **no** en `resp_questions` ni `resp_list`.

1. Ver las opciones del demo Relationship (`resp_questions`, `resp_list` con su índice) y el último Demo
   ID usado.
2. **Demo ID del agregado: prefijo `02_`** con la misma posición si está libre (Relationship `01_02_07` →
   agregado `02_02_07`).
3. `INSERT INTO custom_queries (qid, name)` → `'02_02_07', 'Relationship with Others Combined'`.
4. Una fila por grupo en `custom_query_options (qid, id, name, view, view_disp)`: Self → `01_02_07 = 1` ·
   Direct Manager → `01_02_07 = 2` · Others Combined → `(01_02_07 != 1 AND 01_02_07 != 2)`.
5. **Avisarle al PM el Demo ID**: él configura *Different minimum thresholds per demographic* para esas
   relaciones.

Los grupos cambian por proyecto (a veces solo Self + Others): **los define el PM en la tarea**.

---

## Automatización por cron

> ⚠️ **En transición (📣 Ignacio, 06/10/2026): el equipo está dejando las herramientas dispersas —jails,
> Querious— para hacer todo en SOS, incluidos los cron jobs y la ejecución de scripts.** Ignacio no tiene
> jail ni acceso al repo `cronjobs`. Lo de abajo es el procedimiento **documentado en Confluence**; la
> lógica del script (mapas de campos, bandas, transformaciones, `mac.cron_scripts`, verificaciones)
> probablemente siga valiendo, pero **dónde se edita, se prueba y se sube** puede ser otro en SOS. 🔍 Sin
> verificar cómo queda cada paso.
> **Actualización 06/10:** la guía de SOS lo confirma — **Cron Manager** tiene *Cron Builder* (crear con
> plantillas), *Cron Review*, *Scheduler* (horario y rerun) y *Script Editor*. Ver
> [[Perceptyx/services-os|services-os]].

Tareas: *Automation › New CRON build › 360v2 Data Import* y *… › Automated Comment Processing* (ver
Standard Forms en [[Perceptyx/procedimientos|procedimientos]]).

### 360v2 Data Import

El cron toma el archivo del SFTP del cliente y lo carga en `prefill_data` del app.

**Requisitos:** app activa · tarea con el **CRON logic form** (SFTP del cliente, ruta y nombre del archivo,
campos obligatorios, bandas) y el archivo inicial · archivo **UTF-8** `.txt`, `.csv`, `.pgp` o `.gpg` ·
**jail local funcionando** · acceso al repo `cronjobs`, al SFTP de archivo de cronjobs y a **MailHog** del
jail.

1. **Arranque:** pedir acceso a la base del master app (*projects*) · `git fetch -p --all && git pull
   --all` en el jail · verificar en el SFTP del cliente que el archivo está donde dice el form y es UTF-8.
2. **`prefill_data_all`:** pasar cada encabezado a formato de campo (`First Name` → `first_name`), sumar
   campos de bandas custom (`pyx_tenure`, `pyx_age`, `pyx_generation`) y una columna `filename` (`ALTER
   TABLE`). Hay un Excel de ayuda: *cron_fields_helper*.
3. **Archivos:** carpeta del cliente en `/usr/local/perceptyx/cronjobs/<cliente>` y su par en
   `cronjobs_files/<cliente>/working_360` → copiar las tres plantillas de `cronjobs/template/360` y
   renombrarlas `<appid>_data_import.pl`, `<appid>_ftp_download_batch`, `<appid>_ftp_upload_batch`.
4. **Download batch:** carpeta de origen (en self-service, normalmente `incoming/production_360`),
   carpeta de trabajo, extensión.
5. **Upload batch** (archivado): **no tocar la primera línea**; carpeta de trabajo; `-put *.zip` si el
   script comprime (default), si no la extensión del archivo; encriptados no se comprimen (`-put *.pgp`).
6. **Script principal** (`<appid>_data_import.pl`, se apoya en `cronjobs/perl/Base/OnboardExitBase.pm`):
   - namespace único (reemplazar `360Template` en las dos líneas);
   - `Configure()`: **líneas de prueba del jail sin comentar**, título del mail de log, settings de
     comentarios según el form (1 = on, 2 = off);
   - `GetDataFile1`: regex del nombre, CSV y delimitador; mapa **variables → encabezados** (claves
     globales y las que use el script) y mapa **encabezados → campos de `prefill_data_all`** (todos los
     que se llenan; columnas a ignorar con valor vacío);
   - `ParseDateValue`: formatos de fecha (hire/term/birth vienen por defecto; agregar los que falten);
   - `ProcessFirstAndLastName`: partir nombre completo si no viene separado;
   - `ProcessCalculatedDemographics`: transformaciones del form (ej. `M`/`F` → `Male`/`Female`, "Is
     Manager" según cantidad de reportes). **Trae código que copia `emp_id` a `sso_id`**: ajustarlo o
     sacarlo si no hay SSO;
   - `GetAgeBandValue`, `GetTenureBandValue` (usa la fecha de egreso si hay), `GetGenerationValue`: bandas
     default de Perceptyx, editables según el form.
7. **Probar en el jail:** `ssh` al jail → `dbcopy <appid>` (copia la base) → archivo inicial en la carpeta
   de trabajo → registrar el script en `mac.cron_scripts` **del jail** con tu email → `perl
   <ruta>/<appid>_data_import.pl` → consola limpia, mail en **MailHog**, `prefill_data_all` bien
   (bandas, `sso_id`, campos custom).
8. **Subir el código:** **comentar las líneas de prueba del jail** → branch en `cronjobs` → commit + push
   de los tres archivos → **merge request**.
9. **Programar** en `mac.cron_scripts` **de producción**: `script_name` (ruta completa), `run_time` (hora
   0–23, **hora del Pacífico**; medianoche = `"0 "` con espacio), días con `x`, `is_cron_server = 1` (0 =
   desactivado), `email_log_to` / `email_log_bcc`. Elegir con el CSP una hora con pocos crons.
10. **Primera corrida:** en el SFTP del cliente, **solo ese archivo** (mover viejos o de prueba a `OLD`) →
    **esperar 15 minutos** después del merge → `run_immediately = 1` en `mac.cron_scripts` → mail del
    cron → verificar log limpio, `prefill_data`, que el archivo **salió** del SFTP del cliente y **quedó
    archivado** en cronjobs.

### Automated Comment Processing

Requisitos: survey armado e idiomas configurados en el app.

1. Repo `cronjobs` alineado con master (`git checkout master && git pull`).
2. **Branch con el número de tarea: `PS-<DM Task ID>`** (ej. `PS-0001`).
3. Carpeta del cliente (nombre de la empresa en minúsculas, sin espacios; crearla si no existe).
4. Copiar `template/process_comments_template.pl` → `<appid>_process_comments.pl` y **poner el app ID en
   la línea 17**.
5. Commit, push y **merge request**; si hace falta, pedir el merge en **#cronjobs_dm**.
6. Registrar en `mac.cron_scripts` (**en la base EU si el app es EU**): ruta completa, `run_time` `20`
   (para poblaciones solo EU se puede pasar a `13`), los siete días, `is_cron_server = 1`, tu email.

🔍 **Esto es trabajo de desarrollo**: git, branches, merge requests, Perl sobre una clase base, pruebas
en un entorno propio. Es el lado del puesto que más se acerca a lo que Melanie describió como frontera
(*"growing deeper technical expertise"*), y al de Ignacio construyendo sus propias herramientas.
