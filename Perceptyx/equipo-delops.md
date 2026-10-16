# Equipo — Delivery Ops y alrededores

Quién es quién y quién es dueño de qué. Sin datos de clientes.

Relacionado: [[Perceptyx/_indice|_indice]] · [[Perceptyx/procedimientos|procedimientos]] §
Cola de tareas y escalación

> **Fuentes:** ✅ Confluence *Team Partnership Model – Project Turbo+* (tabla actualizada el
> **11/02/2026**, sección de escalación el **02/12/2025**; exportada por Ignacio el 06/10/2026) · huddle
> de DelOps del 01/10 y sesiones de training (notas de Gemini). 🔍 = rol inferido de lo que hacía la persona.
> ⚠️ **La tabla de equipos es de febrero**: no incluye a la cohorte de septiembre y tiene gente
> desactivada. Puede haber cambiado.

---

## Línea de mando

- **Melanie Munsey** — VP of Customer Value Services. 📣 (selección)
- **Jackie Cech** — manager de Delivery Ops; hiring manager de Ignacio. Habla con engineering por bugs
  (comment theming), resuelve permisos de base, comparte credenciales. ✅ huddle 01/10
- **Edwin Munji** — manager de Delivery Ops. Habla con soporte (Katie) sobre el ruteo de pedidos;
  tiene scoping técnico de extracciones de datos. ✅ huddle 01/10. Tenía que dar la sesión de **SSO y API de Perceptyx** a la cohorte el 22/09 (anunciada por Jackie el 21/09; sin registro de que se haya hecho).
- **Aprobadores de customizations** (subclass files publicados desde SOS, 📣 Jackie 21/09): Jackie, Edwin,
  los dos Jack (Thelen y Smrekar 🔍) y gente de engineering; **Raphael** aprueba mientras EE.UU. duerme. Jackie
  está en el ***pilot team*** de SOS; **Lily** probaba el flujo de customizations.

## El modelo de equipos — *Project Turbo+*

✅ Cada **equipo de PM** tiene **2–3 PFS partners** (PFS = Delivery Ops) alineados, que comparten la
**Team Task Queue** de ese equipo. Más un **Automation Team** transversal.

| Equipo | Program Manager | PFS partners (al 11/02/2026) |
|---|---|---|
| A | Adam Harris | Jon Vail |
| B | Bill Pegans | Emily Zobel |
| C | Kim Heard | *(los tres listados están desactivados)* |
| D | Mindy Philips | "John" Thelen, "Ying" Lily Di |
| E | Pam Jones | Jack Smrekar, Sam Hodges |
| F | Steve Metzger | Timothy (Tim) Sams |
| — | **Automation Team** | Elena Khaletskaya, Mikhail Zuperman, Darrek Schmidt |

- 🔍 *"John Thelen"* en la tabla y *"Jack Thelen"* en el huddle: probablemente la misma persona.
- 🔍 **Equipo C sin partners activos** y tres ingresos en septiembre: es posible que la cohorte nueva
  cubra ese hueco. ✅ **Confirmado: Ignacio está en el equipo de Kim (C)** — en el video *9.23.2026 task walkthrough* (23/09) Emily dice *"So, Nasio, for you it would be Kim"*, y a Andrea le asigna otro (visto el 06/10 en la captura del transcript).
- Desactivados en la tabla (ya no están): Elizabeth Collins (B), Justyna Sosulska, Aleksandra Musijenko,
  Lukasz Zielazek (C).

## Delivery Ops (PFS partners)

- **Emily Zobel** — equipo B. Da el training práctico (28/09, 30/09, 01/10). Tiene fórmulas, snippets y
  scripts de backup que comparte.
- **Jon Vail** — equipo A. ~~🔍 parece PM o cercano a los PM~~ SUPERSEDED 06/10: es **PFS partner**,
  no PM (Confluence). En el huddle habló de timelines comprimidos y de pedidos que le llegan directo por
  Fresh Desk.
- **Lily Di** — equipo D; 360s, comment theming.
- **Jack Thelen** — equipo D; SSO, llamadas con clientes; Guillermo le hizo shadow.
- **Jack Smrekar** — equipo E; Q&A de surveys, llamadas técnicas con clientes (APIs).
- **Sam Hodges** — equipo E.
- **Tim Sams** — equipo F.

## Automation Team

