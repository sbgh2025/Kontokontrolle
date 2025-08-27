import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

DB_NAME = "konto.db"

def get_regeln():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT id, firma, betrag, kategorie FROM regeln ORDER BY id")
    regeln = cur.fetchall()
    conn.close()
    return regeln

def update_regel(id_, firma, betrag, kategorie):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    if betrag == "":
        betrag_val = None
    else:
        try:
            betrag_val = float(betrag.replace(',', '.'))
        except ValueError:
            messagebox.showerror("Fehler", "Betrag muss eine Zahl sein oder leer bleiben.")
            return False
    cur.execute("""
        UPDATE regeln SET firma = ?, betrag = ?, kategorie = ? WHERE id = ?
    """, (firma, betrag_val, kategorie, id_))
    conn.commit()
    conn.close()
    return True

def delete_regel(id_):
    if messagebox.askyesno("Löschen bestätigen", "Regel wirklich löschen?"):
        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()
        cur.execute("DELETE FROM regeln WHERE id = ?", (id_,))
        conn.commit()
        conn.close()
        return True
    return False

def start_regeln_gui():
    def lade_regeln():
        for item in tree.get_children():
            tree.delete(item)
        for regel in get_regeln():
            id_, firma, betrag, kategorie = regel
            tree.insert("", tk.END, values=(id_, firma, betrag if betrag is not None else "", kategorie))

    def on_auswahl(event):
        selected = tree.focus()
        if not selected:
            return
        values = tree.item(selected, 'values')
        entry_id.config(state='normal')
        entry_id.delete(0, tk.END)
        entry_id.insert(0, values[0])
        entry_id.config(state='readonly')

        entry_firma.delete(0, tk.END)
        entry_firma.insert(0, values[1])

        entry_betrag.delete(0, tk.END)
        entry_betrag.insert(0, values[2])

        entry_kategorie.delete(0, tk.END)
        entry_kategorie.insert(0, values[3])

    def regel_speichern():
        id_ = entry_id.get()
        firma = entry_firma.get().strip()
        betrag = entry_betrag.get().strip()
        kategorie = entry_kategorie.get().strip()

        if not firma:
            messagebox.showerror("Fehler", "Firma darf nicht leer sein.")
            return
        if not kategorie:
            messagebox.showerror("Fehler", "Kategorie darf nicht leer sein.")
            return

        if update_regel(id_, firma, betrag, kategorie):
            messagebox.showinfo("Erfolg", "Regel gespeichert.")
            lade_regeln()

    def regel_loeschen():
        id_ = entry_id.get()
        if not id_:
            messagebox.showerror("Fehler", "Keine Regel ausgewählt.")
            return
        if delete_regel(id_):
            messagebox.showinfo("Erfolg", "Regel gelöscht.")
            lade_regeln()
            # Felder leeren
            entry_id.config(state='normal')
            entry_id.delete(0, tk.END)
            entry_id.config(state='readonly')
            entry_firma.delete(0, tk.END)
            entry_betrag.delete(0, tk.END)
            entry_kategorie.delete(0, tk.END)

    root = tk.Tk()
    root.title("Regeln verwalten")

    tree = ttk.Treeview(root, columns=("ID", "Firma", "Betrag", "Kategorie"), show='headings')
    for col in ("ID", "Firma", "Betrag", "Kategorie"):
        tree.heading(col, text=col)
        tree.column(col, anchor='center')
    tree.bind("<<TreeviewSelect>>", on_auswahl)
    tree.pack(fill=tk.BOTH, expand=True, pady=10)

    frame = tk.Frame(root)
    frame.pack(padx=10, pady=10, fill='x')

    tk.Label(frame, text="ID:").grid(row=0, column=0, sticky='e')
    entry_id = tk.Entry(frame, width=10, state='readonly')
    entry_id.grid(row=0, column=1, sticky='w')

    tk.Label(frame, text="Firma:").grid(row=1, column=0, sticky='e')
    entry_firma = tk.Entry(frame, width=40)
    entry_firma.grid(row=1, column=1, sticky='w')

    tk.Label(frame, text="Betrag (optional):").grid(row=2, column=0, sticky='e')
    entry_betrag = tk.Entry(frame, width=40)
    entry_betrag.grid(row=2, column=1, sticky='w')

    tk.Label(frame, text="Kategorie:").grid(row=3, column=0, sticky='e')
    entry_kategorie = tk.Entry(frame, width=40)
    entry_kategorie.grid(row=3, column=1, sticky='w')

    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=5)

    tk.Button(btn_frame, text="Speichern", command=regel_speichern).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text="Löschen", command=regel_loeschen).pack(side=tk.LEFT, padx=5)

    lade_regeln()

    root.mainloop()

if __name__ == "__main__":
    start_regeln_gui()
