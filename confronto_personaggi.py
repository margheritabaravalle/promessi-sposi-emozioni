# confronto_personaggi.py
# Estensione del progetto: invece del tono emotivo generale del capitolo,
# isola le frasi in cui compare il nome di un personaggio specifico e ne
# calcola il sentiment, capitolo per capitolo. Usa lo stesso dizionario di
# parole positive/negative della Fase 2, per restare confrontabile.

import json
import re
import csv


INPUT = "capitoli.json"
OUTPUT = "sentiment_personaggi.csv"

# Stesso dizionario usato in analizza_sentiment.py (Fase 2), per coerenza
# metodologica: i punteggi restano confrontabili tra le due analisi.
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
    "morto", "morta", "morti", "uccidere", "ucciso", "uccisa",
    "uccisi", "violenza", "violento", "violenta", "guerra", "peste",
    "malattia", "malato", "malata", "malati", "orrore", "orribile", "odio",
    "odiare", "rabbia", "ira", "furia", "minaccia", "minacciare",
    "minacciato", "minacciata", "tormento", "tormentare", "tormentato",
    "male", "cattivo", "cattiva", "cattivi", "crudele", "crudeltà",
    "vendetta", "vergogna", "colpa", "rimorso", "sventura", "sciagura",
    "miseria", "abbandono", "abbandonare", "abbandonato", "solitudine",
    "pericolo", "pericoloso", "pericolosa", "fame", "carestia",
}

# Nomi e varianti con cui riconoscere ciascun personaggio nel testo.
PERSONAGGI = {
    "Renzo": ["renzo", "tramaglino"],
    "Lucia": ["lucia", "mondella"],
    "Innominato": ["innominato"],
}


def dividi_in_frasi(testo):
    """Divide un testo in una lista di frasi, usando . ! ? come separatori."""
    frasi = re.split(r"(?<=[.!?])\s+", testo)
    return [f.strip() for f in frasi if f.strip()]


def frasi_del_personaggio(frasi, varianti_nome):
    """Restituisce solo le frasi che contengono almeno una variante del nome."""
    trovate = []
    for frase in frasi:
        frase_minuscola = frase.lower()
        if any(variante in frase_minuscola for variante in varianti_nome):
            trovate.append(frase)
    return trovate


def tokenizza(testo):
    return re.findall(r"[a-zàèéìòù]+", testo.lower())


def calcola_punteggio(testo):
    parole = tokenizza(testo)
    totale_parole = len(parole)
    positive = sum(1 for p in parole if p in PAROLE_POSITIVE)
    negative = sum(1 for p in parole if p in PAROLE_NEGATIVE)
    if totale_parole > 0:
        punteggio = (positive - negative) / totale_parole * 1000
    else:
        punteggio = None  # nessuna frase trovata per questo personaggio/capitolo
    return totale_parole, positive, negative, punteggio


def main():
    with open(INPUT, encoding="utf-8") as f:
        capitoli = json.load(f)

    risultati = []
    for capitolo in capitoli:
        frasi_capitolo = dividi_in_frasi(capitolo["testo"])

        for nome_personaggio, varianti in PERSONAGGI.items():
            frasi_trovate = frasi_del_personaggio(frasi_capitolo, varianti)
            testo_personaggio = " ".join(frasi_trovate)
            totale_parole, positive, negative, punteggio = calcola_punteggio(testo_personaggio)

            risultati.append({
                "capitolo": capitolo["numero"],
                "numero_romano": capitolo["numero_romano"],
                "personaggio": nome_personaggio,
                "numero_frasi": len(frasi_trovate),
                "totale_parole": totale_parole,
                "parole_positive": positive,
                "parole_negative": negative,
                "punteggio": punteggio,
            })

            if punteggio is not None:
                print(f"Cap. {capitolo['numero']:2d} - {nome_personaggio:11s}: "
                      f"{len(frasi_trovate):3d} frasi, punteggio {punteggio:+.2f}")

    with open(OUTPUT, "w", encoding="utf-8", newline="") as f:
        campi = ["capitolo", "numero_romano", "personaggio", "numero_frasi",
                  "totale_parole", "parole_positive", "parole_negative", "punteggio"]
        scrittore = csv.DictWriter(f, fieldnames=campi)
        scrittore.writeheader()
        scrittore.writerows(risultati)

    print(f"\nSalvato in {OUTPUT}")


if __name__ == "__main__":
    main()