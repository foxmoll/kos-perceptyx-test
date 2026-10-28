# Bitácora — Perceptyx

Entrada de todo lo nuevo del dominio. **La más reciente arriba.** Cada entrada lleva fecha, fuente y
marcas de certeza (✅ 📣 🔍) — convención en [[Perceptyx/_indice|_indice]] § Régimen del dominio.

Cuando algo de acá cambia, no se borra: se marca `SUPERSEDED (fecha)` y se enlaza la versión nueva.

---

## 2026-10-28 — Correcciones post-cierre (árbol, regiones, sync) en un survey LEB con otro DM trabajando en paralelo

Sigue el late add del 26/10 (mismo app, EU, LEB): el PM pidió las correcciones de árbol y demos para después del cierre.
Cliente y personas omitidos. Paso a paso con Ignacio. Procedimientos en [[Perceptyx/procedimientos|procedimientos]] §
Actualizaciones después del cierre, § Late adds (pasos 5 y 8) y § Resincronizar all_data.

- ✅ **Toggle de LEB bloqueado:** en el evento cerrado, *Use LEB Data Collector* estaba encendido y con *"This setting
  has been locked by the system administrator"*; *Preview Listening Event* deshabilitado. 📣 Elena (28/10): *"As survey is
  closed — I don't think anything will be switched back to Live in LEB. You can do all changes in AR"*. Matiza la
  práctica de *apagar y avisar* (regla 10, 📣 06/10 a confirmar): con el survey cerrado, Elena no lo exige. Se avisó igual
  al PM que no previsualice ni reactive.
- 🔍 **AR = Advanced Reporting** (el reporting site clásico, `index.cgi?rm=…`), deducido del contexto; no confirmado.
- ✅ **Error de operador:** la primera captura de *Managed Settings* era **otro evento** del mismo master app (otro nombre,
  otro `builder/<n>`). Lo delató el encabezado. Antes de tocar un toggle, verificar nombre del evento y app ID en *My
  Surveys* (buscar por app ID).
- ✅ **Árbol:** diagnóstico previo (2 casos del pedido + 1 desfasado de origen: un participante sin manager en prefill
  colgado del *placeholder* `999999999`, que se dejó igual). Archivo armado **por SQL** (árbol actual con el `mgr_id`
  corregido por `CASE` + el faltante por `UNION ALL`), control de filas (+1) y de huérfanos (0) antes de *Upload
  Managers*. Contra el backup cambiaron solo las 2 filas pedidas. Sin `trend_emp_id` manuales.
- ✅ **Regiones de 3 late adds de otras manos:** `pyx_region` / `pyx_detailed_region` / `pyx_extended_region` desde la
  combinación única por `work_country` del resto de la base. `UPDATE` por SOS, *Preview* = 3 filas. Tercera vez del patrón
  del 23/10 y 26/10.
- ✅ **`0` sin espacio en prefill (3 filas, mismas altas) contra `0 ` en `resp_list`:** el sync avisa *"Don't have index
  value … '0'"*. Se corrigió prefill con `WHERE col = '0' AND CHAR_LENGTH(col) = 1`, para no depender de cómo compara
  la base los espacios finales (🔍 con PAD SPACE, `'0' = '0 '` da verdadero y el `UPDATE` agarraría todo).
- ✅ **Sync (Test → Live):** 12 respondentes con `all_data` vacío (no 10 como el 26/10), más 2 de las altas en región y
  `hire_type`. Verificación contra el backup: 12 / 14 / 14 / 12 cambios por demo y 0 vacíos.
- ⚠️ **Otro DM reordenando el mismo survey a la vez (Andrea, 📣 28/10).** El segundo test de sync mostró, de golpe, 1.629
  valores que cambiaban de opción y cientos de avisos en `02_32_07`. Rastros: un backup manual de `resp_list` de esa
  mañana (`resp_list_backup<iniciales>…`) y seis `sos_dbtool_resp_list_*` en dos minutos. **Se excluyó `02_32_07` del
  sync, pero el reorden también tocaba `02_50_07`, y ese demo entró en el sync en vivo.** Lo detectó el Q&I final.
  Separación contra el backup: lo propio fueron 12 filas (vacío → valor); las otras 2.653 eran el remapeo correcto del
  reorden. La lista de Andrea quedó reescrita a medias (textos de las primeras posiciones sobreescritos: faltan 15–21, 3–9
  repetidos, `0` sin espacio). Se le pasó el diagnóstico; su sync de los dos demos recalcula todo, incluidas las 12.
  🔍 Error de operador (Claude): supuso que el reorden era de un solo demo, en vez de preguntar cuáles eran.
- ✅ **Cierre:** mensaje al PM con lo hecho, sin dar el Q&I por limpio (alertas de `02_32_07` y `02_50_07` por el reorden
  en curso; 3 demos sin opciones, previos).

**Para extraer a procedimientos** (pendiente): antes de un sync en vivo, buscar backups ajenos del día
(`SHOW TABLES LIKE '%resp_list%'`, `'%_backup_%'`) y preguntar qué demos tocan; un test de sync que cambia de golpe entre
dos corridas indica a otra persona escribiendo en el survey. Rearmar el árbol por SQL en vez de Excel. El filtro por
`CHAR_LENGTH` para el `0 `.

---

## 2026-10-27 — Bandas calculadas de edad y tenure + 3 late adds incompletos (LEB EU, cerrado)

Tarea *Data – Calculated demo updates*, el mismo app del ticket del 19/10 (que se dejó para después del cierre). Cliente
omitido. Paso a paso con Ignacio. Procedimiento nuevo en [[Perceptyx/procedimientos|procedimientos]] § Agregar un
demográfico nuevo › Demo calculado desde una fecha.

- ✅ **No había bandas:** `band` es de puesto. *"Update"* = crear Age Band (`02_33_07`) y Tenure Band (`02_34_07`). Corte
  08/10/2026 (lanzamiento). 15.825 participantes y 13.816 respuestas con banda.
- ✅ ***Add / Update Demographics*** pide statuses, crea el demo y reconstruye `all_data`. Tenure quedó alfabética:
  textos reescritos + sync.
- ✅ **3 late adds incompletos** (sin fechas ni demos): `UPDATE` por SOS desde el archivo de la PM, **traduciendo
  formatos** (`TRUE` → `1`, `12,1` → `12.1`, fechas a `AAAA-MM-DD`). Ya habían respondido: *Add missing demographic
  options* (3 demos) + sync de 20 demos. Un demo faltó en la primera lista (lo detectó el test contra el Q&I).
- ✅ **El sync es por demo para todos:** arrastró 2 respondentes de *Abu Dhabi OC* a *Doha OC* (dato de origen) y 7
  vacíos de `absent`. 📣 Ignacio: incluirlo y avisar a la PM.
- ✅ **Árbol:** 2 nuevos agregados con *Upload Managers* (sin encabezado); se perdió el único `trend_emp_id` manual
  (1 → 0) y se restauró. Q&I final: solo 2 cuentas de prueba en `emerge`.
- 🔍 **Para la PM:** fechas, nombre e IDs de manager cargados como demos reportables; el status *Manager* no bloquea
  `birth_date` (*admin* y *hr+* sí).

---

## 2026-10-27 — Archivo final con muestra cargado por LEB (EU, draft): 113 columnas con el límite subido

