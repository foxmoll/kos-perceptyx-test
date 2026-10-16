# DC Mosaic — el Data Collector nuevo

Contexto de engineering sobre **DC Mosaic**, el colector de respuestas que reemplaza al Data Collector
clásico. No es procedimiento de Delivery Ops (regla 5 de [[Perceptyx/_indice|_indice]]): sirve para
entender qué está pasando debajo de los surveys que DelOps toca, y hacia dónde va.

Relacionado: [[Perceptyx/modelo-de-datos|modelo-de-datos]] (arquitecturas legacy y nueva) ·
[[Perceptyx/services-os|services-os]] · [[Perceptyx/cultivate-360|cultivate-360]]

> **Fuente: ✅ Confluence, equipo de Data Collector (no DelOps)**, seis páginas exportadas por Ignacio el
> **06/10/2026**: *DC Mosaic (Ex name: DC vNext)*, *DC Mosaic Onboarding*, *DC Mosaic Technical
> Overview*, *DC Mosaic Glossary*, *DC Mosaic Mixpanel Observability* y *DC Mosaic Roadmap
> Implementation*. Los diagramas no vinieron; la página de roadmap es un índice de links (la lista 2026
> H1 no vino). Links a repos y carpetas internas, omitidos.

---

## Qué es

- ✅ **Mosaic = DC vNext**, con nombre de marca. Cierra la pregunta abierta sobre *Mosaic*.
- **En sentido estricto:** los módulos centrales — **DC API** (backend, Go + PostgreSQL + colas AWS SQS),
  **DC Vue** (la interfaz que ve el respondente, Vue 3 + design system *Vision*) y **DC Adapter**.
- **En sentido amplio:** todo lo que recolecta datos, incluido el **Conversational Listening Agent (CLA)**
  —la parte *conversacional*: un survey en forma de chat con un agente— y, a futuro, *Crowdsource* dentro
  de DC.
- Canal: **#team-dcvnext**.

## Cómo encaja con lo que toca DelOps

✅ **Mosaic toma la definición del survey de un solo lugar, LEB, y escribe lo recolectado de vuelta en la
plataforma Classic (MySQL) a través de un adaptador** (`dc-classic-adapter`, que consume eventos de la API
y escribe en MySQL).

🔍 **Consecuencias para el puesto:**

- Un survey Mosaic **sigue terminando en las tablas de siempre** (`all_data` y compañía). Las tareas de
  datos de DelOps no desaparecen con Mosaic; cambia quién escribe.
- La **regla 10** (LEB pisa lo hecho por fuera) tiene acá su razón: *Settings / Preview / Make Survey
  Active* en LEB **sube la definición a DC** (*"Upload a Survey to DC"*). Por eso SOS › Branching muestra
  una tarjeta *DC vNext* naranja ("sin publicar") cuando un cambio en LEB no se publicó.
- **Live Edit** (editar un survey que ya está recibiendo respuestas) y **Re-Published Survey** son
  conceptos con nombre propio: los cambios después de publicar se manejan "más formalmente". Es la versión
  de producto de la regla 2 (no tocar demos con el survey vivo).

## Por qué existe — lo que engineering dice del sistema viejo

De *Technical Overview*, problemas del *Legacy DC* (Perl/MySQL):

- Customizaciones por cliente difíciles de manejar, que terminan **bifurcando el código** del survey.
- **"Engineers / Project Managers / Data Managers"** están en el camino crítico de cualquier cambio.
- ⚠️ ***"Data Managers / Engineers often can't access functionality they need resulting in them bypassing
  services to directly connect to a DB to issue custom queries/mutations via terminal."*** 🔍 Es
  exactamente el trabajo del training (`UPDATE`s en Querious). Engineering lo lista como **problema a
  eliminar**: coherente con que SOS › Database Tools sea solo lectura.
- Base **single-tenant** (una por survey), datos comunes repartidos (no hay usuario ni compañía
  centrales), caché frágil, Perl difícil de contratar.
- La base depende de convenciones arbitrarias, como **guardar en hora del Pacífico** (por eso los crons
  se programan en hora PT) y códigos opacos de tipo de pregunta (ej. `R2`).

**El diseño nuevo:** multi-tenant, PostgreSQL (mejor soporte de JSON, lecturas y escrituras sin bloqueo),
APIs REST con endpoints **externos** (para los survey builders, con API tokens) e **internos** (para el
frontend; los del participante con OAuth 2.0 y tokens de vida corta). El survey se describe como un
documento JSON de **páginas** y **bloques** (bloques de pregunta y de texto); **no existe "tipo de
survey"** — un onboarding o un 360 son composiciones de bloques. Accesibilidad objetivo: WCAG 2.2 AA.

