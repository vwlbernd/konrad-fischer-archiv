#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from pathlib import Path

SIDEBAR_FILE = Path('../sidebar/_sidebar.md')
MKDOCS_FILE = Path('../artikel/SUMMARY.md')

# Matcht:
# * [Titel](pfad.md)
# * [Titel](pfad.md "Tooltip")
# * [Titel]()
LIST_RE = re.compile(
    r'^(\s*)\*\s+\[(.*?)\]\(\s*([^"\s)]*)'
)

COMMENT_RE = re.compile(r'\s*<!--.*?-->')

def convert_sidebar_to_summary():
    lines = SIDEBAR_FILE.read_text(encoding='utf-8').splitlines()
    out = []

    for raw_line in lines:
        # Kommentare entfernen
        line = COMMENT_RE.sub('', raw_line).rstrip()

        m = LIST_RE.match(line)
        if not m:
            continue

        spaces, title, path = m.groups()

        # Alte Struktur: 2 Spaces = 1 Level
        level = len(spaces) // 2

        # Neue Struktur: 4 Spaces pro Level
        indent = ' ' * (level * 4)

        path = path.strip()

        # Leerer Link → nur Titel
        if path:
            out.append(f'{indent}* [{title}]({path})')
        else:
            out.append(f'{indent}* {title}')

    MKDOCS_FILE.write_text('\n'.join(out) + '\n', encoding='utf-8')


if __name__ == '__main__':
    convert_sidebar_to_summary()
