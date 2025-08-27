Hier ist ein passendes `README.md` für dein GitHub-Repository – verständlich, sauber strukturiert und direkt einsatzbereit:

---

````markdown
# 💼 Kontoauszüge-Importer mit ODS-Unterstützung & Regelverwaltung

Ein Python-Tool zur Verwaltung von Kontoauszügen im `.ods`-Format, inklusive automatischer Kategorisierung und grafischer Benutzeroberfläche für Regeln zur Klassifizierung.

---

## 🧩 Funktionen

- 📂 **Import von ODS-Dateien** (z. B. aus Online-Banking)
- 🧠 **Automatische Kategorisierung** durch selbst definierbare Regeln (Firma + Betrag)
- 👁️ **Übersichtliche GUI** mit Scrollfunktion zur Anzeige aller Buchungen
- 📝 **Regelverwaltung** mit Bearbeiten & Löschen über eigene GUI
- 🗃️ **SQLite-Datenbank** zur persistenten Speicherung

---

## 🖥️ Screenshots

> *(Optional: Du kannst hier Screenshots einfügen, wenn du möchtest.)*

---

## 📦 Voraussetzungen

### Python-Version
- Python 3.7 oder höher

### Benötigte Pakete

Installiere die Abhängigkeiten mit:

```bash
pip install ezodf odfpy
````

> `tkinter` ist bei den meisten Python-Installationen bereits enthalten.

---

## 🚀 Starten

### 1. GUI zum Importieren von Kontoauszügen:

```bash
python importer.py
```

Hier kannst du:

* `.ods`-Dateien importieren
* Neue Regeln definieren (Firma, optional Betrag, Kategorie)
* Automatisch Buchungen kategorisieren

### 2. GUI zur Regel-Verwaltung:

```bash
python regeln_gui.py
```

Hier kannst du:

* Bestehende Regeln anzeigen
* Regeln bearbeiten oder löschen

---

## 🧠 Wie funktionieren Regeln?

Eine Regel besteht aus:

* **Firma (Pflichtfeld)**
* **Betrag (optional)**
* **Kategorie (Pflichtfeld)**

Beim Import von `.ods`-Dateien wird jede Buchung mit der Firmenbezeichnung abgeglichen. Ist ein Eintrag vorhanden, wird automatisch die passende Kategorie übernommen.

Regeln werden *case-insensitive* und als *Teilstring* verglichen.

---

## 🗃️ Datenbankstruktur (`konto.db`)

### Tabelle `buchungen`

| Spalte    | Typ  | Beschreibung             |
| --------- | ---- | ------------------------ |
| id        | int  | Auto-Inkrement           |
| datum     | text | Datum der Buchung        |
| betrag    | real | Betrag (negativ/positiv) |
| firma     | text | Bezeichnung              |
| kategorie | text | Automatisch zugeordnet   |

### Tabelle `regeln`

| Spalte    | Typ  | Beschreibung               |
| --------- | ---- | -------------------------- |
| id        | int  | Auto-Inkrement             |
| firma     | text | Firmenname oder Teil davon |
| betrag    | real | Optional, exakte Beträge   |
| kategorie | text | Zielkategorie              |

---

## 🔒 Datenschutz-Hinweis

Alle Daten bleiben lokal auf deinem System gespeichert. Es gibt **keine externe Übertragung oder Cloud-Anbindung**.

---

## 📜 Lizenz

Dieses Projekt steht unter der MIT-Lizenz. Siehe `LICENSE` für Details.

---

## 💡 Ideen für Erweiterungen

* CSV-Import
* Export als Excel oder PDF
* Mehrstufige Kategorisierung
* Analysefunktionen (Summen, Filter)

---

## 🙌 Mitwirken

Pull Requests, Verbesserungsvorschläge oder Fehlerberichte sind willkommen!

---

```

---

### ✅ Tipps für GitHub:

1. Speichere diesen Inhalt als `README.md` im Wurzelverzeichnis deines Repos.
2. Erstelle ggf. zwei Dateien:
   - `importer.py` für den ODS-Importer
   - `regeln_gui.py` für die Regelverwaltung
3. Optional: Screenshots im Projektordner ablegen und im README verlinken.

Wenn du willst, kann ich dir auch ein passendes `LICENSE`-Template oder `.gitignore` dazuschreiben. Sag einfach Bescheid.
```

