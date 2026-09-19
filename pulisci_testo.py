# pulisci_testo.py
# Legge il testo grezzo estratto dal PDF e produce una versione pulita:
# rimuove il materiale editoriale iniziale di Liber Liber e le righe che
# contengono solo un numero di pagina residuo dall'estrazione del PDF.

import re


INPUT = "promessi_sposi_grezzo.txt"
OUTPUT = "promessi_sposi_pulito.txt"


def rimuovi_intestazione_editoriale(testo):
    """Taglia via tutto ciò che precede l'inizio vero del romanzo."""
    indice_inizio = testo.find("INTRODUZIONE")
    if indice_inizio == -1:
        # Se non troviamo "INTRODUZIONE", non tagliamo nulla e segnaliamo.
        print("Attenzione: non ho trovato 'INTRODUZIONE', nessun taglio effettuato.")
        return testo
    return testo[indice_inizio:]


def rimuovi_numeri_di_pagina(testo):
    """Rimuove le righe composte solo da un numero (numeri di pagina residui)."""
    righe = testo.split("\n")
    righe_pulite = [riga for riga in righe if not re.fullmatch(r"\s*\d+\s*", riga)]
    return "\n".join(righe_pulite)


def main():
    with open(INPUT, encoding="utf-8") as f:
        testo_grezzo = f.read()

    testo = rimuovi_intestazione_editoriale(testo_grezzo)
    numero_righe_prima = len(testo.split("\n"))
    testo = rimuovi_numeri_di_pagina(testo)
    numero_righe_dopo = len(testo.split("\n"))

    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write(testo)

    rimosse = numero_righe_prima - numero_righe_dopo
    print(f"Rimosse {rimosse} righe con soli numeri di pagina.")
    print(f"Testo pulito salvato in {OUTPUT} ({len(testo)} caratteri totali)")


if __name__ == "__main__":
    main()