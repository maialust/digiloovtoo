#!/bin/sh
# Toob 8 peatuki algse HTML-i Pressbooksi avalikust REST APIst kohalikku kausta,
# et embeddid (iframe, YouTube, H5P) saaks tapselt kaitte. Ainult lugemine.
cd "$(dirname "$0")" || exit 1
mkdir -p pressbooks_html
API="https://web.htk.tlu.ee/informaatika/digiloovtoo/wp-json/pressbooks/v2/chapters"
for id in 278 280 286 288 296 282 301 284; do
  echo "-> peatukk $id"
  curl -fsSL -o "pressbooks_html/$id.json" "$API/$id" || echo "   NURJUS: $id"
done
echo
echo "Kohal:"
ls -lh pressbooks_html/*.json | awk '{print "  " $9 "  " $5}'
