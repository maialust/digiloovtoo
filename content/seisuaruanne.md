---
title: "Teadmusbaasi prototüübi seisuaruanne"
description: "Digiloovtöö teadmusbaasi tehniline seis ja õpetajaraamatu migratsiooni tulemused, 26.09.2026"
---

> [!info] Koostatud Maia Lusti jaoks — tööversioon
> Seisuga **26.09.2026**. See leht kirjeldab prototüübi tehnilist seisu ja ühe
> katselise migratsiooni tulemusi. See **ei ole** teadmusbaas ise ega valideeritud
> artefakt. Sisu ja struktuur ei ole veel disaininõuetest tuletatud.

## Mida see leht katab ja mida mitte

Lehel on kirjeldatud, mis on tehniliselt valmis ja mida näitas katse kolida
digiloovtöö õpetajaraamat Pressbooksist Quartzi-põhisesse teadmusbaasi.

**Õpetajaraamatu sisu ennast sellel saidil ei ole.** Põhjus on lahendamata
litsentsi- ja kaasautorlusküsimus: Pressbooksi väljaanne kannab märget
*All Rights Reserved* ja raamatu tasandil on nimetatud mitu autorit. Kuni see ei ole
lahendatud, hoitakse migreeritud sisu ainult kohalikus töökeskkonnas ning
seda ei avaldata. **Lahtine küsimus.**

## Tehniline seis

*Uurija tõendatud leid — kontrollitud töötavast prototüübist, mitte dokumentatsioonist.*

| Komponent | Seis |
|:---|:---|
| Quartz v5 kohalik paigaldus | töötab |
| Eestikeelne kasutajaliides (tuumik) | tehtud, versioonihalduses |
| Eestikeelne kasutajaliides (komponendipaketid) | tehtud kohalikult, **ei ole versioonihalduses** |
| Avaldamine GitHub Pagesile | töötab |
| Obsidian ühise sisukaustaga | töötab |
| Kirjatüüp, värvid, väljatõstekastid | seadistatud |

**Teadaolev puudus:** komponendipakettide eestikeelsed tõlked on tehtud otse
paigaldatud pakettidesse ja need kaovad iga uuenduse või taaspaigalduse järel.
Avalikul saidil on nupud seetõttu praegu ingliskeelsed. Püsiv lahendus on
paranduste versioonihaldusesse viimine või tõlgete pakkumine lähteprojektile.

## Õpetajaraamatu migratsioon

*Uurija tõendatud leid — masinkontroll, iga peatükk võrreldi Pressbooksi
avaliku liidese kaudu saadud algse HTML-iga.*

Kaheksa peatükki toodi üle automaatselt. Seejärel võrreldi iga peatüki
migreeritud faili algse HTML-iga: nähtava teksti maht, loetelupunktid,
rõhutused, pildid, tabelid, välislingid ja sõnavara.

| Peatükk | Tekst alles | Loetelu | Rõhutused | Pildid | Kadunud linke | Kadunud sõnu |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| Digiloovtöö kontseptsioon | 100 % | 4/4 | 1/1 | – | 0 | 0 |
| Sisu ja õpitulemused | 100 % | 10/10 | 3/3 | – | 0 | 0 |
| Persoonad ja stsenaariumid | 101 % | 11/11 | 2/2 | – | 0 | 0 |
| Sprindi mõiste | 100 % | 0/0 | 9/9 | – | 0 | 0 |
| Koostöine projektipõhine õpe | 101 % | 7/7 | 7/7 | – | 0 | 0 |
| Soovitusi protsessi kavandamiseks | 101 % | 7/7 | 7/7 | – | 0 | 0 |
| Taiga kasutamise juhend | 101 % | 18/18 | 11/11 | 5/5 | 0 | 0 |
| Hindamise raamistik | 102 % | 26/26 | 12/12 | – | 0 | 0 |

Üle 100 % tuleneb sellest, et võrdlus loeb algses HTML-is ainult nähtavat teksti,
migreeritud failis aga ka tabelipäiseid ja videote pealkirju, mis algses olid
HTML-i atribuutides.

