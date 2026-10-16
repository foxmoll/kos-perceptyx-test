# Perceptyx — Delivery Operations

Dominio de trabajo de Ignacio en **Perceptyx**, posición **Delivery Operations Manager** (individual
contributor, dentro de Customer Value Services). Ingreso: **14/09/2026** (📣 Ignacio). Dominio abierto el **2026-10-06**, en plena etapa de training.
Herramienta de tickets: **Salesforce** (📣 Ignacio, 2026-10-06) — precisado en el cierre: la unidad de trabajo es la **tarea de proyecto de Certinia** (el PSA dentro de Salesforce), donde también se cargan las horas. Así la nombra toda la documentación.

Relacionado: [[Perceptyx/bitacora|bitacora]]

---

## Régimen del dominio

Híbrido, y la frontera importa:

- ~~**Operacional** para lo que está en curso: tickets, pendientes, quién pidió qué. Prioriza estado
  actual y próxima acción.~~ **SUPERSEDED 2026-10-09** (Ignacio): el vault **no sigue tickets**. Un ticket
  se trabaja, se cierra y se pasa al siguiente; lo que queda es el procedimiento. Lo operacional se
  limita a **ayudar a resolver el ticket que está abierto ahora** — sin registrar su cumplimiento
  ([[KOS/Reglas|Reglas]] § 9).
- **Referencia** para cómo funciona el sistema: plataforma, tipos de ticket, procesos, glosario. Cita
  la fuente, no especula.

### La regla que define este dominio: todo dato tiene fecha de vigencia

El entorno cambia semana a semana (dicho por Ignacio, 2026-10-06). Un dato sin fecha en un entorno así
es un dato que miente en silencio. Por eso:

1. **Todo lo que entra lleva fecha y fuente**: *"vigente al AAAA-MM-DD — fuente: training con X /
   doc Y / ticket Z"*.
2. **Marca de certeza**, la misma convención que la de `inventario/` del vault original:
   ✅ verificado (leído de un doc, del sistema, de un ticket) · 📣 dicho por alguien (anotar quién) ·
   🔍 inferido (hipótesis, puede estar mal).
3. **Lo que cambia no se borra: se marca `SUPERSEDED (fecha)`** y se escribe la versión nueva arriba.
   Saber que un proceso *cambió* —y cuándo— es información que el estado actual solo no da.
4. **Lo dicho en training es "lo que dijo X el día Y"**, no política de la empresa, hasta que aparezca
   en un documento.
5. **Documentos de otros equipos** (engineering, producto) se usan para **entender**, no como
   procedimiento. Si contradicen una página de Delivery Ops sobre cómo hacer una tarea, manda la de
   Delivery Ops (📣 Ignacio, 06/10). Hoy viven en [[Perceptyx/modelo-de-datos|modelo-de-datos]].

### Qué entra y qué no

Decisión de Ignacio, 2026-10-06: *"acá no guardamos info de clientes como hacíamos en Intechsol, sí
sobre procesos y formas de resolver"*.

- **Entra:** cómo funciona la plataforma, tipos de ticket y cómo se resuelven, procesos internos,
  criterios de escalación, glosario, quién en el equipo es dueño de qué.
