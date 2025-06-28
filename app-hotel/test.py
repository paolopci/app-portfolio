import os
from datetime import datetime

import pandas as pd
from fpdf import FPDF

# ---------------------------------------------
# CONFIGURAZIONE
# ---------------------------------------------
CATALOG_FILE = "articles.csv"  # Percorso del catalogo articoli


# ---------------------------------------------
# Utility interne
# ---------------------------------------------

def _load_catalog() -> pd.DataFrame:
    """Carica il catalogo articoli da disco."""
    return pd.read_csv(CATALOG_FILE, dtype={"id": str})


def _save_catalog(df: pd.DataFrame) -> None:
    """Salva il catalogo articoli su disco."""
    df.to_csv(CATALOG_FILE, index=False)


# ---------------------------------------------
# Classe Fattura
# ---------------------------------------------
class Fattura:
    """Rappresenta una fattura e si occupa della creazione del relativo PDF."""

    def __init__(self, article_id: str, name: str, quantity: int, price_each: float):
        self.article_id = article_id
        self.name = name
        self.quantity = quantity
        self.price_each = price_each
        self.total = quantity * price_each
        self.timestamp = datetime.now()

    # -------------------------------------------------
    # Generazione materiale della fattura in formato PDF
    # -------------------------------------------------
    def CreaFattura(self, output_dir: str = ".") -> str:
        """Crea il PDF della fattura restituendo il percorso del file generato.

        Il file viene salvato con il formato
            "Fattura-YYYY-MM-dd-hh-mm-ss.pdf"
        all'interno della cartella indicata da *output_dir*.
        """
        formatted = self.timestamp.strftime("%Y-%m-%d-%H-%M-%S")
        filename = f"Fattura-{formatted}.pdf"
        filepath = os.path.join(output_dir, filename)

        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()

        # Titolo
        pdf.set_font("Helvetica", "B", 16)
        pdf.cell(0, 10, "FATTURA", ln=True, align="C")
        pdf.ln(5)

        # Metadati
        pdf.set_font("Helvetica", "", 12)
        pdf.cell(
            0, 10, f"Data: {self.timestamp.strftime('%d/%m/%Y %H:%M:%S')}", ln=True)
        pdf.cell(0, 10, f"Articolo ID: {self.article_id}", ln=True)
        pdf.cell(0, 10, f"Nome articolo: {self.name}", ln=True)
        pdf.cell(0, 10, f"Quantità: {self.quantity}", ln=True)
        pdf.cell(0, 10, f"Prezzo unitario: EUR {self.price_each:.2f}", ln=True)
        pdf.cell(0, 10, f"Totale: EUR {self.total:.2f}", ln=True)
        pdf.ln(10)

        pdf.output(filepath)
        return filepath


# ---------------------------------------------
# Classe Article (estesa con fatturazione)
# ---------------------------------------------
class Article:
    """Articolo di catalogo con gestione acquisti e fatturazione."""

    def __init__(self, article_id: str):
        self.article_id = article_id.strip()
        self.df = _load_catalog()

    # Helper privato: recupera la riga del catalogo
    def _get_row(self):
        return self.df.loc[self.df["id"] == self.article_id]

    # -----------------------------
    # Verifica disponibilità
    # -----------------------------
    def check_availability(self) -> bool:
        """Stampa <id>, <name>, <in stock> se disponibile e ritorna True."""
        row = self._get_row()
        if row.empty:
            print(f"L'articolo con id '{self.article_id}' non esiste.")
            return False

        name = row["name"].iloc[0] if "name" in self.df.columns else ""
        in_stock = int(row["in stock"].iloc[0])

        if in_stock > 0:
            print(f"{self.article_id}, {name}, {in_stock}")
            return True

        print(f"L'articolo '{self.article_id}' è esaurito.")
        return False

    # -----------------------------
    # Acquisto + emissione fattura
    # -----------------------------
    def purchase(self, quantity: int = 1):
        """Gestisce l'acquisto, aggiorna il magazzino e genera la fattura."""
        # 0. Ottieni quantità da input se non valida
        if quantity is None or quantity <= 0:
            try:
                quantity = int(input("Quanti pezzi vuoi acquistare? ").strip())
            except ValueError:
                print("Quantità non valida.")
                return

        # 1. Recupera info articolo
        row = self._get_row()
        if row.empty:
            print(f"L'articolo con id '{self.article_id}' non esiste.")
            return

        name = row["name"].iloc[0] if "name" in self.df.columns else ""
        in_stock = int(row["in stock"].iloc[0])

        # 2. Verifica disponibilità
        if quantity > in_stock:
            print("Quantità non disponibile in magazzino")
            return

        # 3. Calcola totale
        price = float(row["price"].iloc[0]
                      ) if "price" in self.df.columns else 0.0
        totale = quantity * price

        # 4. Riepilogo
        print(f"{self.article_id}, {name}, {quantity}, {totale:.2f}")

        # 5. Aggiorna magazzino e salva
        self.df.loc[self.df["id"] == self.article_id,
                    "in stock"] = in_stock - quantity
        _save_catalog(self.df)

        # 6. Genera fattura
        fattura = Fattura(self.article_id, name, quantity, price)
        filepath = fattura.CreaFattura()
        print(f"Fattura generata: {filepath}")
        print("Acquisto completato.")


# ---------------------------------------------
# Test manuale
# ---------------------------------------------
if __name__ == "__main__":
    print("=== Catalogo attuale ===")
    print(_load_catalog())

    user_input = input("Inserisci l'id dell'articolo: ").strip()
    article = Article(user_input)

    if article.check_availability():
        try:
            qty = int(input("Quanti pezzi vuoi acquistare? ").strip())
        except ValueError:
            print("Quantità non valida.")
        else:
            article.purchase(qty)
    else:
        print("Acquisto non possibile.")
