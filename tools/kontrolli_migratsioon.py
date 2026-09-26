# -*- coding: utf-8 -*-
"""Vordleb iga peatuki algset Pressbooksi HTML-i migreeritud Markdowniga.
Ainult lugemine: ei muuda uhtegi sisufaili. Kirjutab aruande."""
import json, re, io, os, unicodedata

TOOLS = os.path.dirname(os.path.abspath(__file__))
KAUST = os.path.join(os.path.dirname(TOOLS), "content", "opetajaraamat")
HTMLK = os.path.join(TOOLS, "pressbooks_html")

PEATYKID = [
 (278, "01-digiloovtoo-konstseptsioon.md",                  "Digiloovtöö kontseptsioon"),
 (280, "02-digiloovtoo-sisu-ja-opitulemused.md",            "Sisu ja õpitulemused"),
 (286, "03-persoonad-ja-stsenaariumid-digiloovtoos.md",     "Persoonad ja stsenaariumid"),
 (288, "04-sprindi-moiste-ja-selle-koht-digiloovtoos.md",   "Sprindi mõiste"),
 (296, "05-koostoine-projektipohine-ope.md",                "Koostöine projektipõhine õpe"),
 (282, "06-soovitusi-digiloovtoo-protsessi-kavandamiseks.md","Soovitusi protsessi kavandamiseks"),
 (301, "07-taiga-kasutamise-juhend.md",                     "Taiga kasutamise juhend"),
 (284, "08-digiloovtoo-hindamine.md",                       "Hindamise raamistik"),
]

OLEMID = [('&nbsp;',' '),('&#8211;','-'),('&#8212;','-'),('&#8220;','"'),('&#8221;','"'),
          ('&#8216;',"'"),('&#8217;',"'"),('&amp;','&'),('&lt;','<'),('&gt;','>'),('&#038;','&')]

def lahti(s):
    for a,b in OLEMID: s=s.replace(a,b)
    return s

def html_tekst(h):
    h=re.sub(r'<(script|style)\b.*?</\1>','',h,flags=re.S)
    h=re.sub(r'<[^>]+>',' ',h)
    return " ".join(lahti(h).split())

def md_tekst(m):
    m=re.sub(r'^---\n.*?\n---\n','',m,flags=re.S)          # frontmatter
    m=re.sub(r'!\[[^\]]*\]\([^)]*\)','',m)                  # pildid/videod
    m=re.sub(r'\[([^\]]*)\]\([^)]*\)',r'\1',m)              # lingid -> tekst
    m=re.sub(r'^>\s?','',m,flags=re.M)                      # callout-prefiks
    m=re.sub(r'^\s*\|','',m,flags=re.M)                     # tabeliaare
    m=m.replace('|',' ')
    m=re.sub(r'[*_`#>-]',' ',m)
    return " ".join(m.split())

def sonad(t):
    t=unicodedata.normalize("NFC", t.lower())
    return set(w for w in re.findall(r'[\wõäöüšž]{5,}', t))

read=[]
for pid, fail, nimi in PEATYKID:
    d=json.load(io.open(os.path.join(HTMLK,"%d.json"%pid),encoding="utf-8"))
    html=d["content"]["rendered"]
    md=io.open(os.path.join(KAUST,fail),encoding="utf-8").read()

    h_lingid=set()
    for m in re.finditer(r'<a\b[^>]*href="([^"]+)"', html):
        u=lahti(m.group(1))
        if u.startswith("http"): h_lingid.add(u.rstrip('/'))
    m_lingid=set()
    md_ilma_piltideta = re.sub(r'!\[[^\]]*\]\([^)]*\)', '', md)   # pildid ja videod valja
    for m in re.finditer(r'\]\((https?://[^)\s]+)', md_ilma_piltideta):
        m_lingid.add(m.group(1).rstrip('/'))

    n = dict(
      h_loik   = len(re.findall(r'<p\b', html)),
      h_li     = len(re.findall(r'<li\b', html)),
      h_rasvane= len(re.findall(r'<(strong|b)\b', html)),
      h_kaldu  = len(re.findall(r'<(em|i)\b', html)),
      h_pilt   = len(re.findall(r'<img\b', html)),
      h_tabel  = len(re.findall(r'<table\b', html)),
      h_iframe = len(re.findall(r'<iframe\b', html)),
      h_pealk  = len(re.findall(r'<h[1-6]\b', html)),
      m_li     = len(re.findall(r'^\s*(?:>\s*)?(?:[-*+]|\d+\.)\s+', md, re.M)),
      m_rasvane= len(re.findall(r'\*\*[^*\n]+\*\*', md)),
      m_pilt   = len(re.findall(r'!\[[^\]]*\]\((?!https://www\.youtube)', md)),
      m_video  = len(re.findall(r'!\[[^\]]*\]\(https://www\.youtube', md)),
      m_tabel  = 1 if re.search(r'^\s*(?:>\s*)?\|.*\|\s*$', md, re.M) else 0,
      m_pealk  = len(re.findall(r'^#{1,6}\s', md, re.M)),
    )
    ht, mt = html_tekst(html), md_tekst(md)
    hs, ms = sonad(ht), sonad(mt)
    read.append((pid, nimi, fail, n, len(ht), len(mt), h_lingid, m_lingid, hs-ms, ms-hs))

