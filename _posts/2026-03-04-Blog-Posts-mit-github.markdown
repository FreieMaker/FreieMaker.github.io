---
layout: post
title:  "Blog Posts mit github"
date:   2026-03-04 19:14:02
author: "René Gern"
last_modified_at:  2026-03-04 19:14:02
excerpt: "Wir haben unseren Workflow modernisiert! Ab sofort können Blog-Beiträge direkt über GitHub Issues eingereicht werden – ganz ohne Git-Kenntnisse."
categories: news
tags:  Back
image:
  feature: github-issue-post-hero.png
  topPosition: 0px
bgContrast: dark
bgGradientOpacity: darker
syntaxHighlighter: no
---
Wir freuen uns, eine bedeutende Verbesserung für unsere Autoren vorstellen zu können: Unseren neuen Issue-to-Post Workflow!

Bisher war das Erstellen eines Blog-Beitrags mit einigem technischem Wissen verbunden. Man musste Markdown-Dateien lokal erstellen, Bilder in die richtigen Ordner sortieren und via Git in das Repository pushen. Das ist ab heute Geschichte.

Wie funktioniert es?
Wir nutzen nun die strukturierten GitHub Issue Forms. Jeder, der einen Account bei GitHub hat, kann ab sofort einen Post-Vorschlag einreichen:

Gehe auf unsere [Issue-Seite](https://github.com/FreieMaker/FreieMaker.github.io/issues).
Klicke auf "New Issue" und wähle die Vorlage "Neuer Blog-Post (Vorschlag)".
Fülle das Formular aus: Titel, Autor, Text und lade deine Bilder einfach per Drag & Drop direkt in das Textfeld hoch.
Absenden!
Was passiert im Hintergrund?
Sobald ein Moderator das Issue sichtet und das Label ready-to-publish vergibt, übernimmt unsere neue GitHub Action die Arbeit:

Sie lädt alle Bilder aus dem Issue herunter und speichert sie am richtigen Ort (assets/images/hero/).
Sie generiert automatisch Thumbnails für die Listenansicht (via generate_thumbnails.sh).
Sie wandelt das Formular in eine fertige Jekyll-Markdown-Datei um.
Sie erstellt automatisch einen Pull Request gegen den master-Branch.
Sobald der PR gemergt wird, erscheint der Post live auf der Webseite. So können wir uns voll auf den Inhalt konzentrieren und die Technik der Automatisierung überlassen.

Viel Spaß beim Schreiben!

<div class="img img--fullContainer img--14xLeading" style="background-image: url({{ site.baseurl_featured_img }}github-issue-post-hero.png);"></div>
