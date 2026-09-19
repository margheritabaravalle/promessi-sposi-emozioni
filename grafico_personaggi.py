# grafico_personaggi.py
# Crea un grafico a linee che confronta l'andamento emotivo di Renzo, Lucia
# e l'Innominato lungo i capitoli, usando i dati prodotti da
# confronto_personaggi.py.

import csv
import matplotlib.pyplot as plt
from collections import defaultdict


INPUT = "sentiment_personaggi.csv"
OUTPUT = "grafico_personaggi.png"

COLORI = {
    "Renzo": "#1f77b4",
    "Lucia": "#d62728",
    "Innominato": "#7f3fbf",
}


def leggi_dati(percorso):
    """Restituisce un dizionario {personaggio: [(capitolo, punteggio), ...]},
    includendo solo i capitoli in cui il personaggio compare (punteggio non vuoto)."""
    dati = defaultdict(list)
    with open(percorso, encoding="utf-8") as f:
        lettore = csv.DictReader(f)
        for riga in lettore:
            if riga["punteggio"] == "":
                continue  # personaggio assente in questo capitolo
            capitolo = int(riga["capitolo"])
            punteggio = float(riga["punteggio"])
            dati[riga["personaggio"]].append((capitolo, punteggio))
    return dati


def main():
    dati = leggi_dati(INPUT)

    plt.figure(figsize=(14, 6))

    for personaggio, punti in dati.items():
        punti_ordinati = sorted(punti)
        capitoli = [c for c, _ in punti_ordinati]
        punteggi = [p for _, p in punti_ordinati]
        plt.plot(
            capitoli, punteggi,
            marker="o", markersize=4, linewidth=1.5,
            label=personaggio, color=COLORI.get(personaggio),
        )

    plt.axhline(0, color="black", linewidth=0.8)
    plt.xlabel("Capitolo")
    plt.ylabel("Punteggio emotivo (per 1000 parole)")
    plt.title("Percorso emotivo di Renzo, Lucia e l'Innominato lungo il romanzo")
    plt.legend()
    plt.grid(axis="y", linestyle="--", alpha=0.4)
    plt.tight_layout()

    plt.savefig(OUTPUT, dpi=150)
    print(f"Grafico salvato in {OUTPUT}")


if __name__ == "__main__":
    main()