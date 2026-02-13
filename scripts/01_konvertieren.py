import os
import html2text
from bs4 import BeautifulSoup
import re

source_dir = '../orginal'
target_dir = '../artikel'

if not os.path.exists(target_dir):
    os.makedirs(target_dir)

h = html2text.HTML2Text()
h.ignore_tables = True
h.ignore_emphasis = False
h.body_width = 0

for filename in os.listdir(source_dir):
    if filename.endswith(('.htm', '.html')):
        path = os.path.join(source_dir, filename)
        try:
            with open(path, 'r', encoding='iso-8859-1', errors='replace') as f:
                html_content = f.read()
            
            soup = BeautifulSoup(html_content, 'html.parser')        
            
            # --- PHASE 1: MARKIEREN (OHNE DEN INHALT ZU ISOLIEREN) ---

            # 1. <font> markieren
            for font in soup.find_all('font'):
                # Farbe extrahieren (falls vorhanden)
                color = font.get('color', '').lower()
                
                # Nur bei "red" oder dem Hex-Code für Rot reagieren
                if color == 'red' or color == '#ff0000':
                    # Wir erstellen ein neues <b> Tag
                    new_bold = soup.new_tag('b')
                    
                    # Inhalt des font-Tags sicher in das b-Tag schieben
                    # .decode_contents() bewahrt enthaltene Links/Tags
                    new_bold.append(BeautifulSoup(font.decode_contents(), 'html.parser'))
                    
                    # Das font-Tag durch das fettgedruckte Tag ersetzen
                    font.replace_with(new_bold)
                else:
                    # Alle anderen Font-Tags (andere Farben oder nur size)
                    # werden einfach aufgelöst, der Text bleibt erhalten.
                    font.unwrap()

            # 2. <a name="id"> zu [[[#id]]]
            for a in soup.find_all('a', attrs={'name': True}):
                anchor_id = a['name'].lower() #.replace(' ', '-')
                # Wir ersetzen das GANZE <a> Tag durch den Platzhalter
                a.replace_with(f"[[[#{anchor_id}]]]")

            # 3. Zentrierung markieren (ohne Dopplung)
            center_elements = soup.find_all(lambda tag: tag.name == 'center')
            for elem in center_elements:
                # Prüfen, ob das Element bereits in einem zentrierten Element liegt
                if any(parent.name == 'center' for parent in elem.parents):
                    continue
                elem.insert_before("[[[C_S]]]")
                elem.insert_after("[[[C_E]]]")
                # Wir lassen das Tag hier noch stehen, html2text löscht es später sowieso

            # Interne Links umstellen (bevor html2text läuft)
            for a in soup.find_all('a', href=True):
                if not a['href'].startswith(('http', 'ftp', 'mailto', '#')):
                    new_href = re.sub(r'\.html?(?=#|$)', r'.md', a['href'])
                    if '#' in new_href:
                        base, anchor = new_href.split('#', 1)
                        # base bleibt wie sie ist (oder auch .lower() falls gewünscht)
                        # anchor wird konsequent kleingeschrieben
                        new_href = f"{base}#{anchor.lower()}"

                    #new_href = new_href.replace(' ', '-')
                    a['href'] = new_href

            # --- PHASE 2: KONVERTIERUNG (html2text wandelt jetzt ALLES um) ---
            markdown_text = h.handle(str(soup))
            
            # --- PHASE 3: REINIGUNG & WIEDERHERSTELLUNG ---

            # IDs setzen
            markdown_text = re.sub(r'\[\[\[#(.*?)\]\]\]', r'<a id="\1"></a>', markdown_text)

            # Zentrierung zu <center>
            markdown_text = markdown_text.replace("[[[C_S]]]", "\n\n<center>\n\n")
            markdown_text = markdown_text.replace("[[[C_E]]]", "\n\n</center>\n\n")

            # Maskierungen entfernen
            markdown_text = markdown_text.replace('\\<', '<').replace('\\>', '>')
            markdown_text = markdown_text.replace('\\{', '{').replace('\\}', '}')
            # Manchmal maskiert html2text auch Unterstriche in IDs:
            markdown_text = markdown_text.replace('\\_', '_')

            # Speichern
            target_name = os.path.splitext(filename)[0] + '.md'
            with open(os.path.join(target_dir, target_name), 'w', encoding='utf-8') as f:
                f.write(markdown_text)
                
            print(f"Erfolg: {filename}")
        except Exception as e:
            print(f"Fehler bei {filename}: {e}")

print("\nFertig!")