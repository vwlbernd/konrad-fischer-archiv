#!/usr/bin/env python3
import json
import re
from pathlib import Path

ARTIKEL_DIR = Path("../artikel")
OUTPUT_FILE = Path("../docsify/search-index.json")

# --- Hilfsfunktionen ---------------------------------------------------------

def extract_title(text: str) -> str:
    """Nimmt die erste Markdown-Überschrift (# ...)"""
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("#"):
            return line.lstrip("#").strip()
    return ""

def extract_first_bold(text: str) -> str:
    """Nimmt den ersten fettgedruckten Text (**...** oder __...__)"""
    match = re.search(r"\*\*(.+?)\*\*|__(.+?)__", text)
    if match:
        return match.group(1) or match.group(2)
    return ""

def extract_relevant_content(text: str) -> str:
    """
    Extrahiert nur Markdown-Überschriften und fettgedruckten Text (**...** oder __...__)
    """
    lines = []
    for line in text.splitlines():
        line = line.strip()
        # Überschriften
        if line.startswith("#"):
            lines.append(line.lstrip("#").strip())
        # Bold-Text
        bold_matches = re.findall(r"\*\*(.+?)\*\*|__(.+?)__", line)
        for m in bold_matches:
            lines.append(m[0] or m[1])
    # Alles zusammenführen
    content = " ".join(lines)
    content = re.sub(r"\s+", " ", content)  # mehrfaches Leerzeichen entfernen
    return content.strip()

# --- Index bauen -------------------------------------------------------------

index = {}

for md_file in ARTIKEL_DIR.rglob("*.md"):
    raw = md_file.read_text(encoding="utf-8", errors="ignore")

    title = extract_title(raw)
    if not title:
        # Falls keine Überschrift existiert, ersten Bold-Text als Titel nehmen
        title = extract_first_bold(raw) or "Ohne Titel"

    content = extract_relevant_content(raw)

    path = md_file.stem  # nur Dateiname ohne Pfad und .md

    index[path] = {
        "title": title,
        "content": content,
        "path": path
    }

# --- Schreiben ---------------------------------------------------------------

with OUTPUT_FILE.open("w", encoding="utf-8") as f:
    json.dump(index, f, ensure_ascii=False, separators=(",", ":"))

print(f"✓ {len(index)} Dateien indexiert → {OUTPUT_FILE}")
