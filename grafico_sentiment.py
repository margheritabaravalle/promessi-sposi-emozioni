# grafico_sentiment.py
# Crea un grafico dell'andamento del punteggio emotivo lungo i 38 capitoli,
# evidenziando alcuni capitoli chiave del romanzo per il confronto.

import csv
import matplotlib.pyplot as plt


INPUT = "sentiment_capitoli.csv"
OUTPUT = "grafico_sentiment.png"

# Capitoli "chiave" scelti a priori, in base alla trama, per verificare
# se l'analisi automatica riconosce questi momenti come emotivamente
# marcati. Il numero è quello progressivo (1-38), non il numero romano.
CAPITOLI_CHIAVE = {
    20: "Rapimento di Lucia",
    21: "Conversione dell'Innominato",
    31: "Inizio della peste",
    33: "Morte di don Rodrigo",
}


def leggi_dati(percorso):
    numeri = []
    punteggi = []
    with open(percorso, encoding="utf-8") as f:
        lettore = csv.DictReader(f)
        for riga in lettore:
            numeri.append(int(riga["numero"]))
            punteggi.append(float(riga["punteggio"]))
    return numeri, punteggi


def main():
    numeri, punteggi = leggi_dati(INPUT)

    plt.figure(figsize=(14, 6))
    colori = ["#d62728" if p < 0 else "#2ca02c" for p in punteggi]
    plt.bar(numeri, punteggi, color=colori)

    plt.axhline(0, color="black", linewidth=0.8)
    plt.xlabel("Capitolo")
    plt.ylabel("Punteggio emotivo (per 1000 parole)")
    plt.title("Andamento del tono emotivo nei Promessi Sposi, capitolo per capitolo")
    plt.xticks(numeri)

    # Evidenziamo i capitoli chiave con un'etichetta
    for numero, etichetta in CAPITOLI_CHIAVE.items():
        indice = numeri.index(numero)
        plt.annotate(
            etichetta,
            xy=(numero, punteggi[indice]),
            xytext=(numero, punteggi[indice] + (3 if punteggi[indice] >= 0 else -3)),
            ha="center",
            fontsize=8,
            rotation=90,
            arrowprops=dict(arrowstyle="->", lw=0.8),
        )

    plt.tight_layout()
    plt.savefig(OUTPUT, dpi=150)
    print(f"Grafico salvato in {OUTPUT}")


if __name__ == "__main__":
    main()