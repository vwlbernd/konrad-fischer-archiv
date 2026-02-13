#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
SCRIPT 1 – ENCODING & TYPO-HYGIENE
---------------------------------
Regeln:
- Ersetze bekannte UTF-8-Fehlinterpretationen (z.B. WÃ¤ → Wä, Ã¼ → ü).
- Normalisiere Anführungszeichen (,, "" ‘’ → „ “).
- Ersetze typografische Sonderzeichen durch Unicode-Standard.
- Entferne doppelte Leerzeichen innerhalb von Zeilen.
- Reduziere >2 Leerzeilen auf maximal 1 Leerzeile.
- Leerzeichen am Zeilenende bleiben erhalten.
- Entferne eckige Klammern um Links und um **Bold Text**.
- Lösche leere center tags
- Keine inhaltlichen Änderungen.
"""

import re
from pathlib import Path

TARGET_DIR = Path("../artikel")

MOJIBAKE_MAP = {
    "Ã¤": "ä", "Ã¶": "ö", "Ã¼": "ü", "Ã„": "Ä", "Ã–": "Ö", "Ãœ": "Ü", "ÃŸ": "ß",
    "â€“": "–", "â€”": "—", "â€ž": "„", "â€œ": "“", "â€˜": "‘", "â€™": "’",
    "â€¦": "…", "Â ": " ", "Â°": "°",
}

TYPO_MAP = {
    "”": "“", "«": "„", "»": "“", "\u00a0": " ",
}

# NEU: Wandelt [**Text**](Link) in **[Text](Link)** um
BOLD_LINK_MOVE_RE = re.compile(r"\[\*\*([^*]+)\*\*\]\(([^)]+)\)")

# [Titel](file.md) eingeschlossen in [...] -> [Titel](file.md)
BRACKETED_LINK_RE = re.compile(
    r"\[("              
    r"\[[^\]]+\]"       
    r"\([^)]+\)"        
    r")\]"
)

# [**Bold Text**] -> **Bold Text** (für Text ohne Link)
BRACKETED_BOLD_RE = re.compile(r"\[(\*\*[^*]+\*\*)\]")

# NEU: Erkennt <center>...</center> mit nur Whitespace dazwischen
EMPTY_CENTER_RE = re.compile(r"<center>\s*</center>", re.IGNORECASE | re.DOTALL)

def fix_mojibake(text: str) -> str:
    for wrong, right in MOJIBAKE_MAP.items():
        text = text.replace(wrong, right)
    return text

def normalize_typography(text: str) -> str:
    for wrong, right in TYPO_MAP.items():
        text = text.replace(wrong, right)
    return text

def clean_html_fragments(text: str) -> str:
    """Entfernt leere Center-Tags und verwaiste schließende Tags."""
    # 1. Leere Center-Blöcke (inkl. Zeilenumbrüchen dazwischen) entfernen
    text = EMPTY_CENTER_RE.sub("", text)
    return text

def restructure_bold_links(text: str) -> str:
    """
    Verschiebt Fettdruck-Tags von innerhalb der Link-Klammern nach außen.
    Beispiel: [**Text**](URL) -> **[Text](URL)**
    """
    return BOLD_LINK_MOVE_RE.sub(r"**[\1](\2)**", text)

def unwrap_brackets_logic(text: str) -> str:
    # Erst die Bold-Links umstrukturieren
    text = restructure_bold_links(text)
    
    # Dann doppelte Einklammerungen entfernen
    text = BRACKETED_LINK_RE.sub(r"\1", text)
    text = BRACKETED_BOLD_RE.sub(r"\1", text)
    return text

def normalize_whitespace(text: str) -> str:
    text = re.sub(r"^[ \t]+$", "", text, flags=re.MULTILINE)
    text = re.sub(r"[ \t]{2,}", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text

def process_text(text: str) -> str:
    text = fix_mojibake(text)
    text = normalize_typography(text)
    text = unwrap_brackets_logic(text)
    text = clean_html_fragments(text) # Neu aufgerufen
    text = normalize_whitespace(text)
    return text

def main():
    if not TARGET_DIR.exists():
        print(f"Directory not found: {TARGET_DIR}")
        return

    for path in TARGET_DIR.rglob("*.md"):
        try:
            original = path.read_text(encoding="utf-8", errors="replace")
            cleaned = process_text(original)

            if cleaned != original:
                path.write_text(cleaned, encoding="utf-8")
                print(f"✔ cleaned: {path}")
            else:
                print(f"– unchanged: {path}")
        except Exception as e:
            print(f"✘ error processing {path}: {e}")

if __name__ == "__main__":
    main()