import re
from pathlib import Path

INPUT_FILE = "1suchen.md"
OUTPUT_FILE = "_sidebar.md"

CHAPTER_RE = re.compile(r"^(\d+)\s+(.*)")
LINK_RE = re.compile(r"^\[(.+?)\]\(([^)]+)\)$")
URL_RE = re.compile(r"(https?://\S+|www\.\S+)")

def clean_tooltip(text: str) -> str:
    return (
        text.replace("\\", "\\\\")
            .replace('"', "'")
            .strip()
    )

def generate_sidebar():
    try:
        raw_lines = Path(INPUT_FILE).read_text(encoding="utf-8").splitlines()
    except FileNotFoundError:
        print(f"Fehler: '{INPUT_FILE}' nicht gefunden.")
        return

    # Vorverarbeitung
    lines = [
        l.strip()
        for l in raw_lines
        if l.strip() and l.strip() != "* * *"
    ]

    sidebar = []
    i = 0

    while i < len(lines):
        line = lines[i]

        # Kapitel
        chapter = CHAPTER_RE.match(line)
        if chapter:
            sidebar.append(f"* [{chapter.group(2).strip()}]()")
            i += 1
            continue

        # Link-Zeile
        link = LINK_RE.match(line)
        if not link:
            i += 1
            continue

        text, path = link.groups()
        tooltip = ""
        url_comment = ""

        # Tooltip (optional)
        if i + 1 < len(lines) and not LINK_RE.match(lines[i + 1]):
            tooltip = clean_tooltip(lines[i + 1])

        # URL (optional, aber erwartet)
        if i + 2 < len(lines):
            url_match = URL_RE.search(lines[i + 2])
            if url_match:
                url_comment = f"<!-- {url_match.group(1)} -->"

        sidebar.append(
            f'  * [{text}]({path} "{tooltip}"){(" " + url_comment) if url_comment else ""}'
        )

        i += 3

    Path(OUTPUT_FILE).write_text("\n".join(sidebar), encoding="utf-8")
    print(f"Fertig! → {OUTPUT_FILE}")

if __name__ == "__main__":
    generate_sidebar()
