# Catálogo de servicios (SKUs) — qué compra el cliente

Lo que Perceptyx vende como servicio, con sus **límites contractuales**. Para Delivery Ops sirve para
una pregunta que el resto de la documentación no contesta: **¿esto que me piden está dentro de lo que el
cliente compró?**

Relacionado: [[Perceptyx/procedimientos|procedimientos]] · [[Perceptyx/cultivate-360|cultivate-360]] ·
[[Perceptyx/equipo-delops|equipo-delops]] (Customer Care)

> **Fuente: ✅ *Description of Service – Perceptyx (2025-09)*** (PDF de 54 páginas, Google Drive de
> ventas *Pricing & Packaging*), pasado por Ignacio el **06/10/2026** después de que el bot Pyxee-CVO lo
> citara. Es un documento **comercial/contractual**, no de procedimiento: dice *qué* se entrega y con qué
> tope, no *cómo* se hace. Versión de septiembre de 2025.
>
> ⚠️ **Este documento está en revisión.** En la *PM Power Hour* (abajo) Melanie anunció una
> **racionalización de SKUs** y la simplificación del DOS y del DOP: los nombres y topes de esta nota
> pueden cambiar en 2026.

---

## Por qué le importa a DelOps

- **Cada tarea suele corresponder a un SKU vendido**, con topes: cantidad de demos, de archivos, de
  surveys, de iteraciones con el cliente. Lo que pasa el tope es un **change order** o una compra nueva.
  🔍 Encaja con reglas que ya estaban sueltas: las *jerarquías custom* tienen que estar en contrato (data
  specs) y "más de cinco roles cuesta extra".
- **Patrón de casi todos los SKUs de datos:** Perceptyx da el documento de diseño → workshop → el cliente
  prepara el archivo → Perceptyx carga → el cliente revisa y corrige → recarga → el cliente aprueba →
  se programa lo recurrente (**hasta diario / nightly**). **Extraer los datos de su sistema es siempre
  responsabilidad del cliente.**
- **Aceptación tácita:** en las implementaciones, el cliente tiene **14 días** después de la entrega para
  dar feedback por escrito; si no, se considera aceptado.
- ✅ **DRA = *Data Release Authorization*.** Confirmado en el documento (Data Export, Mayflower/ITSG,
  Custom Report): *"may be required depending on the data provided"*.

## Los SKUs que tocan datos o configuración

| SKU (código) | Qué es | Topes | Dónde está el cómo |
|---|---|---|---|
| **Core Implementation** (`PS-IMPLEMENT-PLATFORM`) | Onboarding de plataforma: comunicaciones, kickoff, readiness técnico (specs, **feeds Push/Pull**, **SSO**), super-usuario admin, roles básicos (admin, manager, respondente), branding, aviso a Customer Care | — | procedimientos § Alta de cliente, § SSO, § Integraciones |
| **Activate Implementation** (`PS-IMPLEMENT-ACTIVATE-PKG`) | Configuración de Activate: prioridades, comportamientos, segmentación, frecuencia y día/hora, **planes de acción asistidos por IA** | Requiere Core | [[Perceptyx/nudge-engine|nudge-engine]] |
| **Custom Roles and Statuses** | Roles/statuses de acceso a reportes y demos | **5 por compra**; solo en eventos Perceptyx-led | — |
| **Clean Data** | Limpiar, consolidar y transformar archivos del cliente al formato de Perceptyx; carga única o recurrente | **Hasta 5 archivos**; cambios al extract después de aprobado = change order | procedimientos § Data specs |
| **Import Data** | Importación única o recurrente con documento de diseño | El cliente transforma al formato | procedimientos § Data file load |
| **Additional Demographics** | Sumar demos al archivo existente | **Hasta 40 campos más**; spec estándar ampliada **hasta 135 campos** | procedimientos § Agregar un demográfico |
| **Trend Connections** | Trend de demos e ítems contra otros surveys | **Hasta 4 surveys** point-in-time de Perceptyx; ítems por **texto exacto / question ID**; 3 iteraciones | procedimientos § Trend mismatch |
| **Branches** | Branching en un survey Perceptyx-led | **Hasta 10** | — |
| **Additional Survey Items** | Ítems escalares extra | **+40** (sobre los 40 incluidos) | — |
| **Alternative URL** | Links directos a un survey | **Hasta 10** | — |
| **Paper Survey** | Imprimir, enviar y cargar respuestas en papel | Correo de EE.UU.; proveedores terceros | — |
| **Data Export** (`-1T`) | Extract a SFTP, único o recurrente (hasta nightly) | User/demos + **hasta 3 surveys**; campos del reporting estándar; **DRA** según datos | — |
| **Custom Report** | Extract con formato acordado, por SFTP o mail | Mail exige **firmar una indemnización**; sin cambios después de aprobado el diseño sin change order; **DRA** | — |
| **Mayflower or ITSG** | Export del **Census anual** a una de esas dos organizaciones de las que el cliente es miembro | **DRA** según datos | — |
| **Cloned 360 with Trending** | Clonar un 360 para otra ronda de los mismos leaders, con trend | Sin cambios de contenido | [[Perceptyx/cultivate-360|cultivate-360]] |
| **Additional 360 Version** | Otra versión de 360 diseñada con un consultor WTC | Hasta 55 ítems escalares + 3 abiertas | ídem |
| **Nudge Mapping** | Mapear comportamientos o ítems custom al *People Insights Model* para que disparen nudges | Hasta 55 comportamientos (360) | [[Perceptyx/nudge-engine|nudge-engine]] |
| **Single Sign-On** (`PLATFORM-ADD-SSO`) | Metadata, llamada, configurar el portal | Okta estándar | procedimientos § SSO |
| **HRIS Connections** (`PLATFORM-ADD-HRIS-CONNECT`) | Conector del HRIS del cliente | **Hasta 94 demos**; conectores: **SFTP genérico, Workday RaaS (JSON), SAP SuccessFactors, Oracle HCM Cloud**; otro HRIS = proyecto custom; hasta diario | procedimientos § Integraciones (Pull) |

