#!/usr/bin/env bash

# Verzeichnisse definieren
SRC_DIR="assets/images/hero"
DST_DIR="assets/images/thumbnail"
WIDTH=350
QUALITY=80

# Kommando-Check (magick vs convert)
if command -v magick >/dev/null 2>&1; then
    CONVERT_CMD="magick"
elif command -v convert >/dev/null 2>&1; then
    CONVERT_CMD="convert"
else
    echo "Error: ImageMagick (magick oder convert) nicht gefunden!"
    exit 1
fi

# Zielverzeichnis sicherstellen
mkdir -p "$DST_DIR"

echo "Prüfe Bilder in $SRC_DIR..."

count=0
EXTENSIONS=("jpg" "jpeg" "png" "JPG" "JPEG" "PNG")

for ext in "${EXTENSIONS[@]}"; do
    # Shell-Globbing sicherstellen
    shopt -s nullglob
    for src_file in "$SRC_DIR"/*."$ext"; do
        filename=$(basename "$src_file")
        dst_file="$DST_DIR/$filename"
        
        if [ ! -f "$dst_file" ] || [ "$src_file" -nt "$dst_file" ]; then
            echo "Generiere Thumbnail: $filename"
            $CONVERT_CMD "$src_file" -resize "${WIDTH}x" -quality "$QUALITY" -strip "$dst_file"
            ((count++))
        fi
    done
done

if [ $count -eq 0 ]; then
    echo "Alle Thumbnails sind aktuell."
else
    echo "Fertig! $count Thumbnails wurden erstellt/aktualisiert."
fi
