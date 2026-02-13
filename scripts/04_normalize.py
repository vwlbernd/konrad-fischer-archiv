#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
SCRIPT – KONSERVATIVE MARKDOWN-NORMALISIERUNG

Regeln:
1. Normalisiere Escape-Sequenzen (\- → -, \. → .).
2. <center> zu <center markdown> (verhindert Duplikate).
3. * * * zu --- (Horizontale Linie vereinheitlichen) vor und nach --- eine Leerzeile.
4. --- Trennlinien am Anfang und am Ende der Seite entfernen.
5. Bei Zeilen mit genau einem Leerzeichen am Ende, zwei Leerzeichen am Ende erzwingen.
"""

import re
from pathlib import Path

# =========================
# KONFIGURATION
# =========================
TARGET_DIR = Path("../artikel")

# =========================
# FUNKTIONEN
# =========================

def normalize_escapes(text: str) -> str:
    """Entfernt Backslash-Escapes vor Bindestrichen und Punkten."""
    text = text.replace(r"\-", "-")
    text = text.replace(r"\.", ".")
    return text

def normalize_center_tags(text: str) -> str:
    """Konvertiert <center> zu <center markdown> für MkDocs."""
    return re.sub(r"<center(?![^>]*\smarkdown)>", r"<center markdown>", text)

def normalize_horizontal_rules(text: str) -> str:
    """
    1. Wandelt * * * in --- um.
    2. Stellt sicher, dass vor und nach --- genau eine Leerzeile ist.
    """
    # Schritt A: Alle Varianten von Trennlinien (* * *, ---, ___) vereinheitlichen
    text = re.sub(r"^\s*([\*\-_]\s*){3,}\s*$", "---", text, flags=re.MULTILINE)

    # Schritt B: Leerzeilen-Management um --- herum
    text = re.sub(r"\n\s*\n\s*---\s*\n\s*\n", r"\n\n---\n\n", text)
    text = re.sub(r"([^\n])\n---\n([^\n])", r"\1\n\n---\n\n\2", text)
    text = re.sub(r"([^\n])\n---", r"\1\n\n---", text)
    text = re.sub(r"---\n([^\n])", r"---\n\n\1", text)

    return text

def strip_edge_horizontal_rules(text: str) -> str:
    """Entfernt Trennlinien am Anfang und Ende des Dokuments."""
    # Entfernt Trenner am Anfang (inkl. optionaler Leerzeilen danach)
    text = re.sub(r"^---\s*\n+", "", text)
    # Entfernt Trenner am Ende (inkl. optionaler Leerzeilen davor)
    text = re.sub(r"\n+---\s*$", "", text)
    return text

def ensure_double_space_line_break(text: str) -> str:
    """
    Sucht Zeilen, die auf genau ein Leerzeichen enden und fügt ein zweites hinzu.
    """
    return re.sub(r"(?<! )[ ]$", "  ", text, flags=re.MULTILINE)

def process_text(text: str) -> str:
    """Wendet die definierten Regeln nacheinander an."""
    # Erst normalisieren
    text = normalize_escapes(text)
    text = normalize_center_tags(text)
    text = normalize_horizontal_rules(text)
    
    # Dann die Ränder säubern (nachdem die Trenner vereinheitlicht wurden)
    text = strip_edge_horizontal_rules(text)
    
    # Restliche Formatierung
    text = ensure_double_space_line_break(text)
    
    # Finaler Cleanup: Mehr als zwei aufeinanderfolgende Leerzeilen verhindern
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip() + "\n"

# =========================
# MAIN (unverändert)
# =========================
def main():
    if not TARGET_DIR.exists():
        print(f"Error: Verzeichnis nicht gefunden: {TARGET_DIR.absolute()}")
        return

    files = list(TARGET_DIR.rglob("*.md"))
    changed_count = 0

    if not files:
        print("Keine .md Dateien gefunden.")
        return

    for path in files:
        try:
            original = path.read_text(encoding="utf-8", errors="replace")
            cleaned = process_text(original)

            if cleaned != original:
                path.write_text(cleaned, encoding="utf-8")
                print(f"✔ normalisiert: {path.name}")
                changed_count += 1
        except Exception as e:
            print(f"✘ Fehler bei {path.name}: {e}")

    print(f"\nFertig. {changed_count} von {len(files)} Dateien aktualisiert.")

if __name__ == "__main__":
    main()