**Lifecycle (paquete de evento) — la automatización de datos que incluye** (✅ DOS, cláusula del
Lifecycle Event Package; verificado el 06/10 después de que el bot Pyxee-CVO la resumiera):

- Carga **continua (diaria o semanal)** del archivo de empleados desde un feed automatizado, en formato
  data spec: **hasta 94 demográficos = 44 estándar de Perceptyx + 10 autogenerados + hasta 40 custom**.
- Perceptyx arma **un (1) script de automatización** con la **plantilla estándar del lifecycle** elegido.
  El script depende de **valores exactos del archivo** (encabezados, IDs numéricos, textos de demos): **el
  cliente es responsable de no cambiar la estructura ni los elementos lógicos del archivo**.
- Hasta **3 *data triggers*** — condiciones del archivo que disparan el survey (en Onboarding, hasta 3
  versiones con esos triggers). Se acuerdan con el cliente **antes** de armar el script; **después, todo
  cambio se cotiza** en tiempo y costo.
- Incluye también hasta 5 super-admins, 3 *user personas*, 10 usuarios de prueba, invitación + 2
  recordatorios, demos de tiempo en reporting y una sesión de lecciones aprendidas.

🔍 **Para DelOps:** cuando un cron de lifecycle se rompe porque el cliente cambió un encabezado o el texto
de una opción, **eso está fuera de lo contratado**: el contrato le asigna al cliente mantener el archivo
igual. Es un dato para el PM, no un arreglo silencioso.

**Paquetes de evento** (cada uno con su alcance propio, no detallado acá): **Lifecycle**, **Anniversary**,
**Multi-Rater** (360), **Pulse**, **Census**. Más SKUs de consultoría (diseño de survey, presentación
ejecutiva, entrevistas, workshops), de **healthcare** (Safety Culture, AHRQ, satisfacción de enfermería,
médicos) y **Custom Scoped Project** para lo que no entra en nada.

## Soporte (complementa Customer Care en [[Perceptyx/equipo-delops|equipo-delops]])

- **Gold Support:** helpdesk para hasta **10 administradores / ambassadors**, por portal o teléfono.
- **Gold – End-user Support:** también los empleados que responden pueden contactar a Customer Care.
- ⚠️ **Gold – FedRAMP, GovCloud, US Citizen Support:** para el sector público de EE.UU. ***"All personnel
  who have access to customer systems, data, or support tickets must be verified US citizens."*** 🔍
  **Ignacio, desde Uruguay, no puede tocar sistemas, datos ni tickets de esos clientes.** Si una tarea es
  de un cliente GovCloud (la tercera región que aparece en DC Mosaic), no es para él: verificarlo antes de
  abrirla.

---

## Cómo se lee un contrato y cómo se estiman las horas (PM Power Hour)

> **Fuente:** transcripción de la ***PM Power Hour: Pricing, Packaging & Scoping***, sesión interna de
> **Melanie Munsey con los program managers** (~35 personas), que Ignacio obtuvo vía el bot Pyxee-CVO el
> 06/10/2026. 📣 Melanie y participantes. Fecha de la sesión no consta; 🔍 **principios de 2026** (el
> estimador es de *"February 2026"* y los cambios de precios fueron *"last year"*, 2025). Los clientes que
> se usan como ejemplo, omitidos. Es una sesión **para PMs**, no para DelOps: vale como contexto.

**Leer un contrato (order form):**

