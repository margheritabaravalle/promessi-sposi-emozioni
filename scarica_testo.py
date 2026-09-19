# scarica_testo.py
# Scarica il PDF de "I Promessi Sposi" (edizione Liber Liber) da un mirror
# universitario ed estrae il testo completo in un file .txt.

import requests
from pypdf import PdfReader
import io


URL = "https://linux.studenti.polito.it/static_resources/liberliber/biblioteca/m/manzoni/i_promessi_sposi/pdf/i_prom_p.pdf"
OUTPUT = "promessi_sposi_grezzo.txt"


def scarica_pdf(url):
    """Scarica il contenuto binario del PDF dall'URL indicato."""
    risposta = requests.get(url)
    risposta.raise_for_status()
    return risposta.content


def estrai_testo_da_pdf(contenuto_pdf):
    """Estrae il testo da tutte le pagine di un PDF."""
    lettore = PdfReader(io.BytesIO(contenuto_pdf))
    pagine_testo = []
    for numero, pagina in enumerate(lettore.pages, start=1):
        testo_pagina = pagina.extract_text()
        if testo_pagina:
            pagine_testo.append(testo_pagina)
        print(f"Pagina PDF {numero}/{len(lettore.pages)} estratta")
    return "\n\n".join(pagine_testo)


def main():
    print("Scarico il PDF...")
    contenuto_pdf = scarica_pdf(URL)
    print(f"PDF scaricato ({len(contenuto_pdf)} byte). Estraggo il testo...")

    testo = estrai_testo_da_pdf(contenuto_pdf)

    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write(testo)

    print(f"\nTesto salvato in {OUTPUT} ({len(testo)} caratteri totali)")


if __name__ == "__main__":
    main()