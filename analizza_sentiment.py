# analizza_sentiment.py
# Calcola un punteggio di sentiment per ciascun capitolo, contando quante
# parole positive e negative (secondo un dizionario italiano predefinito)
# compaiono nel testo, normalizzato sul numero totale di parole.

import json
import re
import csv


INPUT = "capitoli.json"
OUTPUT = "sentiment_capitoli.csv"

# Dizionario semplificato di parole italiane positive e negative.
# Scelte a mano, pensando al lessico tipico della narrativa ottocentesca
# (paura, morte, speranza, pace, ecc.). È un metodo volutamente semplice:
# non riconosce ironia, negazioni o sfumature di contesto - un limite da
# discutere esplicitamente nel progetto.

PAROLE_POSITIVE = {
    "gioia", "gioioso", "gioiosa", "gioiosi", "gioiose", "felice", "felici",
    "felicità", "contento", "contenta", "contenti", "contente", "allegro",
    "allegra", "allegri", "allegre", "allegria", "sorriso", "sorridere",
    "sorrise", "sorrideva", "sorridente", "amore", "amare", "amato", "amata",
    "amati", "amate", "amava", "amò", "speranza", "sperare", "sperava",
    "speranzoso", "fiducia", "pace", "tranquillo", "tranquilla", "tranquilli",
    "tranquille", "tranquillità", "serenità", "sereno", "serena", "sereni",
    "serene", "consolazione", "consolare", "consolato", "consolata", "bontà",
    "buono", "buona", "buoni", "buone", "benedizione", "benedire",
    "benedetto", "benedetta", "grazia", "salvezza", "salvare", "salvato",
    "salvata", "coraggio", "coraggioso", "coraggiosa", "vittoria", "trionfo",
    "festa", "festeggiare", "dolcezza", "dolce", "dolci", "affetto",
    "tenerezza", "pietà", "misericordia", "perdono", "perdonare",
    "perdonato", "gratitudine", "grato", "grata", "piacere", "piacevole",
}

PAROLE_NEGATIVE = {
    "paura", "spavento", "spaventato", "spaventata", "spaventoso",
    "spaventosa", "terrore", "terribile", "terrificante", "angoscia",
    "angoscioso", "angosciosa", "ansia", "tristezza", "triste", "tristi",
    "dolore", "dolori", "doloroso", "dolorosa", "sofferenza", "soffrire",
    "soffriva", "sofferto", "pianto", "piangere", "pianse", "piangeva",
    "disperazione", "disperato", "disperata", "disperati", "morte", "morire",
    "morto", "morta", "morti", "morte", "uccidere", "ucciso", "uccisa",
    "uccisi", "violenza", "violento", "violenta", "guerra", "peste",
    "malattia", "malato", "malata", "malati", "orrore", "orribile", "odio",
    "odiare", "rabbia", "ira", "furia", "minaccia", "minacciare",
    "minacciato", "minacciata", "tormento", "tormentare", "tormentato",
    "male", "cattivo", "cattiva", "cattivi", "crudele", "crudeltà",
    "vendetta", "vergogna", "colpa", "rimorso", "sventura", "sciagura",
    "miseria", "abbandono", "abbandonare", "abbandonato", "solitudine",
    "pericolo", "pericoloso", "pericolosa", "fame", "carestia",
}


def tokenizza(testo):
    """Divide il testo in parole minuscole, senza punteggiatura."""
    return re.findall(r"[a-zàèéìòù]+", testo.lower())


def calcola_punteggio(testo):
    """Restituisce un dizionario con conteggi e punteggio normalizzato."""
    parole = tokenizza(testo)
    totale_parole = len(parole)

    conteggio_positive = sum(1 for p in parole if p in PAROLE_POSITIVE)
    conteggio_negative = sum(1 for p in parole if p in PAROLE_NEGATIVE)

    # Punteggio normalizzato: differenza ogni 1000 parole, per poter
    # confrontare capitoli di lunghezza diversa.
    if totale_parole > 0:
        punteggio = (conteggio_positive - conteggio_negative) / totale_parole * 1000
    else:
        punteggio = 0

    return {
        "totale_parole": totale_parole,
        "parole_positive": conteggio_positive,
        "parole_negative": conteggio_negative,
        "punteggio": round(punteggio, 2),
    }


def main():
    with open(INPUT, encoding="utf-8") as f:
        capitoli = json.load(f)

    risultati = []
    for capitolo in capitoli:
        analisi = calcola_punteggio(capitolo["testo"])
        risultati.append({
            "numero": capitolo["numero"],
            "numero_romano": capitolo["numero_romano"],
            **analisi,
        })
        print(f"Capitolo {capitolo['numero']:2d} ({capitolo['numero_romano']:>7}): "
              f"punteggio {analisi['punteggio']:+.2f} "
              f"(+{analisi['parole_positive']} / -{analisi['parole_negative']})")

    with open(OUTPUT, "w", encoding="utf-8", newline="") as f:
        campi = ["numero", "numero_romano", "totale_parole",
                 "parole_positive", "parole_negative", "punteggio"]
        scrittore = csv.DictWriter(f, fieldnames=campi)
        scrittore.writeheader()
        scrittore.writerows(risultati)

    print(f"\nSalvato in {OUTPUT}")


if __name__ == "__main__":
    main()