r=[]
r.append("---\ntitle: \"Migratsiooni kontrollaruanne\"\n---\n")
r.append("> [!warning] Masinkontroll, mitte sisuline hinnang")
r.append("> Vordleb migreeritud faile Pressbooksi algse HTML-iga. Loendab elemente ja sonu.")
r.append("> Ei hinda, kas sisu on oige. Koostatud automaatselt.\n")
r.append("## Kokkuvote\n")
r.append("| Peatukk | Tekst alles | Loetelu | Rasvane | Pildid | Video | Tabel | Kadunud linke |")
r.append("|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|")
for pid,nimi,fail,n,hl,ml,hlink,mlink,puudu,lisa in read:
    pct = (100.0*ml/hl) if hl else 0
    kad = len(hlink-mlink)
    r.append("| %s | %.0f %% | %d / %d | %d / %d | %d / %d | %d | %s | %s |" % (
        nimi, pct, n['m_li'], n['h_li'], n['m_rasvane'], n['h_rasvane'],
        n['m_pilt'], n['h_pilt'], n['m_video'],
        ("%d / %d" % (n['m_tabel'], n['h_tabel'])) if n['h_tabel'] else "-",
        kad if kad else "-"))
r.append("\nVeerud naitavad **migreeritud / algne**. Video-veerg loeb YouTube'i manustusi.\n")

r.append("## Uksikasjad peatukkide kaupa\n")
for pid,nimi,fail,n,hl,ml,hlink,mlink,puudu,lisa in read:
    r.append("### %s" % nimi)
    r.append("Allikas: Pressbooks id %d - Fail: `%s`\n" % (pid, fail))
    r.append("- Nahtavat teksti: algses %d tahemarki, migreeritus %d (%.0f %%)" % (hl, ml, 100.0*ml/hl if hl else 0))
    r.append("- Pealkirju (h1-h6): algses %d, migreeritus %d" % (n['h_pealk'], n['m_pealk']))
    r.append("- Loetelupunkte: algses %d, migreeritus %d" % (n['h_li'], n['m_li']))
    r.append("- Rasvaseid kohti: algses %d, migreeritus %d" % (n['h_rasvane'], n['m_rasvane']))
    r.append("- Pilte: algses %d, migreeritus %d" % (n['h_pilt'], n['m_pilt']))
    r.append("- iframe'e algses: %d (neist YouTube migreeritus: %d)" % (n['h_iframe'], n['m_video']))
    r.append("- Tabeleid: algses %d, migreeritus %s" % (n['h_tabel'], "jah" if n['m_tabel'] else "ei"))
    r.append("- Valislinke: algses %d, migreeritus %d" % (len(hlink), len(mlink)))
    kad = sorted(hlink-mlink)
    if kad:
        r.append("\n**Kadunud lingid:**\n")
        for u in kad: r.append("- `%s`" % u)
    lisandunud = sorted(mlink-hlink)
    if lisandunud:
        r.append("\n**Lisandunud lingid (kontrolli!):**\n")
        for u in lisandunud: r.append("- `%s`" % u)
    if puudu:
        n_ = sorted(puudu)
        r.append("\n**Sonu, mis on algses aga mitte migreeritus (%d):** %s" %
                 (len(n_), ", ".join(n_[:40]) + (" ..." if len(n_)>40 else "")))
    r.append("")

out=os.path.join(KAUST,"_migratsiooni_kontroll.md")
io.open(out,"w",encoding="utf-8").write("\n".join(r)+"\n")
print("Aruanne:", out)
print()
for pid,nimi,fail,n,hl,ml,hlink,mlink,puudu,lisa in read:
    print("%-36s tekst %3.0f%%  li %2d/%-2d  rasv %2d/%-2d  pilt %d/%d  link %d/%d  kadunud-sonu %d" % (
        nimi, 100.0*ml/hl if hl else 0, n['m_li'], n['h_li'], n['m_rasvane'], n['h_rasvane'],
        n['m_pilt'], n['h_pilt'], len(mlink), len(hlink), len(puudu)))