## Glosario útil para DelOps

Términos del *DC Mosaic Glossary* (lenguaje común del dominio Survey). Solo los que sirven para leer
tareas y documentación:

| Término | Qué es | También llamado |
|---|---|---|
| **Legacy DC** | El colector clásico Perl/MySQL | Classic DC, DC vOld |
| **Legacy Reporting** | Reporting clásico Perl/MySQL | Classic / Old Reporting |
| **New Reporting** | Reporting de nueva generación | ⚠️ **Advanced Analytics, Analytics Studio**, Reporting vNext |
| **DC Client** | El sistema que arma el survey y se lo pasa a DC | Survey Builder. Ej.: **Ask/OnDemand (OD)**, Dialogue, 360 |
| **Attributed Demographics** | Demos del respondente provistos antes de que conteste | **Precoded Demographics** (y *prefill demographics*) |
| **Known Participants / Anonymous Respondents** | Invitados conocidos (con demos) / quienes entran por link de distribución | |
| **Survey Edition** | **Draft** (preview) y **Published** (todo lo demás) | |
| **Survey Status** | Active / Inactive, solo para publicados | Unlocked / Locked |
| **Conditional Logic** | Qué preguntas ve cada uno según respuestas | **Skip Logic** (Ask) = el *branching* |
| **Auth Code** | Código del usuario en la URL | **AC**, Invite / Access Code — el parámetro `ac` con el que DC busca al respondente en `emerge` |
| **PIN** | Código que el usuario tipea | |
| **HRIS** | Método de Ask Self-Service para subir datos de empleados; DC lo usa para conditional logic | |

⚠️ **Trampa de nombres:** *Advanced **Reporting*** (legacy; necesita una columna por demo en
`prefill_data`, ver [[Perceptyx/modelo-de-datos|modelo-de-datos]]) **no es** *Advanced **Analytics***
(el reporting nuevo).

**Términos de 360** (complementan [[Perceptyx/cultivate-360|cultivate-360]]):

- **Managed 360** = **PYX-Led 360** = **Classic 360**: lo configura Professional Services. Es el que
  opera DelOps (360v2, MySQL).
- **Self-Service 360 (SS360)**: el cliente lo configura en la plataforma (360vNext, PostgreSQL).
- **Participant (Ratee)** / **Rater** / **Self-Assessment** / **Relationship** / **Relationship Group**
  (cada rater en exactamente uno) / **Additional Raters** (pares, externos).
- **Reporting Threshold**: mínimo de respuestas (ej. 3 no-self) para que el leader sea **Report
  Eligible**. **Report Ineligible**: no nominó raters a tiempo, o no contestaron suficientes. 🔍 Es lo que
  configura el PM con el demo oculto de relaciones combinadas.
- **Nomination**: fase en que el leader elige a sus raters. **180**: un solo tipo de relación (casi
  siempre el manager).
- **Cohort** (fechas comunes) vs. **Non-Cohort / Always-On** (continuo).
- **Report Release Delay**: espera configurada después del cierre para que admins o Perceptyx limpien los
  datos del reporte.

## Observabilidad (Mixpanel)

De *Mixpanel Observability*, lo que sirve como contexto:

- Cada evento lleva `company_id` (de UDS), **región: US, EU o *GovCloud US*** (una tercera región que no
  aparece en ninguna página de DelOps), `db_name` (= el app ID del survey) y **`event_build_type`: OD,
  360 o Nudge**.
- `dc_version` distingue **Conversational Listening** (CLA) de **DC vNext** (tradicional).
- **Estándar de privacidad:** a Mixpanel no va contenido (ni chat, ni respuestas, ni texto de preguntas):
  solo largos, conteos, IDs y tiempos.
- Para anónimos, DC genera un UUID que se usa como el `client_id` de las subapps legacy; para link único,
  LEB le pasa el `client_id` como `external_participant_id`.

---

## Lo que esto cambia en la lectura del dominio

- 🔍 **Hay trabajo de IA en la plataforma, pero en engineering, no en DelOps:** el **Conversational
  Listening Agent** es un survey conversacional con un agente. Matiza la idea 6 de la síntesis del
  [[Perceptyx/_indice|_indice]]: la frontera de IA existe en Perceptyx; lo que no aparece documentado es
  **MCP** ni un rol de DelOps en eso.
- 🔍 **"Data Managers" confirma el linaje del nombre del equipo** (DM → PFS → Delivery Ops): engineering
  sigue usando *Data Managers* para quienes operan los datos.
- 🔍 **La dirección es explícita:** dejar de escribir directo en la base. Las tareas de "arreglar
  `all_data` a mano" son, para engineering, un síntoma del sistema viejo.
