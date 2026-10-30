# Plataforma — herramientas, tablas y glosario

Lo que Delivery Ops usa y toca. Cómo se combinan en cada tarea está en
[[Perceptyx/procedimientos|procedimientos]].

> Fuente: sesiones de training del 28/09 al 01/10/2026, conocidas por **notas de Gemini**. **Vigente
> al 2026-10-01.** 📣 salvo que se marque otra cosa. Nombres de tablas y scripts tal como los
> transcribió Gemini: la grafía exacta (guiones bajos, mayúsculas) **no está verificada**.

---

## Herramientas

| Herramienta | Para qué | Notas |
|---|---|---|
| **Salesforce** | Donde viven las tareas (tickets) | Se cierran con estado *Complete* + iniciales. 📣 Ignacio |
| **UDS** | ✅ **Unified Data Store** (Confluence *Activate / Nudge Setup*, 06/10). ⚠️ **Contradicción:** *Manager Heirarchy Tree* (engineering) lo llama ***User Directory Service***. 🔍 Probablemente la misma cosa con dos nombres en distintas épocas; la de Activate es la página más operativa. El almacén único de compañías, usuarios, roles y demográficos de la plataforma nueva (PIP); otros sistemas (Nudge Engine, binlog) se sincronizan contra él. Admin en *Administrator Portal › PYX Admin* | Login con Okta. ~~Qué es: sin confirmar~~ resuelto 06/10 |
| **MAC** | Registro de clientes y sus *master apps* (*Customers Table*, *Functions › Create New App*). **Desde el 26/10/2026 se entra por SOS › Customer Hub** (US y EU, Okta, sin password de MAC — 📣 Ignacio, [[KOS/Reglas\|Reglas]] § 9) | ✅ Confluence |
| **Okta** | Login único de Perceptyx **y** proveedor de identidad (SSO) de cada cliente: *Security › Identity Providers* (SAML 2.0), *Directory › Groups* (Group UUID del cliente) | Requiere Okta Verify. ✅ Confluence |
| **Service desk (Atlassian)** | *Auto Tickets* internos, ej.: crear usuario SFTP | ✅ Confluence |
| **Gainsight** | 🔍 Customer success; el doc dice que todavía no tiene un flag de admins de plataforma | ✅ mencionado en Confluence |
| **Plataforma (PIP) admin** | `app.perceptyx.com` / `app.eu.perceptyx.com` → engranaje → *Pyx Admin* → *Shadow Company*: *Platform Settings › Integrations*, *Data Management › API Tokens* | ✅ Confluence |
| **SSO Helper Script** (`Extract_SAML.py`) | Script de BBEdit: del metadata XML del cliente saca el certificado x509 formateado, el EntityID y la URL de SSO para Okta | ✅ Confluence |
| **Data Audit Script** | Audita el archivo del cliente antes del Data File Builder (entre otras cosas, nombres de columna reservados) | ✅ Confluence |
| **Jira (proyecto SPT)** | Seguimiento de engineering, ej.: SPT-721 | ✅ Confluence |
| **Data Specs Audit script** (`dataspecs_automation`) | Audita el archivo del cliente contra el data spec | ✅ Confluence |
| **FTP dmtask** | Donde el PM sube los Standard Forms antes de pedir trabajo (= *DM Task* en Transmit) | ✅ Confluence |
| **Repo `cronjobs`** (git) | Scripts de cron por cliente (`/usr/local/perceptyx/cronjobs/<cliente>`), plantillas en `template/`, base Perl en `perl/Base/`. Branch `PS-<DM Task ID>` + merge request; canal **#cronjobs_dm** | ✅ Confluence |
| **`mac.cron_scripts`** | Tabla que programa los crons (hora del Pacífico, días, `is_cron_server`, `run_immediately`) | ✅ Confluence |
| **MailHog** | Bandeja de prueba del jail para los mails de log del cron | ✅ Confluence |
| **Scripts Perl de demos** | `datafile_builder.pl`, `cleanup_values_with_different_case.pl`, `rebuild_resp_list_options.pl`, `add_new_values.pl`, `verify_survey_integrity.pl` | ✅ Confluence |
| **@Pyxee-csg** (Slack **#pyxee-csg**) | 🆕 **Bot interno de IA** que responde preguntas usando Confluence, knowledge bases y carpetas de Google. 🔍 Útil para las preguntas abiertas de este dominio | ✅ Confluence *WTC* |
| **@Pyxee-CVO** | 🆕 Otro bot de IA interno, *"with access to CVO KB"* (base de conocimiento de Customer Value). Responde citando la fuente. Al 06/10 **no sabía qué es MCP** | 📣 Ignacio, captura 06/10 |
| **Gainsight** | Customer success: CSAT de proyectos, métricas de adopción de Activate (nudges), **DRA firmado**, flags de clientes | ✅ Confluence |
| **Freshdesk** | Ticketing de **Customer Care** (soporte) | ✅ Confluence |
| **Postman** | Probar credenciales de la API (workspace *Platform Services*) | Si no está instalado: IT o manager. ✅ Confluence. 📣 Jackie, 21/09: **es lo único para lo que DelOps lo usa hoy** |
| **1Password** | Vault *Customer API*: entrega de credenciales por share link restringido y con vencimiento | ✅ Confluence. 📣 Jackie, 21/09: otro **vault aparte con los SFTP de los clientes** (al 21/09 la cohorte no lo tenía) |
| **Developer Portal** | Documentación de la API para el cliente | ✅ Confluence |
| **Querious** | Cliente MySQL (Mac) para consultar y actualizar las bases de cada survey | Hace falta una conexión **read-write** aparte para los `UPDATE`. ⚠️ **Al cambiar *Selected Database*, puede seguir mostrando el resultado de la base anterior** (27/10/2026: los conteos de un survey aparecieron como si fueran de otro). Mirar la base en la barra y repetir la query. US pide password SSH; EU no. ⚠️ **En retirada** a favor de SOS, pero **al 06/10 sigue siendo la herramienta de escritura** hasta que SOS habilite leer y escribir (📣 Ignacio) |
| **SOS** — ✅ **Services OS** | La plataforma interna de operaciones de Customer Value, organizada por el recorrido del cliente: soporte, diseño, launch, reporting, archivos, scripts. **Destino de la consolidación** (jails, Querious, crons). Entrar: VPN → Okta → tile *Services OS* → rol | Detalle y tabla de *qué reemplaza a qué* en [[Perceptyx/services-os|services-os]]. ✅ Confluence *Services OS — User Guide* (06/10) |
| **Operations Tools** (en la app, `ondemand.…`) | Operaciones sobre un survey sin SQL: backup de tablas (*Utilities*), add/update demographics, participant data, data file builder del manager tree. 📣 Jackie, 21/09: *Utilities › **Quality and integrity checks*** (= `verify_survey_integrity` con interfaz) y *Data › **Sync reporting demographics from participant data*** (resincroniza `all_data` tras reordenar); el que junta el inglés para traducir | Alternativa cuando faltan permisos de escritura en la base. Se espera que pasen a SOS |
| **Survey Setup › Survey Configurations** | Estado del survey (*Deactivation*), configuración de comentarios (Snowflake, modelo léxico/supervisado) | |
| **LE app / LE data file builder** | Carga de listas de participantes (*Bring Your Own List*) | El builder agrega bandas y corrige fechas |
| **Master app menu** | Encontrar el *master app ID* de un cliente | Se busca tipeando la inicial |
| **Reporting site** | *Trend mismatch report* y reportes | |
| **Transmit** | Cliente de archivos (SFTP): carpeta *incoming* de cada tarea | |
| **Text Expander** | Snippets: scripts de backup, queries de chequeo, `;me` para iniciales | Cada uno arma los suyos con lo que comparte el equipo. ✅ 16/10 (captura): además hay un grupo **compartido de la organización, *DM Snippets***, de **solo lectura** (los cambios se piden con *Request change*). Se busca y expande desde cualquier app con **⌘/**. Visto: ***Backup Table*** `;bck` (→ `mac.create_backup`, [[Perceptyx/procedimientos#Reglas que valen para toda tarea\|procedimientos § regla 1]]), `;terms` (sacar bajas anteriores a una fecha de corte) y `;updatesso` (reemplazar una URL en los emails y traducciones). ~~🔍 por el nombre, el `UPDATE` del SSO ID~~: **equivocado**, la captura del 16/10 muestra otra cosa. Los dos están en [[Perceptyx/procedimientos|procedimientos]]. Otros nombres que aparecieron en las búsquedas (✅ solo nombre y abreviatura, contenido no visto, 16/10): *Update translation MD5* `;md5` (✅ contenido visto 29/10: `md5(lower())` sobre `need_translation` y `translated_phrases`, [[Perceptyx/procedimientos#Traducciones|procedimientos § Traducciones]]), *Update Trend Mismatches* `;dmtaskrbt4`, *Update email to no-email* `;noemail`, *Comments - Themes Update* `;dmtcommentthemes`, *Dare.bulk_operation to update data in batches* `;dbre`, *dbre join instead of inner join* `;joindbre`, *Join alternative* `;join2`, `;reorder` (`set @s = -1; update ().resp_list set option_order…`), `;nogap` (`UPDATE new_menu_options SET universal = 0…`), `;tgthier`, `;dataload`, *Datafile - Remove Terms* `;dmtterm`, *MySQL export query* `;sqlexport`, *Database Deployment - New App* `;dmtnewapp` / *Clone App* `;dmtcloneapp`, *Users - Reporting User Setup* `;dmtuseraccts`, *Survey Closed Checklist Task Template* `;dmtaskdc8`, *Internal Communication Survey Close* `;slackclose`, *Waggl - Create / Update Dashboard* `;dmtwdashboard`, *Waggl - Create/Update Existing Sub…* `;dmtwsubscription`, *Waggl - Roster QA* `;dmtwrosterqa`, *Waggl - Roster Upload* `;dmtwrosterupload`. 🔍 Es un mapa de tareas que el equipo resolvió alguna vez: antes de armar una query, buscar ahí con ⌘/ |
| **BBEdit** | Editor de texto (audit files, fórmulas) | Gemini lo escribe "DBEdit" |
| **Excel + helper formulas** | Generar `UPDATE`s y reordenar índices | Documento de helper formulas compartido por el equipo. 📣 **Ignacio, 08/10: tiene una copia guardada en su equipo de trabajo**, directo en **Descargas** (`Downloads`) |
| **Snowflake** | Procesamiento y tematización de comentarios | Ver bug del modelo léxico |
| **Fresh Desk** | Soporte al cliente | Los pedidos que llegan por ahí o por mail **tienen que convertirse en ticket** (huddle 01/10) |
| **LEB** | ✅ **Listening Event Builder** — el constructor de surveys de PIP. Puede pisar cambios hechos por fuera (toggles) | Ver [[Perceptyx/procedimientos#LEB (Listening Event Builder): toggles, archivos finales, clonado|procedimientos § LEB]] |
| **LEAP** | = **LEB** mal transcripto por Gemini. **Asumido** (decisión de Ignacio, 06/10) | — |
| **Nudge Engine Admin UI** (`ne-admin-ui`) | Configurar el motor de nudges por cliente | Ver [[Perceptyx/nudge-engine|nudge-engine]]. ✅ Confluence |
| **Temporal** | Motor de workflows: imports y corridas del Nudge Engine devuelven una URL de seguimiento | ✅ Confluence |
| **Slack** | Preguntas al equipo; buscar en el historial antes de preguntar | |
| **Confluence** | Documentación (ej.: *snowflake comments*) | |
| **Certinia** (en Salesforce) | Carga de horas (time entry) — 📣 Ignacio, 06/10 | Usar *Time entry* (menú *More*, a la derecha), **no** *Time sheet entry*: copiar el proyecto a *project assignment*, elegir milestone, cargar horas |

~~**Accesos al 01/10/2026:** Andrea, Guillermo e Ignacio dieron `command denied` al escribir en la base
de producción; Jackie lo está mirando.~~ SUPERSEDED 06/10: Ignacio **ya tiene permisos de escritura**
(📣 Ignacio). Si vuelve a aparecer `command denied`, el backup sale igual por Operations Tools ›
Utilities. ✅ **23/10/2026:** `INSERT command denied` en la conexión RW de **EU** (import de un late add). 🔍 El permiso
de escritura del 06/10 sería solo de US, o por servidor: pedido a Jackie. ~~🔍 solo de US~~ SUPERSEDED (29/10/2026): 📣 Ignacio, **en Querious no tiene escritura ni en EU ni en US; en SOS › Database Tools sí, en los dos.** ✅ 30/10: `show grants for current_user()` en la conexión *EU RW* devuelve `GRANT SELECT ON *.* TO imoll@%`; Jackie dice que en EU hay un login de lectura y otro de escritura (abierta en [[Perceptyx/_indice|_indice]] § Preguntas abiertas). Ese chequeo es la forma rápida de saber qué permite un login. Las escrituras van por SOS (*Preview change* hace backup de cada fila y tiene Undo, [[Perceptyx/services-os|services-os]] § Lectura o escritura); los backups manuales, por *Operations Tools › Utilities*. Las credenciales de la conexión read-write están en el chat
de Jackie — **no se copian al vault**.

### URLs de trabajo

Para encabezar cada respuesta sobre un ticket con las herramientas y sus links ([[KOS/Reglas|Reglas]] § 9).
`<app_id>` = el ID del survey/app (ej. el de la tarea); EU: `ondemand.eu.perceptyx.com`.

| Herramienta | URL / acceso | Fuente |
|---|---|---|
| **App (Advanced Reporting)** | `https://ondemand.perceptyx.com/<app_id>/index.cgi?rm=<pantalla>` | ✅ capturas 08/10 |
| › Survey Admin | `rm=admin` | ✅ |
| › User Editor (*View/Edit Users*) | `rm=users_editor` | ✅ 08/10 |
| › Manager Hierarchy Tree (*Settings › Add Users*) | `rm=managers_tree` | ✅ 08/10 |
| › Operations Tools | `rm=operations_tools` | ✅ 08/10 |
| › Report Editor › Configuration (toggles: Snowflake, modelo de temas, *Deactivate Survey?*) | `rm=configure` | ✅ capturas 30/10 |
| › Translation Tool · Emails | `rm=translation_tool` · `rm=survey_launch` | ✅ 21/09 |
| **SOS** | `https://services-os.ssvcs.pyx-int.com/` — Perl Scripts: `#perl` | ✅ captura 08/10 |
| **Querious** | App de escritorio, base = `<app_id>`. Credenciales: fuera del vault. **Hosts** (📣 Ignacio, 30/10), por túnel SSH al host `pms` de su región: US solo lectura `classic-mysql-us-ro.production.us.pyx-int.com` · US lectura/escritura `classic-mysql-us.production.us.pyx-int.com` (SSH `pms.perceptyx.com`) · EU solo lectura `classic-mysql-eu-ro.production.eu.pyx-int.com` · EU lectura/escritura `classic-mysql-eu.production.eu.pyx-int.com` (SSH `pms.eu.perceptyx.com`). En los dos de lectura/escritura, el login de Ignacio tiene **restringidos los comandos de escritura** | ✅ capturas 08/10 · 📣 30/10 |
| **Excel** | Local. Helper formulas en Descargas (§ arriba) | 📣 Ignacio |

---

## Tablas de un survey

Cada survey tiene su base (**MySQL 8.0** ✅ Confluence). Cómo se conectan y por qué: [[Perceptyx/modelo-de-datos|modelo-de-datos]]. Las tablas que aparecieron:

| Tabla (según Gemini) | Qué guarda |
|---|---|
| `rest questions` | Definición de preguntas y demos: IDs, opciones, índices. 🔍 **Nombre real muy probablemente `resp_questions`** (aparece en Confluence *PFS LEB Learnings*; Gemini lo oyó "rest") |
| `surv_groups`, `resp_groups`, `surv_questions`, `surv_options`, `resp_list`, `progress`, `filestorage`, `categories`, `category_qid` | Estructura del survey que **LEB reescribe** al previsualizar / activar. ✅ Confluence |
| `emerge`, `emerge_group`, `emerge_group_rel`, `survey_launch_batches`, `survey_launch_emails`, `survey_launch_batched_group_rel`, `dc_info` | Lanzamiento y distribución del survey; no se copian al clonar un survey managed. ✅ Confluence |
| `prefilled data` | Valor de cada demo por participante (la fuente). ✅ Nombre real: **`prefill_data`** (Confluence, 06/10) |
| `prefill_data_all` | Lista completa de empleados cargada desde el data file (típicamente en el master app). ✅ Confluence |
| `users`, `emerge`, `survey respondents` | Tablas que se sincronizan con UDS por binlog. ✅ Confluence |
| `all data` | Datos para reportes: respuestas + índices de demos. ✅ Nombre real: `all_data` |
| `prefill_linkage_ids` | Una fila: qué columnas unen `emerge` con `prefill_data` ✅ |
| `settings` (del app) | Configuración; ej. `app.uds_binlog_config` = qué tablas van por binlog ✅ |
| `ss_app_invitees` | Event Builder (arquitectura nueva): invitados con columna JSON para el esquema variable ✅ |
| `prefill linkage` | Vínculo entre prefill y preguntas. ✅ Nombre real: `prefill_linkage` |
| `manager tree` | Jerarquía de managers (también tiene manager ID). ✅ Nombre real: `managers_tree` (con `tree_path` y `trend_emp_id`) |
| ~~`Q condition`~~ → **`surv_questions_conditional`** | Condiciones de branching. ✅ Nombre real visto en Querious (23/09); *q_condition* existe pero como **columna** de `popup_definitions` |
| `popup_definitions` | Definiciones que aparecen al pasar por una palabra; pueden tener condición por población ✅ |
| `my_queries`, `comparison_views`, `custom_crosstab_options` | Filtros guardados, vistas comparativas y crosstabs: dependencias de índices de demos ✅ |
| `trend custom linkages` | Mapeo de demos contra surveys anteriores para trends. ✅ Nombre real: `trend_custom_linkages` |
| `comments theme matches` | Temas asignados a cada comentario (`model ID = 10` = supervisado) |

---

## Glosario

| Término | Qué es |
|---|---|
| **Demo** | Demográfico (edad, tenure, ubicación, nivel de management…) |
| **Banding** | Agrupar un valor continuo en bandas (generación, edad, tenure de 10 años) |
| **Branching** | Lógica condicional del survey según respuestas o demos |
| **Trend / trended** | Comparar un survey con surveys anteriores del mismo cliente |
| **Manager tree** | Jerarquía para reportes por manager |
| **Clearout** | Limpieza previa al lanzamiento (comentarios de prueba) |
| **Audit file / audit report** | Salida de una carga; se le entrega al PM |
| **360s** | Línea de producto de evaluaciones 360 |
| **Busy season** | Temporada alta; según el equipo afloja en **noviembre–diciembre** (huddle 01/10) |
| **EU / US** | Entornos separados por región |
| **Master app** | La aplicación madre de un cliente en MAC (`ondemand.perceptyx.com/<id>`); de ella cuelgan los surveys. Una por cliente |
| **PIP** | People Insights Platform — la plataforma 2.0 (toggle *Platform 2.0 Experience* en UDS; indicador en Salesforce) |
| **Binlog listener** | Mecanismo nuevo que sincroniza tablas de una aplicación con UDS. Reemplaza a Listening Home / triggers |
| **LH** | Listening Home — mecanismo viejo de sincronización |
| **PFS** | ✅ ***Platform Services***, **nombre anterior de Delivery Ops**: Jackie, 16/09 — *"right before you guys started, we used to be called platform services and we changed our name to delivery operations… wherever you see PFS, that's us"*. Las plantillas de Certinia todavía lo usan |
| **PS** | 🔍 Probablemente Professional Services |
| **Special Projects** | Equipo que migra clientes existentes a binlog listeners (vía tarea PFS) |
| **AE / CSM** | Account Executive / Customer Success Manager — confirman lo contractual (ej.: cantidad de admins) |
| **Shadow Company** / **Switch to company** | En UDS, entrar a operar una compañía como si se estuviera dentro (US / EU) |
| **Group UUID** | ID de 36 caracteres del grupo del cliente en Okta = `uds_company_id` en MAC ✅ |
| **`EU-`** | Prefijo obligatorio del nombre de un cliente EU en UDS, Okta y MAC ✅ |
| **Platform Admin** | Admin del cliente con acceso al *Administrator Portal* de PIP; 2–5 por cliente ✅ |
| **ASK** | 🔍 Producto self-service (sus tablas `emerge` ya tienen binlog) |
| **Listening Event Builder (LEB)** | ✅ Constructor de surveys de PIP; puede usar la URL de SSO si hay feed automatizado + binlog + SSO |
| **Managed survey** | Survey con el toggle *managed*: al clonarlo, los toggles de LEB se deshabilitan y las tablas de datos quedan vacías ✅ |
| **Team Task Queue** | La cola de tareas de cada equipo de PM; dueño: sus PFS partners ✅ |
| **Assist / Team Assist** | Columna de ayuda opcional / workflow de ayuda requerida (con Slack) ✅ |
| **SSO Team** | `pyx_sso@perceptyx.com`: arma la conexión SSO con el cliente y la prueba. 🔍 Si es parte de DelOps, sin confirmar |
| **Metadata (SAML)** | XML con certificado, EntityID y URL de SSO. Hay dos: el de Perceptyx (va al cliente) y el del cliente (se carga en Okta) |
| **Routing rule** (Okta) | Regla que manda a los usuarios de un cliente (por `company_ID` = Group ID) a su IdP |
| **Assertion Consumer Service URL** | La URL de SSO del cliente; va en el *Login URL* de UDS (en EU, con un sufijo fijo) |
| **Valor de autenticación** | Lo que identifica al usuario en el SSO: Employee ID u otro (recomendado) o email |
| **Palabras reservadas** | Nombres de columna que MySQL 8.0 no acepta sin comillas (`group`, `order`, `key`…) — rompen cargas directas a LEB |
| **Líneas de producto** | ~~**Ask** (Classic / Self-Service) — encuestas · **Sense** (Classic) — lifecycle · **Cultivate – 360 Feedback** · **Dialogue** · **Activate**~~ **SUPERSEDED 06/10 — nombres viejos.** Según Melanie (PM Power Hour, ~principios de 2026): **Sense, Cultivate, OnDemand y "Perceptyx Insights Platform" son nombres viejos**; ahora es **la plataforma Perceptyx**, con la suite **Discover** de *listening channels* (**point-in-time**, **lifecycle**, crowdsource, 360…) y los **agentes de IA**: *employee activation agent* (**Activate**, nudges), *conversational listening* (beta) y *narrative analysis agent*. **Grow** ya no se usa. Los Standard Forms y muchas tablas siguen usando los nombres viejos (`ondemand`, `Sense – Classic`) |
| **Listening channel** | Suscripción a una parte de la plataforma; incluye self-service y es requisito para comprar un evento gestionado ✅ (📣 Melanie) |
| **DOS / DOP** | *Description of Service* / *Description of Product*: las páginas del contrato que describen cada SKU. En simplificación en 2026 |
| **End size** | Tope de participantes del contrato; figura en la página de detalles del proyecto en Certinia |
| **Squeaky Clean** | El proceso/reporte de higiene de datos de proyectos en Certinia (fechas, horas, revisión del manager) |
| **Amsterdam** | ✅ **DC Amsterdam**: el Data Collector que se usa hoy en la mayoría de los surveys (📣 Jackie, 23/09); Mosaic es el nuevo y mantiene paridad de estilo con él |
| **SmartCat** | Proveedor de traducción con **revisión humana** (🔍 hoy con IA de base): más caro, mejor, **~5 días**. La alternativa es **Microsoft**: automática, inmediata, casi gratis. Ver [[Perceptyx/procedimientos|procedimientos]] § Traducciones (📣 Jackie, 21/09) |
| **Translation tags** | Envoltorio del texto traducible en emails (y survey): **`[%- obj.translate_this("…") %]`** (✅ captura 21/09). El texto va **entre las comillas dobles** del tag. **Comillas dobles adentro rompen el email** → pasarlas a simples (📣 Jackie, 21/09) |
| **Merge fields** | Campos de `prefill_data` que se insertan en un email (*Hola [first name]*) |
| **Bucket** (traducciones) | Agrupación de frases en *Translate Survey Content*; separa, ej., lo ya traducido de un app anterior |
| **Core library** (traducciones) | Traducciones propias de Perceptyx del texto estándar; se usan siempre |
| **Subclass file** | Archivo de código que **recodifica una parte chica** de una plantilla para un cliente (ej. página de PIN). Se edita y publica desde SOS › Customizations (merge request a `apps @ master` en GitLab); se intenta evitar (📣 Jackie, 21/09). 🔍 En la pantalla de SOS correspondería a *custom code* o *template overlay* |
| **Code freeze** | Período (temporada alta de launches) en que se evitan los deploys de código, subclasses incluidas |
| **Boomi → Merge** | Sistema de **ingesta de datos** actual (Boomi) y su reemplazo en curso (Merge). 📣 Jackie, 21/09 |
| **`progress`** (tabla) | **Timestamp por página** de cada respondente: cuánto tarda en pasar el survey (📣 Jackie, 21/09) |
| **AE** | Account Executive (ventas) |
| **Lifecycle event** | Survey continuo disparado por un evento del empleado (candidato, ingreso, egreso), alimentado por cron. Tiene *add-ons* (email alerts, exit launch pad, raw data extract, anonimización) |
| **CRON build** | Armado de una carga automática; categoría *Automation › New CRON build › …* |
| **Data spec** | Formato exigido al archivo del cliente. 🔍 Por las excepciones: CSV con coma, `customerid_demographic_data_file_YYYY-MM-DD.csv`, emp_id y columnas únicas, PGP/GPG si va encriptado |
| **Trend Mismatch Report** | Excel con las opciones de demo que no coinciden entre el app actual y el de trend; insumo de `trend_custom_linkages` |
| **`trend_custom_linkages`** | `cond1` (app actual) · `trend_app_id` · `cond2` (app anterior). El par `cond1`+`trend_app_id` no se repite |
| **Trend Report Systems** (MAC) | Con qué apps trendea un app (hasta 5; más, por `mac.trend_apps`) |
| **Jail** | ✅ **Entorno de desarrollo propio** de cada uno (`<usuario>.perceptyx.com`): copia de bases con `dbcopy <appid>`, clon del repo `cronjobs`, MailHog para ver los mails. Ahí se prueban queries y scripts antes de producción (Confluence *Automation Setup – 360*, 06/10). ⚠️ **Se está dejando de usar** a favor de SOS (📣 Ignacio, 06/10); ~~Ignacio no tiene jail.~~ SUPERSEDED (30/10/2026): ✅ Ignacio tiene usuario en el **host de scripts de PM**,
`pms.eu.perceptyx.com` (US: `pms.perceptyx.com`, SG: `pms.sg.perceptyx.com`). Se entra por `ssh <usuario>@pms.eu.perceptyx.com`
o con Transmit (SFTP). Es FreeBSD, con roles *appserver, redis, devjail*. Cada usuario tiene `/usr/home/<usuario>/` con
`script_input/` y `script_output/`, y los scripts están en `/usr/local/www/perceptyx/perl/scripts/`. El banner explica que
los scripts conectan a la MySQL de producción con **credenciales propias de cada usuario**, en las variables
`MYSQL_HOST`, `MYSQL_USER` y `MYSQL_PASS`, que se cargan desde `~/.profile`; los usuarios salen de un pillar de Salt.
**El 30/10 a Ignacio no le anduvo:** `proot` dio *command not found*, `perl comments_verify_steps.pl` dio *Can't locate
DBI.pm* y `mysql` intentó un socket local. 🔍 Todo apunta a que su `~/.profile` no tiene el entorno armado: falta
`proot` (que en otros usuarios probablemente prepara Perl) y faltan las credenciales. Lo arregla quien da de alta los
usuarios. 📣 **IT Help (Caroline Amaro, 30/10):** el *DBI.pm* aparece cuando la sesión usa el **Perl del sistema**. La
solución es `perlbrew switch perl-5.28.1`, salir y volver a entrar. Si después falta algo, la cuenta en el host la
termina de armar **#team-infraplat**. ✅ **Probado el 30/10:** después de `perlbrew switch perl-5.28.1` y de volver a
entrar, `perl -v` da 5.28.1 y `perl -MDBI` anda. `MYSQL_HOST` y `MYSQL_USER` siguen vacías, y el script corta con
`DBI connect('<app>:classic-mysql-eu.production.eu.pyx-int.com','',...) failed: Access denied for user 'imoll'@'10.80.101.15'
(using password: NO)`. **El Perl ya está; faltan las credenciales en `~/.profile`.** Eso lo da de alta #team-infraplat
(pillar `pillar/common/users/pms/eu/init.sls`). ⚠️ En ese host **no se usa `sudo`**: es compartido, y `sudo rm -rf /tmp/pyx` o `service mysql-server start`
son comandos de un jail local, no de este host ([[Perceptyx/procedimientos#Comentarios con modelo léxico (workaround de bug)|procedimientos § Comentarios con modelo léxico]]). 📣 Jackie, 21/09: hay jail **de producción** y **local de test**; los locales **ya no se crean y se dan de baja**. Para practicar: los surveys del master app ***LEB enablement*** |
| **360v2** | Tipo de app de *Cultivate – 360 Feedback*. Leader (ratee) + raters; demos propios Survey Version, Relationship, ratee_id, Participant Fullname. Ver [[Perceptyx/cultivate-360|cultivate-360]] |
| **CRON logic form** | El formulario que define una automatización (SFTP, archivo, campos, bandas, transformaciones) |
| **`prefill_data_all`** | Lista completa de empleados que carga el cron (fuente de verdad del master app) |
| **`custom_queries` / `custom_query_options`** | Demos "ocultos" calculados (ej. relaciones combinadas del 360, ID con prefijo `02_`) |
| **`rm=`** | Parámetro de URL del app para ir a una pantalla: `rm=operations_tools`, `rm=24` (prefill linkage), `rm=21` (upload prefill), `rm=configure`, `rm=admin` |
| **CSP** | ✅ ***Content Security Policy*** (📣 Ignacio, 06/10): cabeceras de seguridad HTTP de los dominios de Perceptyx (proyecto de seguridad 2026 tras pentests). ⚠️ **No encaja con el uso en la guía de cron del 360** (*"work with the CSP on the schedule"*): ahí es 🔍 otra sigla, probablemente un rol de persona. Esa queda abierta El 06/10 el bot Pyxee-CVO propuso *Customer Success Partner*, **pero solo después de que Ignacio sugiriera "Customer Support something", y citando una transcripción donde la sigla no aparece**: no cuenta como dato (Reglas § 1) |
| **SOT** | *Source of Truth*: la base MySQL del survey, contra la que SOS cruza UDS y Okta ✅ |
| **DC vNext** | ✅ *Data Collector vNext*: la versión nueva de la aplicación que recolecta respuestas (y carga los demos a `all_data`). Lo que no es DC vNext sigue necesitando una columna por demo en `prefill_data` |
| **Mosaic** | ✅ **DC Mosaic = DC vNext** con nombre de marca: el Data Collector nuevo (toma el survey de LEB, escribe en MySQL Classic por un adaptador). Incluye el *Conversational Listening Agent*. Ver [[Perceptyx/dc-mosaic|dc-mosaic]] |
| **CLA** | *Conversational Listening Agent*: survey conversacional con un agente, parte de DC Mosaic ✅ |
| **OD** | Ask / **OnDemand** (el survey builder clásico; `ondemand.perceptyx.com`) ✅ |
| **Managed 360 / SS360** | 360 operado por Perceptyx (= PYX-Led = Classic, 360v2) / 360 self-service del cliente ✅ |
| **Advanced Reporting ≠ Advanced Analytics** | El primero es reporting **legacy**; el segundo (*Analytics Studio*) es el **nuevo** ✅ |
| **GovCloud US** | Tercera región de datos, además de US y EU (Mixpanel de DC Mosaic) ✅ |
| **PYX-led / Self-led** | Surveys operados por Perceptyx (MySQL, una base por evento) / self-service del cliente (vNext, PostgreSQL + Snowflake en 360) ✅ |
| **Attributed demographics** | = *prefill demographics*: demos que se completan solos desde el HRIS del cliente, no los contesta el respondente ✅ |
| **Data Hub** | Ingesta de usuarios a UDS conectada a la fuente del cliente (`uds_active = 3`) ✅ |
| **`uds_active`** | `2` en el alta normal; `3` = ingesta por Data Hub (el binlog lo ignora) ✅ |
| **WTC** | ✅ ***Workforce Transformation Consulting*** (📣 Ignacio + Confluence, 06/10): el equipo de consultores (experiencia del empleado, L&D, ciencia del comportamiento) que asesora al cliente a nivel ejecutivo; sus entregables son **Activate, EP y Design**. Es uno de los roles de SOS |
| **EP** | 🔍 *Executive Presentation*: la presentación de resultados al cliente (*"EP Readout"*, QA de *"exec presentation files"*) — la hace WTC |
| **ERC**, **I2I**, **EXO / EXOps** | Siglas del lado de consultoría sin expandir. **EXOps** es una de las cuatro familias de rol del estimador de horas. **I2I** = 🔍 *Insights to Impact* (workshop del catálogo) |
| **CSQL** | Oportunidad comercial que levanta servicios hacia el CSM cuando el cliente pide algo fuera de contrato (más participantes que el end size, más idiomas, más dashboards). 🔍 *Customer Success Qualified Lead* |
| **BMS** | *Be More Smarter*: tours y guías dentro de SOS ✅ |
| **Overlay / db_override** | Capas de customización de plantillas de un survey (sobre el *apps-repo* / editada en la base) ✅ |
| **`tree_path`** | Camino desde la raíz en `managers_tree` (`ceo.vp.dir.emp`); filtra toda la organización debajo de un manager ✅ |
| **Snapshot (árbol)** | En UDS, una jerarquía congelada al crearla, asociada a un survey; Draft → Live → Closed ✅ |
| **Dialogue** | Producto (ver líneas de producto); sus comentarios van a Snowflake para NLP. 🔍 *Crowdsource* parece su nombre de código |
| **DM** | ✅ ***Data Managers*** (engineering, *DC Mosaic Technical Overview*: *"Engineers / Project Managers / Data Managers"*). Rastro de un nombre anterior del equipo: carpeta SFTP *DM Task*, branches `PS-<DM Task ID>`, y engineering habla de *"Operations/DMs"* como quienes arreglan `all_data`. Linaje probable: **DM → PFS → Delivery Ops** |
| **Certinia task** | La unidad de trabajo: una **tarea de proyecto de Certinia** dentro de Salesforce (con *Attachment URL*, categoría, comentarios). Lo que se llamaba "ticket" |
| **SKU** | Código de servicio vendido (`PS-EVENT-ADD-…`, `PLATFORM-ADD-…`; `-1T` = una vez). Ver [[Perceptyx/catalogo-servicios|catalogo-servicios]] |
| **Change order** | Pedido formal cuando algo pasa el alcance contratado |
| **People Insights Model** | El modelo de contenido estándar de Perceptyx; punto de partida de surveys y del mapeo de nudges |
| **FedRAMP / US Citizen Support** | Clientes del sector público de EE.UU.: solo personal **ciudadano estadounidense** puede tocar sus sistemas, datos o tickets |
| **DCT** | 🔍 Sin expandir; nombre de la sesión de QA de branching del 02/10 (*QA DCT*). ¿*Data Collector Test*? |
| **App ID con `OD`** | App de OnDemand → `ondemand.perceptyx.com` / `ondemand.eu.perceptyx.com` (📣 Jackie, 23/09) |
| **Revert to draft** | En LEB, vuelve el survey a borrador; **borra las respuestas** |
| **HRIS data available** | Opción de LEB para traer los invitados del master app (feed por SFTP o conector) |
| **Info Needed** | Estado de una tarea de Certinia cuando falta algo del PM o del cliente |
| **DC Amsterdam** | ✅ El colector de respuestas que se usa mayormente hoy (Jackie, 23/09); Mosaic es el nuevo |
| **`rm=18&tbl=<tabla>`** | Ver/editar una tabla del survey desde el app, a mano. ✅ El parámetro es **`tbl`** (link de *View/Edit Prefill Data*: `rm=18&tbl=prefill_data`); en el audio sonaba *"table equals"* |
| **Operations Tools** (`rm=operations_tools`) | ✅ Catálogo por secciones (*Data Collector / Survey*, *Participant Data*, *Utilities*, *Utilities: Product & Technology*, *Deprecated*), cada herramienta con los productos a los que aplica (360, Ask, Sense) y **Run / Download / Help**. Vistas: *Participant Data* → Add / Update Demographics, Add missing demographic options, **Build Hierarchy from Loaded Data**, Create demographic options from participant data, Data File Builder (✅ 16/10: *Process Data* = *Export Files (for LEB)* / *Export Files* / *Direct Import (drops existing participants)*), Participant Count by Demographic Report, Populate Survey Launch Fields, Remove Ineligible Participants · *Utilities* → Backup Table, Check Bad Email Domains, Clear Data, Healthcare Data Extract, Index Demographics, Manage Quality & Integrity Email Notifications, Populate Initial Dummy Translation, **Quality and Integrity Checks** (devuelve un `.xlsx`), Translation Export |
| **Managed Settings** (LEB) | ✅ Pantalla del builder: toggle **Enable DC Mosaic** (*"By default, managed events use DC Amsterdam"*) + **Sync Settings** (Use LEB Data Collector / Filestorage / Categories). Si hay cambios sin aplicar: banner *"change pending to be reviewed"* → **Review Changes**. Menú de LEB: Overview, Managed Settings, Content, Styling, Invite, Communications, Settings, Launch |
| **Reporting site** | `www.perceptyx.com/<app_id>` (EU: `eu.perceptyx.com/<app_id>`): el sitio de cada survey; también tiene la configuración (*Functions › Survey Setup*) |
| **Master app / self-service app** | La app del cliente en la plataforma (`ondemand…`), desde donde se arman los surveys en LEB |
| **Self-service / guided / managed** | Niveles de servicio: lo arma el cliente / el cliente con ayuda de los PMs / Perceptyx (lo más común para DelOps) |
| **QID de demo `PP_SS_07`** | `02` = armado en LEB, `01` = classic; `SS` secuencia; `07` = demo del archivo. Preguntas: 4 dígitos, los dos primeros = página ✅ (Jackie, 16/09) |
| **`R249`** | Q type de la escala de favorabilidad (*strongly agree … strongly disagree*) |
| **Ready to Start** | Estado que hace aparecer una tarea en el workspace de DelOps (con fecha de vencimiento y resource role Platform Services) |
| **TSM** | Technical Success Manager: rol de onboarding técnico de clientes nuevos (🔍 el de Guillermo) |
| **DO** | Delivery Ops: **`#do_support`** (canal de Slack), *DO Dash*, *DO %* (Salesforce) |
| **Survey Admin Links** (`rm=admin`) | ✅ *Functions › Survey Setup* del reporting site (*Advanced Reporting*). Botones **Rebuild Setup Configuration** (el *"Rebuild Setup"* de las guías) y **Flush All Caches**. Secciones: **Report Menu Setup** (Survey Configurations, Survey Themes, Configure Toolkit, Configure Executive Presentation, Configure Dashboard, Menu Options) · **Survey Content Setup** (Emails, Respondents, Launch Schedules · DC Templates · Popup Definitions · **Conditional Survey Questions** · Actionable Insights · Category Mapping · Selected Languages) · **Demographic Data Functions** (**View/Edit Prefill Data**, **Demographic Hierarchy Tool**, **Custom Trend Mapping**) · Translation Functions (**Translate Survey Content** → `rm=translation_tool`) · **User Administration** (Users, Statuses, User Permissions, View User Activity, Send User Accounts) · **Comment Report Functions** (Standard Themes, Custom Theme Keywords, Comment Rules, Upgrade to Comments 2018) — ✅ captura 21/09 |
| **Menú del reporting site** | Report Editor (nuevo), Dashboard, Favorability, Gap, Trend y Hot Spot Reports, Comparison / Reference / Life Cycle Reports, View Action Plans, **Functions** |
| **Mapping** (UDS) | Vínculo de un usuario de UDS con un survey o un acceso a reportes; un usuario puede tener muchos ✅ |
| **Binlog drift** | Demora en la sincronización con UDS; se mira en el *PM Dashboard* de la página de SPT ✅ |
| **Divergent users** | Dos registros de UDS para la misma persona (uno por email, otro por emp_id) ✅ |
| **SPT** → **CVOps** | Ex *Special Projects Team* (🔍 expansión); ✅ **hoy se llama CVOps** (Services OS User Guide). SPT sigue siendo el prefijo de su **proyecto de Jira** (SPT-721) |
| **Record Deletion / Participant Identifier Removal** | Las dos opciones de borrado a pedido del cliente ✅ |
| **DRA** | ✅ ***Data Release Authorization*** (*Description of Service – Perceptyx (2025-09)*, leído el 06/10; lo había adelantado el bot Pyxee-CVO). *"May be required depending on the data provided"* en Data Export, Custom Report y Mayflower/ITSG. Se **marca en Gainsight**; Customer Care lo verifica ante un export de datos crudos; requisito para la API |
| **Technical Contact / Technical Owner** | La persona del cliente que recibe las credenciales de la API ✅ |
| **DM Task (US/EU)** | Carpeta del SFTP (vista en Transmit) donde se guardan los archivos por cliente ✅. 📣 Jackie, 21/09: son **dos conexiones** (*DM Task* y *DM Task EU*), el lugar donde **el PM deja los archivos** para DelOps |
| **Snippets nombrados** | `;me` (iniciales), `;apiconfirm` (acuse de API), `;apicredentials` (entrega de credenciales) |
| **Push / Pull** | Integración de datos: el cliente sube archivos por SFTP / Perceptyx los trae de su HRIS ✅ |
| **Platform Onboarding** | Equipo que hace el onboarding inicial del cliente nuevo y pasa las integraciones a PFS ✅ |
| **Nudge / rationale / job type** | Ver [[Perceptyx/nudge-engine|nudge-engine]] |

### Deformaciones de Gemini

Las notas automáticas cambian la jerga. Equivalencias deducidas del contexto (🔍 salvo que se
confirmen):

- *Pearl* = **Perl** · *DBEdit* = **BBEdit** · *perceptics* = **Perceptyx**
- *get manager accounts* (*"get pearl get manager accounts"*) = 🔍 el script **`get-mgr-counts`** (por el contexto: app ID, archivo de conteos) · *in action* = **inactive** · *SSL ID* = **SSO ID** — call del 09/10
- *Representational State Transfer questions* = la tabla **rest questions** (Gemini expandió "REST") → 🔍 en realidad **`resp_questions`**
- *LEAP* = **LEB** (Listening Event Builder). **Se asume así** (decisión de Ignacio, 06/10): nadie va a poder confirmar qué quiso decir una transcripción
- *LE app* / *LE data file builder* (training 28/09) = ✅ **LEB** y su Data File Builder: la ruta *Invite › Bring your own list* es la de LEB (*Reserved Column Names*)
- *restless* = probablemente **rest questions** → `resp_questions`
- *perceptual banding* = 🔍 *pyx banding*, el mismo de arriba
- *py bands* = 🔍 **pyx bands**: las bandas propias de Perceptyx (`pyx_age`, `pyx_tenure`, `pyx_generation`, nombres de campo confirmados en *Automation Setup – 360*). Resuelta por cruce en el cierre del 06/10
- *prefilled data* = la tabla **`prefill_data`** ✅ (Confluence 06/10)
- *F ID* / *M ID* = 🔍 **emp ID** (*"emp ID"* suena *"M ID"*): el ID único con el que se une todo — la linkage estándar es **Employee ID ↔ `emp_id`** (*360 Data Upload Steps*). Resuelta por cruce en el cierre del 06/10
- *off-codes* / *O code* = ✅ **auth codes**: `prefill_data` tiene una columna **`auth`** al lado de `pyx_pin` (captura de Querious, 23/09) — sesión QA del 02/10
- *rad ID* = 🔍 **ratee ID** (`ratee_id`): en el huddle se hablaba de prefill en 360s *"linked to the rad ID"*, y en 360 el prefill se vincula al leader por `ratee_id`. Resuelta por cruce en el cierre del 06/10
