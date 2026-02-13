#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from pathlib import Path

SIDEBAR_FILE = Path('../sidebar/_sidebar.md')
MKDOCS_FILE = Path('../artikel/SUMMARY.md')

LIST_RE = re.compile(r'^(\s*)\*\s+\[(.*?)\]\(([^ )]+)(?:\s+".*?")?\)')
COMMENT_RE = re.compile(r'\s*<!--.*?-->')

def convert_sidebar_to_summary():
    lines = SIDEBAR_FILE.read_text(encoding='utf-8').splitlines()
    out = []

    for line in lines:
        line = COMMENT_RE.sub('', line).rstrip()

        m = LIST_RE.match(line)
        if not m:
            continue

        spaces, title, path = m.groups()

        # alte Struktur: 2 Spaces = 1 Level
        level = len(spaces) // 2
        indent = ' ' * (level * 4)

        out.append(f'{indent}* [{title}]({path})')

    MKDOCS_FILE.write_text('\n'.join(out) + '\n', encoding='utf-8')

if __name__ == '__main__':
    convert_sidebar_to_summary()
