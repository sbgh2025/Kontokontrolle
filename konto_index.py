import tkinter as tk
from tkinter import messagebox
import subprocess
import os

# Basisverzeichnis (LebenslaufTest/src)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

def make_path(relative_path):
    return os.path.join(BASE_DIR, relative_path)

def run_script(script_path):
    try:
        subprocess.run(["python3", script_path], check=True)
    except subprocess.CalledProcessError:
        messagebox.showerror("Fehler", f"Skript konnte nicht ausgeführt werden:\n{script_path}")
    except FileNotFoundError:
        messagebox.showerror("Fehler", f"Skript wurde nicht gefunden:\n{script_path}")

class IndexApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Kontokontrolle")
        self.geometry("750x250")
        self.configure(padx=20, pady=20)

        tk.Label(self, text="Bitte wählen Sie eine Kategorie:", font=("Arial", 16, "bold")).pack(pady=10)

        self.sections = {}

        self.create_main_button("📊 Kontokontrolle", [
            ("Datenbank, Regeln erstellen, Datenbankbefüllung", make_path("Kontoorganisation/konto.py")),
            ("Regeln verwalten", make_path("Kontoorganisation/konto_regeln.py")),
        ])


    def create_main_button(self, title, buttons):
        main_button = tk.Button(
            self,
            text=title,
            font=("Arial", 13, "bold"),
            bg="lightgray",
            relief=tk.RAISED,
            command=lambda: self.toggle_section(title)
        )
        main_button.pack(fill=tk.X, pady=5)

        section_frame = tk.Frame(self)
        self.sections[title] = section_frame

        for label, path in buttons:
            tk.Button(
                section_frame,
                text=label,
                command=lambda p=path: run_script(p),
                bg="lightblue",
                font=("Arial", 11),
                anchor="w"
            ).pack(fill=tk.X, pady=2, padx=10)

    def toggle_section(self, title):
        frame = self.sections[title]
        if frame.winfo_ismapped():
            frame.pack_forget()
        else:
            for other_frame in self.sections.values():
                other_frame.pack_forget()
            frame.pack(fill=tk.X, padx=10, pady=5)

if __name__ == "__main__":
    app = IndexApp()
    app.mainloop()