**Automaatne teisendus lõhkus kaks asja, mis tuli käsitsi parandada:**

1. Kaks tabelit — sprinditsükli ajakava ja õpilase enesehindamise mudel — teisenesid
   vormingusse, mida veebiplatvorm tabelina ei tunne. Enesehindamise mudelist oli
   kuuest veerust alles jäänud ainult üks: kogu hinnanguskaala oli kadunud.
   Mõlemad ehitati algsest HTML-ist uuesti.
2. Viis joonist viitasid endiselt Pressbooksi serverile ja neli videot olid
   teisendusel kaotsi läinud. Joonised toodi kohalikku kausta, videod taastati
   algsest asukohast.

**Analüütiline tõlgendus.** Masinkontroll kinnitab, et sisu ei ole kaotsi läinud.
See **ei** kinnita, et tulemus on teadmusbaas. Kontroll loendab, mitte ei mõista.

## Kolm leidu struktuuri kohta

*Uurija tõendatud leid — loendatud migreeritud failidest ja algsest HTML-ist.*

1. **Peatükkides ei ole ühtegi alapealkirja.** Kaheksast peatükist ei sisalda
   ükski ühtegi `h1`–`h6` elementi — ei migreeritud failis ega Pressbooksi algses
   HTML-is. Struktuuri kannavad kujundus ja väljatõstekastid, mitte semantika.
   Tagajärg: lehel ei teki sisukorda ega ankruid.

2. **Peatükid ei viita üksteisele.** Migreeritud peatükkides on null sisemist linki.
   Seosevaade kuvab seetõttu kaheksat lehte, mis ripuvad ühe koondlehe küljes ega
   ole ülejäänud teadmusbaasiga ühendatud.

3. **Mõisted on peidus kastides, mitte omaette sõlmedena.** Definitsioonid
   (persoona, stsenaarium, sprint, Taiga, ADDIE, liftikõne) esinevad peatükkide
   sees väljatõstekastidena. Teadmusbaasis peaksid need olema eraldi kirjed,
   millele peatükid viitavad.

**Analüütiline tõlgendus.** Kolm leidu osutavad samasse kohta: raamatu kolimine
annab teksti, mitte teadmusbaasi. Seosevõrk ei teki peatükkidest, vaid mõistekihist,
mida praegu ei ole. Mõistekihti ei tohi tuletada olemasoleva materjali ümber
paigutamisest — see peab tulenema põhjendatud disaininõuetest.

## Otsused, mis vajavad arutelu

**Lahtised küsimused.**

1. **Litsents ja kaasautorlus.** Millistel tingimustel tohib õpetajaraamatu sisu
   teadmusbaasis taaskasutada ja avaldada? Kes peab nõusoleku andma?
2. **Mõistekihi allikas.** Kas digiloovtöö mõistevõrgu sõlmed tuletatakse
   disaininõuetest, ainekavast või õpetajate tegelikust sõnavarast? Kes otsustab,
   mis on mõiste ja mis on peatüki pealkiri?
3. **Sõltuvus TLU serverist.** Peatükis "Persoonad ja stsenaariumid" on üks
   interaktiivne H5P element. Seda ei saa staatilisse saiti üle tuua — ainus
   võimalus on manustada see TLU Pressbooksi serverist. Kas teadmusbaas tohib
   sõltuda serverist, mida autor ise ei halda? See on jätkusuutlikkuse nõue.
4. **Artefakti piir.** Kas õpetajaraamat on teadmusbaasi osa või selle sisend?
   Praegu on see kolitud katseliselt, mitte põhjendatud otsuse alusel.

## Metoodiline märkus

Migratsioon, kontroll ja käesolev aruanne valmisid tehisintellekti abil
(Anthropic, Claude; september 2026): skriptide kirjutamine, elementide loendamine
ja teksti koostamine. Kõik arvulised väited on tuletatud failidest ja Pressbooksi
avalikust liidesest ning on korratavad. Sisulised otsused, tõlgendused ja
vastutus tulemuse eest jäävad autorile.
