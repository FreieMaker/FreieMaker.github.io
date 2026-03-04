#!/usr/bin/env bash

# Verzeichnisse definieren
SRC_DIR="assets/images/hero"
DST_DIR="assets/images/thumbnail"
WIDTH=600
QUALITY=85

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

# Funktion zur Thumbnail-Erstellung
generate_thumbnail() {
    local src_file="$1"
    local filename=$(basename "$src_file")
    local dst_file="$DST_DIR/$filename"
    
    echo "Generiere Thumbnail (600px): $filename"
    $CONVERT_CMD "$src_file" -resize "${WIDTH}x" -quality "$QUALITY" -strip "$dst_file"
}

# Falls ein Argument übergeben wurde, bearbeite nur diese Datei
if [ -n "$1" ]; then
    if [ -f "$SRC_DIR/$1" ]; then
        generate_thumbnail "$SRC_DIR/$1"
    else
        echo "Error: Datei $SRC_DIR/$1 nicht gefunden!"
        exit 1
    fi
    exit 0
fi

# Falls kein Argument, bearbeite alle Bilder
echo "Prüfe alle Bilder in $SRC_DIR..."
count=0
EXTENSIONS=("jpg" "jpeg" "png" "JPG" "JPEG" "PNG")

for ext in "${EXTENSIONS[@]}"; do
    shopt -s nullglob
    for src_file in "$SRC_DIR"/*."$ext"; do
        generate_thumbnail "$src_file"
        ((count++))
    done
done

echo "Fertig! $count Thumbnails wurden aktualisiert."
