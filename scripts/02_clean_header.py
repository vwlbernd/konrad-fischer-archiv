import os
import re

TARGET_FOLDER = '../artikel'
# Regex für das Bild
MARKER_PATTERN = (
    r'!\[[^\]]*\]\('
    r'\s*\.\./medien/B00000\.(?:jpg|jpeg|png|JPG|JPEG|PNG)'
    r'(?:\s+"[^"]*")?\s*\)'
)

def clean_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()

        # Alle Vorkommen des Bildes finden
        matches = list(re.finditer(MARKER_PATTERN, content))
        
        if not matches:
            return False

        # --- ANFANGS-INDEX BESTIMMEN ---
        # Suche nach dem Ende des ERSTEN Bildes
        first_img_end = matches[0].end()
        # Suche ab dort das nächste </center>
        center_close_match = re.search(r'</center>', content[first_img_end:], re.IGNORECASE)
        
        if center_close_match:
            # Startpunkt ist nach dem </center>
            start_index = first_img_end + center_close_match.end()
        else:
            # Falls kein </center> gefunden wurde, nimm das Bild-Ende
            start_index = first_img_end

        # --- END-INDEX BESTIMMEN ---
        if len(matches) > 1:
            # Suche den Bereich VOR dem LETZTEN Bild
            last_img_start = matches[-1].start()
            # Suche rückwärts ab dem letzten Bild nach dem nächsten <center>
            # Wir nehmen rfind im Substring vor dem Bild
            center_open_index = content[:last_img_start].lower().rfind('<center>')
            
            if center_open_index != -1:
                # Endpunkt ist direkt vor dem <center>
                end_index = center_open_index
            else:
                # Falls kein <center> gefunden wurde, nimm den Bild-Anfang
                end_index = last_img_start
            
            output = content[start_index:end_index].strip()
        else:
            # Wenn es nur ein Bild gibt, nimm alles bis zum Dateiende
            output = content[start_index:].strip()
            
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(output)
        return True
            
    except Exception as e:
        print(f"Fehler bei {filepath}: {e}")
        return False

if __name__ == "__main__":
    if not os.path.exists(TARGET_FOLDER):
        print(f"Ordner '{TARGET_FOLDER}' nicht gefunden.")
    else:
        count = 0
        for filename in os.listdir(TARGET_FOLDER):
            if filename.endswith('.md'):
                if clean_file(os.path.join(TARGET_FOLDER, filename)):
                    count += 1
        print(f"✅ Fertig! {count} Dateien wurden gesäubert.")