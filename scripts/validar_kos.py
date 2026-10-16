#!/usr/bin/env python3
"""Validador estructural de KOS.

Comprueba invariantes que hoy dependen solo de que el modelo lea bien las reglas:

1. Wikilinks rotos: [[destino]] que no resuelve a ningún archivo del vault.
2. Lanzadores: cada `KOS/Agents/<X>.md` citado en `.claude/commands/` existe.
3. Mapa de dominios: cada carpeta de primer nivel aparece en KOS/Bootstrap.md.
4. Nombres duplicados: dos notas de contenido con el mismo nombre (MANIFESTO § Contenedores).
5. Archivos de estructura (_indice, _dashboard, _esquema, README) enlazados con wikilink corto.
6. Adaptadores de operador (CLAUDE.md, AGENTS.md): apuntan a KOS/Bootstrap.md y no copian el mapa.

No juzga conocimiento: solo estructura. Sale con código 1 si encuentra errores.
Uso: python3 scripts/validar_kos.py [raíz-del-vault]
"""
import re
import sys
from collections import defaultdict
from pathlib import Path

# Carpetas que no son conocimiento curado: el archivo de fuentes crudas copia texto ajeno
# y sus "wikilinks" no son del vault.
EXCLUIR = {".git", ".obsidian", ".trash", ".github", "raw"}
# UKG-Ready está archivado y congelado (CLAUDE.md § Archive): se informa, no falla.
ARCHIVADOS = {"UKG-Ready"}
BOOTSTRAP = "KOS/Bootstrap.md"
ADAPTADORES = ("CLAUDE.md", "AGENTS.md")
ESTRUCTURA = {"_indice", "_dashboard", "_esquema", "README"}
# Carpetas que no se exige declarar en el mapa de dominios.
NO_DOMINIO = {".git", ".obsidian", ".trash"}

WIKILINK = re.compile(r"(!?)\[\[([^\]\n]+?)\]\]")
FENCE = re.compile(r"^(```|~~~)")
INLINE_CODE = re.compile(r"`[^`\n]*`")


def archivos(raiz):
    for p in raiz.rglob("*"):
        rel = p.relative_to(raiz)
        if rel.parts and rel.parts[0] in EXCLUIR:
            continue
        if p.is_file():
            yield p


def lineas_sin_codigo(texto):
    en_bloque = False
    for n, linea in enumerate(texto.splitlines(), 1):
        if FENCE.match(linea.strip()):
            en_bloque = not en_bloque
            continue
        if not en_bloque:
            yield n, INLINE_CODE.sub("", linea)


def main():
    raiz = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    todos = list(archivos(raiz))
    # Para resolver enlaces se indexa también raw/: un link a una fuente archivada es válido.
    resolubles = todos + [p for p in (raiz / "raw").rglob("*") if p.is_file()]
    rutas = {p.relative_to(raiz).as_posix() for p in resolubles}
    rutas_lower = {r.lower() for r in rutas}
    por_nombre = defaultdict(list)
    for r in rutas:
        nombre = r.rsplit("/", 1)[-1]
        por_nombre[nombre.lower()].append(r)
        if nombre.lower().endswith(".md"):
            por_nombre[nombre[:-3].lower()].append(r)

    errores, avisos = [], []

    def reportar(rel, msg):
        (avisos if rel.split("/")[0] in ARCHIVADOS else errores).append(msg)

    # 1 y 5. Wikilinks
    for p in todos:
        if p.suffix not in (".md", ".canvas"):
            continue
        rel = p.relative_to(raiz).as_posix()
        carpeta = rel.rsplit("/", 1)[0] if "/" in rel else ""
        for n, linea in lineas_sin_codigo(p.read_text(encoding="utf-8", errors="replace")):
            for _, cuerpo in WIKILINK.findall(linea):
                destino = re.split(r"[|#^]", cuerpo.replace("\\|", "|"), maxsplit=1)[0].strip()
                if not destino:
                    continue  # [[#Encabezado]]: enlace interno a la misma nota
                d = destino.lower()
                candidatos = [d, d + ".md"]
                ok = False
                for c in candidatos:
                    if "/" not in c:
                        if c in por_nombre:
                            ok = True
                    else:
                        norm = (Path(carpeta) / c).as_posix() if c.startswith("..") or c.startswith("./") else c
                        norm = str(Path("/" + norm).resolve())[1:].lower() if ".." in norm or "./" in norm else norm
                        if norm in rutas_lower or any(r.endswith("/" + c) for r in rutas_lower):
                            ok = True
                        # Obsidian también resuelve relativo a la nota
                        rel_nota = str(Path("/" + carpeta + "/" + c).resolve())[1:].lower()
                        if rel_nota in rutas_lower:
                            ok = True
                    if ok:
                        break
                if not ok:
                    reportar(rel, f"{rel}:{n}: wikilink roto [[{cuerpo}]]")
                elif "/" not in destino and destino in ESTRUCTURA:
                    reportar(rel, f"{rel}:{n}: [[{cuerpo}]] es un archivo de estructura; enlazalo con su ruta")

    # 2. Lanzadores → agentes
    for cmd in sorted((raiz / ".claude" / "commands").glob("*.md")):
        texto = cmd.read_text(encoding="utf-8")
        for agente in re.findall(r"KOS/Agents/[\w\-]+\.md", texto):
            if not (raiz / agente).is_file():
                errores.append(f".claude/commands/{cmd.name}: apunta a {agente}, que no existe")

    # 3. Mapa de dominios
    mapa = (raiz / BOOTSTRAP).read_text(encoding="utf-8")
    for d in sorted(raiz.iterdir()):
        if d.is_dir() and d.name not in NO_DOMINIO and f"`{d.name}/" not in mapa:
            errores.append(f"{d.name}/: carpeta de primer nivel no declarada en {BOOTSTRAP}")

    # 6. Adaptadores: finos y apuntando al bootstrap neutral (KOS/Operadores.md § Principio)
    for nombre in ADAPTADORES:
        adaptador = raiz / nombre
        if not adaptador.is_file():
            errores.append(f"{nombre}: falta el adaptador de operador")
            continue
        texto = adaptador.read_text(encoding="utf-8")
        if BOOTSTRAP not in texto:
            errores.append(f"{nombre}: no apunta a {BOOTSTRAP}")
        if "### Creative Domain" in texto or "## Permanent Rules" in texto:
            errores.append(f"{nombre}: copia el mapa o las reglas de {BOOTSTRAP}; tiene que apuntar, no duplicar")

    # 4. Nombres duplicados entre notas de contenido
    vistos = defaultdict(list)
    for p in todos:
        if p.suffix == ".md":
            rel = p.relative_to(raiz).as_posix()
            if rel.startswith(".claude/"):
                continue  # los lanzadores comparten nombre con su agente a propósito
            vistos[p.stem.lower()].append(rel)
    for nombre, lista in sorted(vistos.items()):
        if len(lista) > 1 and nombre not in {e.lower() for e in ESTRUCTURA}:
            msg = f"nombre duplicado '{nombre}': " + ", ".join(sorted(lista))
            if all(r.split("/")[0] in ARCHIVADOS for r in lista):
                avisos.append(msg)
            else:
                errores.append(msg)

    for e in errores:
        print(f"ERROR  {e}")
    for a in avisos:
        print(f"AVISO  {a}  (dominio archivado)")
    print(f"\n{len(errores)} errores, {len(avisos)} avisos")
    return 1 if errores else 0


if __name__ == "__main__":
    sys.exit(main())
