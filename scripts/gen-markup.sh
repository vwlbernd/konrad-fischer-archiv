#!/bin/bash

echo "=== Dynamische Verarbeitung gestartet ==="

# Die Schleife sucht nach allen Dateien, die mit einer Zahl beginnen und auf .py enden
# Durch das 'ls [0-9]*.py' werden sie automatisch alphabetisch/numerisch sortiert
for script in $(ls [0-9]*.py 2>/dev/null); do
    
    echo "------------------------------------"
    echo "[PROCESS] Gefunden: $script"
    
    # Ausführung
    python3 "$script"
    
    # Erfolgskontrolle
    if [ $? -eq 0 ]; then
        echo "[DONE] $script erfolgreich abgeschlossen."
    else
        echo "[CRITICAL] Fehler in $script! Abbruch der Kette."
        exit 1
    fi
done

echo "------------------------------------"
echo "=== Alle gefundenen Scripte wurden verarbeitet! ==="