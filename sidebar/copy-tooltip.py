#!/usr/bin/env python3
import re
from pathlib import Path

SRC = Path("sidebar-save.md")
DST = Path("_sidebar.md")

def escape_quotes(s):
    """Escaped doppelte Anführungszeichen für Markdown-Tooltips"""
    return s.replace('"', '&quot;') if s else s

link_re = re.compile(
    r'''
    ^(?P<indent>\s*\*\s*)
    \[(?P<label>[^\]]+)\]
    \((?P<target>[^)\s]+)
    (?:\s+"(?P<title>[^"]*)")?
    \)
    (?:\s*(?P<comment><!--.*?-->))?
    ''',
    re.VERBOSE
)

def parse_sidebar(path):
    data = {}
    if not path.exists():
        return data

    for line in path.read_text(encoding="utf-8").splitlines():
        m = link_re.search(line)
        if not m:
            continue

        target = m.group("target")
        data[target] = {
            "label": m.group("label"),
            "title": m.group("title"),
            "comment": m.group("comment"),
        }

    return data

src_data = parse_sidebar(SRC)

out_lines = []

for line in DST.read_text(encoding="utf-8").splitlines():
    m = link_re.search(line)
    if not m:
        out_lines.append(line)
        continue

    target = m.group("target")
    if target not in src_data:
        out_lines.append(line)
        continue

    src_label = src_data[target]["label"]
    src_title = src_data[target]["title"]
    src_comment = src_data[target]["comment"]

    # Tooltip aus Quelle zusammensetzen
    combined_tooltip = escape_quotes(src_label)
    if src_title:
        combined_tooltip += " | " + escape_quotes(src_title)

    new_line = line

    # Tooltip ersetzen oder einfügen
    if m.group("title"):
        # bestehenden Tooltip ersetzen
        new_line = re.sub(
            r'"[^"]*"',
            f'"{combined_tooltip}"',
            new_line,
            count=1
        )
    else:
        # Tooltip ergänzen
        new_line = re.sub(
            rf'\({re.escape(target)}\)',
            f'({target} "{combined_tooltip}")',
            new_line,
            count=1
        )

    # HTML-Kommentar ergänzen, falls vorhanden und im Ziel fehlt
    if src_comment and not m.group("comment"):
        new_line = new_line.rstrip() + " " + src_comment

    out_lines.append(new_line)

DST.write_text("\n".join(out_lines) + "\n", encoding="utf-8")
