#!/usr/bin/env python3
"""
Pressbooks -> Quartz migratsioon.

Loeb Pressbooksi AVALIKKU REST API-t (ainult lugemine) ja kirjutab tulemuse
Quartzi content/ kausta alla. Pressbooksis ei muuda see midagi.

Kasutus projektikaustast (~/Desktop/KBdevelopment/quartz):
    python3 tools/pressbooks_to_quartz.py --nimekiri
    python3 tools/pressbooks_to_quartz.py --osa opetajaraamat --limit 1
    python3 tools/pressbooks_to_quartz.py --osa opetajaraamat

Vajab: python3 (standardteek) ja quarto (kasutab Quarto kaasas olevat pandocit).
"""

import argparse, json, pathlib, re, subprocess, sys, urllib.request

BASE = "https://web.htk.tlu.ee/informaatika/digiloovtoo"
API = BASE + "/wp-json/pressbooks/v2"

DIV_ATTR = re.compile(r"^:{3,}\s*\{([^}]*)\}\s*$")
DIV_NIMI = re.compile(r"^:{3,}\s+([A-Za-z][\w-]*)\s*$")
DIV_LOPP = re.compile(r"^:{3,}\s*$")

OHUMARGID = [
    ("H5P", re.compile(r"h5p", re.I)),
    ("iframe", re.compile(r"<iframe", re.I)),
    ("YouTube", re.compile(r"youtube\.com|youtu\.be", re.I)),
    ("shortcode", re.compile(r"\[[a-z_]+[^\]]*\]", re.I)),
    ("sonastik", re.compile(r"glossary|sonastik", re.I)),
]


def api(tee):
    with urllib.request.urlopen(tee, timeout=60) as r:
        return json.load(r)


def pandoc(html):
    p = subprocess.run(
        ["quarto", "pandoc", "-f", "html", "-t", "markdown", "--wrap=none"],
        input=html, capture_output=True, text=True,
    )
    if p.returncode != 0:
        sys.exit("pandoc ebaonnestus:\n" + p.stderr[:800])
    return p.stdout


def _ava(rida):
    m = DIV_ATTR.match(rida) or DIV_NIMI.match(rida)
    return m.group(1) if m else None


def _lopp(read, i):
    """Rea i peal avaneva fenced div'i sulgeva rea indeks."""
    syg = 0
    for j in range(i, len(read)):
        if _ava(read[j]) is not None:
            syg += 1
        elif DIV_LOPP.match(read[j]):
            syg -= 1
            if syg == 0:
                return j
    return len(read) - 1


def _pealkiri_ja_sisu(read):
    """Eraldab textbox'i seest paisediv'i sisu pealkirjaks."""
    pealkiri, sisu, i = "", [], 0
    while i < len(read):
        kl = _ava(read[i])
        if kl is not None and "header" in kl:
            j = _lopp(read, i)
            tekst = [r.strip() for r in read[i + 1:j]
                     if r.strip() and _ava(r) is None and not DIV_LOPP.match(r)]
            pealkiri = " ".join(tekst).strip()
            i = j + 1
            continue
        if kl is not None or DIV_LOPP.match(read[i]):
            i += 1
            continue
        sisu.append(read[i])
        i += 1
    return pealkiri, sisu


def _kastiks(pealkiri, sisu):
    while sisu and not sisu[0].strip():
        sisu.pop(0)
    while sisu and not sisu[-1].strip():
        sisu.pop()
    paise = "> [!note]" + (" " + pealkiri if pealkiri else "")
    return [paise] + ["> " + r if r.strip() else ">" for r in sisu] + [""]


def korista(md):
    """Pandoci valjund -> Obsidiani/Quartzi sobiv Markdown."""
    md = re.sub(r"^(#{1,6} .+?)\s*\{[^}]*\}\s*$", r"\1", md, flags=re.M)
    read = md.split("\n")
    valja, i = [], 0
    while i < len(read):
        kl = _ava(read[i])
        if kl is not None and "textbox" in kl:
            j = _lopp(read, i)
            pealkiri, sisu = _pealkiri_ja_sisu(read[i + 1:j])
            valja.extend(_kastiks(pealkiri, sisu))
            i = j + 1
            continue
        if kl is not None or DIV_LOPP.match(read[i]):
            i += 1          # muu div: marker ara, sisu jaab alles
            continue
        valja.append(read[i])
        i += 1
    return re.sub(r"\n{3,}", "\n\n", "\n".join(valja)).strip() + "\n"


