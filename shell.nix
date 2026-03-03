{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = with pkgs; [
    imagemagick
  ];

  shellHook = ''
    echo "--- Freie Maker Bild-Optimierungs-Umgebung ---"
    echo "Nutze './generate_thumbnails.sh' um die Vorschaubilder zu aktualisieren."
  '';
}
