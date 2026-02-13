#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
SCRIPT – KONSERVATIVE MARKDOWN-NORMALISIERUNG
Regeln:
Properties hinzufügen:
---
title: "Titel aus der Sidebar"
description: "Zusammenfassung aus der Sidebar"
author: "Konrad Fischer"
original_url: "Link zum Original"
---
"""

import re
from pathlib import Path

# =========================
# KONFIGURATION
# =========================
TARGET_DIR = Path("../artikel")
SIDEBAR_FILE = Path("../sidebar/_sidebar.md")
DEFAULT_AUTHOR = " "

# =========================
# SIDEBAR PARSEN
# =========================

SIDEBAR_REGEX = re.compile(
    r'\[(?P<linktext>[^\]]+)\]\('
    r'(?P<file>[^)\s]+\.md)\s+"(?P<tooltip>[^"]+)"\)'
    r'\s*<!--\s*(?P<url>[^>]+)\s*-->'
)

def parse_sidebar():
    metadata = {}

    if not SIDEBAR_FILE.exists():
        raise FileNotFoundError(f"Sidebar nicht gefunden: {SIDEBAR_FILE}")

    content = SIDEBAR_FILE.read_text(encoding="utf-8")

    for match in SIDEBAR_REGEX.finditer(content):
        filename = match.group("file").strip()
        tooltip = match.group("tooltip").strip()
        url = match.group("url").strip()

        if "|" in tooltip:
            title, description = tooltip.split("|", 1)
        else:
            title = tooltip
            description = ""

        metadata[filename] = {
            "title": title.strip(),
            "description": description.strip(),
            "url": url
        }

    return metadata


# =========================
# FRONTMATTER ERZEUGEN
# =========================

def yaml_escape(value: str) -> str:
    return value.replace('"', '\\"')


def build_frontmatter(meta: dict) -> str:
    return (
        "---\n"
        f'title: "{yaml_escape(meta["title"])}"\n'
        f'description: "{yaml_escape(meta["description"])}"\n'
        f'author: "{DEFAULT_AUTHOR}"\n'
        f'original_url: "{yaml_escape(meta["url"])}"\n'
        "---\n\n"
    )


def remove_existing_frontmatter(text: str) -> str:
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            return parts[2].lstrip()
    return text


# =========================
# MAIN
# =========================

def main():
    if not TARGET_DIR.exists():
        raise FileNotFoundError(f"Verzeichnis existiert nicht: {TARGET_DIR}")

    sidebar_data = parse_sidebar()

    if not sidebar_data:
        raise RuntimeError("Keine Metadaten in Sidebar gefunden.")

    files = list(TARGET_DIR.rglob("*.md"))
    changed = 0

    for path in files:
        if path.name not in sidebar_data:
            continue

        meta = sidebar_data[path.name]
        original = path.read_text(encoding="utf-8")

        body = remove_existing_frontmatter(original)
        frontmatter = build_frontmatter(meta)
        new_content = frontmatter + body.lstrip()

        if new_content != original:
            path.write_text(new_content, encoding="utf-8")
            print(f"✔ aktualisiert: {path.name}")
            changed += 1

    print(f"\nFertig. {changed} Dateien geändert.")


if __name__ == "__main__":
    main()
