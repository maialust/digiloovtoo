#!/bin/sh
# Laeb 7. peatuki pildid Pressbooksist kohalikku kausta.
# Pildid ei lae gitti (content/opetajaraamat/ on .git/info/exclude'is).
cd "$(dirname "$0")/.." || exit 1
mkdir -p content/opetajaraamat/images
echo "-> kanban.jpg"
curl -fsSL -o "content/opetajaraamat/images/kanban.jpg" "https://web.htk.tlu.ee/informaatika/digiloovtoo/wp-content/uploads/sites/3/2023/06/Kanban-1024x568.jpg" || echo "   NURJUS: kanban.jpg"
echo "-> rollid-1.jpg"
curl -fsSL -o "content/opetajaraamat/images/rollid-1.jpg" "https://web.htk.tlu.ee/informaatika/digiloovtoo/wp-content/uploads/sites/3/2023/06/Rollid-1-1024x558.jpg" || echo "   NURJUS: rollid-1.jpg"
echo "-> issues.jpg"
curl -fsSL -o "content/opetajaraamat/images/issues.jpg" "https://web.htk.tlu.ee/informaatika/digiloovtoo/wp-content/uploads/sites/3/2023/06/Issues-1024x247.jpg" || echo "   NURJUS: issues.jpg"
echo "-> issues_inside.jpg"
curl -fsSL -o "content/opetajaraamat/images/issues_inside.jpg" "https://web.htk.tlu.ee/informaatika/digiloovtoo/wp-content/uploads/sites/3/2023/06/Issues_inside-1024x379.jpg" || echo "   NURJUS: issues_inside.jpg"
echo "-> projektid.jpg"
curl -fsSL -o "content/opetajaraamat/images/projektid.jpg" "https://web.htk.tlu.ee/informaatika/digiloovtoo/wp-content/uploads/sites/3/2023/06/projektid-1024x527.jpg" || echo "   NURJUS: projektid.jpg"
echo
echo "Kohal:"
ls -lh content/opetajaraamat/images/*.jpg 2>/dev/null | awk '{print "  " $9 "  " $5}'
