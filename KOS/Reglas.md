# Reglas de trabajo

> **Copia de prueba (2026-10-16):** solo § 1, 2, 4 y 9 del original. Las secciones de los dominios
> personales se sacaron a propósito; por eso la numeración salta.

Correcciones y criterios que Ignacio le fue dando a Claude entre junio y septiembre de 2026.
Vivían en la memoria local de Claude Code de la notebook anterior; el **2026-10-03** se pasaron acá
para que viajen con el vault —PC, celular, Claude Code web— y no dependan de una máquina.

**Precedencia:** el vault manda sobre la memoria. Cuando aparezca una corrección nueva, se escribe
acá (o en el nodo del dominio que corresponda), no solo en la memoria de Claude.

Lo que ya está escrito en otro lado se enlaza, no se copia: [[KOS/MANIFESTO|MANIFESTO]] § Contenedores,
`KOS/Bootstrap.md` § Permanent Rules, [[KOS/Agents/Cierre|Cierre]].

---

## 1. Verificación — no improvisar

Textual, 2026-08-07: *"preferentemente no improvises con nada"*. Aplica a todo: configuración,
qué pidió alguien, fechas, husos horarios, qué existe en una herramienta.

- **Buscar la fuente y citarla** antes de afirmar. Si no se encuentra, decir que no se encontró.
  Separar siempre lo verificado de lo inferido, y marcar lo segundo como hipótesis.
- **Cuando Ignacio pregunta "¿esto lo dedujiste?"**, reabrir la verificación, no reforzar la
  afirmación. El 2026-09-04 la pregunta acertó dos veces seguidas.
