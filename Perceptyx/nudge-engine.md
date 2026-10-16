# Nudge Engine — configuración de Activate / Nudges

Cómo se da de alta y se configura un cliente en el **Nudge Engine**, el motor que manda *nudges*
(empujones personalizados) a los empleados según datos de survey, comportamientos organizacionales y
reglas de timing.

Relacionado: [[Perceptyx/procedimientos|procedimientos]] · [[Perceptyx/plataforma|plataforma]] (UDS,
Temporal)

> **Fuente: ✅ Confluence *Activate / Nudge Setup***, exportada por Ignacio el **06/10/2026**. La página
> no dice qué equipo es dueño de la tarea. Ejemplos con nombres de clientes: ninguno. Dice que la página
> de Job Type Mapping es *"recently deployed"* — lo más nuevo de la guía.

---

## Lo esencial

- **Herramienta:** *Nudge Engine Admin UI* (`ne-admin-ui`), una por región (US y EU, URLs internas en
  Confluence).
- **Orden estricto:** 1 → 7. **El paso 1 (importar la compañía) es requisito de todo lo demás.**
- **Home:** el dashboard *Configuration Status* muestra con tilde verde: usuarios con rol
  `intelligent_nudges`, usuarios con demográficos de UDS, company settings, estado del engine y timing.
- **El engine toma todo de UDS** (Unified Data Store): compañía, usuarios, roles y demográficos. Lo que
  falta en UDS se arregla en UDS y después se re-sincroniza acá.
- **Los procesos corren en Temporal**: cada import o corrida devuelve una URL de workflow para
  seguimiento. Es la fuente de verdad para depurar; al escalar a engineering, mandar el **Workflow ID**.

**La falla más común es silenciosa** (lo dice la guía): pocos usuarios con el rol `intelligent_nudges`.
Su ejemplo: **74/55.796** → el 99,9 % de los empleados no recibe nada, y el programa "parece andar".

---

## Paso a paso

### 1. Import Company

- **Requisitos:** la compañía existe en **UDS** con Company ID válido · acceso admin a `ne-admin-ui` ·
  **customer success confirmó que el cliente está aprobado** para nudges · el cliente tiene datos de
  survey o engagement en la plataforma.
- Buscar (mínimo 3 caracteres, hasta 10 resultados) → seleccionar **una** compañía → *Import* → dispara
  un workflow de Temporal.
- ⚠️ **Verificar que el Company ID sea el del cliente correcto antes de importar** (subsidiarias
  regionales con nombres parecidos). Una compañía equivocada arrastra todo lo que sigue.

### 2. Activar el engine y correrlo a mano

- Estado tras importar: **Inactive** (rojo). *Activate Nudge Engine* → crea un schedule diario en
  Temporal (hora aleatoria entre **19:00 y 03:00 UTC**).
- Aparece el banner amarillo *"No Nudge Engine runs yet… check back tomorrow!"* → **no esperar**:
  *Advanced* → **Sync from UDS** tildado (siempre en la primera corrida) → *Manually Run Nudge Engine*.
- Verificar en la URL de Temporal que la corrida terminó bien antes de seguir.
- Estados: **Active** (verde) · **Paused** (azul; conserva todo, para incidentes o eventos sensibles de la
  compañía) · **Deactivate** (corte duro; hay que reactivar).

### 3. Sincronizar y verificar usuarios

- Dos métricas `X/Y`: usuarios con rol **`intelligent_nudges`** (`role_type='intelligent_nudges'`,
  `role_name='enable_access'`) y usuarios con **demográficos de UDS**.
- **El rol se asigna en UDS, no acá.** Si la cuenta es baja: coordinar la asignación (la guía nombra a
  Cerwin Villanueva y a Andrew Sears) → *Sync UDS Users*.
- Demográficos faltantes → **#product_support**.
- *Sync UDS Users* también después de cualquier carga grande de HR (altas, bajas, cambios de
  organización). *Sync Specific User* (por email) para depurar a una persona.

### 4. Company Settings

Antes: confirmar con customer success el **timezone principal**, si hay requisitos de privacidad, qué
nudges o rationales excluir, y con producto si va **solo generated** o catálogo completo.

| Campo | Qué hace | Ojo |
|---|---|---|
| **Default Timezone** (`time_zone`) | Zona IANA por defecto | Mal puesta → nudges a las 3 AM para toda la compañía |
| **Disable Click Tracking** (`is_privacy_company`) | Apaga el tracking de clics | **Obligatorio en clientes con GDPR / privacidad estricta** — omitirlo es riesgo de cumplimiento |
| **Generated Nudges Only** | Solo nudges generados desde los datos del survey | Más a medida, menos variedad |
| **Excluded Nudges** | Lista separada por comas | Ej.: cliente sin programa de wellness |
| **Excluded Rationales** | Lista separada por comas | Más quirúrgico: apaga la lógica que dispara categorías enteras |

Revisar con customer success antes de salir en vivo y **cada trimestre**.

### 5. Job Type Mapping (`/companies/{id}/job-types`) — página nueva

- **Default Job Type:** el que reciben los que no matchean ninguna regla. `null` = los no matcheados
  quedan fuera del contenido por tipo de puesto (decisión intencional).
- **Job Type Counts:** usuarios por job type (solo los >0). Si un job type no aparece, su regla no
  matchea a nadie; si el default junta demasiados, faltan reglas.
- **Reglas:** job type + operador **ALL** (todas las condiciones; más seguro para empezar) o **ANY** +
  condiciones `tipo=valor` sobre demográficos de UDS (los valores se cargan de la API: solo existen los
  que hay en los datos). Filas incompletas se descartan sin aviso. **Borrar una regla reasigna en el acto**
  a sus usuarios al default.
- Revisar los counts después de crear o cambiar reglas.

### 6. Nudge Timing

- Requiere timezone (paso 4) y job types (paso 5) configurados, y la **cadencia aprobada por el cliente**
  (días laborales, períodos de bloqueo).
- Campos: **Name** · **Start Time** (opcional, futuro) · **Cadence** (la mayoría semanal o quincenal) ·
  **Preferred Days** (mejor mar–jue) · **Preferred Time(s)** (mejor 9–10 AM) · **Jitter** (default 30
  min; evita picos de mail y filtros de spam) · **Minimum Gap** (evita amontonamiento, sobre todo después
  de una pausa).
- **Después de guardar: *Refresh*** y verificar que **Users with Scheduled Nudges** subió y que **Earliest
  Event Time** es futura y razonable. **Workflows Validated** tiene que ser `true` antes de salir en vivo
  (`false` = problema de backend → engineering).
- Las configs borradas quedan visibles con `deleted_at` (auditoría).

### 7. Monitorear

- *Recent Runs*: últimas 5 corridas (Workflow ID, estado, inicio, link a Temporal).
- **Diario las dos primeras semanas después del lanzamiento, después semanal.** Un *running* que no
  termina puede ser un workflow colgado.

---

## Lo que no está claro

- ⚠️ La guía numera mal: el paso 6 dice requerir *"Job types are configured (Step 6 complete)"*; debería
  ser el paso 5.
- 🔍 **Quién hace esto** — Delivery Ops, Automation, otro equipo. La página no lo dice.
- 🔍 **"Activate"** parece el nombre del producto de nudges; no está definido en la página.