Sigue la tarea del 26/10 (audit FAILED por 113 columnas). 📣 La PM: *"this customer is already known to have over 99
columns… proceed"*. Elena: *"ignore the warning and proceed"*. Cliente omitido. Paso a paso con Ignacio. Procedimiento en
[[Perceptyx/procedimientos#4b. Carga por *Bring your own list* con el archivo de DOC (tarea real, 27/10/2026)|procedimientos § 4b]].

- ✅ **Dependencias:** 0 en todo, salvo 2 `popup_definitions` (glosario, sin condición sobre demos) → **por LEB**. Un primer
  conteo salió de la base de **otro survey**: Querious mostraba el resultado anterior al cambiar de base. Lo delató un
  `prefill_data` idéntico al del late add del día anterior.
- ✅ **Sync Settings:** los 6 toggles están en *Managed Settings* › *Sync Settings*. Default: 3 encendidos y 3 apagados.
  Primero creí que no estaban, porque la sección está más abajo en la página.
- ✅ **Dos bloqueos de LEB:** `sequence` (renombrada a `sequence_`) y el límite de 99 demos. Tim Sams pasó en Slack la
  configuración del master app, que se subió a 120.
- 🔍→❌ **Propuesta descartada por Ignacio:** cargar solo los 60 demos del Q3. Qué demos entran lo decide la PM, y la
  PM dijo todos. Se destildaron solo identificadores, fechas, muestra y vacías (30): quedaron 83.
- ✅ **Conteos:** 71.672 importados → filtro `q4_sampled` = *Yes* → 35.464 en `prefill_data` y en `emerge`. 83 demos.
- ✅ **Q&I:** *Missing all_data columns* hasta el Preview. Después, ceros sin espacio (LEB recortó el `0 ` de DOC; se
  corrigieron 1.398 + 4.002 filas y 3 opciones) y 30 demos sin opciones: columnas del spec vacías desde el cliente, con
  los datos en `gender1`, `country`, etc. Opción en blanco creada. La alerta de *no options* queda.
- ✅ **Cierre:** mensaje a la PM con el PDF *Data File Review* de DOC (aclarando que el límite de 99 se dispensó), demos
  vacíos, *Reply-to* vacío en Communications, participantes abiertos en `emerge` (¿cerrar?) y el aviso de la regla 10.

---

## 2026-10-26 — Late add en un survey LEB vivo (EU, 4 personas): cargado por SOS e invitado

Tarea *Live Support (Data/Survey)*: sumar participantes y mandarles la invitación. Cliente y personas omitidos. Paso a
paso con Ignacio. Procedimiento en [[Perceptyx/procedimientos#Late adds: sumar participantes a un survey que ya está en vivo (Elena, call del 16/10)|procedimientos § Late adds]].

- ✅ **Pasos 1–3:** los encabezados del archivo mapearon 51 de 51 contra `prefill_data` (minúsculas, `_`; *Employee ID*
  → `emp_id`, *Manager Employee ID* → `mgr_id`). Hubo que reordenar para dejar `emp_id, first_name, last_name, email,
  mgr_id` primero. 0 coincidencias por ID y por email.
- ✅ **`pyx_*`:** 6 de 9 con valores en la base. Reglas deducidas de queries agrupadas (procedimientos § Late adds,
  entre los pasos 5 y 6).
- ✅ **Paso 5:** Querious dio otra vez `INSERT command denied` en EU (segunda vez, confirma el 23/10). Un primer
  `INSERT` armado en Excel mostró 25 filas en el *Preview* y no se confirmó. El segundo, armado desde el texto, entró: 4
  filas (`sequence` > 18068).
- ✅ **Paso 6:** *Upload Respondents* + *Populate* (Blanks Only) completó 7 SSO: los 4 nuevos y 3 altas anteriores.
- ✅ **Paso 7:** el Q&I marcó `active` en `1`/`0` contra opciones *true/false*. `UPDATE` de 4 filas por SOS y Q&I de
  nuevo sin alertas de linkage. Quedaron, previas al ticket: 10 participantes con `all_data` vacío (190 líneas en 47
  demos), 3 demos sin opciones y 1 participante fuera del árbol → PM.
- ✅ **Paso 8:** no hizo falta rebuild. Un nuevo tenía en el árbol un manager distinto del archivo → PM.
- ✅ **Paso 9:** sin envíos programados en *Launch Schedule*. *Send Email › Survey Invitation* fila por fila, con
  `sent_date` en los 4. 📣 Ignacio decidió invitar también a 2 *Not eligible / Unpaid Leave*, porque lo pidió el cliente.
- ✅ **Cierre:** validación de Elena 0 / 0. Mensaje al PM con todo lo que no es del ticket.
- 🔍 **Patrón confirmado por segunda vez:** las 3 altas anteriores a este late add (las últimas `sequence` antes de las
  nuestras) tenían las `pyx` de región vacías. Late adds de otras manos cargados **sin calcular las `pyx`**: quedan fuera
  de los cortes por región. Sube la confianza en la hipótesis del 23/10.
- ✅ **Error de operador:** se dio un mensaje al PM con un marcador adentro, antes de tener el dato, e Ignacio lo mandó.
  Regla nueva en [[KOS/Reglas|Reglas]] § 9.

---

## 2026-10-26 — Archivo final con muestra en LEB (EU, draft): audit de DOC FAILED, no se cargó

Tarea *PFS: Load Final Data File – OPTIONAL*, survey de LEB, EU, non-healthcare, sin jerarquía, versión del spec
"unknown". Pedido: cargar solo los registros con *Yes* en la columna de muestra. Cliente y personas: omitidos.
Trabajada paso a paso con Ignacio.

- ✅ **Estado del survey:** *Deactivation* sin tildar no dice si está en vivo o sin lanzar. El sitio de reportes del sub
  app (`?rm=dashboard`) **no tiene LEB ni *Manage settings***. La lista ***My Surveys*** del master app sí tiene una
  columna **Status** (*Draft*). → [[Perceptyx/procedimientos|procedimientos]] § Carga del archivo final, paso 3.
- ✅ **Llegar al master app sin MAC:** la URL de MAC de la tarea es la de US, y un cliente EU no aparece ahí (nombre
  `EU-…`). La URL de MAC EU sigue sin estar en el vault. Se resolvió con **SOS › Customer Hub › Reporting**, que entra por
  Okta → [[Perceptyx/services-os|services-os]] § Customer Hub.
- ✅ **Columna de muestra:** tres valores (*Yes*, *No (Direct)*, *No (already was in Q3)*). ~49 % *Yes*, y los conteos
  cerraron. El archivo traía además una columna `sequence`, que choca con el campo autogenerado del mismo nombre (§ LEB);
  el audit no la marcó.
- ✅ **DOC = audit del data spec (v3.1)**. Cierra la pregunta abierta del 08/10. El primer build dio **HTTP 502**; el
  segundo tardó ~7 min. → [[Perceptyx/services-os|services-os]] § DOC.
- ~~🔍 El audit lee los encabezados crudos, no el mapeo~~ **SUPERSEDED (mismo día):** *Missing required fields* salió
  porque **el mapeo de las 5 columnas no se había aplicado**. Con el mapeo aplicado, desapareció.
- ✅ **Falla dura real:** *File exceeds column limit of 99 (found 113)*. Más 15 `mgr_id` sin empleado (irrelevante sin
  jerarquía). La tarea dice *"upon audit pass, load; if not… the task will then be closed"* → **no se cargó**: resumen
  al PM (SKU *Additional Demographics* o archivo corregido o *Data Spec Compliance Review Request*) y tarea cerrada.
- ✅ **Las descargas de DOC no sirven para el PM** (📣 Ignacio: *"no aporta nada enviárselos"*): el *Audit report* repite
  por fila los campos v3.1 que faltan (*Nudge / AI Coach Eligible*), y *Export findings* es un PDF para el cliente.
- 🔍 **Abierto:** cómo se filtra la muestra al cargar en LEB (paso 4.6) no se probó. Tampoco si 113 columnas entran con el
  SKU de 135. Se verá si vuelve la carga.

---

## 2026-10-23 — Late add en un survey LEB vivo (app EU, 3 personas): bloqueado en el import por permisos

Ticket *Data – (Late) Add – Live*, cliente y personas omitidos. Se empezó en Antigravity y se siguió en Claude Code.
Procedimiento en [[Perceptyx/procedimientos#Late adds: sumar participantes a un survey que ya está en vivo (Elena, call del 16/10)|procedimientos § Late adds]].

- ✅ **Backups** por *Operations Tools › Utilities › Backup table* (sin escritura en Querious). Los nombres no se anotaron:
  se recuperan con `SHOW TABLES LIKE '%backup%';`.
- ✅ **Chequeo de "ya están":** 0 coincidencias por ID y por email en `prefill_data` y `emerge`, comparando en minúsculas.
- ✅ **Columnas `pyx_*` calculadas:** `prefill_data` del survey LEB tiene `pyx_*` que el Data File Builder de Operations
  Tools **no calcula**. Se derivaron de lo ya cargado: región desde `work_country`, `pyx_role_tenure_band` desde
  `years_in_role` (rangos sin solapamiento) y `pyx_tenure` desde `original_hire_date`, con corte en 21/09/2026 (no desde
  `years_of_service`, que se solapa entre bandas). Las otras cuatro `pyx` estaban en NULL en todas las filas.
- ✅ **Altas anteriores sin `pyx`:** tres filas sueltas (06/10, 12/10, 19/10) con todas las `pyx` en NULL, una con la fecha
  en `dd/mm/aaaa` y otra sin país. 🔍 Late adds anteriores cargados sin calcularlas: quedan fuera de los cortes por región
  y antigüedad. Para el PM (regla 8).
- ✅ **Data File Builder:** ver § Late adds, paso 4 (encabezados obligatorios, `emp_id_1`, nombres de salida).
- ✅ **Querious:** el primer import corrió el archivo como **SQL** (*syntax error* en la línea 1, la de encabezados). Con
  formato **Tab**, destino base + tabla y la pantalla de *Column Mapping*, el mapeo coincidió solo.
- ✅ **Bloqueo:** `INSERT command denied` en la conexión RW de EU (23/10). No se escribió nada (conteo de
  `sequence > 22903` = 0). Contradice *"ya tiene permisos de escritura"* (06/10, [[Perceptyx/plataforma|plataforma]] §
  Accesos): 🔍 el permiso sería por servidor. Pedido a Jackie.
- ✅ **Destrabado por SOS:** *Database Tools › Insert* con un `INSERT … VALUES` armado a mano (41 columnas; las vacías se
  omiten para que queden NULL). *Preview load* del archivo no hizo nada. Entraron 3 filas (`sequence` 22904–22906), con
  `ismanager` = `0 ` y las `pyx` correctas. `auth` quedó NULL: ✅ **no hace falta completarlo**. Dos de las tres altas anteriores (22901, 22903) tienen `auth` NULL en `prefill_data` y respondieron el survey. Coincide con Elena, que no lo completó. 🔍 Que `prefill_data.auth` = `emerge.auth` en el resto (17.782 de 17.785) es efecto de la carga inicial de LEB, no un requisito. Ver
  [[Perceptyx/services-os|services-os]] § Database Tools.
- ✅ **Paso 6:** *Upload Respondents* con el `emerge.txt` del builder (generó `auth`), *Populate Survey Launch Fields* para
  `sso_id` (Blanks Only, 3 filas, respaldó `emerge`), `lang` y `theme` en NULL en toda la base (nada que completar), e
  invitación con *Send Email › Survey Invitation* fila por fila: `sent_date` en las 3.
- ✅ **Paso 7:** *Q&I Checks* (Data Collector / Participant Data) sin alertas de linkage: los valores de los 3 ya existían
  en `resp_list`, no hizo falta *Add missing demographic options* ni mirar el toggle de LEB. Única alerta: *Verify all_data
  demographics match prefill_data*, un participante con `Non-Union` en `prefill_data` y vacío en `all_data` (1 ocurrencia).
  No es de los 3 nuevos (su valor en esa columna es otro y todavía no entraron al survey). 🔍 Previo al ticket; mismo tipo
  de caso que la entrada del 20/10.
- ✅ **Paso 8 no hizo falta:** los 3 ya estaban en `managers_tree` antes de la carga (backup del paso 1), con su manager y
  `tree_path`. La alta 22901 está en el árbol con manager, pero sin `mgr_id` en `prefill_data`: para el PM.
- ✅ **Cierre:** validación final de Elena en 0 en los dos sentidos (`emerge` sin `prefill_data` y al revés). Mensaje al PM
  con lo que no es del ticket: altas anteriores sin `pyx` (una sin `mgr_id` ni país, otra con fecha en otro formato), la
  alerta de `all_data` y el cuidado con LEB.
- ✅ **Errores del operador anterior corregidos en el camino:** comparar IDs sin pasar a minúsculas, y la compuerta LEB
  dada en verde sin mirar el toggle *Use LEB Data Collector*.

## 2026-10-21 — Reporte de Leaders of Leaders del 862013: el adjunto era otra lista (corrección)

Revisión de un caso de Wailam (Slack, 21/10): el PM pidió verificar el reporte que mandamos en el cierre del 862013
y comparó con un archivo de 2025 del mismo reporte. Cliente, personas y app omitidos.

- ✅ **El archivo adjunto al cierre no era el reporte de Leaders of Leaders.** Eran 101 filas de vistas de comparación
  (80 My Leader + 21 My Business Unit), o sea la lista de vistas dentro de umbral, con `user_completions` y
  `comparison_completions`. Solo 25 filas tenían diferencia de 0 o 1 y 4 tenían diferencias de decenas de miles.
  Las idénticas no cuadran con el comentario del cierre (3 My Leader contra 4 My Business Unit anunciadas; el archivo
  tenía 0 My Business Unit).
- ✅ **Formato del reporte de 2025** (archivo de referencia): una fila por par (líder de líderes, manager de su descendencia),
  con `username`, `status`, `emp_id`, `# Completions In Hierarchy`, `their mgr_id`, `username of leader`, `status2`,
  `# Completions In Hierarchy3` y `# diff`.
- 🔍 **Definición inferida del ejemplo de 2025:** las dos columnas de conteo son *hierarchy completions* (no
  `user_completions`), y `diff = completions del LoL − completions del manager` (12 − 11 = 1). El vínculo sería
  manager directo (`their mgr_id` = `emp_id` del LoL). Un solo ejemplo: confirmar con el PM.
- 🔍 **Cómo armarlo:** `get-mgr-counts` (columna *hierarchy completions*, verificada por encabezado), lista de cuentas
  `leader_of_leaders`, pares directos, cruce y filtro `|diff| ≤ 1`. Los open roles (IDs no numéricos) quedan aparte hasta
  que el PM decida. Pasos completos en la conversación del 21/10; no se corrió en la base.
- ⚠️ **Pendiente:** responder al PM (mensaje en inglés, sin enviar) y generar el reporte correcto con acceso a la base.
- 📣 Ignacio, 21/10: la fórmula de concatenación `TEXTJOIN` para listas `IN (…)` queda en
  [[Perceptyx/procedimientos#Parte 2.1 — Contar: `get-mgr-counts`|procedimientos § Parte 2.1]] (sin probar; sin commit por decisión de Ignacio).

---

## 2026-10-20 — Integridad: `all_data` desfasado contra `prefill_data` en un participante (5 demos, survey LEB EU, cerrado)

Ticket de integridad, cliente y personas omitidos. Procedimiento en [[Perceptyx/procedimientos#Resincronizar `all_data` después de reordenar — *Operations tools › Data › Sync reporting demographics from participant data*|procedimientos § Resincronizar]] y [[Perceptyx/modelo-de-datos#El valor en `all_data` es una posición, no un texto ni una clave|modelo-de-datos § posiciones]].

- ✅ **Síntoma:** *Quality and Integrity Checks* → *Verify all_data demographics match prefill_data*: cinco demos de texto o código vacíos en `all_data` para un participante, con `prefill_data` correcto. Es copia de reporte desfasada, no pérdida de datos.
- ✅ **Diagnóstico en solo lectura:** la columna `prefill_data` de cada demo sale de `prefill_linkage` (`resp_id` → `emerge_id`, que es el nombre de la columna). Las opciones están en `resp_list`. Columnas verificadas en [[Perceptyx/modelo-de-datos#Columnas verificadas en la base (✅ 20/10/2026, Querious, survey LEB EU)|modelo-de-datos]].
- ✅ **Antes de escribir:** cuatro dependencias revisadas (branching, trends, filtros guardados y comparison views): 0 filas en las cuatro.
- ✅ **Escritura:** backup desde la app (el snippet SQL dio `execute command denied` con la conexión de lectura). *Test Mode* listó las mismas cinco discrepancias. En vivo, la fila cambió y solo esa: verificado contra el backup con la query de § Resincronizar.
- ✅ **Cierre:** el chequeo de integridad volvió a correr limpio.
- ✅ **Posición confirmada:** el índice que escribió el sync coincide con la posición 0-based por `seq`, con la opción vacía contando como 0 (ver modelo-de-datos). `option_id` y `option_order` no sirven para eso.
- 🔍 **Conexión de Querious:** la pestaña decía `classic-mysql-us`, y ahí apareció el backup que creó la app EU, con las mismas filas. 📣 Ignacio: la VPN de US sirve para los dos entornos. Por confirmar con Jackie que la lectura EU pasa por ese host, para no leer un servidor distinto al de la app.
- 🔍 **`emerge.survey_closed` = 0** para un participante en un survey cerrado. Es un flag por participante: no reemplaza la compuerta de *Deactivation* en *Survey Configurations*.
- 🔍 **Tensión:** el procedimiento dice que el sync ordena las opciones alfabéticamente; acá el índice siguió `seq`. Por confirmar.
- ✅ **Error evitado en el camino:** el procedimiento pide el paso a paso con queries y la lectura del ticket desde el primer mensaje. No hay cambio de procedimiento: es la regla de [[KOS/Reglas|Reglas]] § 9 que ya existía.

## 2026-10-15 — Ticket 862013: user setup de dos status con controles de integridad (cierre reportado, sin verificar)

Trabajo hecho el 15/10 y **no registrado en el vault en su momento**. Esta entrada sale de los comentarios de cierre
que Ignacio pegó el 20/10; no se verificó nada en la base desde esta sesión. Cliente, app y personas omitidos.
Pedido: ver [[Perceptyx/procedimientos|procedimientos]] § Usuarios Manager (el caso es parecido, pero el umbral y el SSO ID cambian).

- ✅ **Pedido** (texto de la tarea): dos status de reporte. Precondiciones a cargo del solicitante, incluidos los controles
  de cierre, que no debían empezar antes del 14/10. **SSO ID = employee ID**. Integridad: borrar usuarios con menos de
  10 preguntas, y quitar vistas de comparación dentro de umbral. Reporte de Leaders of Leaders con diferencia de 0 o 1
  completions contra un manager de su descendencia.
- 📣 **Resultado reportado:** 4.371 cuentas Manager con 10 o más completions de jerarquía, **inactivas**, con SSO ID =
  emp_id. De ellas, 1.363 quedaron como `leader_of_leaders`. Vistas de comparación: My Leader, My Business Unit y My
  Organization (Blue Box). `sso_id` ya no era único, así que no hubo cambio ahí. **Sin borrados** por integridad.
- 📣 **Estado de la tensión activos/inactivos (09/10):** para este ticket las cuentas quedaron inactivas, según el reporte.
  No cambia lo que muestra la herramienta.
- ⚠️ **Decisiones abiertas al cierre** (el solicitante tiene que responder; no se resolvieron):
  - 80 vistas My Leader y 21 My Business Unit dentro de umbral (menos de 10 completions de diferencia contra la vista
    propia). 3 y 4 son idénticas. Lista adjunta. ¿Se borran?
  - 14 vistas My Leader que apuntan a la cima del árbol, o sea muestran lo mismo que Company Overall. ¿Se mantienen?
  - 82 nodos *open role* (IDs no numéricos) con 10 o más completions recibieron cuenta de líder. ¿Mantienen cuenta?
  - 22 cuentas de personas que no están en `prefill_data` ni en `emerge`, probablemente términos que siguen en el árbol
    de managers. ¿Se mantienen o se borran?
  - Grupos 3 y 4 (104 cuentas) no tienen vista My Business Unit porque no tienen valor de Business Unit.
- 📣 Ninguna cuenta leader o leader_of_leaders ve menos de 10 preguntas. 12 cuentas `market_report` preexistentes muestran
  0 preguntas; no se tocaron.
- ⚠️ **Método distinto del procedimiento:** *Quality and Integrity Checks* expiró en la verificación de vistas de
  comparación (unas 13.000 vistas). La lista de dentro de umbral se calculó directo desde la base con las completions de
  jerarquía, no desde el check.
- ~~📣 El reporte de Leaders of Leaders (diferencia de 0 o 1 completions) se adjuntó al cierre. No está en el vault.~~ SUPERSEDED (2026-10-21): el archivo adjunto era la lista de vistas de comparación, no el reporte. Ver la entrada del 21/10 arriba.

---

## 2026-10-20 — Comentarios automáticos, survey cerrado (odpsegps269): verificación post-cierre

Ticket de verificación de comentarios automáticos en un survey cerrado (US, LEB, no healthcare). Cliente y personas
omitidos. Procedimiento en [[Perceptyx/procedimientos#Comentarios con modelo léxico (workaround de bug)|procedimientos § Comentarios con modelo léxico]].

- ✅ **Dónde está la configuración:** *Report Editor › Configuration*, con los campos Filter y Bucket. Filter `Snowflake`
  muestra el procesamiento automático ("Enables automated comments processing (Snowflake)"); Filter `Themes matching`
  muestra el modelo: *usage of machine learning level* (valor *Level 0: lexical keyword matching*) y *supervised* (apagado).
  El procedimiento decía *Survey Setup › Survey Configurations*: ruta corregida.
- ✅ **Estado:** procesamiento automático activo, modelo léxico. Aplica el workaround.
- ✅ **Script `comments verify steps` (SOS, opción 2 *After Close*):**
  - Paso 1, temas duplicados: ninguno.
  - Paso 2, hacer visibles los temas: completado. ⚠️ **Escribe en la base y se corrió sin backup previo** (regla 1).
  - Paso 3, verificación: la automatización de Snowflake reporta *mismatches in comment qid counts* y pide dejarla terminar
    o volver a correr. Temas supervisados: 0, con aviso de consultarlo con el PM.
- ⚠️ **Pendiente:** respuesta del PM (mensaje en inglés, enviado por Ignacio). No se corrió el workaround en SQL hasta
  tener esa respuesta. Con cero temas supervisados, la reinserción podría no tener qué restaurar.
- 🔍 Hay tablas de backup de hoy en el app (`comments_themes_matches_partial_removal_20261020_…` y
  `…_terms_removal_20261020_…`). No se sabe si las generó el script o una corrida anterior de alguien del equipo.
- 🔍 El procedimiento está fechado al 01/10 y dice que el script manual se sigue corriendo hasta que los chequeos
  automáticos entren en el survey launch audit. Falta confirmar con Jackie si sigue vigente.

---

## 2026-10-20 — Late add en un survey vivo: el archivo ya estaba cargado

Ticket real de late add (EU, LEB, en vivo), trabajado paso a paso con Ignacio. Cliente, personas y app ID:
omitidos. Procedimiento actualizado en [[Perceptyx/procedimientos#Late adds: sumar participantes a un survey que ya está en vivo (Elena, call del 16/10)|procedimientos § Late adds]].

- ✅ **Resultado:** los 20 registros del archivo ya estaban en `prefill_data`, `emerge` y `managers_tree`, con el mismo
  email. No hubo altas. El nombre del archivo decía 10 y traía 21 filas: el conteo tiene que salir del contenido.
- ✅ **La addenda del cliente listaba 13 IDs.** Los 13 coincidieron 1 a 1 en `prefill_data` y `emerge`. Los otros 7
  del archivo también estaban por ID y por email.
- ✅ **Los IDs están guardados en minúsculas;** el cliente los manda en mayúsculas. Buscar en mayúsculas da cero y
  parece que los IDs no existen.
- ✅ **`mgr_id` aparecía dos veces** en el archivo, con la misma información. Se mapeó una.
- 📣 Ignacio: el blanco de nombres y emails en las consultas fue redacción propia (datos personales fuera del chat),
  no un dato faltante.
- ⚠️ **Un participante existente con otro manager:** el archivo y el sistema difieren en el manager de uno de los 20.
  Ambos managers existen en el árbol. No se tocó nada: es un cambio de jerarquía de alguien ya en el survey, y el
  procedimiento de late add no lo cubre. Pendiente de respuesta del PM (regla 8), con el mensaje en inglés.
- 🔍 Las 7 filas de `emerge` tienen fecha de creación del 16/10, misma fecha de la call con Elena. No está confirmado
  que sea la misma carga.

📣 Ignacio, 2026-10-20: los mensajes a PMs y al equipo se escriben en inglés (incorporado a [[KOS/Reglas|Reglas]] § 9).
## 2026-10-20 — Ticket nuevo sin procedimiento: user setup con varios status, empleados y umbral por país

Conversación del 17/10, cerrada el 20/10. Ignacio pegó la tarea; no se trabajó todavía (faltan app ID, LEB/Classic,
estado del survey y el ticket de user setup anterior). Cliente, survey y tickets: omitidos.

**El patrón** (✅ texto de la tarea): cinco status de acceso a reportes — dos de manager (general y de un país) y tres de
**empleado** que ven los resultados **de su manager**, o del siguiente nivel si no llega al umbral. El país lleva un
**umbral más alto (25)**, que la tarea llama *"minimum comment threshold"*. Se pide **replicar la lógica de un survey
anterior** (su app y su ticket de user setup) y que reportes, dashboards, demos y restricciones por status coincidan con
un **app de usuarios de prueba ya aprobado**. Plazo: QA terminado el jueves anterior a la activación del lunes.

Lo que sale de cruzarlo con el vault:

- ✅ **El vault solo cubre los status de manager** ([[Perceptyx/procedimientos|procedimientos]] § Usuarios Manager): *Add
  Users* en dos pasadas y vista del primer superior que llega. **No hay procedimiento para usuarios empleado** con la
  vista del manager. En *Add Users* solo se vieron poblaciones de managers.
- ✅ **`get-mgr-counts` no cuenta comentarios** (invitados, respuestas, completions). 🔍 Si el umbral es de comentarios,
  esa herramienta no alcanza para clasificar. 🔍 *"Comment threshold"* también puede ser un mínimo configurado en el
  status, o sea configuración de reportes y no de creación de usuarios.
- 🔍 **Dos umbrales en el mismo app:** en las tareas vistas, *Add Users* tomaba un solo umbral, ya configurado por el PM.
  No se sabe si admite uno por status.
- 🔍 **Cinco status = el tope de *Custom Roles and Statuses* por compra** ([[Perceptyx/catalogo-servicios|catalogo-servicios]]):
  dentro del alcance si el contrato es el estándar.
- 🔍 El snippet ***Users - Reporting User Setup*** (`;dmtuseraccts`, [[Perceptyx/plataforma|plataforma]] § Text
  Expander) es el primer lugar donde buscar. Su contenido no se vio.
- 🔍 Vía probable, sin probar: leer en el survey anterior cómo quedó cada status (`users`, `statuses`) **antes** de
  definir la lógica, y comparar `statuses` contra el app de prueba.

**Lo que salió mal en la respuesta (Claude):** pidió cinco datos juntos y metió el análisis en el medio. Eso viola la
regla *de a una pregunta por mensaje* ([[KOS/Reglas|Reglas]] § 1, 17/10). La sesión arrancó en una rama `claude/…`
**desactualizada**, sin esa regla ni el mapa de tickets, y no se trajo `main` antes de leer. Quedó en
[[KOS/Execution|Execution]] § Vault Sync.

---

## 2026-10-19 — Ticket nuevo sin procedimiento: cambiar las bandas de un demo calculado

Ticket real que Ignacio trabajó con Antigravity y revisó con Claude. Cliente y app: omitidos. Patrón: el
cliente pide **cortes propios** para la banda de edad (desde la fecha de nacimiento) y la de tenure (desde la
fecha de ingreso original), en un survey de LEB, EU, **en vivo**.

- 📣 Ignacio: **se trabaja después del cierre del survey**, no desactivándolo antes. Pasó a la regla 2 de
  [[Perceptyx/procedimientos|procedimientos]].
- 📣 Ignacio: el backup a mano `CREATE TABLE <tabla>_AAAAMMDD_<iniciales> LIKE <tabla>` + `INSERT … SELECT` **es
  válido**, lo vio con otros DM. Pasó a la regla 1 como tercera vía.
- Sin procedimiento escrito: quedó en procedimientos § Pendientes, con lo que hay que averiguar al hacerlo.
- La prueba del operador y los cambios de arquitectura que salieron de ella (mapa de tickets, compuertas): [[KOS/Operadores|Operadores]] § Antigravity.

---

## 2026-10-16 — KOS de equipo en el GitHub de la empresa: decisiones de base, ejecución en pausa

Conversación de Ignacio con Claude. Se descartó NotebookLM como base, porque no escribe, no sigue el grafo y no
carga protocolo. Se decidió un repo de la empresa en inglés, con su propia capa `KOS/`, Gemini como
operador inicial y Claude si se aprueban licencias. La fuente de verdad de Perceptyx se muda ahí y este vault la
incluye como submódulo. Ignacio frenó la ejecución: primero planear sin romper el vault actual. Detalle y pendientes en [[Perceptyx/_indice|_indice]] § Proyecto: KOS de equipo.

---

## 2026-10-16 — Call con Elena: late adds en un survey vivo, de punta a punta

Grabación de Zoom de Ignacio (~55 min), transcripta con Whisper y cruzada con capturas del video. Elena
Khaletskaya (Automation) resolvió en vivo una tarea *Data – (Late) Add – Live*. Cliente, personas y app:
omitidos. Procedimiento completo en [[Perceptyx/procedimientos#Late adds: sumar participantes a un survey que ya está en vivo (Elena, call del 16/10)|procedimientos § Late adds]].

- **Orden: `prefill_data` → `emerge` → `managers_tree`.** 📣 Si `emerge` va primero, la persona puede
  recibir la invitación sin demográficos conectados.
- ✅ **Data File Builder** con *Export Files* y *Hard Reset = No*. ⚠️ *Direct Import* **borra a los
  participantes existentes**. Devuelve AUDIT, `prefill_data`, `emerge` y `resp.html`; 📣 pasa los emp IDs
  a minúscula.
- ✅ **`prefill_data` se carga por import de Querious** (`.txt`, conexión RW); `emerge`, por
  `rm=survey_launch`. 📣 Alinear antes los encabezados del archivo con `information_schema.columns` en
  Excel ahorra el mapeo a mano.
- ⚠️ **Chequear antes si los del archivo ya están** (`prefill_data` y `emerge`, por emp ID y por email):
  en el caso, 13 de ~20 ya estaban. `prefill_data` acepta duplicados sin avisar; se olvidó y hubo que
  borrar por `sequence`.
- ✅ **Q&I después de un late add:** valores de demo nuevos (*Add missing demographic options*, de a un
  demo), mayúsculas distintas (`select distinct binary …`), opción duplicada en `resp_list` (**renombrar,
  no borrar**: rompe índices), `"0"` → `"0 "`.
- ✅ **Backup por SQL:** `CALL mac.create_backup('<app>','<tabla>', @results)`. ~~Tercera vía~~ Corregido el
  mismo día con una captura de Ignacio: **es lo que corre el snippet *Backup Table* (`;bck`)** del grupo
  compartido *DM Snippets* de Text Expander, la misma vía que la de Emily, no una tercera. Nombra con fecha y
  hora, sin iniciales. Detalle en la regla 1 de procedimientos.
- ✅ **Dos snippets más del grupo *DM Snippets*** (capturas de Ignacio): `;terms` saca de `emerge` y
  `prefill_data` las bajas anteriores a una fecha de corte, y `;updatesso` reemplaza una URL en los mails, las
  traducciones y los JSON de recordatorios. Mi suposición de que `;updatesso` era el `UPDATE` del SSO ID
  **estaba mal**: quedó tachada en plataforma. Procedimientos nuevos en
  [[Perceptyx/procedimientos|procedimientos]]. La búsqueda mostró ~25 nombres de snippets más (en plataforma §
  Text Expander), que sirven de mapa de tareas ya resueltas.
- ⚠️ **Rebuild del `managers_tree` (*Upload Managers*) pierde los `trend_emp_id` puestos a mano**:
  restaurar desde el backup. Verde = trend natural; amarillo = a otro nodo.
- 📣 Elena usa la terminal (jail) para agregar opciones en masa, aunque el equipo pide pasar a SOS; no sabe
  cómo se hace ahí. Abre tres preguntas en [[Perceptyx/_indice|_indice]] § Preguntas abiertas.
- 📣 Hábito: guardar las queries de cada tarea en Querious con el app ID en el nombre.

---

## 2026-10-09 — Call de otro DM con Andrea: la misma tarea de usuarios Manager, en otro orden

Transcripción automática + 2 capturas, pasadas por Ignacio. Ignacio no estaba. 🔍 Que la trainee es Andrea se
deduce de la transcripción (*"ayer Jackie…"*); la fecha la confirma el reloj de las capturas. Nombres: omitidos. Detalle en
[[Perceptyx/procedimientos|procedimientos]] § Usuarios Manager › Cómo lo resolvió otro DM.

- **Otro orden, el mismo chequeo:** primero `get-mgr-counts`, con el backup (`users` + contraseñas
  temporales) mientras corre. El archivo da el número esperado y cada pasada de *Add Users* se compara con
  él (1.102 / 758). Jackie hizo al revés.
- **Tercera vía para el superior:** `users` como oráculo — *¿el jefe tiene cuenta Manager?* = *¿llega al
  umbral?*. 416 jefes distintos, 374 resueltos al primer nivel; el resto, con `tree_path`.
- **Paso nuevo: SSO ID** (`update users set sso_id = email …`). El valor lo dice el pedido: email acá,
  emp_id en el checklist del 24/09.
- **Formato de username no especificado:** se copia el de los managers existentes.
- ⚠️ **Apóstrofo en un apellido** rompió un `UPDATE` armado en Excel. Comillas dobles o `''`.
- ⚠️ **Tensión:** el DM dice que *Add Users* crea **inactivos**; Ignacio, que quedan **activos**. Sin
  resolver: query de verificación en procedimientos.
- ChatGPT dio una fórmula de `tree_path` que contaba desde el CEO; el *next level up* se cuenta desde el
  final. La fórmula del vault ya lo hace.
- 🔍 Tercera tarea de este tipo en dos semanas: choca con *"no la vas a ver mucho"* (Emily, 24/09).
- **Dos capturas de la misma call** (13:05 del 09/10 → ✅ la fecha): el diálogo ***Add Users*** arranca con
  ***Based on… = Completed***, así que para un pedido por *responses* hay que cambiarlo, y **no tiene campo
  de activo/inactivo** (el check del DM estaba en otro lado). Ruta en el menú: ***Reference Reports ›
  Manager Hierarchy Tree***.

---

## 2026-10-09 — Call con Jackie (08/10): la tarea 890116 resuelta en vivo

Transcripción + 4 capturas pasadas por Ignacio. Cliente y personas: omitidos.

- ✅ **La herramienta para crear usuarios Manager es *Manager Hierarchy Tree › Settings › Add Users***
  (`rm=managers_tree`): población (cumplieron / no cumplieron el umbral), status, formato de username,
  respondents o completed. Resuelve usernames repetidos y deja saltear los que ya existen. **Cierra** el
  pendiente de la entrada del 08/10 (*"falta la vía de carga"*) y la pregunta del shadow sobre cómo se
  crean los Below Threshold: **segunda pasada** con su status.
- ✅ `rm=managers_tree` **existe**: lo que el bot Pyxee-CVO había nombrado sin poder verificarlo.
- 📣 **`view_disp` es lo que el usuario ve al entrar**; `view_name` no importa.
- 📣 **Username por defecto:** inicial + apellido. **Respondents vs. completions** lo especifica siempre el
  pedido — confirma la regla de Ignacio del 08/10.
- ✅ **Carga masiva de un `UPDATE`:** CSV → tabla nueva en Querious → índice → `UPDATE … JOIN`, con
  `status = 'mgrbt'` como seguro. Pocos casos: `UPDATE`s generados en Excel.
- ✅ **Límites de SOS › Database Tools hoy:** solo `SELECT`, máximo 10.000 filas, `LIKE` con un bug →
  [[Perceptyx/services-os|services-os]].
- **Avisos normales** del *Quality and Integrity Checks* sobre `users`: emails en blanco, *"solo ven 6–7
  preguntas"*, status con acceso total que no es admin.
- **Dos vías para el superior** que llega a 5, con la misma validez: el `INDEX`/`MATCH` en cadena de
  Jackie y la fórmula sobre `tree_path` de Ignacio. Jackie pidió formas *"más inteligentes"*: la de
  `tree_path` es una.
- **Estado de la 890116:** creados 1.235 Manager y 868 Below Threshold, 868 vistas actualizadas, Q&I
  corrido. ~~⚠️ **No consta** el cierre en Salesforce (*Complete* + `;me`) ni si se avisó al PM.~~ Retirado
  el 09/10: el vault no sigue el cumplimiento de tickets (Reglas § 9).
- 📣 Ignacio, 09/10: los usuarios que crea *Add Users* **quedan activos**. Los accesos 📣 🔍 **los envía el PM**
  (*"supongo, porque no es tarea nuestra"*).
- Todo en [[Perceptyx/procedimientos|procedimientos]] § Usuarios Manager / Manager Below Threshold › Cómo
  lo resolvió Jackie.
- **Dos reglas nuevas de Ignacio** (09/10, en [[KOS/Reglas|Reglas]] § 9): el vault es **base de conocimiento,
  no seguimiento de tickets** (cambia el régimen del dominio en [[Perceptyx/_indice|_indice]]), y el
  **formato de respuesta** para un ticket: herramientas con URL primero, después los pasos con queries y
  fórmulas; si es paso a paso, resumen corto y un paso por vez. Para eso, tabla nueva en
  [[Perceptyx/plataforma|plataforma]] § URLs de trabajo.

---

## 2026-10-08 — Cierre: sesión del 21/09 (*DelOps Emails*) y sus capturas

**ΔK** (lo que se sabe hoy y no se sabía al empezar esta sesión):

- **Hay herramientas que reportan *y* arreglan.** El Launch Audit (9 categorías, `emerge` / `users`) es la
  tarea *"launch audit"* de la línea de tiempo y absorbió los scripts Python + planillas. Refina la idea 7
  de la síntesis: lo que se achica es el SQL a mano, no la intervención ([[Perceptyx/_indice|_indice]]).
- **Varias vías, misma validez** (regla nueva, [[KOS/Reglas|Reglas]] § 9) → idea 9 de la síntesis. Lo de
  Emily (Perl) y lo de Jackie (ops tools) quedaron juntos, sin jerarquía.
- **En SOS solo las queries son de solo lectura** (📣 Ignacio): `SUPERSEDED` la "solo lectura v1" de
  Customizations; la captura lo confirma (merge request a `apps @ master`).
- **Emails y traducciones**, de cero: sintaxis real del translation tag (`obj.translate_this("…")`), el error
  de las comillas, cómo probar un email de verdad, el flujo ops tool → Translation Tool, Microsoft vs.
  SmartCat.
- **Binlog inactivo = ediciones en MAC / prefill que no llegan a UDS** — aviso visto en el Launch Audit;
  conecta con [[Perceptyx/procedimientos|procedimientos]] § Sincronización con UDS.
- Corrección propia: *approve alerts* no es un campo del diálogo (es *include previously approved*);
  aprobar es la pregunta interactiva del script.

**Queda abierto:** *Big Brother report* · cuándo *blank out all_data* (Emily sí / default no) · sesión de
Edwin del 22/09 (SSO y API) · accesos del 21/09 (SSH Querious, Transmit, vault SFTP) sin confirmar ·
agrupar las 135 combinaciones de branching (espera las reglas) · **`procedimientos.md` llegó a ~1600 líneas:
partirlo por área** es el próximo trabajo de estructura.

---

## 2026-10-08 — Tarea 890116: usuarios Manager / Manager Below Threshold (~~en curso~~ resuelta el 08/10 en la call con Jackie — entrada del 09/10)

- Primera tarea de este tipo, survey de LEB, umbral 5. Cliente: omitido.
- ✅ `statuses` trae `mgr` y `mgrbt`; columnas reales de `users`; usuarios `mgr` existentes restringidos
  **por jerarquía** (`emp_id_view`) y **por demográfico** (`view`).
- ✅ `get-mgr-counts` exporta a *Files* los conteos por manager (*Hierarchy* y *Direct Reports*: count,
  invitees, responses, completions) y remite a *Users Upload* / *Users → Manage* para crear los usuarios.
- 📣 **Regla de Ignacio:** el umbral se cuenta con la palabra del ticket — *responses* es *Responses*, no
  *Completions*. Ignacio dijo que ya lo había dicho; no estaba escrito en el vault.
- ✅ `tree_path` real: IDs de 9 dígitos, arranca en el CEO, termina en el propio empleado. Con eso, la
  fórmula de Excel que busca para cada `mgrbt` el ancestro más cercano con ≥ 5 — **verificada por Ignacio**
  (chequeos en 0 y dos casos subidos a mano).
- ✅ **User Editor** del app (`rm=users_editor`): alta de a uno, con pestañas *Data Access: Demographic /
  Hierarchy / User Based* que 🔍 corresponden a `view` / `emp_id_view` / `username_view`. *Inactive User*
  viene tildado por defecto. **No tiene carga masiva**; en SOS tampoco apareció *Users Upload*.
- 🔍 **Se debilita** la hipótesis de procedimientos § Armar un árbol de managers (*"el camino LEB es el de la
  arquitectura nueva"*, acceso por *Edit Reporting Access*): en este survey **de LEB** el acceso a reportes
  por jerarquía se resuelve en la tabla clásica `users`, con statuses `mgr` / `mgrbt`.
- **Estado al cierre:** planilla lista (status y `emp_id_view` por manager). **Falta crear los usuarios.**
  📣 Jackie le mostró a Ignacio en una call cómo se hace la carga; Ignacio lo muestra en la próxima sesión.
- Todo en [[Perceptyx/procedimientos|procedimientos]] § Usuarios Manager / Manager Below Threshold.

---

## 2026-10-08 — Primera tarea real: carga del archivo final en LEB (en curso)

Tarea de *final data file* + audit para un app de LEB: cliente grande, non-healthcare, spec 2.1.0, con
branching, árbol de managers desde el CEO y exclusiones (terms, interns, contractors, ingresos desde el
01/10). El PM pidió además guardar una copia de la población completa antes de excluir. Cliente, IDs y
personas: omitidos. **Quedó a mitad de camino**: archivo ubicado, falta descifrar, auditar y cargar.

- ✅ **"Audit" en la tarea ≠ Launch Audit.** Ignacio corrió el Launch Audit (modo `emerge`) antes de tocar
  nada. Es la tarea de la línea de tiempo que va **antes del launch y después de la carga**: mide lo que ya
  está cargado contra UDS, no el archivo. El audit de la tarea es el del **data spec**. Lo que encontró
  (divergentes, ~12k *meta mismatches*, Okta incompleto) describe la población vieja: se exporta como
  "antes" y no se arregla todavía.
- ✅ **Aviso visto en vivo: *"Prefill→UDS binlog inactive"*** en el app de la tarea. Pasa a ser un chequeo
  **antes de cargar** (§ Sincronización con UDS ya lo decía). 🔍 Los miles de *meta mismatches* pueden
  venir de ahí: cambios en prefill que nunca llegaron a UDS. Sin verificar.
- ✅ **Dónde estaba el archivo:** ni en la tarea ni en el SFTP del cliente (nada posterior a 2024).
  Ignacio pasó la tarea a **Info Needed** y preguntó; la PM respondió en ~3 h: *estaba en el SFTP de
  cronjobs, lo moví al DM SFTP y lo adjunté*. El link quedó en el campo ***Attachment URL*** de la tarea.
  🔍 Confirma la hipótesis de la sesión: **el cron consume el archivo del SFTP del cliente y lo archiva
  en cronjobs**; un SFTP del cliente vacío no quiere decir que el archivo no exista.
- 🔍 El nombre archivado lleva un prefijo con fecha y hora (`<cliente>_AAAAMMDD_HHMMSS_` + el nombre del
  spec): probablemente el sello del cron. El archivo vino `.pgp` → se descifra en *SOS › IT Tools*.
- 🔍 **"Moved", no "copied":** el `.pgp` en DM Task puede ser el único ejemplar fuera del sistema, y es
  la copia de la población completa que pidió el PM. *SOS › Files* no sirve para eso (TTL de 30 días).
- 🔍 **DOC (*SOS › Design & Build*) como lugar del audit del data spec**: la guía dice *"receive, audit and
  export customer data files"*. Que su audit **sea** el del spec es inferencia → pregunta abierta.
- Riesgos de las exclusiones, anotados para cuando se cargue: **fecha de ingreso actual vs. original**
  (recontratados), la columna que identifica interns/contractors, **LOA** nombrado como ejemplo pero no
  en la lista, el **CEO** no puede quedar filtrado, y gente huérfana si se excluye a su manager.
- *Services OS — User Guide* re-exportada el 08/10: **sin cambios** respecto del 06/10.
  ⚠️ *(Nota del merge, 08/10: otra sesión del mismo día registró un re-export **v27 con cambios** —
  lectura/escritura por módulo; entrada *Re-export de la guía de Services OS* abajo. 🔍 Probablemente
  dos exports distintos; vale el v27 hasta que Ignacio confirme cuál es el último.)*
- Todo en [[Perceptyx/procedimientos|procedimientos]] § Carga del archivo final (paso 1b) y § Launch Audit.

---

## 2026-10-08 — Helper formulas: dónde está

- 📣 Ignacio: el documento de **helper formulas** (genera los `UPDATE`) lo tiene **guardado en su equipo
  de trabajo**, directo en **Descargas** (`Downloads`). Anotado en [[Perceptyx/plataforma|plataforma]] § herramientas.

---

## 2026-10-08 — Shadow *Users set up* (24/09), segunda parte

Fuente: transcripción de la segunda grabación (8 min), pasada por Ignacio.

- 📣 Emily **se equivocó de columna** en el BUSCARV del conteo (7 = *hierarchy responses* en vez de 8 =
  *hierarchy completions*); lo detectó comparando las dos columnas y no afectaba: las diferencias estaban
  muy por encima de 5. Queda como chequeo en [[Perceptyx/procedimientos|procedimientos]] § Usuarios de
  manager.
- Segundo nivel resuelto con otro BUSCARV y un control de que el manager elegido coincida con el
  `mgr_id`. **El cierre de la tarea tampoco se vio en esta parte.**

---

## 2026-10-08 — Umbral de la tarea: lo que dice el pedido manda

- 📣 **Ignacio, 08/10:** la tarea dice *responses* → se cuenta por **respondents**, no completions. Al PM
  se le pregunta solo si el pedido se contradice. Volcado a [[Perceptyx/procedimientos|procedimientos]]
  § Usuarios de manager.

---

## 2026-10-08 — Shadow *Users set up* (24/09): transcripción completa

Fuente: transcripción del video, pasada por Ignacio el 08/10. **Supera** al resumen de Gemini de la
entrada de abajo. No se archiva: tiene nombres de empleados del cliente.

- ✅ Sección reescrita: [[Perceptyx/procedimientos|procedimientos]] § Usuarios de manager. Lo nuevo:
  - *Manager Hierarchy Tree › Settings › Add Users*: los campos de la pantalla; el **nombre del status
    de manager cambia según el cliente**;
  - el status de "siguiente nivel" **lo crea el PM**, con su propia configuración de reportes;
  - `emerge.survey_completed = 1` = completion; las preguntas en `all_data` son las columnas `000000…`;
  - `UPDATE` de status **con `AND status = manager`**, por los duplicados permitidos;
  - **los backups no se borran nunca**: sirven para revertir si el PM vuelve semanas después;
  - el ancestro se busca con **BUSCARV en cadena** (jefe → jefe del jefe), no partiendo el `tree_path`.
- **SUPERSEDED (08/10):** Gemini decía que en la sesión se crearon los usuarios (ya existían), que la
  creación era "por completions" (el checklist pedía respondents) y que la búsqueda del ancestro quedaba
  sin método (el método se armó).
- ⚠️ **Sigue abierto:** el cierre (la sesión se cortó) y, para la tarea del 08/10, cómo se **crean** los
  Below Threshold (¿otra pasada de *Add Users* o todos como Manager y reasignar?).

---

## 2026-10-08 — Shadow *Users set up* (24/09, resumen de Gemini): usuarios Manager / Below Threshold

Fuente: notas de Gemini de la sesión del **24/09** con Emily (Guillermo, Andrea, Ignacio), pasadas por
Ignacio el 08/10. **Solo resumen, sin transcript.** El docx no se archiva (§ 9: se extrae, no se archiva).

- ✅ Procedimiento volcado a [[Perceptyx/procedimientos|procedimientos]] § Usuarios de manager. Lo nuevo:
  - la tarea tiene **dos partes**: crear usuarios Manager (criterios del checklist del PM: activo
    deshabilitado, SSO ID = emp_id, duplicados permitidos, username inicial + apellido) y reasignar a los
    **Below Threshold** — status de "siguiente nivel" + vista del primer manager de arriba que llega;
  - **el umbral es de completions, no de respondents** — en ese caso; Emily lo confirmó con el PM. Es una
    pregunta **por tarea**;
  - `get-mgr-counts` → Excel filtrado → backup de `users` y contraseñas temporales → `tree_path` +
    búsquedas en Excel → tres `UPDATE` (status, view display, `emp_id_view`); ojo con comas en los nombres.
- **SUPERSEDED (08/10, mismo día):** la hipótesis de la entrada anterior (*"Manager Below Threshold es un
  status"*, `emp_id_view` = ancestro con ≥5) **se confirma en lo esencial**. Lo que no estaba: la parte
  de crear usuarios sale del checklist del PM, y el umbral puede ser completions.
- ⚠️ **Sigue abierto:** la query para encontrar el ancestro (Emily lo dejó pendiente; la sesión se cortó),
  el nombre real del status, la pantalla exacta donde se crean los Manager, y el cierre (quién manda los
  accesos).

---

## 2026-10-08 — Primera tarea real: `PFS: Creates Manager Users`

Fuente: captura de la tarea de Certinia que pasó Ignacio (✅ el pedido; cliente y survey omitidos).

- ✅ **El patrón del pedido** (tipo *Standard*, prioridad *Normal – complete by due date*): usuarios
  **Manager** para quien llega a **5 o más respuestas en su jerarquía**; **Manager Below Threshold** para
  los que no, con acceso al **primer nivel de arriba que sí llega**.
- ~~El vault no tiene procedimiento para esto~~ **SUPERSEDED (08/10):** estaba en el shadow del 24/09,
  sin volcar — entrada de arriba. 🔍 Lectura armada antes de encontrarlo: `get-mgr-counts` → ≥5 vista
  propia → <5 status *Below Threshold* con `emp_id_view` del ancestro → integridad → Launch Audit `users`.
  Coincidió en lo esencial.

---

## 2026-10-08 — Re-export de la guía de Services OS (versión 27)

- ✅ La guía ahora etiqueta **cada módulo** como READ ONLY o READ & WRITE → tabla en
  [[Perceptyx/services-os|services-os]] § Lectura o escritura. **Customizations figura READ & WRITE**: la guía
  alcanzó lo que mostró Jackie el 21/09 y confirmó Ignacio el 06/10 (el cuerpo todavía dice *"Read-only in v1"*).
- Nueve módulos READ ONLY, no solo Database Tools. 🔍 No contradice a Ignacio si se lee *"lo único de solo
  lectura"* como *lo único que reemplaza algo que escribía*: los otros ocho son visores. Lectura propia, sin
  confirmar.
- Detalle agregado: estados de Branching, metadata de Customizations (otros surveys que comparten el
  overlay), presets del image optimizer, columnas y subida en Files, Feedback triageado dentro de SOS.
- El *SOS Cheat sheet* son dos planillas de Google embebidas: el export no las trae. Siguen sin incorporar.

---

## 2026-10-06 — Captura del 21/09: SOS › Customizations

- ✅ *"Browse and edit a survey's file overlays against `apps @ master` — push changes as a merge request"*:
  **confirma con la pantalla** lo que dijo Ignacio (en SOS solo las queries son de solo lectura).
- Cuatro tipos de archivo (*custom code*, *template overlay*, *DB override*, *data*) contra las tres capas de
  la guía; paneles File Tree / Viewer / File Metadata → [[Perceptyx/services-os|services-os]].
- Con esto quedan volcadas **todas las capturas pedidas del 21/09**.

---

## 2026-10-06 — Capturas del 21/09: emails y traducciones (5)

- ✅ **Editor de emails** (`rm=survey_launch`): *Load Email / Body From Another Survey*, remitente, reply-to y
  asunto por defecto, imagen como `cid: banner`, y **la sintaxis real del translation tag**:
  `[%- obj.translate_this("…") %]` — explica de raíz el error de las comillas dobles.
- ✅ Ops tool ***Translations for Data Collector (DC)***: cinco campos y sus defaults; **no envía** a
  traducir, eso es en el *Translation Tool*.
- ✅ **Survey Admin** (`rm=admin`): completadas *User Administration* y *Comment Report Functions* en el mapa
  de [[Perceptyx/plataforma|plataforma]].
- ✅ ***Translation Tool***: las seis acciones de la entrada, la grilla de idiomas (`&trans_lang=`), y la vista
  por idioma con pestañas *Client* / *Core*, cuatro estados con color, *Lock translation*, *Refetch
  SmartCAT*, buckets. El inglés guardado lleva HTML: confirma por qué tiene que coincidir tal cual.
- Todo en [[Perceptyx/procedimientos|procedimientos]] § Emails y § Traducciones. Clientes de las capturas:
  omitidos.

---

## 2026-10-06 — Capturas de la sesión del 21/09 (8)

- ✅ ***Quality and Integrity Checks***: el diálogo real. **Corrige** lo anotado del transcript: el campo es
  *Include previously approved alerts*; **aprobar** una alerta es la pregunta interactiva del final del
  script. Y aparece una opción no explicada, *Run Big Brother report only* (pregunta abierta).
- ✅ **SOS › Perl Scripts**: 73 scripts, con nombre y descripción; corren en una terminal embebida. Salida real
  de `verify-survey-integrity` (usuarios con `emp_id_view` de alguien que no es manager; registros fuera de
  `managers_tree`).
- ✅ ***Sync reporting demographics***: *Test Mode* (default sí) y *blank out all_data* (default **no**, Emily
  usaba sí: pregunta abierta). Y la lista de ops tools de datos, con *Remove Ineligible Participants* y
  *Remove Partial Responses*.
- ✅ Las **nueve tarjetas** del Launch Audit con su *family* técnica (`divergent_users`, `name_cleanup`,
  `wrong_active_state`…), *Export* por tarjeta, y el aviso **binlog inactive** en *SSO ID Hygiene*: si el
  binlog está apagado, lo editado en MAC o prefill no llega a UDS.
- ✅ **SOS › Launch** y ***Survey Launch Audit***: tablas `emerge` / `users`, *Start Audit*, limpiar caché de
  plataforma (survey, todos, usuarios puntuales), widgets USER / META y MAPPINGS. La página dice que los
  arreglos llegan *"en fases siguientes"*; Jackie ya los usaba.
- Todo en [[Perceptyx/procedimientos|procedimientos]] § Emails, traducciones y chequeos del app y
  [[Perceptyx/services-os|services-os]]. Nombre del cliente de la captura: omitido.

---

## 2026-10-06 — Sesión del 21/09: *DelOps Emails* (Jackie, transcript completo)

- Transcript completo (0:02 → 54:01) pasado por Ignacio. Sin capturas todavía. Clientes nombrados: omitidos.
- **Nuevo en procedimientos** → [[Perceptyx/procedimientos|procedimientos]] § Emails, traducciones y chequeos
  del app: *Quality and integrity checks* y *Sync reporting demographics* (ops tools), la tarea **Launch
  Audit** con sus nueve categorías, **armar, corregir y probar emails** (translation tags, merge fields, el
  error de las comillas dobles, probar agregándose como respondente) y **traducciones** (ops tool de inglés,
  Microsoft vs. SmartCat, *Translate Survey Content*, carga de archivo del cliente).
- **SOS** → [[Perceptyx/services-os|services-os]]: Perl viejos vs. Python nuevos, Files, IT Tools, y
  ⚠️ **Customizations**: Jackie **edita y publica** subclass files desde ahí (flujo de aprobación por Slack,
  deploys 10:00 y 15:00 Central, code freeze en temporada alta), mientras la guía de SOS lo describe como
  **solo lectura (v1)**. 🔍 Piloto vs. guía; queda como pregunta.
- **Herramientas y glosario** → [[Perceptyx/plataforma|plataforma]]: Transmit (*DM Task* / *DM Task EU*),
  vault de SFTP de clientes en 1Password, Postman solo para probar la API, **Boomi → Merge** (ingesta),
  jails locales dados de baja, master app **LEB enablement** para practicar.
- 🔍 **Conexión con lo de Emily:** el 21/09 Jackie mostró con interfaz (ops tools) lo que Emily enseñó una
  semana después con scripts Perl (reordenar → resincronizar `all_data`, verify integrity). **Son dos formas
  de hacer lo mismo, con la misma validez** (regla de Ignacio, abajo); quedaron juntas en § Reordenar.
- 🔍 El Launch Audit explica **cuándo** aparecen en la práctica los problemas de UDS de § Sincronización con
  UDS: *divergent identity* es la categoría más frecuente, y es exactamente el caso de *divergent users* de
  Confluence.
- **Respuestas de Ignacio (06/10), mismo día:**
  1. **Regla nueva:** *"siempre registrá las distintas formas de hacer lo mismo, por ahora con la misma
     validez"* → [[KOS/Reglas|Reglas]] § 9.
  2. **En SOS lo único de solo lectura, por ahora, son las queries a las bases** (*Database Tools*). Cierra
     la duda de Customizations: **se edita y publica desde SOS**, como mostró Jackie; la "solo lectura v1" de
     la guía queda `SUPERSEDED` para ese módulo.
- Accesos pendientes **al 21/09**: SSH keys de Querious, credenciales de Transmit, vault de SFTP en
  1Password. Si ya se resolvieron, no consta.

---

## 2026-10-06 — Capturas de la plantilla de proyecto (16/09)

- ✅ ***2026 LEB Project Timeline*** (plantilla de Certinia, Gantt), fases 1 a 1.6.5 →
  [[Perceptyx/procedimientos|procedimientos]] § La plantilla de proyecto.
- 🔍 **Hallazgo:** en el modelo LEB el **PM es quien carga, arma el árbol y construye** por defecto; las
  tareas de Delivery Ops (`PFS:`) son casi todas **OPTIONAL** (respaldo cuando el PM no las hace). Lo propio
  de DelOps sin alternativa: **QA** (histórico, archivo inicial, survey en inglés, traducciones) y **carga
  de datos históricos**. Cambia la imagen del puesto: menos "el que carga todo", más **respaldo técnico +
  control de calidad**, y lo que se complica (como la carga final del 23/09).
- Faltan las fases posteriores (lanzamiento, reporting, cierre).
- Captura de `prefill_data` del survey de prueba de Jackie: **las columnas estándar del data spec** en la
  práctica (identidad, `auth`, `mgr_id`, `sso_id`, `active`, fechas, organización, país/estado/ciudad) y
  los **backups de `all_data`** con fecha o nombre → [[Perceptyx/modelo-de-datos|modelo-de-datos]].
- 📣 Ignacio: **DO Support es el canal de Slack de Delivery Ops**: **`#do_support`**. Relación con *#pfs_support*: primero supuesta, después corregida, y finalmente **Ignacio decide tratarlas como el mismo canal** (*"puede ser que anteriormente se llamara así"*): donde la documentación diga `#pfs_support`, hoy es `#do_support`.
- ✅ Captura de ***Functions › Survey Setup*** (`rm=admin`, *Survey Admin Links*): mapa completo de las
  pantallas de configuración del reporting site → [[Perceptyx/plataforma|plataforma]]. Corrige un dato: el
  atajo a una tabla es **`rm=18&tbl=`**, no `table=`. *Rebuild Setup* de las guías = el botón **Rebuild Setup
  Configuration**.

---

## 2026-10-06 — Sesión del 16/09: *Databases general* (Jackie, transcript completo)

- La **primera sesión de training** (tercer día de Ignacio), en dos partes, completa (0:00 → 56:09).
  Clientes nombrados: omitidos.
- **Modelo de datos contado por DelOps** → [[Perceptyx/modelo-de-datos|modelo-de-datos]] § Cómo lo explica
  Delivery Ops: una app/base por survey, master app vs. sub apps, tabla por tabla, y **cómo leer un QID**
  (`02` = LEB, `01` = classic, `07` = demo del archivo; preguntas con la página en los dos primeros dígitos).
  Coincide con engineering.
- **Cola de tareas**, lo que faltaba → [[Perceptyx/procedimientos|procedimientos]] § Cola de tareas: la
  plantilla de proyecto (Gantt) de los PM, **cuándo aparece una tarea** (Ready to Start + vencimiento +
  resource role), los estados, qué mirar en la tarea (servidor, prioridad, tipo *custom*), comentarios con
  historial y horas en múltiplos de 0,25.
- ✅ **PFS = Platform Services**, de boca de Jackie: el cambio de nombre fue **justo antes de que entrara la
  cohorte**.
- **Guillermo** va a onboarding/implementación (🔍 rol TSM) con JT; **Andrea**, Bill y Steve; **Ignacio**,
  Kim, con oferta de *shadow* con Elena.
- Herramientas diarias según Jackie: **Certinia** (la mayor parte del tiempo), los **reporting sites** y
  **SOS** (*"in its infancy… but amazing"*); Querious, cada vez menos.
- Accesos pendientes al 16/09: licencia de SQL (Querious) y **llaves SSH**.

---

## 2026-10-06 — Cinco capturas del video del 23/09

Pedidas para cerrar lo que el audio no decía. Datos de clientes visibles en las capturas: no copiados.

- ✅ **SOS › Design & Build › DOC** es donde Jackie dedujo el CEO: *drop a file → audits, maps, builds the
  LEB-ready file*. Tres pasos: Load File (activo), Configure Demographics (V2), Verify Data (V3). Fases de
  SOS confirmadas: Initiation, Design & Build, Launch, Reporting, Close.
- ✅ **Corrección de un nombre que venía mal desde el training:** la tabla de branching es
  **`surv_questions_conditional`**, no *"Q condition"* (Gemini). Corregido en procedimientos y plataforma.
  Lista exacta de las nueve queries de dependencias del snippet *check resp*.
- ✅ **`prefill_data` tiene columna `auth`** → *off-codes* = auth codes, confirmado.
- ✅ **Managed Settings**: toggle *Enable DC Mosaic* (default DC Amsterdam) + los tres de sync.
- ✅ **Operations Tools**: catálogo de herramientas por sección; *Build Hierarchy from Loaded Data* existe
  (Download, 360 y Ask) — lo que había dicho el bot sobre el nombre era cierto. *Create demographic options
  from participant data* trae **Test Mode = Yes por defecto**.
- ✅ Los demos *attributed* tienen ID `02_XX_07` (coincide con engineering).

---

## 2026-10-06 — Video del 23/09 completo: una carga final de punta a punta (Jackie)

- Transcript completo (0:02 → 1:19:19), copiado del panel del visor de Drive. **Quien muestra es Jackie**,
  no Emily. → [[Perceptyx/procedimientos|procedimientos]] § Carga del archivo final en un survey de LEB.
- **La fuente más valiosa del dominio hasta ahora:** una tarea real, de tomarla en la cola a cargar las
  horas, con todo lo que se rompió en el camino.
- Lo que aporta que no había:
  - **Cómo se toma una tarea** (campo *Resource* + Save → *My Tasks*) y por qué marcar *In Progress*.
  - **La decisión LEB vs. clásica**, con criterio explícito: sin dependencias de índices → LEB (limpio); con
    dependencias → clásica. Junta la regla 3, la regla 10 y el modelo de datos en una sola decisión.
  - **Duplicados de HRIS** (registro nuevo al cambiar de rol o país): diagnóstico por SQL, arreglo en el
    master, y la advertencia de que el feed diario lo pisa.
  - **Los checks de integridad típicos** y qué hacer con cada uno (países sancionados → PM).
  - ✅ ***Build Hierarchy from Loaded Data*** existe (lo había nombrado el bot sin fuente) y **SOS deduce el
    CEO** de un árbol.
- Asignación de la cohorte: Ignacio → Kim; Andrea → Bill y Steve.
- Jackie: **la IA es muy buena con SQL**, usarla. 🔍 Encaja con la tarea de agrupar combinaciones del 02/10.

---

## 2026-10-06 — Video *9.23.2026 task walkthrough* (solo una captura)

- Ignacio tiene grabaciones de sesiones en el Drive de la empresa con transcript visible pero sin botón de
  descarga. De la captura de la primera ya salieron dos cosas:
- ✅ **Equipo confirmado: Kim (C).** Emily, 23/09: *"So, Nasio, for you it would be Kim."* Pregunta abierta
  cerrada.
- ✅ **El DelOps Workspace en Salesforce**: un *Task Workspace* por PM, *My Current Tasks*, *Open Tasks –
  All DelOps* y la cola de Cron/Automation → [[Perceptyx/procedimientos|procedimientos]] § Cola de tareas.
- ~~El resto del video, pendiente hasta tener el transcript.~~ Llegó completo: ver entrada de arriba.

---

## 2026-10-06 — Sesión del 02/10: *QA DCT* (volcada)

- Era la sesión de las 10:30 del 02/10 que estaba pendiente. Llegaron solo las **notas rápidas** de
  Gemini. Emily, Andrea, Guillermo, Ignacio.
- **QA de branching**: walkthrough del survey con códigos de prueba (*"off-codes"* → 🔍 auth codes) para
  verificar que cada combinación de demos precargados vea las preguntas correctas.
- 📣 **Ignacio calculó 135 combinaciones** (país × ubicación × subtipo × tipo). El QA manual no escala;
  Emily lo frenó para definir el proceso con Jackie.
- **Tarea asignada a Ignacio:** agrupar las combinaciones con IA para reducir las pruebas. ⚠️ Chequear
  antes la lista de clientes sin GPT; alcanza con reglas + combinaciones, sin datos de personas. Método
  sugerido en [[Perceptyx/procedimientos|procedimientos]] § QA de branching: agrupar por **camino** del
  survey, no por combinación.
- No consta qué pasó después.

---

## 2026-10-06 — Segundo cierre del día

Lo que cambió desde el primer cierre (DC Mosaic, siglas, catálogo de SKUs, PM Power Hour, consultas al
bot):

- **Síntesis del _indice ampliada a ocho ideas.** Nueva: *el alcance lo define el contrato* (topes por
  SKU, presupuesto de horas por rol, CSQL para lo que excede, clientes FedRAMP fuera de alcance).
- **Siglas:** cerradas WTC, DRA (✅ Data Release Authorization), DC vNext = Mosaic, LEAP = LEB (por
  decisión). Abierta solo la del **CSP del cron**.
- **El bot Pyxee-CVO como herramienta:** útil para **encontrar** documentos (llevó al DOS y a la PM Power
  Hour), no para **cerrar** datos. En el mismo día: confirmó una sugerencia sin fuente (CSP), generalizó una
  cláusula de un paquete a "cualquier survey" (data automation) y repitió la misma respuesta con el título
  de la pregunta (árbol de managers). Regla en Reglas § 1.
- **Dos reglas nuevas en Reglas § 9:** lista de clientes sin GPT; clientes FedRAMP / US Citizen solo para
  ciudadanos de EE.UU.
- **Huecos que ya no se resuelven buscando:** MCP, el procedimiento de DelOps para el árbol de managers, el
  de *Create Data Automation*, el CSP del cron. Quedan para personas (Melanie, Jackie, Emily).
- Prolijidad: se sacó del repo un archivo de bloqueo de Word (`~$…docx`, 162 bytes, venía de la migración
  inicial) y se agregó `~$*` al `.gitignore`.

---

## 2026-10-06 — Árbol de managers según Pyxee-CVO (sin poder verificar)

- El bot respondió con un procedimiento citando *LEB FAQ – (Gemini Friendly).pdf*; **Ignacio no tiene
  acceso a ese archivo**. Queda 📣, no ✅.
- Lo que dice: habilitar *Manager Hierarchy* (hasta 3 días hábiles), herramienta *Build Hierarchy from
  Loaded Data*, `rm=managers_tree`, solo con feed automatizado, antes de crear el evento.
- 🔍 Parece el flujo del PM en LEB (incluye *"pedir un audit a PFS"*), no el de DelOps. Se juntó con el
  camino clásico del training en [[Perceptyx/procedimientos|procedimientos]] § Armar un árbol de managers.
- Segunda consulta pidiendo *"for a delivery ops manager"* y un link de Confluence: misma respuesta con el
  título adaptado a la pregunta, **sin link** (no hay página en lo que indexa el bot). Sumó la ruta de
  acceso a reportes (*Edit Reporting Access › Hierarchy View*), que 🔍 conecta con los árboles *snapshot*
  de UDS: el camino LEB es el de la arquitectura nueva.

---

## 2026-10-06 — "¿Cómo se crea una data automation?" (Pyxee-CVO)

- Respuesta del bot **verificada contra el DOS**: el núcleo es real (✅ un script con plantilla estándar,
  hasta 3 *data triggers* acordados antes, cambios posteriores cotizados, el cliente mantiene el archivo
  igual, 94 demos = 44 + 10 + 40), **pero es la cláusula del *Lifecycle Event Package***, generalizada a
  "cualquier survey", y escrita **para el cliente**. No es el procedimiento de DelOps para armarla.
- Lo que el bot agregó y **no está en el DOS** (CSV UTF-8, clave GPG, raíz del SFTP, nightly) queda 📣:
  plausible y coherente con la guía de cron del 360, sin fuente.
- 🔍 Consecuencia útil: si un cron de lifecycle se rompe porque el cliente cambió el archivo, eso **está
  fuera de contrato** — dato para el PM.
- *Create Data Automation* sigue siendo un hueco.

---

## 2026-10-06 — PM Power Hour (contratos y horas) y el CSP inducido

- ⚠️ **Lección sobre el bot:** Pyxee-CVO dijo *"no sé"* qué es CSP; cuando Ignacio sugirió *"Customer
  Support something"*, contestó *"Customer Success Partner"* citando una transcripción **donde la sigla no
  aparece** (verificado). No cuenta como dato. Registrado en Reglas § 1 como caso de pregunta inductora.
- La transcripción citada sí sirve: ***PM Power Hour: Pricing, Packaging & Scoping*** (Melanie con los
  PMs, 🔍 ~principios de 2026) → [[Perceptyx/catalogo-servicios|catalogo-servicios]] § Cómo se lee un
  contrato. Lo nuevo:
  - **Renombres de producto:** Sense, Cultivate, OnDemand e *Insights Platform* son nombres viejos; ahora
    *listening channels* (point-in-time, lifecycle…) y agentes de IA (Activate, conversational listening,
    narrative analysis). El mapa de productos del batch 5 queda SUPERSEDED en el glosario.
  - **End size** = tope de participantes; pasarlo no tiene tolerancia contractual → CSQL al CSM.
  - **Estimador de horas** (feb. 2026): presupuesto de horas por proyecto para **cuatro familias de rol,
    una es PFS = DelOps**. Las horas que Ignacio carga se miden contra eso.
  - Lifecycle ahora es SKU de una vez; *human translations* → *premium translations* (SmartCat vs.
    Microsoft); el catálogo de SKUs está en revisión.
- Nombres de clientes de la transcripción, omitidos; el texto no se archiva.

---

## 2026-10-06 — *Description of Service* (catálogo de SKUs)

- ✅ **DRA = Data Release Authorization**, confirmado en el documento que citó el bot: pasa de 📣 a ✅.
- ✅ Nota nueva [[Perceptyx/catalogo-servicios|catalogo-servicios]]: qué vende Perceptyx como servicio y
  con qué **topes** (demos, archivos, surveys, iteraciones). Responde *"¿esto está en el contrato?"*.
- ⚠️ **Hallazgo con consecuencia directa:** los clientes con *Gold – FedRAMP / GovCloud / US Citizen
  Support* solo pueden ser atendidos por **ciudadanos de EE.UU.** Ignacio no puede tocar sus sistemas,
  datos ni tickets. Regla nueva en Reglas § 9.
- 🔍 Los conectores de HRIS (Workday RaaS, SuccessFactors, Oracle HCM) son terreno conocido para Ignacio
  desde UKG.
- 🔍 Mayflower e ITSG no son clientes: son organizaciones externas a las que algunos clientes mandan su
  Census anual.

---

## 2026-10-06 — Consulta a Pyxee-CVO

- Ignacio le preguntó al bot interno **Pyxee-CVO** (*"Pyxee assistant with access to CVO KB"*; distinto
  de @Pyxee-csg). Captura del 06/10.
- 📣 **DRA = *Data Release Authorization***, citando *Description of Service – Perceptyx (2025-09)*. Puede
  exigirse según los datos que lleve un export. Marcado 📣 y no ✅ porque un chatbot no es fuente
  (Reglas § 1): pasa a ✅ cuando se lea el documento citado.
- **MCP: *"Sorry, I don't know."*** Tercera fuente que no lo conoce (Confluence de DelOps, Confluence de
  otros equipos, base de conocimiento de Customer Value). La pregunta ya no se resuelve buscando: hay que
  hacérsela a una persona.

---

## 2026-10-06 — Siglas cerradas: WTC, DRA, CSP; equipos vecinos

- 📣 Ignacio: **CSP = Content Security Policies**, **WTC = Workforce Transformation Consulting**, **DRA =
  algún acuerdo de datos**. Con las páginas que pasó:
  - ✅ **WTC**: consultoría ejecutiva (Activate, EP, Design). Es el equipo con más IA documentada:
    agentes GPT, prompts, el bot interno **@Pyxee-csg** que contesta con Confluence.
  - ✅ **DRA**: se marca en Gainsight; Customer Care lo exige para exports de datos crudos.
  - ⚠️ **CSP** como *Content Security Policy* (cabeceras de seguridad) **no encaja** con *"work with the
    CSP on the schedule"* de la guía de cron. Registrado como dos cosas distintas; la del cron sigue
    abierta, menor.
- ✅ **Customer Care**: planes **Gold / Silver / Legacy** desde Q3 2025 (quién puede abrir ticket: admins
  y usuarios finales, o solo admins). El plan se ve en la cuenta de Salesforce y arriba del proyecto en
  Certinia.
- ⚠️ **Regla nueva (Reglas § 9):** Perceptyx tiene una **lista de clientes con los que no se puede usar
  GPT**. Antes de pegarle a una IA algo de un cliente, chequearla.
- Contraseñas de grabaciones que trae la página de WTC: **no se copiaron**. Nombres de clientes de los
  docs de seguridad, tampoco.
- Duplicados: *Customer Care & Support Plans* (×2) y *Perceptyx API Setup Process* (ya procesada el
  06/10), **idénticos**.

---

## 2026-10-06 — DC Mosaic (otros equipos) y LEAP cerrada

- 📣 Ignacio: **LEAP = LEB se asume**; nadie puede confirmar qué quiso decir una transcripción. Cerrada.
- ✅ **Mosaic = DC vNext**, el Data Collector nuevo → nota nueva [[Perceptyx/dc-mosaic|dc-mosaic]] (seis
  páginas del equipo de Data Collector; el roadmap vino como índice de links).
- ✅ **Mosaic toma el survey de LEB y escribe en MySQL Classic por un adaptador**: las tablas de siempre
  siguen recibiendo los datos. Da la razón técnica de la regla 10 (publicar en LEB sube el survey a DC).
- ✅ **"Data Managers"** en engineering: confirma el linaje DM → PFS → Delivery Ops.
- 🔍 **Engineering lista como problema del sistema viejo que los Data Managers escriban directo en la base
  por terminal** — el trabajo del training. Nueva idea 7 en la síntesis del _indice.
- 🔍 **Hay IA en la plataforma:** el *Conversational Listening Agent* (survey conversacional). Matiza la
  idea 6: la IA existe, en engineering; MCP sigue sin aparecer.
- Glosario: Managed 360 vs. SS360, *Advanced Reporting* (legacy) ≠ *Advanced Analytics* (nuevo), OD =
  OnDemand, región *GovCloud US*.

---

## 2026-10-06 — Cierre: relectura completa del dominio

Primer día del dominio: training (5 notas de Gemini) + ~40 páginas de Confluence (DelOps y otros
equipos). Al cierre se releyó todo para revisar conexiones hechas con poca información al principio.

**Lo que cambió al mirar todo junto:**

- ✅ **"LE app" del training = LEB.** La carga del 28/09 era una carga a LEB por el camino seguro (Data
  File Builder). Antes figuraba como una app aparte.
- 🔍 **Tres deformaciones de Gemini resueltas por cruce:** *py bands* = **pyx bands** (`pyx_age`,
  `pyx_tenure`, `pyx_generation`); *M ID / F ID* = **emp ID** (la linkage estándar es Employee ID ↔
  `emp_id`); *rad ID* = **ratee ID**.
- **Nombres de tabla normalizados** en [[Perceptyx/procedimientos|procedimientos]] (`prefill_data`,
  `resp_questions`, `all_data`, `trend_custom_linkages`, `managers_tree`), con nota de la revisión.
- **"Ticket" = tarea de proyecto de Certinia** (el PSA dentro de Salesforce). Toda la documentación la
  llama así; precisado en el _indice y en Reglas § 9.
- 🔍 **Linaje del nombre del equipo: DM → PFS → Delivery Ops.** "DM" sobrevive en la carpeta *DM Task*,
  en los branches `PS-<DM Task ID>` y en engineering (*"Operations/DMs"*).
- 🔍 **Jess = Jess Schwab**, autora de formularios de lifecycle desde 2022: antigüedad en el área.
- 🔍 **MCP no aparece en ninguna página.** La frontera que Melanie le ofreció al puesto en la selección no
  está documentada como trabajo de DelOps. Pasa a preguntas abiertas.
- **Síntesis de seis ideas** que ordenan el dominio, nueva sección en el [[Perceptyx/_indice|_indice]].
- Ajuste de sistema: Inicio ahora lee las entradas de la **última fecha** de esta bitácora (un día puede
  tener muchas) y las preguntas abiertas del _indice.

**Lo que se confirmó de lo inferido temprano:** el modelo de capas de un demo (🔍 en el training → ✅ por
engineering, con el mecanismo de posición); que el *task pool* ya no existe; que PFS = Delivery Ops.
**Lo que no se sostuvo:** Jon Vail como PM (corregido en el batch 2); "SOS" como herramienta de scripts
(es la plataforma de todo).

---

## 2026-10-06 — Otros equipos, segundo envío: jerarquía de managers y Snowflake

- 📣 Ignacio: **estos y los cinco anteriores son de otros equipos, no de DelOps.** Quedó como regla 5 del
  régimen del dominio: se usan para entender, no como procedimiento.
- ✅ **`managers_tree` por dentro**: la raíz es `emp_id = 0`, y `tree_path` es el camino precalculado
  desde la raíz. Explica el "quitar el 0 del CEO" y por qué cambiar un manager obliga a rebuild.
- ✅ **Jerarquía en la arquitectura nueva**: árboles como *snapshot* en UDS (Draft → Live → Closed),
  armados para reporting. Muchos nodos sueltos = HRIS mal → se corrige en la fuente.
- ✅ **Dialogue → Snowflake** (NLP), una sola dirección; lo que no cumple se saltea sin aviso.
- ⚠️ **Contradicción registrada:** UDS = *Unified Data Store* (Activate) vs. *User Directory Service*
  (Manager Hierarchy Tree). Abierta, menor.
- *Demographics Data* vino dos veces, idéntica.

---

## 2026-10-06 — Engineering: modelo de datos (fuera del espacio de DelOps)

- 📣 Ignacio: **las páginas del espacio de Delivery Ops ya están todas**. Lo que sigue viene del resto de
  Confluence. Este batch: cinco páginas de engineering → nota nueva
  [[Perceptyx/modelo-de-datos|modelo-de-datos]].
- ✅ **El modelo mental del training queda confirmado, con el mecanismo:** el valor de un demo en
  `all_data` es la **posición** de la opción en `resp_list` (0 = vacío). Explica de un golpe por qué
  reordenar obliga a reconstruir, por qué la carga final de 360 no re-sube `_resp.html` y por qué los
  trends necesitan una tabla de traducción.
- ✅ Los demos se copian a `all_data` **cuando el respondente entra al survey**, y lo hace solo el Data
  Collector.
- ✅ **El binlog ignora `DELETE` y `TRUNCATE`** — 🔍 borrar de `prefill_data` no borra de UDS (importa para
  los pedidos de borrado de PII). Tampoco viajan usuarios internos (`@pyx.com`, `@perceptyx.com`).
- ✅ **DC vNext = Data Collector vNext.** Dos arquitecturas conviviendo: la legacy que opera DelOps
  (MySQL, una base por survey, una columna por demo) y la nueva (PostgreSQL, Snowflake, Data Hub, JSON).
- 🔍 Muchas tareas de DelOps son consecuencias operativas del modelo legacy; engineering ya documenta sus
  límites (clientes con 100+ demos y decenas de miles de opciones).
- 📣 Ignacio: vienen cinco más.

---

## 2026-10-06 — Guía de Services OS

- ✅ **SOS = Services OS**, la plataforma interna de operaciones de Customer Value → nota nueva
  [[Perceptyx/services-os|services-os]].
- ✅ **Mapa de reemplazos**, explícitos en la guía: Trend Mapping reemplaza el setup de trend en MAC; Menus
  las tablas de menús; Launch Audit los pedidos a CVOps; Launch Dashboard el mail semanal. Y por lectura
  propia: Cron Manager ← jail + git; Database Tools ← Querious (**pero solo lectura**); IT Tools ← SFTP y
  PGP; UDS User Health ← el troubleshooting manual de UDS; DOC ← audit de data specs.
- ✅ **SPT ahora se llama CVOps.**
- 🔍 **El hueco que deja:** si Database Tools es solo lectura, ¿por dónde pasan las escrituras que el
  training hizo en Querious? Abierta.
- Anotados los procedimientos afectados (trend mismatch, troubleshooting de UDS, cron de 360) con un
  puntero a SOS, sin borrar el método documentado.

---

## 2026-10-06 — SOS como destino de todo

- 📣 Ignacio: **no tiene jail ni acceso al repo `cronjobs`**. El equipo se está moviendo de las
  herramientas dispersas (jails, Querious) a **hacer todo en SOS** —cron jobs y ejecución de scripts
  incluidos—.
- 🔍 Consecuencia para el vault: **parte de lo documentado en Confluence describe herramientas en
  retirada**. Marcado en [[Perceptyx/cultivate-360|cultivate-360]] § Automatización por cron y en
  [[Perceptyx/plataforma|plataforma]] (SOS, jail, Querious). La lógica de cada procedimiento probablemente
  sigue; el *dónde* puede cambiar. Coincide con lo que Emily dijo el 01/10 (SOS en uso hace ~1 mes) y con
  el *"cambia semana a semana"* del 06/10.
- *Related Resources – Cultivate: 360 Feedback* vino **vacía** (la página es solo título; probablemente
  links o páginas hijas que el export no trae).
- CSP y el orden de columnas del 360: Ignacio tampoco lo sabe; siguen abiertas.

---

## 2026-10-06 — Batch Confluence 6: 360

- ✅ Cinco páginas de **Cultivate – 360 Feedback** → nota nueva [[Perceptyx/cultivate-360|cultivate-360]]:
  carga inicial y final, los cuatro demos propios (Survey Version, Relationship, ratee_id, Participant
  Fullname), usuarios de prueba, demo oculto de relaciones combinadas y automatización por cron.
- ✅ **Llegó la página real de usuarios de prueba**; la del batch 3 era una conversión fallida. Marcada
  SUPERSEDED.
- ✅ **El jail es el entorno de desarrollo propio** (copia de bases, repo `cronjobs`, MailHog). Pregunta
  cerrada.
- ⚠️ Dos páginas de carga 360 **no coinciden en el orden de columnas**; se sigue la que parece más nueva.
- 🔍 **La regla de la carga final es la regla 3 de siempre:** si no hay demos nuevos, no se vuelve a subir
  `_resp.html` — se suman valores con scripts, para no mover Demo IDs ni índices de un survey ya armado.
- 🔍 La automatización por cron es **desarrollo de verdad** (git, branches, merge requests, Perl sobre una
  base, pruebas en el jail). Es la cara del puesto más cercana a la frontera técnica que nombró Melanie.

---

## 2026-10-06 — Batch Confluence 5: data specs, trends, standard forms

- ✅ **Data specs**: el PM revisa → Delivery Ops corre el audit → carga apenas pasa, o se pide excepción.
  En **self-service no se carga al pasar**: se arma el cron. Lista de lo que nunca se acepta (xlsx para
  automatización, columnas duplicadas, archivos que no parsean, jerarquías custom sin contrato) y de lo que
  se suele aprobar.
- ✅ **Trend mismatch**: la versión escrita de lo que Emily mostró el 01/10. La regla que no estaba en el
  training: **el par `cond1` + `trend_app_id` no se repite**; se fusiona por `cond2` con `OR`. Y la query
  de fusión se prueba primero en el *jail*.
- ✅ **Standard Forms** da el **mapa de productos**: Ask (Classic / Self-Service), Sense (lifecycle:
  candidato, onboarding, exit), Cultivate – 360 Feedback, Dialogue. Y la taxonomía de tareas
  (*Automation › New CRON build › …*).
- ✅ Nombres reales confirmados: `trend_custom_linkages`, `managers_tree`.
- ⚠️ *Create Data Automation* vino **vacía**.
- 📣 Ignacio: el próximo batch trae lo de **360**.

---

## 2026-10-06 — Batch Confluence 4: SSO y columnas reservadas

- ✅ **SSO completo**, del mail del PM a la routing rule en Okta: [[Perceptyx/procedimientos|procedimientos]]
  § SSO. Cierra el circuito que el alta dejaba abierto (el certificado "falso" se reemplaza acá).
- ✅ **US y EU difieren en una sola cosa** en la configuración de Okta: el sufijo de la Login URL en UDS.
- 🔍 **El Group ID de Okta es el hilo del cliente** entre Okta (IdP Username, routing rule), MAC
  (`uds_company_id`) y UDS.
- ✅ **Columnas con nombre reservado** (`group`, `order`, `key`…) rompen las cargas **directas** a LEB; el
  camino normal (Data Audit Script + Data File Builder) ya lo controla. Confirma que las bases son
  **MySQL 8.0** y que **SPT es también un proyecto de Jira**.
- Abierta nueva: si el SSO Team es parte de Delivery Ops.

---

## 2026-10-06 — Batch Confluence 3: UDS, borrado y PII, API, 360

- ✅ **UDS** — cómo decide la sincronización (binlog encendido/apagado, usuario nuevo vs. solo mapping) y
  el troubleshooting cuando un cambio no llega (drift, caracteres especiales, usuarios divergentes, sso_id
  duplicado). Dos trampas: **los clones copian el binlog** y **un feed diario pisa los arreglos
  manuales**.
- ✅ **Borrado de registros / remoción de PII**: política + flujo en Certinia. **Delivery Ops revisa,
  ejecuta y documenta.** Dos opciones con impactos distintos (la remoción de identificadores también se
  lleva comentarios y jerarquía de managers). Falta el *Execution Checklist*.
- ✅ **API estándar**: datos crudos a nivel de registro, **sin umbral de anonimato y sin poder limitarla a
  un survey**; credenciales solo por 1Password. 🔍 Explica el patrón del huddle: por eso los
  stakeholders de privacidad del cliente la frenan.
- ✅ **PFS = Platform Services**, prácticamente confirmado: el workspace de Postman se llama así.
- ⚠️ **360 Test Leader & Raters** es una conversión automática fallida (la página misma lo dice). Lo real
  está en un Google Doc.
- 🔍 **El hilo que une los tres documentos de datos:** lo que manda es la fuente. `prefill_data(_all)`
  manda sobre UDS, el feed del cliente manda sobre `prefill_data`, y el sistema del cliente manda sobre el
  feed. Un arreglo hecho más abajo de la fuente (un `UPDATE`, un borrado) se deshace solo si arriba sigue
  igual. Vale para demos, para SSO y para el borrado de PII.

---

## 2026-10-06 — Batch Confluence 2: equipos, integraciones, LEB, Nudge Engine

Cinco archivos. El PDF *Platform Technical Setup* vino de nuevo y es **idéntico byte a byte** al ya
procesado: sin novedades. Los otros cuatro:

- ✅ **UDS = Unified Data Store** (*Activate / Nudge Setup*). Pregunta cerrada.
- ✅ **El modelo de equipos ya existe** (*Team Partnership Model – Project Turbo+*): seis equipos de PM
  (A–F) con 2–3 PFS partners cada uno, dueños de su *Team Task Queue*, más un Automation Team.
  Escalación en cuatro niveles (equipo → *Assist* → *Team Assist* → urgente solo PM). **Cierra la
  hipótesis del _indice:** el *task pool* que describió Melanie ya fue reemplazado antes de que entrara
  Ignacio. Corrige un rol inferido: **Jon Vail es PFS partner, no PM.**
- ✅ **Integraciones de datos** (*Data Integrations*): Platform Onboarding → Push (SFTP) al equipo PFS del
  PM / Pull a Automation. Avisarle a Kevin Carlson al tomar una. 🔍 Lo más parecido a lo que Ignacio
  hacía en UKG.
- ✅ **LEB pisa lo hecho por fuera** (*PFS LEB Learnings*): con *Use LEB Data Collector* encendido,
  previsualizar, *Next: Settings* o activar reescribe la estructura del survey y `all_data`. Nueva
  **regla 10** en procedimientos — es el riesgo silencioso de todo lo que se enseñó en el training (SQL
  por fuera).
- ✅ **Nudge Engine** (*Activate / Nudge Setup*): guía de 7 pasos → nota nueva
  [[Perceptyx/nudge-engine|nudge-engine]]. La falla típica es silenciosa: pocos usuarios con el rol
  `intelligent_nudges`.
- 🔍 Dos deducciones de nombres: **LEAP = LEB** (por contexto del huddle) y **rest questions =
  `resp_questions`** (la tabla aparece con ese nombre en el doc de LEB). Las dos a confirmar.
- Abiertas nuevas: a qué equipo está asignado Ignacio; práctica del equipo con el toggle de LEB; quién
  configura el Nudge Engine.

---

## 2026-10-06 — *(Temp) Platform Configuration* US y EU (Confluence)

- ✅ Dos páginas exportadas por Ignacio (.doc, en realidad HTML de Confluence). Reemplazan al PDF como
  fuente principal del alta de cliente: [[Perceptyx/procedimientos|procedimientos]] § Alta de un cliente,
  reescrita con los 10 pasos, dueño por bloque y tabla de diferencias US/EU.
- ✅ **Resuelve una pregunta abierta:** `uds_company_id` = **Group UUID del cliente en Okta**.
- **Lo nuevo que no tenía el PDF:** el paso de Okta (identity provider SAML + metadata), los pasos del PM
  (usuarios admin, SFTP, System Admin, envío de accesos) y las FAQ del binlog.
- 🔍 **El dato más útil para el día a día está en las FAQ:** cambiar emp_id, nombre, email o sso_id en
  `users` o `emerge` **no llega a UDS** — se cambia en `prefill_data(_all)`. Es la misma lógica que la
  regla 4 del training, vista desde la plataforma.
- **¿Cuál es más nueva?** 📣 Ignacio: *"creo que son posteriores pero no estoy seguro"*. Evidencia en
  procedimientos § Qué versión manda: capturas del 28/04/2026 y texto viejo editado a medias en la EU →
  🔍 probablemente sí. ✅ Cerrado el mismo día: 📣 Ignacio vio que el PDF **se creó en febrero** → (Temp) es la
  vigente. Pasó a preguntas abiertas. Lo que solo tenía el PDF (toggle Platform 2.0,
  máximos de usuarios) se conserva ahí.

---

## 2026-10-06 — Primer documento de Confluence: *Platform Technical Setup* (US)

- ✅ Exportado por Ignacio el 06/10. Volcado en [[Perceptyx/procedimientos|procedimientos]] § Alta de un
  cliente; términos nuevos (UDS, MAC, PIP, binlog, PFS) en [[Perceptyx/plataforma|plataforma]].
- **Primera fuente documental del dominio**: lo que dice pasa como ✅, no 📣.
- ✅ **Confirma un nombre que Gemini había deformado:** la tabla es **`prefill_data`**, no *prefilled
  data*.
- ~~🔍 **Abierto:** quién ejecuta este alta — el documento habla de PFS y del PM, no de Delivery Ops.~~
  SUPERSEDED 06/10: 📣 Ignacio — **PFS es el nombre anterior de Delivery Ops** (*"Platform Services,
  creo"*). El alta de clientes nuevos **es tarea de Delivery Ops**. Ojo al leer Confluence: los docs
  viejos dicen PFS.
- 🔍 Sigue abierto: qué es **UDS** (Ignacio no está seguro) y qué es `uds_company_id`. Pasaron a
  [[Perceptyx/_indice#Preguntas abiertas para el equipo|_indice § Preguntas abiertas]].
- No incorporado: la variante **EU** y las **FAQ del binlog listener**.

---

## 2026-10-06 — Primer batch de training (sesiones 28/09 → 01/10)

Volcado desde cinco **notas de Gemini** que pasó Ignacio. **Los archivos originales no se archivan en el
vault**: tienen nombres de clientes. Lo procedimental se extrajo a
[[Perceptyx/procedimientos|procedimientos]], lo de herramientas a [[Perceptyx/plataforma|plataforma]] y
las personas a [[Perceptyx/equipo-delops|equipo-delops]]. Acá queda lo que pasó en cada sesión.

### 01/10 — Task practice (Emily, Andrea, Guillermo, Ignacio)

- Primera práctica con tarea real: **reordenar cinco demos** de un survey cerrado, repartidos entre los
  tres nuevos. Ignacio hizo uno de punta a punta (tenure), con Emily guiando.
- 📣 Ignacio dijo sentirse *"somewhat lost"*; Emily y Andrea: la práctica es la forma de aprender.
- **Los tres dieron `command denied`** al escribir en producción → Emily corrió los `UPDATE`. Jackie lo
  está mirando. Credenciales read-write en el chat de Jackie.
- **La Mac de Ignacio laggeaba con Querious.** Consejo de Emily: reiniciar; si sigue, ticket de soporte.
- Asignado a Ignacio (y a Guillermo): **completar las actualizaciones de demos restantes** siguiendo
  backup + sync. ✅ Hecho (📣 Ignacio, 06/10).
- Próxima sesión: **02/10, 10:30** (hora de Emily), tarea nueva. ⚠️ **No volcada.**

### 01/10 — DelOps Team Huddle (equipo completo)

- ✅ **Decisión:** se sigue corriendo el script de comment theming hasta confirmación oficial, aunque
  engineering dice que el bug está arreglado. Reportar a Jackie los casos con backups.
- **Busy season:** los seniors no tienen tiempo para mentorear; afloja en noviembre–diciembre (Lily).
  Jackie pidió pasarle **tareas estándar a los nuevos** para que trabajen y hagan shadow.
- **Timelines comprimidos en LEAP** (Jon Vail): los PM no llegan a hacer QA cuando el cliente se atrasa
  con contrato o archivos y mantiene la fecha. Pide más autoridad para correr fechas.
- **Pedidos que esquivan el ruteo** (Fresh Desk, mails directos a ingenieros) → Edwin le recuerda a
  soporte que los convierta en tickets.
- **Patrón: el cliente pide API para sacar datos crudos y sus propios stakeholders prohíben exportar
  datos crudos o PII.** Apareció en dos cuentas. Lectura del equipo: casi siempre lo que el cliente
  necesita ya lo da el reporting, o se resuelve con una **extracción agregada one-time por script** (hay
  precedente y scoping técnico, en manos de Edwin y Mikhail). 🔍 Toca directo la frontera
  *"Enterprise API now with MCPs"* que nombró Melanie en la selección.
- Bug abierto en Q&A: preguntas multi-respuesta que muestran valores fuera de rango (0 u 8 en lugar de
  7). Hipótesis de Jon: índices desincronizados o un bug viejo que poblaba ceros.

### 01/10 — Demo updates (Emily)

- Demostración: agregar un demo nuevo, workaround de comentarios con modelo léxico (US y EU), reordenar
  un demo que estaba en trends.
- Ignacio preguntó por métodos alternativos de agregar demos y observó que la app o los scripts
  reducen el riesgo de olvidar un paso.
- Andrea planteó el miedo a romper datos en tareas reales. Respuesta de Emily: **no hay tareas de
  prueba, son reales; el backup es la red**. Preguntar en Slack sin culpa, buscar antes en el historial
  y en Confluence.

### 30/09 — After-survey updates (Emily, Andrea, Ignacio)

- Tarea del mismo día al cierre de un survey: manager IDs, rebuild del manager tree y demos.
- **Las tareas se vuelven urgentes** porque el cliente manda tarde la información o el PM detecta
  errores. Si uno está desbordado: pedirle al PM pasarla al día siguiente o escalarla a otro del
  equipo. Emily trabaja 8 horas o más en busy season.
- Andrea y Jackie tuvieron un fallo del data file builder de SOS → bug reportado.

### 28/09 — Data file load (Emily, Andrea, Guillermo; Ignacio se sumó empezada)

- Carga de un archivo de participantes con el LE builder, sin manager tree porque el PM no lo pidió.
- Guillermo: fue más simple que otras tareas que vieron.

### Lo que queda abierto de este batch

- ~~⚠️ Permisos de escritura en producción (Jackie).~~ SUPERSEDED 06/10: 📣 Ignacio — **ya tiene
  permisos de escritura**. Fecha exacta de la resolución: no consta.
- ~~⚠️ ¿Se terminaron los demos asignados el 01/10?~~ SUPERSEDED 06/10: 📣 Ignacio — **sí, terminados.**
- ~~⚠️ Sesión del 02/10 10:30 sin volcar~~ SUPERSEDED 06/10: volcada (*QA DCT*, ver entrada de arriba).
- **Time entry = Certinia, dentro de Salesforce** (📣 Ignacio, 06/10). **LEAP**: Ignacio tampoco sabe
  qué es (06/10) — sigue abierto. Las deformaciones de Gemini sin resolver
  ([[Perceptyx/plataforma#Deformaciones de Gemini|plataforma § Deformaciones]]).
- La hipótesis del _indice (¿task pool o asignación por PM?): el huddle muestra una **cola de tareas que
  la gente "agarra"** — 🔍 indicio de que el task pool sigue vigente al 01/10.

---

## 2026-10-06 — Apertura del dominio

- 📣 Ignacio: está **en training** como Delivery Operations Manager, conociendo el sistema y los
  tickets que va a trabajar. El entorno *"es muy dinámico y cambia semana a semana"*.
- Sin información de training volcada todavía.
- ~~⚠️ **No consta en el vault la fecha real de ingreso.**~~ SUPERSEDED (2026-10-06, misma sesión):
  📣 Ignacio confirma que **arrancó el 14/09/2026**, la fecha que estimaba la oferta del 24/08. Al 06/10 lleva tres semanas adentro.
- 📣 Ignacio: **los tickets viven en Salesforce.** No hay conector de Salesforce en el vault: lo que
  entre de un ticket entra porque Ignacio lo pasa.
- 📣 Ignacio: **acá no se guarda información de clientes**, a diferencia de Intechsol. Se guardan
  procesos y formas de resolver. Regla de alcance en [[Perceptyx/_indice|_indice]] § Qué entra y qué no.