- Saltear las páginas legales (MSA, definiciones, uptime) e ir al **order form**. Ahí importa:
  - **Fechas de cada período (term)** → son las *contract start / end dates* del proyecto en Certinia. Los
    servicios se dan **por período** (un contrato de 3 años trae los servicios cada año, y se busca que se
    usen en su año).
  - **End size**: el tope de **participantes** del contrato. Si el archivo del cliente lo pasa, **no hay
    tolerancia contractual**: se levanta un **CSQL** para que lo vea el CSM (decisión comercial; alguien
    había oído "5–10 % de margen" y Melanie lo corrigió). Si viene por debajo, no se devuelve nada. El end
    size figura en la página de detalles del proyecto. 🔍 **Para DelOps:** un archivo con más
    participantes que el end size es una señal para avisar al PM, no algo para cargar sin decir nada.
  - Los **listening channels** suscriptos y los **eventos** comprados por año, con sus add-ons; después
    del order form viene el **DOP** (*Description of Product*) y el **DOS** (*Description of Service*) con
    el detalle de cada SKU.
- **Listening channel** = suscripción a una parte de la plataforma (point-in-time, lifecycle, crowdsource,
  360…). Incluye el uso **self-service**; **para comprar un evento gestionado hay que tener el channel**.
- **Lifecycle Event Package ahora es de una sola vez** (antes recurrente): se implementa y se cierra. Si el
  cliente quiere cambiar su encuesta de egreso al año siguiente, compra el SKU de nuevo.
- **Import Historical Data** = datos de **otro proveedor** (no un refresh interno). En negocio nuevo se
  intenta limitar a surveys point-in-time.
- **Traducciones:** un evento gestionado con idiomas **tiene que tener el SKU de traducción**; el
  self-service usa traducción automática sin límite. *"Human translations"* pasa a llamarse ***premium
  translations***. Humano = **SmartCat** (caro, lo paga Perceptyx); máquina = Microsoft. Criterio de
  Melanie: *"err on the side of spending pennies over thousands"*. El proceso está en revisión: **no
  cambiar lo que se hace hasta que haya guía nueva**.
- **Premium benchmark cuts:** el número contratado (ej. 5) es **para todo el contrato**, no por survey.
- Ante cualquier duda del contrato: el **CSM** o el **AE**, o el manager.

**El estimador de horas (desde febrero 2026):**

- Planilla de Google en la *template gallery* (*"updated estimator February 2026"*). El **PM** la completa
  con los datos del contrato, la guarda en la carpeta del proyecto, y el **manager actualiza las horas en
  Certinia** y marca un checkbox de revisión.
- Da horas por **familia de rol**: **platform services (PFS = Delivery Ops)**, PMs, consultores (WTC) y
  **EXOps**. 🔍 **Las horas de DelOps de cada proyecto salen de acá**: es el presupuesto contra el que se
  van a medir las horas que Ignacio carga en Certinia.
- Insumos: tipo de proyecto (pulse, census, lifecycle inicial / aniversario / refresh, multi-rater),
  tamaño (**50.000+ empleados = "large" automático**), FedRAMP, papel, años de trend, data export,
  Mayflower, idiomas, roles/statuses por encima de 5, branching, versiones, workshops, healthcare, y
  **build approach**: correr el survey en **Mosaic, Amsterdam o Classic** cambia las horas.
- Se hace **tres semanas antes del *start work date***, cuando el proyecto aparece en el reporte
  **Squeaky Clean** (el proceso de higiene de datos en Certinia). Lo ya empezado se revisa de a poco.
- Para qué: forecast de capacidad (el año anterior hubo que sumar recursos temporales y partners),
  detectar **proyectos que se van de horas** (*"90 % de las horas en el mes uno de tres"*) y encontrar lo
  que se entrega **sin estar en el contrato** → **CSQL** al CSM. El tiempo de estimar se carga al proyecto,
  no a horas administrativas. Mensaje explícito: **sin juicio** si el real difiere del estimado; el
  objetivo es medir.
- Otro uso de los datos de proyecto en Certinia: **programar las ventanas de mantenimiento** de los
  servidores US y EU en los períodos de menos surveys.

## Lectura

- 🔍 **El conector de HRIS es el terreno de Ignacio:** Workday, SuccessFactors y Oracle HCM son el mundo
  de UKG, del otro lado. Las integraciones *Pull* las hace Automation, pero el conocimiento de esos
  sistemas es escaso y transferible.
- 🔍 **Las "iteraciones" tienen tope** (casi siempre 3): cuando un cliente pide la cuarta corrección de
  un archivo o un trend, eso ya no es la tarea original. Es un dato para hablar con el PM, no para
  negociar con el cliente. ✅ La PM Power Hour lo confirma como política: lo que se entrega fuera de
  contrato se documenta y se convierte en **CSQL**.
- 🔍 **Las horas de DelOps ya tienen presupuesto por proyecto** (el estimador). Cargar bien las horas en
  Certinia no es burocracia: es el dato con el que la dirección decide capacidad y detecta proyectos
  desbordados.
