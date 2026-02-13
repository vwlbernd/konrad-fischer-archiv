import os
import re

# Pfad zu deinen Markdown-Dateien anpassen
DIRECTORY = '../artikel'

# Mapping für Flaggen -> Emojis (nur wenn sie GIFs sind)
FLAG_MAP = {
    "AUSTRIA": "🇦🇹", "deutsch": "🇩🇪", "SCHWEIZ": "🇨🇭", "FRANCE": "🇫🇷",
    "ITALIA": "🇮🇹", "ESPANA": "🇪🇸", "NORGE": "🇳🇴", "SUOMI": "🇫🇮",
    "SVERIGE": "🇸🇪", "DANMARK": "🇩🇰", "HOLLAND": "🇳🇱", "BELGIQUE": "🇧🇪",
    "ENGLISH": "🇬🇧", "english": "🇬🇧", "USA": "🇺🇸", "NIPPON": "🇯🇵",
    "CHINA": "🇨🇳", "POLSKA": "🇵🇱", "HRVATSKA": "🇭🇷", "CZESKO": "🇨🇿",
    "MAGYAR": "🇭🇺", "ROMANIA": "🇷🇴", "TURKIYE": "🇹🇷", "HELLAS": "🇬🇷",
    "ELLAS": "🇬🇷", "BRASIL": "🇧🇷", "ARGENTINA": "🇦🇷", "CHILE": "🇨🇱",
    "CANADA": "🇨🇦", "MEXIKO": "🇲🇽"
}

# Blacklist der GIF-Namen (ohne Endung)
DELETE_LIST = [
    "U", "EIS", "Ske", "atom", "AFFE", "CUBA", "FIRE", "HANF", "OT01", "OT02", 
    "OT03", "OT04", "OT05", "PERU", "SSSR", "WURM", "bruch", "EGYPT", "emfly", 
    "HAUS3", "HAUS4", "HAUS5", "HOUSE", "TAUBE", "TIMOR", "US-BX", "ANGOLA", 
    "ARABIA", "DOMREP", "EMDRAG", "emroll", "GUINEA", "hammer", "ISLAND", 
    "HOUSE2", "KOREA1", "KOREA2", "PANAMA", "SRBIJA", "TAIWAN", "BLUBAND", 
    "BOLIVIA", "ECUADOR", "emumsch", "EMBRIEF", "english", "LESDRAG", "nuclear", 
    "SAOTOME", "SCHELLE", "URUGUAY", "CAPVERDE", "COLOMBIA", "EQGUINEA", 
    "HONDURAS", "MOZAMBIQ", "PARAGUAY", "PORTUGAL", "SALVADOR", "SLOVENIA", 
    "WINKDRAG", "AUSTRALIA", "COSTARICA", "crossfish", "GUATEMALA", "MAKEDONIA", 
    "NICARAGUA", "VENEZUELA", "YUGOSLAVIA", "BOSNIAHERZEGOWINA"
]

def clean_md_files(directory):
    # DIESER REGEX IST SICHERER:
    # 1. (?:\[)? -> Optionale öffnende Klammer für Links
    # 2. !\[[^\]]*\] -> Das Bild-Alt-Attribut (darf keine ] enthalten)
    # 3. \([^)]+?\/([^/)]+?)\.(?:gif|GIF)\) -> Der Pfad zu einem GIF
    # 4. (?:\]\([^)]*\))? -> Optionaler Link-Teil am Ende
    img_regex = re.compile(r'(\[?(!\[[^\]]*\]\([^)]+?\/([^/)]+?)\.(?:gif|GIF)\))\]?(?:\([^)]*\))?)')

    for filename in os.listdir(directory):
        if filename.endswith(".md"):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            def replacement_logic(match):
                full_block = match.group(1) # Der komplette Treffer
                img_name = match.group(3)   # Nur der Dateiname (z.B. "hammer")

                # 1. Flaggen ersetzen
                if img_name in FLAG_MAP:
                    return FLAG_MAP[img_name]
                
                # 2. Löschliste
                if img_name in DELETE_LIST:
                    return "" 
                
                return full_block

            new_content = img_regex.sub(replacement_logic, content)
            
            # Säuberung von überflüssigen Leerzeichen
            new_content = re.sub(r'  +', ' ', new_content)

            if new_content != content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"✔ Bereinigt: {filename}")

if __name__ == "__main__":
    clean_md_files(DIRECTORY)