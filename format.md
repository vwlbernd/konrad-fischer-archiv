# Master-Formatierung für das Konrad-Fischer-Archiv

## 1. Mission & Sicherheit
- **Mission:** Wandle unstrukturierte Web-Scrapes in semantisch korrektes, sauberes Markdown um. Bewahre den authentischen Ton des Autors, aber optimiere die Lesbarkeit durch moderne Markdown-Strukturen.
- **Scope:** Bearbeite ausschließlich Dateien im Ordner `/artikel`. Andere Ordner ignorieren.
- **Inhaltsschutz:** Text (Polemik, Großschreibung, Interpunktion) zu 100% erhalten. Keine stilistische Glättung.
- **Technik:** Speichern in UTF-8 ohne BOM.

## 2. Kopf-Struktur & Navigation
- **H1-Fix:** Die erste Zeile muss eine `# H1` sein. Entferne vorangestellte Redundanzen wie "Konrad Fischer".
- **Callout-Navigation:** Transformiere Link-Wüsten am Anfang (zwischen H1 und erstem `* * *`) in:
  > [!abstract] Inhaltsverzeichnis
  > 1. [Titel](dateiname.md)
- **Titel-Extraktion:** Ersetze Dateinamen-Links (z.B. `[2beton.md](2beton.md)`) durch echte Seitentitel aus der `_sidebar.md` oder dem H1 der Zieldatei.

## 3. Hierarchie & Anker
- **Überschriften:** Wandle isolierte Kapitelnummern (`8 Sichtbeton!`) oder fette Themenzeilen (`**B) Objektfehler**`) konsequent in `##` oder `###` um.
- **Anker-Erhalt:** HTML-Anker wie `<a id="anker"></a>` müssen exakt an ihrer Position bleiben. Sie sind für die Sidebar-Verlinkung kritisch.

## 4. Semantisches Layout (Kontext-Regeln)
- **Zitate erkennen:** Texte, die wie Leserbriefe oder Briefe wirken (oft kursiv oder in Anführungszeichen), werden zu Blockquotes (`> `).
- **Bildunterschriften:** Kursiver Text unmittelbar unter `![](...)` bleibt einfacher Text (`_..._`) und wird KEIN Blockquote.
- **HTML-Erhalt:** `<center>` Tags zwingend beibehalten. Rein dekorative Tags (`<b>`, `<i>`) in Markdown (`**`, `_`) wandeln. `<br>` durch einfachen Zeilenumbruch ersetzen.

## 5. Technische Korrektur
- **Hard Line Breaks:** Sätze, die mitten in der Zeile durch das Scraping umgebrochen wurden, zusammenfügen.
- **Bild-Handling:** Bilder brauchen davor und danach genau eine Leerzeile. Falls im `<center>`, bleibt dieser die äußere Hülle.
- **Link-Fix:** Ändere Endungen in Links von `.htm` / `.php` konsequent auf `.md`. Behalte Anker-Links (`.md#anker`) bei.
- **Säuberung:** Entferne Scraper-Relikte wie `Weiter? ===>`, `[weiter ...]`, `(aktualisiert 16.06.08)` restlos.

## 6. Bild-Unterschriften (Line Breaks)
- Um Bild und Caption visuell zu binden erzwinge einen **Soft Line Break**: Setze am Ende der Zeile mit dem Bild-Tag `![](...)` exakt **zwei Leerzeichen**, gefolgt von einem einfachen Zeilenumbruch.
- Die Caption `_..._` folgt direkt in der nächsten Zeile. 
- Beispiel-Syntax (Punkt steht für Leerzeichen): `![Alt-Text](bild.jpg)..` \n `_Unterschrift_`

## 7. Referenz-Beispiele (Vorher/Nachher)

### A: Navigation
**V:** `[1: Start](2bet.md) [2: Schäden](2bet02.md) **8: Sichtbeton!**`
**N:** > [!abstract] Inhaltsverzeichnis
> 1. [Stahlbetonbau - Spitzenarchitektur?](2bet.md)
> 2. [Betonschäden durch schlechte Baustoffqualität](2bet02.md)
> 8. **Sichtbeton!**

### B: Zitate
**V:** `_**"Ohne Kosten"** SZ 99_ Der Autor meint...`
**N:** > **"Ohne Kosten"**
> SZ 99
> 
> Der Autor meint...

### C: Bilder
![Bild](../m/1.jpg)  
_Unterschrift_

### D: Fragestunde
**V:** `Ö.S. schrieb: Text KF: Antwort`
**N:** **Ö.S. schrieb:**
> Text

**KF:** Antwort