- **No entra:** nombres de clientes, datos de sus cuentas, contenido de sus encuestas, capturas con
  datos de clientes. Un ticket se registra como **patrón** ("pedido de tipo X → se resuelve así"), no
  como caso de un cliente. Si un ejemplo necesita contexto, se anonimiza ("cliente enterprise, ~10k
  empleados").
- Es el modelo opuesto al de `UKG-Ready/clientes/`: allá la ficha de cliente era la unidad; acá la
  unidad es el **proceso**.

---

## Lo que se entiende al 08/10 — síntesis

Escrita en el cierre del 06/10, después de procesar el training y ~40 páginas de Confluence; la idea 8 se sumó en el segundo cierre del mismo día; la 9 y el refinamiento de la 7, en el cierre del 08/10. Son las
ideas que ordenan todo lo demás; si una tarea nueva no encaja en ninguna, es señal de que hay algo que
aprender.

1. **Delivery Ops es el equipo dueño de los datos del cliente dentro de la plataforma; el PM es dueño
   del cliente.** El PM define, pide y habla con el cliente; DelOps carga, transforma, configura,
   verifica y le devuelve al PM lo raro (audit files, faltantes, excepciones). Se repite en todas las
   páginas. El nombre del equipo cambió dos veces (🔍 DM → PFS → Delivery Ops) y los documentos usan los
   tres.
2. **Lo que manda es la fuente.** HRIS del cliente → feed → `prefill_data(_all)` → UDS. Un arreglo hecho
   más abajo de la fuente se deshace solo cuando llega el próximo dato de arriba. Vale para demos, SSO,
   jerarquías y borrado de PII.
3. **En `all_data` el valor de un demo es una posición, no un texto.** De ahí salen casi todas las
   reglas de cuidado: no reordenar sin reconstruir, sumar opciones al final, traducir posiciones en los
   trends, revisar dependencias antes de tocar.
4. **Hay capas que pisan a otras sin avisar:** LEB pisa lo hecho por SQL; el feed diario pisa lo hecho a
   mano; el binlog ignora `DELETE`; lo que no cumple una condición se saltea sin error. Antes de dar algo
   por hecho, verificar en la capa que el usuario realmente ve.
5. **Todo se está mudando.** De Querious, jails y MAC a SOS; de MySQL por survey a la arquitectura nueva
   (UDS, Data Hub, PostgreSQL, Snowflake). La documentación describe muchas veces la herramienta vieja.
   Leer cada procedimiento preguntando *"¿dónde se hace esto hoy?"* —
   [[Perceptyx/services-os|services-os]] tiene la tabla.
6. 🔍 **La frontera que nombró Melanie en la selección (*"Enterprise API now with MCPs"*) no aparece en
   ninguna página de Confluence.** La API estándar sí está documentada (y choca con privacidad); MCP no.
   O todavía no existe como trabajo de DelOps, o vive en otro lado — el 06/10 tampoco lo conocía el bot
   interno de Customer Value (Pyxee-CVO). *Matiz del 06/10:* **sí hay IA en la plataforma** —el
   *Conversational Listening Agent* de DC Mosaic—, pero en engineering, no en DelOps
   ([[Perceptyx/dc-mosaic|dc-mosaic]]). Y la **cultura de IA** documentada está en **consultoría (WTC)**:
   agentes GPT, prompts, un bot interno sobre Confluence (`@Pyxee-csg`) — y una lista de clientes con los
   que no se puede usar IA ([[Perceptyx/equipo-delops|equipo-delops]] § Equipos vecinos).
7. **Engineering quiere eliminar el trabajo de escribir directo en la base.** DC Mosaic lista como
   problema del sistema viejo que los *Data Managers* tengan que conectarse a la base y mutar datos por
   terminal — es el trabajo del training. SOS con base solo lectura va en la misma dirección. 🔍 El valor
   del puesto a mediano plazo está más en entender el modelo y los procesos que en dominar los `UPDATE`.
   *Refinada el 08/10 (sesión del 21/09 + Ignacio):* en SOS **solo las queries a la base son de solo
   lectura**; las escrituras no desaparecen, **pasan a herramientas con propósito** que reportan y
   arreglan (Launch Audit, Sync reporting demographics, Customizations con merge request). Lo que se
   achica es el SQL a mano, no la intervención de DelOps. Confianza: subió.

8. **El alcance lo define el contrato, no la costumbre.** Cada servicio tiene topes (demos, archivos,
   participantes, iteraciones) y desde 2026 un presupuesto de horas por rol, incluido DelOps. Lo que el
   cliente pide por encima —o lo que se venía entregando "porque siempre se hizo"— se documenta y va al
   CSM como **CSQL**; no se absorbe en silencio ([[Perceptyx/catalogo-servicios|catalogo-servicios]]).
   Y los clientes **FedRAMP / US Citizen** están fuera del alcance de Ignacio por contrato.

9. **Casi toda tarea tiene más de una vía, y por ahora valen igual** (regla de Ignacio, 06/10 —
   [[KOS/Reglas|Reglas]] § 9). Script Perl en SOS, ops tool del app, módulo nuevo de SOS: debajo hacen **los
   mismos chequeos** (verify integrity = Quality & integrity checks; rebuild Perl = Sync reporting
   demographics). Conocer una vía alcanza para entender las otras; elegir entre ellas no es tarea del vault
   hasta que el equipo deje de usar alguna. *Sumada el 08/10.*

---

## Proyecto: KOS de equipo (en planificación desde el 2026-10-16)

Ignacio quiere replicar el KOS para todo Delivery Ops: que el equipo consulte, que **agregue conocimiento
de forma estructurada** y que siempre pueda saber **por qué** algo se hace como se hace. Diseño discutido con
Claude el 16/10. NotebookLM no sirve como base: es de solo lectura sobre fuentes sueltas, no escribe, no
sigue el grafo y no carga protocolo. Puede ser, como mucho, una vista de consulta.

**Decisiones de Ignacio (16/10):**

| Tema | Decisión |
|---|---|
| Dónde vive | Repo en el **GitHub de la empresa** (📣 Ignacio: existe) |
| IA | **Gemini** está aprobada para todos (📣). **Claude** está aprobada como herramienta, pero las licencias necesitan un **business case** |
| Idioma | **Inglés** |
| Quién escribe | El equipo también, por PR. Ignacio cuida el protocolo: revisa PRs y corre Reflect |

**Arquitectura propuesta** — 📣 Ignacio, 16/10: *"esperemos un poco, por ahora quiero planear bien la movida sin romper nada de lo que tengo armado acá"*. **Nada ejecutado:** el vault personal no cambia hasta que el plan esté cerrado (detalle de operadores en [[KOS/Operadores|Operadores]]):

- Repo de la empresa = dominio Perceptyx (en inglés) + su propia capa `KOS/` recortada: Bootstrap de un
  dominio, Reglas § 1–4 y § 9 escritas para un equipo, agentes útiles (procesar-raw, Reflect, Cierre y uno
  de ayuda con tickets) + validador con GitHub Action.
- Adaptadores: `GEMINI.md` (operador inicial, Gemini CLI 🔍 sin verificar que esté habilitado en el
  Workspace de Perceptyx) y `CLAUDE.md` cuando lleguen las licencias. Los dos apuntan al mismo Bootstrap.
- Humanos: Obsidian (grafo) o GitHub; escriben por PR.
- *(Propuesta)* La **fuente de verdad de Perceptyx se mudaría al repo del equipo**. Este vault lo incluiría como submódulo
  en `Perceptyx/`. Lo personal (bitácora del training, selección, notas sobre personas, la síntesis en
  primera persona) se queda acá, fuera del repo del equipo.

**Pendiente:**
- 🔍 Confirmar con IT qué licencia de Gemini tiene Perceptyx. Si es **Gemini Enterprise**, **Google Antigravity** vendría incluido y podría ser el operador sin el business case de Claude ([[KOS/Operadores|Operadores]] § Gemini). Si no, ver si **Gemini CLI** está habilitado.
- Business case para licencias de Claude.
- Separar nota por nota qué va al equipo y qué queda personal; traducir; definir cómo se integra el submódulo con
  el validador del KOS personal.

---

## Preguntas abiertas para el equipo

Lo que el vault no puede resolver solo y conviene preguntar en Slack o a Emily/Jackie. Se tacha con
fecha y respuesta cuando se contesta; la respuesta va a la nota que corresponda.

| Pregunta | Abierta | Por qué importa |
|---|---|---|
| **Late adds — cómo agregar opciones de demo faltantes en SOS.** Elena (16/10) lo hace con un script por terminal (jail), *"they don't want us to use that"*; la vía del app (*Add missing demographic options*) va de a un demo. ¿Hay módulo de SOS que lo haga de una? | 16/10 | Con muchos demos nuevos, de a uno es lento ([[Perceptyx/procedimientos#Late adds: sumar participantes a un survey que ya está en vivo (Elena, call del 16/10)\|procedimientos § Late adds]]) |
| **Late adds en un survey armado en LEB.** Elena cargó por la vía clásica (Data File Builder + Querious + *Survey Launch*) un app cuya carga inicial vino de LEB. ¿Choca con la regla 10 (LEB pisa lo hecho por fuera al previsualizar / activar)? 🔍 Con el survey ya activo nadie debería volver a activarlo, pero no se habló. Y ¿cuándo se usa *Export Files (for LEB)*? | 16/10 | Si LEB pisa, los late adds desaparecen de `prefill_data` / `emerge` sin aviso |
| **Late adds: ¿subir `emerge` por *Survey Launch* dispara la invitación?** Elena carga `prefill_data` primero porque `emerge` *"could be that invitation will be sent or reminders"*. ¿Se envía sola o depende de la programación de recordatorios? | 16/10 | Decide si hay que coordinar con el PM el momento de la carga |
| ***Manager Hierarchy Tree › Add Users***, ¿deja los usuarios **activos o inactivos**? Ignacio (09/10): activos. Un DM (call del 09/10): *"siempre inactivos"*. ✅ El diálogo no tiene campo de activo/inactivo (captura del 09/10). Se resuelve con la query de [[Perceptyx/procedimientos#Activos o inactivos — tensión abierta\|procedimientos § Activos o inactivos]] en la próxima tarea | 09/10 | Si el pedido dice inactivos y quedan activos, los managers entran antes de tiempo a los reportes |
| ~~¿**LEAP** es **LEB** mal transcripto por Gemini?~~ **Cerrada 06/10 por decisión de Ignacio**: se asume que sí — nadie puede confirmar qué quiso decir una transcripción | 06/10 | — |
| ¿Dónde está, si existe, el trabajo de **MCP / Enterprise API** que nombró Melanie? No aparece en Confluence, y **el bot Pyxee-CVO (base de conocimiento de Customer Value) tampoco lo conoce** (06/10). Queda preguntarle a una persona — Melanie o Jackie | 06/10 | Es la frontera de crecimiento que se le ofreció al puesto |
| ~~¿Qué significa **UDS**?~~ ✅ **Resuelta 06/10:** *Unified Data Store* (Confluence *Activate / Nudge Setup*) | 06/10 | — |
| ~~En MAC, ¿`uds_company_id` es el ID de la compañía en UDS?~~ ✅ **Resuelta 06/10** por la página *(Temp) Platform Configuration*: es el **Group UUID del cliente en Okta** (*Directory › Groups*) | 06/10 | — |
| ~~¿Cuál es la página oficial del alta de cliente?~~ ✅ **Resuelta 06/10**: *(Temp) Platform Configuration*; el PDF se creó en febrero (📣 Ignacio) | 06/10 | — |
| ~~¿A qué **equipo de PM** está asignado Ignacio?~~ ✅ **Kim (equipo C)** — video del 23/09: *"for you it would be Kim"* | 06/10 | — |
| Cuando se hace un `UPDATE` por fuera en un survey armado en **LEB**, ¿se apaga el toggle o se avisa al PM? 📣 06/10: Ignacio cree que las dos cosas. 🟡 **Matiz del video del 23/09 (Jackie):** la decisión previa es **cargar por LEB si no hay dependencias** (y así no hay conflicto); la vía clásica, con los toggles en mente, solo si las hay | 06/10 | Si no, previsualizar o activar el survey deshace el cambio |
| Pedir el ***Execution Checklist*** de borrado / remoción de PII y el *Request Form* | 06/10 | Delivery Ops es quien ejecuta el borrado; la política dice qué, el checklist dice cómo |
| **UDS**: ¿*Unified Data Store* o *User Directory Service*? Dos páginas lo expanden distinto | 06/10 | Menor; para leer bien la documentación |
| ~~¿Qué significa **DRA**?~~ ✅ 06/10: ***Data Release Authorization*** — confirmado en *Description of Service* (2025-09) | 06/10 | — |
| ~~¿Dónde está el Google Doc original de *360 Survey Test Leader & Raters Setup*?~~ ✅ **Resuelta 06/10**: llegó la página real | 06/10 | — |
| ¿El **SSO Team** (`pyx_sso@`) es parte de Delivery Ops? ¿Quién hace la configuración en Okta? | 06/10 | Define si el SSO es tarea de Ignacio |
| Volver a exportar ***Create Data Automation*** (vino vacía) y conseguir la página del **data spec** | 06/10 | Es el paso que sigue al audit en apps self-service. **El bot Pyxee-CVO no lo resuelve** (06/10): contestó con la cláusula de *contrato* del Lifecycle (qué se le promete al cliente), no con el cómo de DelOps |
| ~~¿Qué es el **jail**?~~ ✅ **Resuelta 06/10**: el entorno de desarrollo propio (*Automation Setup – 360*) | 06/10 | — |
| En 360, ¿qué orden de columnas vale? *360v2 Load Data File* y *360 Data Upload Steps* no coinciden (Job Title 6.º vs. 10.º) | 06/10 | 🔍 Se sigue *Data Upload Steps* (parece más nueva). Ignacio tampoco lo sabe (06/10) |
| Below Threshold: ~~¿con qué query se encuentra el ancestro?~~ ✅ 08/10: BUSCARV en cadena (transcripción del 24/09). Sigue abierto: **¿cómo se crean los Below Threshold** cuando la tarea pide crearlos (otra pasada de *Add Users* o todos como Manager y reasignar)? Y cómo se cierra la tarea | 08/10 | Define la tarea `PFS: Creates Manager Users` ([[Perceptyx/procedimientos\|procedimientos]] § Usuarios de manager) |
| ~~¿Tiene Ignacio **jail** propio y acceso al repo `cronjobs`?~~ **Respondida 06/10**: no — el equipo se está moviendo a hacer todo en **SOS**, crons y scripts incluidos | 06/10 | — |
| ¿Qué es el **CSP** de la guía de cron del 360 (*"work with the CSP on the schedule"*)? *Content Security Policy* no encaja; *Customer Success Partner* lo propuso un bot inducido por la pregunta, sin fuente real (06/10) | 06/10 | Menor; solo si aparece una tarea de cron. Preguntarle a una persona |
| ¿Cómo se hace en **SOS** lo que Confluence describe con jail, Querious y git? 🟡 **Parcialmente resuelta 06/10** (guía de SOS): crons → Cron Manager, trends → Trend Mapping, SFTP/PGP → IT Tools, UDS → UDS User Health. ~~**Sigue abierto: las escrituras**~~ ✅ 06/10 (📣 Ignacio): **siguen en Querious** hasta que SOS habilite escritura | 06/10 | — |
| ~~¿Qué es **WTC**?~~ ✅ 06/10: *Workforce Transformation Consulting* (📣 Ignacio + Confluence). ~~Mosaic~~ ✅: DC Mosaic = DC vNext | 06/10 | — |
| ¿Qué proceso definió Jackie para el **QA de branching** (sesión del 02/10)? ¿Qué es **DCT**? | 06/10 | El QA manual de 135 combinaciones no escala; hay una tarea de Ignacio colgada de eso |
| ¿Quién configura el **Nudge Engine** (Activate)? | 06/10 | La guía no lo dice; Ignacio tampoco lo sabe (06/10). Baja prioridad hasta que aparezca una tarea |
| ¿Siguen haciendo falta el toggle *Platform 2.0 Experience* y los máximos de usuarios admin/creator del master app? (estaban en el doc viejo, no en el nuevo) | 06/10 | Si hacen falta y se omiten, el cliente queda sin PIP o con usuarios fuera de contrato |
| ~~**SOS › Customizations**: ¿solo lectura o edición + push?~~ ✅ **Resuelta 06/10** (📣 Ignacio): se edita y publica; **en SOS solo las queries a las bases son de solo lectura** | 06/10 | — |
| **SOS, lectura/escritura**: la guía (v27, 08/10) marca nueve módulos READ ONLY. ¿*"Lo único de solo lectura son las queries"* quería decir *lo único que reemplaza algo que escribía*? (🔍 [[Perceptyx/services-os#Lectura o escritura, módulo por módulo\|services-os § Lectura o escritura]]) | 08/10 | Si no, hay una contradicción entre Ignacio y la guía sin resolver |
| ¿Hay grabación o notas de la sesión de **Edwin del 22/09** (SSO y API)? | 06/10 | Cubre dos huecos: SSO (¿es tarea de DelOps?) y la API |
| ¿El audit de **DOC** (*SOS › Design & Build*) es el audit del **data spec** que piden las tareas de carga, o hay que correr otro (`dataspecs_automation`)? | 08/10 | Decide con qué herramienta se cumple el paso "upon audit pass" de cada tarea de archivo final |
| ¿Qué es el ***Big Brother report*** (opción de *Quality and Integrity Checks*)? | 06/10 | No se explicó; puede ser un chequeo útil |
| En *Sync reporting demographics* / el rebuild Perl, ¿cuándo *blank out all_data* si prefill está vacío? Emily: sí; el default de la herramienta: no | 06/10 | Decide si se borran respuestas de demo en `all_data` |
| ~~¿*PFS* = *Platform Services*?~~ ✅ **Resuelta**: Jackie, 16/09 (*"we used to be called platform services"*) | 06/10 | — |

### Búsquedas pendientes en Confluence (armada el 06/10)

Lo que el vault sabe que existe y no tiene, o no sabe cómo se hace. Se tacha cuando llega.

1. *Data Deletion & Participant Identifier Removal Execution Checklist* + *Request Form*
2. *Create Data Automation* (re-exportar; vino vacía) — automatización **self-service**
3. La página del **data spec** (*Tech Specs*, *data specifications*, *demographic data file*) — 🟡 06/10: las columnas estándar se vieron en un `prefill_data` de prueba ([[Perceptyx/modelo-de-datos|modelo-de-datos]]); falta el documento con formatos y valores válidos
4. *snowflake comments* (la citó Emily el 01/10) — comentarios y modelo léxico
5. ~~Manager tree — cómo funciona~~ (engineering, 06/10). **Procedimiento para armarlo:** dos rastros sin verificar en [[Perceptyx/procedimientos|procedimientos]] § Armar un árbol de managers; falta la fuente — buscar *LEB FAQ* o la guía de LEB en Academy, o pedir acceso al PDF que cita el bot
6. *Lifecycle* — *Onboarding*, *Exit*, *Candidate*, *Decision Points* (Sense)
7. ~~Glosario o siglas~~ — casi todas resueltas el 06/10; queda el CSP del cron
8. *Okta Runbook* · *Overview of SSO Implementation and Support*
9. *Standard HRIS Integration Playbook* (integraciones Pull)
10. Onboarding de Delivery Ops / PFS (*new hire*, *onboarding checklist*)
11. Lista de tipos de tarea de Certinia (*Task Category*, *Task Workstream*)
12. *binlog listener FAQ* · *PM Dashboard* (binlog drift)
13. *Advanced reporting* y *branching* complejo
14. Guías por módulo de SOS: *Trend Mapping*, *Cron Manager*, *UDS User Health*, *DOC*, *SOS Cheat sheet*

---

## Estructura

Todo lo nuevo **entra primero a la [[Perceptyx/bitacora|bitacora]]**, fechado. Cuando un tema junta
masa y se consulta por sí mismo, se extrae a una nota propia y se enlaza desde acá — sin carpetas por
adelantado ([[KOS/MANIFESTO#Contenedores|MANIFESTO § Contenedores]]).

- [[Perceptyx/bitacora|bitacora]] — qué pasó, sesión por sesión. La más reciente arriba.
- [[Perceptyx/procedimientos|procedimientos]] — cómo se resuelve cada tipo de tarea: reglas generales
  (backup, survey cerrado, dependencias, test → live, verificar, LEB) y un paso a paso por tarea (cola
  y escalación, integraciones push/pull, LEB, data file load, after-close updates, demo nuevo, reordenar
  demo, comentarios léxicos, alta de cliente, SSO, sincronización con UDS, borrado y PII, API, datos de
  prueba 360, columnas reservadas, data specs, trend mismatch, standard forms, usuarios Manager / Manager
  Below Threshold, late adds en un survey vivo, bajas por fecha de corte, cambio de URL en los emails). **Leer antes de tocar una
  tarea.**
- [[Perceptyx/plataforma|plataforma]] — herramientas (Salesforce, Querious, SOS, Operations Tools…),
  tablas de un survey, glosario y las deformaciones de las notas de Gemini.
- [[Perceptyx/equipo-delops|equipo-delops]] — quién es quién: equipos de PM y sus partners, Automation,
  canales de Slack.
- [[Perceptyx/modelo-de-datos|modelo-de-datos]] — cómo se conectan las tablas de un survey y **por qué**
  las reglas del training son las que son; legacy (MySQL) vs. arquitectura nueva.
- [[Perceptyx/dc-mosaic|dc-mosaic]] — el Data Collector nuevo (ex DC vNext): cómo se conecta con LEB y
  con las tablas Classic, glosario del dominio Survey y de 360. Contexto de engineering.
- [[Perceptyx/catalogo-servicios|catalogo-servicios]] — qué compra el cliente (SKUs) y con qué topes: para
  saber si un pedido está dentro del contrato. Incluye la restricción de clientes FedRAMP.
- [[Perceptyx/services-os|services-os]] — **SOS**: módulos y la tabla de qué herramienta vieja reemplaza
  cada uno. Leer antes de seguir un procedimiento de Confluence que use jail, Querious o MAC.
- [[Perceptyx/nudge-engine|nudge-engine]] — configuración del Nudge Engine (Activate) por cliente.
- [[Perceptyx/cultivate-360|cultivate-360]] — producto 360: carga de datos, demos propios, usuarios de
  prueba, demo oculto de relaciones y automatización por cron.

### Documentos de Confluence incorporados

Cada uno con su fecha de exportación: si la página cambia, el vault no se entera solo.

| Página | Exportada | Dónde quedó |
|---|---|---|
| *(Temp) Platform Configuration (US)* | 06/10/2026 | [[Perceptyx/procedimientos#Alta de un cliente en la plataforma (Platform Configuration, US y EU)|procedimientos § Alta de un cliente]] — fuente principal |
| *(Temp) Platform Configuration (EU)* | 06/10/2026 | ídem, tabla de diferencias US/EU |
| *Team Partnership Model – Project Turbo+* | 06/10/2026 | [[Perceptyx/procedimientos#Cola de tareas y escalación (Project Turbo+)|procedimientos § Cola de tareas]] · [[Perceptyx/equipo-delops|equipo-delops]] |
| *Data Integrations* | 06/10/2026 | [[Perceptyx/procedimientos#Integraciones de datos (Push / Pull)|procedimientos § Integraciones]] |
| *PFS LEB Learnings* | 06/10/2026 | [[Perceptyx/procedimientos#LEB (Listening Event Builder): toggles, archivos finales, clonado|procedimientos § LEB]] + regla 10 |
| *Activate / Nudge Setup* | 06/10/2026 | [[Perceptyx/nudge-engine|nudge-engine]] |
| *UDS* | 06/10/2026 | [[Perceptyx/procedimientos#Sincronización con UDS (binlog): cómo decide y por qué no llega un cambio|procedimientos § Sincronización con UDS]] |
| *Customer Survey Data Management & Record Removal Policy* | 06/10/2026 | [[Perceptyx/procedimientos#Borrado de registros y remoción de PII (pedido del cliente)|procedimientos § Borrado y PII]] |
| *Certinia Request Process – Record Deletion / PII Removal* | 06/10/2026 | ídem |
| *Perceptyx API Setup Process* | 06/10/2026 | [[Perceptyx/procedimientos#Habilitar la API estándar para un cliente|procedimientos § API]] |
| *360 Survey Test Leader & Raters Setup Guide* — ⚠️ conversión incompleta, **SUPERSEDED** por la página real | 06/10/2026 | — |
| *SSO Team Process (US & EU)* | 06/10/2026 | [[Perceptyx/procedimientos#SSO del cliente (después del alta)|procedimientos § SSO]] |
| *SSO – OKTA Configuration (US)* y *(EU) NEW* | 06/10/2026 | ídem § Configuración en Okta (capturas de 02/2024) |
| *SSO Helper Script* | 06/10/2026 | ídem; el `.py` no vino |
| *Reserved Column Names in Direct LEB Data Loads* | 06/10/2026 | [[Perceptyx/procedimientos#Columnas con nombre reservado (carga directa a LEB)|procedimientos § Columnas reservadas]] |
| *Data Specs Process for Healthcare and Non-Healthcare* | 06/10/2026 | [[Perceptyx/procedimientos#Data specs: auditoría del archivo del cliente y excepciones|procedimientos § Data specs]] |
| *Data Spec Compliance Review Process* | 06/10/2026 | ídem |
| *Load Trend Mismatch File* | 06/10/2026 | [[Perceptyx/procedimientos#Trend mismatch: cargar linkages custom de trend|procedimientos § Trend mismatch]] |
| *Standard Forms* | 06/10/2026 | [[Perceptyx/procedimientos#Standard Forms: lo que el PM tiene que entregar antes de pedir trabajo|procedimientos § Standard Forms]] |
| *Create Data Automation* — ⚠️ **exportada vacía** | 06/10/2026 | — |
| *360v2 Load Data File – Cultivate: 360 Feedback* | 06/10/2026 | [[Perceptyx/cultivate-360|cultivate-360]] § Carga (versión vieja del orden de columnas) |
| *360 Data Upload Steps* | 06/10/2026 | ídem § Carga — fuente principal |
| *Create 360 Combined Relationship Demo (Hidden Demo)* | 06/10/2026 | ídem § Demo oculto |
| *360 Survey Test Leader & Raters Setup* | 06/10/2026 | ídem § Usuarios de prueba (reemplaza a la conversión fallida) |
| *Automation Setup – Cultivate: 360 Feedback* | 06/10/2026 | ídem § Automatización por cron |
| *Related Resources – Cultivate: 360 Feedback* — ⚠️ **exportada vacía** | 06/10/2026 | — |
| *Services OS — User Guide* | 06/10/2026 · re-export 08/10/2026 (v27, lectura/escritura por módulo; otra sesión del 08/10 la registró *sin cambios* — 🔍 confirmar cuál export es el último) | [[Perceptyx/services-os|services-os]] |
| ***Description of Service – Perceptyx (2025-09)*** (PDF, Drive de ventas) | 06/10/2026 | [[Perceptyx/catalogo-servicios|catalogo-servicios]] |
| ***PM Power Hour: Pricing, Packaging & Scoping*** (transcripción, vía Pyxee-CVO; sesión de Melanie con PMs, ~principios 2026) | 06/10/2026 | [[Perceptyx/catalogo-servicios|catalogo-servicios]] § Cómo se lee un contrato |
| **Otros equipos — varios:** *Workforce Transformation Consulting Team (WTC)* · *Customer Care & Support Plans* (×2, idénticas) | 06/10/2026 | [[Perceptyx/equipo-delops|equipo-delops]] § Equipos vecinos |
| **Otros equipos — seguridad:** *Content Security Policy (CSP) Header Implementation and Fine-Tuning* · *Secure HTTP and API Development* | 06/10/2026 | Solo glosario (CSP); contenido de ingeniería de seguridad, sin uso para DelOps |
| **Otros equipos — DC Mosaic:** *(Ex name: DC vNext)* · *Onboarding* · *Technical Overview* · *Glossary* · *Mixpanel Observability* · *Roadmap Implementation* (índice de links, sin la lista) | 06/10/2026 | [[Perceptyx/dc-mosaic|dc-mosaic]] |
| **Otros equipos:** *Attributed Demographics in Sub Apps* · *Attributed Demographics – Next Steps* · *Prefill data table* · *Demographics Data* (×2, idénticas) · *360 Data Management and Flows* · *Manager Heirarchy Tree* · *Manager Hierarchy Filtering* · *Snowflake Integration* | 06/10/2026 | [[Perceptyx/modelo-de-datos|modelo-de-datos]] |
| *Platform Technical Setup* (US) — **anterior**, creada en febrero | 06/10/2026 | ídem, § Qué versión manda — lo que solo tenía esta versión |
