#!/usr/bin/env bash

# Verzeichnisse definieren
SRC_DIR="assets/images/hero"
DST_DIR="assets/images/thumbnail"
WIDTH=350
QUALITY=80

# Zielverzeichnis sicherstellen
mkdir -p "$DST_DIR"

echo "Prüfe Bilder in $SRC_DIR..."

# Zähler für Statistik
count=0

# Unterstützte Endungen
EXTENSIONS=("jpg" "jpeg" "png" "JPG" "JPEG" "PNG")

for ext in "${EXTENSIONS[@]}"; do
    for src_file in "$SRC_DIR"/*."$ext"; do
        # Prüfen ob Datei existiert (falls keine Dateien für die Endung da sind)
        [ -e "$src_file" ] || continue
        
        filename=$(basename "$src_file")
        dst_file="$DST_DIR/$filename"
        
        # Nur generieren wenn Thumbnail fehlt oder Quellbild neuer ist
        if [ ! -f "$dst_file" ] || [ "$src_file" -nt "$dst_file" ]; then
            echo "Generiere Thumbnail: $filename"
            magick "$src_file" -resize "${WIDTH}x" -quality "$QUALITY" -strip "$dst_file"
            ((count++))
        fi
    done
done

if [ $count -eq 0 ]; then
    echo "Alle Thumbnails sind aktuell."
else
    echo "Fertig! $count Thumbnails wurden erstellt/aktualisiert."
fi