- **Elena Khaletskaya**, **Mikhail Zuperman** (precedente de extracciones agregadas por script),
  **Darrek Schmidt**. Toman lo de CRON, scripts e integraciones *Pull*; miran la columna *Assist*.
  📣 **16/10:** Elena le mostró a Ignacio una tarea de **late adds** en una call de Zoom (también hace
  tareas de datos, no solo automatización). Usa scripts por terminal en el jail y ofreció compartir
  snippets y queries ([[Perceptyx/procedimientos#Late adds: sumar participantes a un survey que ya está en vivo (Elena, call del 16/10)|procedimientos § Late adds]]).

## Cohorte de ingreso (busy season 2026)

- **Andrea Durán** — ingresó con Ignacio; Equipos: **Bill y Steve**.
- **Guillermo Martinez** — ingresó con Ignacio; 📣 16/09: trabaja en **onboarding /
  implementación** de clientes nuevos (dueño de esos proyectos junto con **JT**; *Implementation Workspace*), no
  en un equipo de PM. Se reúne con *"the other TSM, Jack"* → 🔍 su rol es **TSM** (Technical Success Manager).
- **Ignacio Moll** — ingreso 14/09/2026. Equipo: ✅ **C (Kim Heard)** (16/09 y 23/09). Jackie ofreció
  sumarlo de *shadow* con **Elena** (Automation).

## Alrededor

- **Program managers** — dueños de la relación con el cliente; definen alcance (ej.: manager tree sí/no),
  reciben los audit files. Los seis de la tabla, arriba.
- **Kevin Carlson** — **Platform Onboarding**: hace el onboarding inicial de clientes nuevos y pasa las
  tareas de integración de datos. Avisarle al tomar una. ✅ Confluence *Data Integrations*
- **Cerwin Villanueva** / **Andrew Sears** — asignan el rol `intelligent_nudges` en UDS (el documento
  nombra a uno en cada párrafo). ✅ Confluence *Activate / Nudge Setup*
- **Katie** — 🔍 soporte al cliente; recibe pedidos que deberían convertirse en tickets.
- **Jess** (🔍 **Jess Schwab**) — lidera reuniones de requerimientos con clientes (API, huddle 01/10). En Confluence es autora de los Standard Forms de lifecycle (2022–2023) y aparece en el ejemplo del cron de comentarios: alguien con años en el área. Rol exacto, sin confirmar.

## Equipos vecinos

> ✅ Confluence *Workforce Transformation Consulting Team (WTC)* y *Customer Care & Support Plans*,
> exportadas el 06/10/2026.

- **WTC — Workforce Transformation Consulting.** Consultores (experiencia del empleado, L&D, ciencia del
  comportamiento) que asesoran al cliente a nivel ejecutivo y producen **Activate, EP (presentación
  ejecutiva) y Design**. Miden utilización y fechas de entregables en **Certinia**, CSAT de proyectos y
  adopción de nudges en **Gainsight**. Usan SOS para encontrar app IDs (*"MAC IDs: OLD way"*). Son el
  equipo con **más uso documentado de IA** de toda la empresa (ver abajo).
- **Customer Care (CC) — soporte.** Atiende por Freshdesk. Desde Q3 2025 los clientes eligen plan:
  - **Gold**: pueden contactar a CC **admins y usuarios finales**.
  - **Silver**: **solo admins**, en su horario local (US o EU); los usuarios finales van por sus admins.
    Clientes viejos que ya tenían soporte a usuarios finales no se cortan; se discute en la renovación.
  - **Legacy**: clientes que todavía no renovaron.
  - El plan se ve **en Salesforce, a nivel de cuenta**, y **arriba de todo en la página del proyecto en
    Certinia**. El uptime no cambia según el plan.
  - 🔍 Para DelOps: explica por qué algunos pedidos de usuarios finales llegan por el PM o por mail
    directo (el huddle del 01/10) y no como ticket de CC.

### IA en Perceptyx — lo que muestra la página de WTC

- Hay una biblioteca de **agentes GPT internos** (análisis de temas de comentarios, armado de ERC, QA de
  presentaciones, diseño de surveys, asistente de 360) y de prompts, con entrenamientos desde 2024.
- Existe **#pyxee-csg**, un bot de Slack que responde con contenido de Confluence y knowledge bases.
- ⚠️ **Hay una lista de clientes con los que no se puede usar GPT**, y el uso de datos de clientes con IA
  se habilitó en 2025 **"excepto para estos clientes"**. Regla nueva en [[KOS/Reglas|Reglas]] § 9.
- 🔍 Cambia la idea 6 de la síntesis del [[Perceptyx/_indice|_indice]]: la cultura de IA de la empresa
  está en consultoría (GPT, prompts), no en DelOps; MCP sigue sin aparecer.

## Canales de Slack

- **#do_support** — ✅ canal de Slack de Delivery Ops (📣 Ignacio, 06/10). Los PM piden ahí lo urgente; lo
  toma el primero que puede.
- ~~**#pfs_support**~~ → **`#do_support`**. Así lo nombra la página de *Project Turbo+* (anterior al cambio
  de nombre). Decisión de Ignacio, 06/10: *"puede ser que anteriormente se llamara así"* → **toda referencia a
  `#pfs_support` en la documentación se lee hoy como `#do_support`** (abierto a todos, para urgencias y
  visibilidad amplia). Tratado como equivalencia de trabajo, no como dato verificado.
- **#ps_task_escalation** — urgencias con impacto en vivo; **solo PMs**.
- **#product_support** — pasar clientes a SSO, demográficos en UDS.
- **#pyxee-csg** — bot de IA interno que contesta con Confluence y knowledge bases (`@Pyxee-csg`).
- **#team-dcvnext** — equipo de DC Mosaic. **#it_help** — IT y accesos.