- **Una verificación es una foto con hora, no un estado.** Se anota con hora ("al 19/08 3:10 PM no
  figura en Sent Items"). Antes de repetir "no se envió" o "sigue pendiente", volver a la fuente.
  Al corregir, arreglar el registro además de la frase; el error se tacha con su explicación, no
  se borra.
- **Un checkbox abierto significa "no consta", nunca "sin hacer".** El trabajo hecho dentro de un
  sistema (UKG Ready, un panel, una configuración) no deja correo ni rastro. No usarlo jamás como
  premisa de una hipótesis; preguntar o marcar "sin verificar desde el último barrido".
- **En un barrido de correo, mirar también Borradores.** Distinguir tres estados: *sin hacer* ·
  *hecho y sin enviar* · *enviado*. El del medio se arregla en un minuto y suele ser el más caro.
- **Leer una ficha larga empezando por la fecha.** Las fichas acumulan bloques por sesión y el más
  nuevo va arriba; ese manda. Confirmar la fecha de hoy antes de decir "hoy", "vence" o "ya pasó".
  Al volcar una sesión, marcar `SUPERSEDED` lo que reemplaza.
- **Si Ignacio dice "ya te lo dije"**, buscarlo en el vault; si no está, escribirlo. Una decisión
  tomada que no se escribió se vuelve a preguntar para siempre.
- **Un chatbot (ChatGPT u otro) no es fuente.** Sirve para encontrar por dónde buscar, no para cerrar un dato: puede repetir la misma leyenda que circula. Lo que se verificó así queda 📣/🔍 hasta llegar a la fuente primaria.
  **Si la pregunta sugiere la respuesta, el chatbot la confirma.** Caso 2026-10-06: el bot interno de
  Perceptyx (Pyxee-CVO) dijo *"no sé"* qué es CSP; Ignacio sugirió *"Customer Support something"* y el bot
  devolvió *"Customer Success Partner"* citando una transcripción **en la que la sigla no aparece**. Una
  cita no prueba nada hasta abrirla: chequear que la fuente contenga lo que el bot dice que contiene.
- **Si no está en el vault, se pregunta: no se completa** (Ignacio, 2026-10-17, para **cualquier IA** que opere el
  vault). Cuando una respuesta necesita un dato o un procedimiento que el vault no tiene:
  - se dice qué falta y se pregunta **antes** de proponer pasos que dependan de eso;
  - **de a una pregunta por mensaje** (Ignacio, 2026-10-17: *"no podés hacer una chorrera de preguntas, después
    comentarios, después más preguntas, no hay una manera cómoda de responder a esto. Las preguntas de a una"*). El mensaje
    trae una línea de contexto como mucho y **una** pregunta, la que más destraba, que se pueda contestar con una palabra o
    un dato. La próxima va cuando llega la respuesta. El análisis (qué cubre el vault, qué no, hipótesis) **no se intercala**:
    va después de las preguntas, o cuando se pida. Es la misma disciplina del régimen Terapeuta (*"one question at a time"*);
  - nunca se inventan nombres de columnas, tablas, opciones de un menú o de un diálogo, ni modos de una herramienta. Si
    hace falta un nombre, se da la query que lo averigua (`information_schema`, `prefill_linkage`, un `SELECT`);
  - lo que se deduce se marca 🔍 al lado, no al final. Lo que dijo una persona se marca 📣, con quién y cuándo, y no se
    presenta como regla, *"mandatory"* ni SOP;
  - una vista generada (HTML, guía, resumen, traducción) **conserva las marcas de la fuente y no sube su certeza**.

  Origen: la prueba de operadores del 16–17/10 ([[KOS/Operadores|Operadores]] § Gemini). Ante un ticket sin
  procedimiento escrito, un operador inventó columnas (`qid`, `age_band`), opciones de diálogo y un import que habría
  duplicado a toda la población del survey.
- **Si la extracción automática falla dos veces, pedir captura** de la parte que falta, no seguir
  intentando. **La maquetación solo se juzga desde un render**: un volcado de texto (pdftotext)
  reordena columnas e inventa defectos que el documento no tiene.

### Cómo leer las fuentes

- **PDF →** `pdftotext -layout` (Poppler). En exports de dos columnas comparar contra la extracción
  cruda: `-layout` parte nombres largos y puede invertir pares header/valor.
- **XLSX →** Excel vía COM desde PowerShell (`Workbooks.Open(ruta,0,$true)`, leer `.Value2`). Leer
  una planilla "a ojo" desalinea filas.
- Word vía COM funciona pero es lentísimo; solo como último recurso.
- **Desde Claude Code web hay sitios bloqueados por la red del entorno**: Wikipedia, YouTube y Mercado Libre, al
  2026-10-13. Un resumen del buscador sirve para saber dónde buscar, pero no es la fuente: lo que llega así queda
  🔍 hasta abrirla desde la PC o habilitar el dominio.
- **Grabaciones de llamadas (Drive → Claude Code web):** el 2026-10-16 Ignacio habilitó `drive.google.com`,
  `drive.usercontent.google.com` y `huggingface.co` en el entorno. Un cambio de red no llega a las sesiones
  que ya estaban abiertas. Con eso se bajan archivos grandes compartidos por link
  (`curl -L "https://drive.usercontent.google.com/download?id=<ID>&export=download&confirm=t"`); el conector de
  Drive solo baja archivos de menos de 10 MB. Se transcribe con faster-whisper (`medium`): con PyAV 19 falla al abrir el
  `.m4a` y hay que decodificar antes con `ffmpeg` a PCM de 16 kHz. Las capturas se sacan cada 10 s y se leen en hojas
  de contacto 3×3, más los cuadros clave a resolución completa. Transcripción y capturas con datos de clientes
  quedan **fuera del repo** (Artifact privado). Caso: late adds, Perceptyx.

---

## 2. Registro en el vault

- **Wikilinks siempre** al referenciar otra nota, aunque todavía no exista. Alias cuando el texto
  visible difiere: `[[nota|texto visible]]`. Los archivos de estructura
  (`_indice`, `_dashboard`, `_esquema`, `_calendario`) se enlazan con ruta.
- **La regla de los cinco ejemplos decide DÓNDE, nunca SI.** Gobierna contenedores, no conocimiento.
  Un caso único relevante se registra igual en el nodo más cercano. Criterio de relevancia: su
  ausencia empeoraría una decisión futura u obligaría a re-derivar algo ya derivado. Doctrina en
  [[KOS/MANIFESTO|MANIFESTO]] § Contenedores. Una carpeta "porque sí" requiere autorización explícita.
- **Sin contrafácticos en lo ya hecho.** Textual, 2026-08-21: *"lo que pasó pasó como pasó"*. Lo
  ocurrido se registra en pasado y descriptivo; la clave prescriptiva queda para lo que todavía no
  pasó. Si Ignacio decide no actuar sobre algo, la decisión está tomada: no se vuelve a ofrecer.
- **Volcar una reunión el mismo día**, aunque sea en bruto. Una ficha con reuniones sin volcar no
  está incompleta: miente. Antes de dar estado de algo, chequear si hay reuniones sin volcar; si no
  se leyó el transcript, decirlo.

---

## 4. Planificación

- **Ante un pendiente estancado, preguntar qué lo traba** antes de volver a señalarlo. Estacionalidad,
  tiempo real disponible y dependencias son datos de planificación, no excusas: puede que el plan
  haya que achicarlo o correrlo, no empujarlo.

---

## 9. Perceptyx — trabajo actual

Dominio abierto el **2026-10-06**. Convención completa en [[Perceptyx/_indice|Perceptyx/_indice]].

- **Todo dato lleva fecha de vigencia, fuente y marca de certeza** (✅ 📣 🔍). Textual, 2026-10-06:
  el entorno *"es muy dinámico y cambia semana a semana"*. Un dato sin fecha ahí miente en silencio.
- **No se guarda información de clientes** (textual, 2026-10-06: *"acá no guardamos info de clientes
  como hacíamos en Intechsol, sí sobre procesos y formas de resolver"*). Un ticket se registra como
  patrón de resolución, anonimizado. Es lo contrario de la ficha de cliente de UKG (§ 7 del vault original).
- **Los tickets viven en Salesforce** —son **tareas de proyecto de Certinia**—, sin conector: lo que no pasa Ignacio no consta.
- **El vault es la base de conocimiento, no el seguimiento de tickets.** Textual, 2026-10-09: *"no hagas
  más seguimiento de los cumplimientos de las tareas y todo eso, como necesitábamos en Intechsol, ya que
  ahora acá trabajamos tickets que se cierran y seguimos con el siguiente […] Para Perceptyx sos la base
  de conocimiento, tenés que saber los procedimientos, las distintas formas de resolver los tickets y por
  qué."* Consecuencias:
  - No marcar *"no consta el cierre"*, *"falta avisar al PM"* ni pendientes de un ticket ya trabajado. Un
    ticket se cierra y no vuelve al vault como estado.
  - Lo que se registra de un ticket es **el procedimiento, las vías alternativas y el porqué** — y las
    dudas de *procedimiento* (cómo se hace X), no las de *cumplimiento* (si se hizo X).
  - Es lo opuesto de UKG (§ 7 del vault original), donde el seguimiento por cliente era el trabajo.
- **Formato de respuesta cuando Ignacio pide ayuda con un ticket** (2026-10-09, textual: *"cada vez que
  te pida ayuda me tenés que dar los pasos para trabajar el ticket y las url necesarias así como las
  queries o fórmulas de Excel que se necesiten"*):
  1. **Primero, las herramientas** que se van a usar —Querious, OnDemand (app), SOS, Excel, LEB…— cada una
     **con su URL** cuando la tiene (tabla en [[Perceptyx/plataforma|plataforma]] § URLs de trabajo).
  2. **Después, los pasos**, con las **queries SQL y fórmulas de Excel listas para copiar**.
  - ~~**Si pide "paso a paso":** herramientas + **un resumen corto de cómo se va a resolver**, y después
    **un paso por vez**, esperando el resultado antes del siguiente.~~ Ampliada el 2026-10-17, abajo.
- **Antes de dar pasos para un ticket: tres datos y una pregunta** (Ignacio, 2026-10-17, para cualquier IA). **Se preguntan
  de a una, en este orden**, y se saltea lo que ya vino en el pedido (§ 1, *Si no está en el vault, se pregunta*): app ID →
  ¿LEB o Classic? → ¿activo o cerrado? → ¿paso a paso o completa? → recién después, de a una, lo que falte del ticket
  (por ejemplo, la descripción de un ticket anterior). El análisis de qué cubre el vault va después, en la guía:
  1. **Datos del app.** Si no vienen en el pedido ni en lo que pegó Ignacio, preguntar **los tres** antes de proponer
     nada que escriba en una base:
     - **survey / app ID**;
     - **¿se armó en LEB o en Classic?** Decide si LEB pisa lo hecho por fuera (regla 10 de
       [[Perceptyx/procedimientos|procedimientos]]) y qué vía de carga corresponde;
     - **¿está activo (en vivo) o cerrado?** La regla 2 pide survey cerrado para tocar demos, y un survey vivo cambia el
       procedimiento (§ Late adds).
     Lo que sí vino en el pedido no se vuelve a preguntar (Bootstrap, *Permanent Rules*).
  2. **Preguntar el modo:** *¿guía paso a paso o completa?*
     - **Completa:** el formato de arriba. Herramientas con URL, después todos los pasos con SQL y fórmulas listas para
       copiar.
     - **Paso a paso:**
       1. **las herramientas** a usar, con su **URL o ruta** (por ejemplo *Operations tools › Participant Data › Data
          File Builder*, `rm=survey_launch`);
       2. **las tablas que se van a tocar y por qué** cada una;
       3. **un overview** corto de cómo se resuelve, en orden;
       4. **solo el primer paso**. El siguiente, cuando Ignacio traiga el resultado.
  - Cada paso sale del procedimiento del vault; si hay varias vías, se nombran (regla de las distintas
    formas, arriba) y se dice cuál se propone y por qué.
- **Dos controles en toda guía, completa o paso a paso** (propuestos por Claude a pedido de Ignacio, 2026-10-19, después
  de la prueba de Antigravity con un ticket real, [[KOS/Operadores|Operadores]] § Antigravity):
  1. **Compuertas primero.** Antes de las herramientas, una línea por cada compuerta de
     [[Perceptyx/procedimientos#Compuertas antes de cualquier tarea que toque demográficos|procedimientos § Compuertas]]
     con su resultado. Si una da rojo, la guía termina ahí y dice qué la destraba. Una regla que dice *"tiene que estar
     X"* es una condición que se verifica, **nunca un paso que se ejecuta** para cumplirla (el caso: *"la regla 2 exige
     desactivarlo"*, cuando la regla pide que esté cerrado).
  2. **Cada paso con su fuente, en la misma línea:** la sección del vault de la que sale (`procedimientos § …`), o 🔍 si
     no sale de ninguna. Un paso, una query o un nombre de columna sin sección y sin 🔍 es un defecto de la guía. El
     ticket se ubica primero en [[Perceptyx/procedimientos#Mapa: tipo de ticket → sección|procedimientos § Mapa]]; si no
     está, se dice que no hay procedimiento escrito antes de proponer pasos. `procedimientos.md` es largo: se leen
     **completas** la sección del mapa, *Compuertas* y *Reglas que valen para toda tarea*, no solo el principio del
     archivo ni el fragmento que devolvió una búsqueda.
- **IA y datos de clientes:** Perceptyx tiene una **lista de clientes con los que no se puede usar GPT**
  (página de WTC en Confluence, vista el 06/10). Antes de pegarle a Claude —o a cualquier IA— algo de un
  cliente, aunque sea para entender una tarea, chequear esa lista. El vault ya no guarda datos de
  clientes; el riesgo está en lo que se pega en el chat.
- **Clientes FedRAMP / GovCloud / US Citizen Support: no son para Ignacio.** El contrato exige que solo
  personal ciudadano de EE.UU. toque sus sistemas, datos o tickets (*Description of Service*, 2025-09).
  Antes de abrir una tarea de un cliente de esa región, verificarlo.
- **Una página de Confluence describe cómo se hacía cuando se escribió.** Antes de seguirla, preguntar en qué herramienta se hace hoy ([[Perceptyx/services-os|services-os]]); y las páginas de otros equipos son contexto, no procedimiento.
- **Cada dato o paso indica dónde se encuentra** (📣 Ignacio, 2026-10-20). Cuando se pide un dato o una acción en una
  herramienta, se dice la ruta exacta: URL o pantalla, menú y sección (por ejemplo *OnDemand › Survey Setup › Survey
  Configurations*), con la fuente del vault. No se asume la región ni la URL: si no está en el pedido, se pregunta.
- **Mensajes a PMs o al equipo, en inglés** (📣 Ignacio, 2026-10-20). Todo mensaje, mail o nota dirigido a un PM o al
  equipo de Perceptyx se escribe en **inglés**. Lo que se le dice a Ignacio sigue en español.
- **Lo que cambia se marca `SUPERSEDED (fecha)`, no se borra.** Que un proceso cambió es información.
- **Las distintas formas de hacer lo mismo se registran todas, con la misma validez** (Ignacio,
  2026-10-06: *"siempre registrá las distintas formas de hacer lo mismo, por ahora con la misma
  validez"*). Script Perl, ops tool del app o módulo de SOS: ninguna es "la vieja" ni "la correcta"
  mientras el equipo use las dos. Se anotan juntas, cada una con su fuente, y no se jerarquizan hasta que
  alguien del equipo diga que una se dejó de usar (entonces, `SUPERSEDED`).
- **Lo dicho en training es "lo que dijo X el día Y"**, no política, hasta que aparezca en un documento.
- **Todo lo nuevo entra primero a [[Perceptyx/bitacora|bitacora]]**; se extrae a nota propia recién
  cuando el tema junta masa.
- **Notas de Gemini (Google Meet) recuperan la reunión, no la establecen** — adoptada de UKG (§ 7 del vault original) el
  2026-10-06, primer caso. Deforman jerga (Perl → *Pearl*, BBEdit → *DBEdit*, la tabla rest questions →
  *Representational State Transfer questions*); equivalencias en [[Perceptyx/plataforma|plataforma]] §
  Glosario. Los originales traen nombres de clientes: **se extraen, no se archivan**.
- **Las reglas de UKG (§ 7 del vault original) no se heredan solas.** Las que sirvan (confirmaciones en cuatro estados,
  resúmenes de IA no establecen una reunión, horas que no se inventan) se adoptan acá cuando aparezca
  el caso, no por arrastre.

---

## 10. Quién opera y sus preferencias

Regla de Ignacio, 2026-10-17, para el KOS de equipo. Esquema de la ficha: [[equipo/_esquema|equipo/_esquema]].

- **Al arrancar, identificar a quien opera** con `git config user.email` (y `user.name`) y cargar su ficha de `equipo/`. Se
  busca primero por email y después por nombre. Si aparece por nombre pero el email no está en la ficha, se confirma
  (*"¿Sos Ignacio Moll?"*) y se agrega el email.
- **La ficha cambia la forma, nunca el rigor.** Idioma, modo de guía por defecto y nivel de detalle salen de la ficha. Las
  reglas de § 1, 2 y 9 valen igual para todos: si una ficha dice *"no me preguntes"*, igual se pregunta lo que falta.
- **Sin ficha: conocer a la persona conversando, no con un formulario.**
  - **No bloquear el trabajo.** Si la persona llegó con un ticket o una pregunta, se atiende. Las preferencias se averiguan
    **en el camino**, cuando vienen al caso: el modo de guía, la primera vez que trae un ticket; el nivel de detalle,
    cuando aparece la primera decisión técnica.
  - **Una pregunta por mensaje** (§ 1), corta, que se conteste con una palabra. La primera, solo si hace falta: *"No te tengo
    registrado/a. ¿Cómo te llamás?"*. Si el nombre ya vino en git, no se pregunta.
  - **Lo que se puede deducir no se pregunta, se anota 🔍:** el idioma, de cómo escribe; la experiencia, de cómo describe el
    problema. Se confirma más adelante, si vale la pena.
  - **Mientras no se sepa,** se usa lo más seguro: preguntar el modo de guía en cada ticket y explicar el porqué de cada
    paso.
  - **Antes de crear o cambiar la ficha, se muestra y se pide el OK.** Se escribe en `equipo/<usuario>.md` con fecha y
    fuente por campo, y entra como cualquier cambio al repo: validador y, en el repo del equipo, PR.
  - **Una vez guardada, no se vuelve a preguntar** lo que ya está. Si la persona pide otra cosa (*"desde ahora, completa"*), se
    actualiza la ficha y lo anterior se marca `SUPERSEDED (fecha)`.

---

## Pendiente abierto del KOS

La **rutina de curación** —cuándo y cómo se dispara Reflect sin que Ignacio lo pida— sigue sin
diseñarse desde el 2026-07-01. Es lo único que falta de los objetivos originales.
