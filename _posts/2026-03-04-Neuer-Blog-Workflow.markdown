---
layout: post
title:  "Bloggen leicht gemacht: GitHub Issues als Schreibmaschine"
date:   2026-03-04 19:00:00
author: "Gemini CLI & René"
last_modified_at:  2026-03-04 19:00:00
excerpt: "Wir haben unseren Workflow modernisiert! Ab sofort können Blog-Beiträge direkt über GitHub Issues eingereicht werden – ganz ohne Git-Kenntnisse."
categories: news
tags:  Back
image:
  feature: issue_workflow_hero.png
  topPosition: 0px
bgContrast: dark
bgGradientOpacity: darker
syntaxHighlighter: no
---
Wir freuen uns, eine bedeutende Verbesserung für unsere Autoren vorstellen zu können: Unseren neuen **Issue-to-Post Workflow**!

Bisher war das Erstellen eines Blog-Beitrags mit einigem technischem Wissen verbunden. Man musste Markdown-Dateien lokal erstellen, Bilder in die richtigen Ordner sortieren und via Git in das Repository pushen. Das ist ab heute Geschichte.

### Wie funktioniert es?

Wir nutzen nun die strukturierten **GitHub Issue Forms**. Jeder, der einen Account bei GitHub hat, kann ab sofort einen Post-Vorschlag einreichen:

1.  Gehe auf unsere [Issue-Seite](https://github.com/FreieMaker/FreieMaker.github.io/issues).
2.  Klicke auf **"New Issue"** und wähle die Vorlage **"Neuer Blog-Post (Vorschlag)"**.
3.  Fülle das Formular aus: Titel, Autor, Text und lade deine Bilder einfach per Drag & Drop direkt in das Textfeld hoch.
4.  Absenden!

<div class="img img--fullContainer img--14xLeading" style="background-image: url({{ site.baseurl_featured_img }}issue_template_mockup.png);"></div>

### Was passiert im Hintergrund?

Sobald ein Moderator das Issue sichtet und das Label `ready-to-publish` vergibt, übernimmt unsere neue **GitHub Action** die Arbeit:
- Sie lädt alle Bilder aus dem Issue herunter und speichert sie am richtigen Ort (`assets/images/hero/`).
- Sie generiert automatisch Thumbnails für die Listenansicht (via `generate_thumbnails.sh`).
- Sie wandelt das Formular in eine fertige Jekyll-Markdown-Datei um.
- Sie erstellt automatisch einen Pull Request gegen den `master`-Branch.

Sobald der PR gemergt wird, erscheint der Post live auf der Webseite. So können wir uns voll auf den Inhalt konzentrieren und die Technik der Automatisierung überlassen.

Viel Spaß beim Schreiben!
