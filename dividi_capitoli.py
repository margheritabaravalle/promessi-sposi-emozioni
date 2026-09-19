# dividi_capitoli.py
# Divide il testo pulito nei singoli capitoli, individuando le intestazioni
# "CAPITOLO" seguite da un numero romano, e salva il risultato in un file
# JSON: una lista di capitoli, ciascuno con numero e testo.

import re
import json


INPUT = "promessi_sposi_pulito.txt"
OUTPUT = "capitoli.json"


def dividi_in_capitoli(testo):
    """Divide il testo in una lista di capitoli (numero + contenuto)."""
    # Pattern per intestazioni tipo "CAPITOLO I", "CAPITOLO XXXVIII"
    pattern = re.compile(r"CAPITOLO\s+([IVXLCDM]+)\b")

    # Troviamo tutte le posizioni in cui inizia un capitolo
    corrispondenze = list(pattern.finditer(testo))

    capitoli = []
    for i, corrispondenza in enumerate(corrispondenze):
        numero_romano = corrispondenza.group(1)
        inizio_contenuto = corrispondenza.end()

        # Il capitolo finisce dove inizia il prossimo, oppure a fine testo
        if i + 1 < len(corrispondenze):
            fine_contenuto = corrispondenze[i + 1].start()
        else:
            fine_contenuto = len(testo)

        contenuto = testo[inizio_contenuto:fine_contenuto].strip()
        capitoli.append({
            "numero": i + 1,
            "numero_romano": numero_romano,
            "testo": contenuto,
        })

    return capitoli


def main():
    with open(INPUT, encoding="utf-8") as f:
        testo = f.read()

    capitoli = dividi_in_capitoli(testo)

    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(capitoli, f, ensure_ascii=False, indent=2)

    print(f"Trovati {len(capitoli)} capitoli.")
    for capitolo in capitoli:
        print(f"  Capitolo {capitolo['numero']} ({capitolo['numero_romano']}): "
              f"{len(capitolo['testo'])} caratteri")
    print(f"\nSalvato in {OUTPUT}")


if __name__ == "__main__":
    main()