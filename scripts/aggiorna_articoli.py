import json
import re
from pathlib import Path

base = Path("contenuti")
destinazione = base / "articoli.json"
articoli = json.loads(destinazione.read_text(encoding="utf-8"))

def valore(testo):
    testo = testo.strip().strip('"').strip("'")
    return testo

for file in (base / "post").glob("*.md"):
    testo = file.read_text(encoding="utf-8")
    parti = testo.split("---", 2)
    if len(parti) < 3:
        continue

    intestazione, corpo = parti[1], parti[2]
    dati = {}

    for riga in intestazione.splitlines():
        if ":" in riga and not riga.startswith(" "):
            chiave, contenuto = riga.split(":", 1)
            dati[chiave.strip()] = valore(contenuto)

    titolo = dati.get("title", file.stem)
    data = dati.get("date", "")[:10]
    categoria = dati.get("category", "Pensieri")
    copertina = dati.get("cover", "").lstrip("/")

    paragrafi = [
        p.strip() for p in re.split(r"\n\s*\n", corpo)
        if p.strip()
    ]

    estratto = re.sub(r"!\[[^\]]*\]\([^)]+\)", "", corpo)
    estratto = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", estratto)
    estratto = re.sub(r"[*_#>`]", "", estratto)
    estratto = " ".join(estratto.split())[:220]

    articolo = {
        "id": file.stem,
        "titolo": titolo,
        "data": data,
        "categoria": categoria,
        "copertina": copertina,
        "estratto": estratto,
        "contenuto": paragrafi,
        "immagini": []
    }

    articoli = [a for a in articoli if a["id"] != articolo["id"]]
    articoli.append(articolo)

articoli.sort(key=lambda a: a["data"], reverse=True)
destinazione.write_text(
    json.dumps(articoli, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8"
)
print("Biblioteca aggiornata:", len(articoli), "articoli")