def slugi(s):
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", s.lower())).strip("-")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--osa")
    ap.add_argument("--limit", type=int)
    ap.add_argument("--nimekiri", action="store_true")
    a = ap.parse_args()

    print("Loen sisukorda...", flush=True)
    toc = api(API + "/toc")
    osad = toc.get("parts", toc if isinstance(toc, list) else [])

    if a.nimekiri or not a.osa:
        print("\nOsad selles raamatus:\n")
        for o in osad:
            print(f"  {o.get('slug'):40} {len(o.get('chapters', [])):2} ptk   {o.get('title','')}")
        print("\nVali uks: --osa <slug>")
        return

    osa = next((o for o in osad if o.get("slug") == a.osa), None)
    if not osa:
        sys.exit(f"Osa '{a.osa}' ei leitud. Vaata: --nimekiri")

    ptk = osa.get("chapters", [])
    if a.limit:
        ptk = ptk[: a.limit]

    valja = pathlib.Path("content") / a.osa
    valja.mkdir(parents=True, exist_ok=True)
    raport = []

    print(f"\nOsa: {osa.get('title')}  ({len(ptk)} peatukki)\n", flush=True)

    for i, p in enumerate(ptk, 1):
        pid, pealkiri = p["id"], p.get("title", f"Peatukk {i}")
        print(f"  [{i}/{len(ptk)}] {pealkiri}", flush=True)
        andmed = api(f"{API}/chapters/{pid}")
        html = (andmed.get("content") or {}).get("rendered", "")
        link = andmed.get("link", "")

        for nimi, muster in OHUMARGID:
            if muster.search(html):
                raport.append((pealkiri, nimi))

        md = korista(pandoc(html))
        fail = valja / f"{i:02d}-{p.get('slug') or slugi(pealkiri)}.md"
        fail.write_text(
            "---\n"
            f'title: "{pealkiri}"\n'
            f'allikas: "{link}"\n'
            f"pressbooks_id: {pid}\n"
            "---\n\n" + md,
            encoding="utf-8",
        )

    read = [f"- [[{a.osa}/{i:02d}-{p.get('slug') or slugi(p.get('title',''))}|{p.get('title','')}]]"
            for i, p in enumerate(ptk, 1)]
    (valja / "index.md").write_text(
        "---\n"
        f'title: "{osa.get("title")}"\n'
        f'allikas: "{BASE}/part/{a.osa}/"\n'
        "---\n\n"
        "> [!warning] Migreeritud sisu, avaldamata\n"
        "> Toodud Pressbooksist katsetamiseks. Litsents ja kaasautorlus on lahendamata,\n"
        "> seetottu ei ole see kaust gitis ega avalikul saidil.\n\n"
        "## Peatukid\n\n" + "\n".join(read) + "\n",
        encoding="utf-8",
    )

    r = ["# Migratsiooniraport\n\n", f"Osa: {osa.get('title')} ({len(ptk)} peatukki)\n"]
    if raport:
        r.append("\n## Tahelepanu vajab\n\n")
        r.append("Need elemendid ei kandu staatilisse saiti automaatselt:\n\n")
        r.append("| Peatukk | Element |\n|---|---|\n")
        for pn, el in raport:
            r.append(f"| {pn} | {el} |\n")
    else:
        r.append("\nErilist tahelepanu vajavaid elemente ei leitud.\n")
    (valja / "_migratsiooniraport.md").write_text("".join(r), encoding="utf-8")

    print(f"\nValmis. {len(ptk)} faili kaustas {valja}")
    print(f"Raport: {valja}/_migratsiooniraport.md")


if __name__ == "__main__":
    main()
