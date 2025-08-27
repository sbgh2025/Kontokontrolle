import sqlite3
import ezodf
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

DB_NAME = "konto.db"

# Datenbank vorbereiten
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS buchungen (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            datum TEXT,
            betrag REAL,
            firma TEXT,
            kategorie TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS regeln (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            firma TEXT,
            betrag REAL,
            kategorie TEXT
        )
    """)
    conn.commit()
    conn.close()

# ODS importieren (Kategorie anhand Firmenname, ohne Betragsfilter)
def import_ods(file_path):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    ezodf.config.set_table_expand_strategy('all')
    doc = ezodf.opendoc(file_path)
    sheet = doc.sheets[0]

    headers = [cell.value for cell in sheet.row(0)]
    try:
        idx_datum = headers.index("Valutadatum")
        idx_firma = headers.index("Beguenstigter/Zahlungspflichtiger")
        idx_betrag = headers.index("Betrag")
    except ValueError as e:
        messagebox.showerror("Fehler", f"Spalten nicht gefunden: {e}")
        return

    rows = list(sheet.rows())
    for row in rows[1:]:
        datum = str(row[idx_datum].value).strip()
        firma = str(row[idx_firma].value).strip()
        betrag_str = str(row[idx_betrag].value).replace(',', '.').strip()

        if not datum or not betrag_str:
            continue

        try:
            betrag = float(betrag_str)
        except ValueError:
            continue

        # Kategorie nur über Firmenname finden (case-insensitive, Teilstring)
        cur.execute("""
            SELECT kategorie FROM regeln
            WHERE LOWER(?) LIKE '%' || LOWER(firma) || '%'
            ORDER BY LENGTH(firma) DESC
            LIMIT 1
        """, (firma.lower(),))
        match = cur.fetchone()
        kategorie = match[0] if match else ""

        cur.execute("INSERT INTO buchungen (datum, betrag, firma, kategorie) VALUES (?, ?, ?, ?)",
                    (datum, betrag, firma, kategorie))

    conn.commit()
    conn.close()
    messagebox.showinfo("Import", "ODS erfolgreich importiert.")

# Regel hinzufügen
def neue_regel(firma, betrag, kategorie):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("INSERT INTO regeln (firma, betrag, kategorie) VALUES (?, ?, ?)", (firma, betrag, kategorie))
    conn.commit()
    conn.close()

# GUI starten
def start_gui():
    def lade_buchungen():
        for row in tree.get_children():
            tree.delete(row)
        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()
        for row in cur.execute("SELECT datum, betrag, firma, kategorie FROM buchungen ORDER BY datum DESC"):
            tree.insert("", tk.END, values=row)
        conn.close()

    def ods_auswaehlen():
        file_path = filedialog.askopenfilename(filetypes=[("ODS Dateien", "*.ods")])
        if file_path:
            import_ods(file_path)
            lade_buchungen()

    def regel_hinzufuegen():
        firma = entry_firma.get().strip()
        betrag_text = entry_betrag.get().strip()

        if betrag_text == "":
            betrag = None
        else:
            try:
                betrag = float(betrag_text.replace(',', '.'))
            except ValueError:
                messagebox.showerror("Fehler", "Bitte einen gültigen Betrag eingeben oder das Feld leer lassen.")
                return

        kategorie = entry_kategorie.get().strip()

        if not firma:
            messagebox.showerror("Fehler", "Firma darf nicht leer sein.")
            return
        if not kategorie:
            messagebox.showerror("Fehler", "Kategorie darf nicht leer sein.")
            return

        neue_regel(firma, betrag, kategorie)
        messagebox.showinfo("Regel", "Neue Regel gespeichert.")
        entry_firma.delete(0, tk.END)
        entry_betrag.delete(0, tk.END)
        entry_kategorie.delete(0, tk.END)

    root = tk.Tk()
    root.title("Kontoauszüge Importer")

    frame_top = tk.Frame(root)
    frame_top.pack(pady=10)
    tk.Button(frame_top, text="ODS importieren", command=ods_auswaehlen).pack()

   
    # Frame für Scrollbar und Treeview
    frame_table = tk.Frame(root)
    frame_table.pack(fill=tk.BOTH, expand=True, pady=10)

    # Vertikaler Scrollbar – LINKS
    scrollbar = tk.Scrollbar(frame_table, orient=tk.VERTICAL)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Treeview
    tree = ttk.Treeview(frame_table, columns=("Datum", "Betrag", "Firma", "Kategorie"),
                        show='headings', yscrollcommand=scrollbar.set)
    for col in ("Datum", "Betrag", "Firma", "Kategorie"):
        tree.heading(col, text=col)
        tree.column(col, anchor='center')
    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Scrollbar mit Treeview verbinden
    scrollbar.config(command=tree.yview)

    frame_regel = tk.LabelFrame(root, text="Neue Regel hinzufügen")
    frame_regel.pack(padx=10, pady=10, fill="x")

    tk.Label(frame_regel, text="Firma:").grid(row=0, column=0, sticky="e")
    entry_firma = tk.Entry(frame_regel, width=30)
    entry_firma.grid(row=0, column=1)

    tk.Label(frame_regel, text="Betrag (optional):").grid(row=1, column=0, sticky="e")
    entry_betrag = tk.Entry(frame_regel, width=30)
    entry_betrag.grid(row=1, column=1)

    tk.Label(frame_regel, text="Kategorie:").grid(row=2, column=0, sticky="e")
    entry_kategorie = tk.Entry(frame_regel, width=30)
    entry_kategorie.grid(row=2, column=1)

    tk.Button(frame_regel, text="Speichern", command=regel_hinzufuegen).grid(row=3, column=0, columnspan=2, pady=5)

    lade_buchungen()

    root.mainloop()

if __name__ == "__main__":
    init_db()
    start_gui()
