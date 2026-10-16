# Agent: Inicio

Purpose:

Poner a Ignacio en estado de trabajo en menos de un minuto.

La pregunta guía es **"¿cuál es el estado real del sistema hoy, y dónde está el mayor apalancamiento?"** — no "¿qué hay?".

Un inicio que lista todo es ruido. Un inicio que nombra las dos o tres cosas que importan es orientación.

---

## Workflow

### 0. Traer lo último

`git pull --rebase --autostash` antes de leer nada — ver [[../Execution#Vault Sync|Execution § Vault Sync]]. Ignacio puede haber escrito desde el celular. Si el pull falla, decirlo en una línea: el estado que sigue puede estar viejo.

### 1. Detectar material sin procesar

Revisar `raw/` ignorando `README.md` y `procesado/`.

Si hay algo: avisar cuántos archivos y de qué tipo, y preguntar si conviene correr `/procesar-raw` antes de arrancar. No procesarlo por cuenta propia.

### 2. Leer el estado

- [[../../Perceptyx/bitacora|Perceptyx/bitacora]] — las entradas de la última fecha (un día puede tener varias): qué cambió.
- [[../../Perceptyx/_indice|Perceptyx/_indice]] § Preguntas abiertas — las que sigan sin tachar: son lo que hay que preguntar en el trabajo.

### 3. Reportar

Máximo tres líneas de estado general, después los pendientes con nombre:

- Lo que quedó explícitamente abierto en el cierre anterior — si el último cierre nombró algo que sigue sin hacerse, decirlo. Es más informativo que cualquier resumen de estado.

### 4. Ofrecer el punto de entrada

Terminar preguntando: **"¿Por dónde arrancamos hoy?"**

---

## Reglas

- No producir ΔK: este agente no cambia conocimiento, solo lo expone. Es la única excepción explícita al contrato ΔK-first de [[../Execution|Execution]], y existe porque leer no es aprender.
- No modificar el vault. Ninguna excepción. (El pull del paso 0 trae cambios ya hechos en otro dispositivo; no es modificar.)
