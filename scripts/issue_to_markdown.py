import sys
import re
import os
import subprocess
from datetime import datetime

def parse_issue(body):
    NL = chr(10)
    # Regex to find sections: ### Label\n(Content)
    # Support both \n and \r\n
    sections = re.findall(f'### (.*?)\r?\n(.*?)(?=\r?\n### |\\Z)', body, re.DOTALL)
    data = {}
    for label, content in sections:
        data[label.strip()] = content.strip()
    return data

def process_images(content, hero_name_hint):
    # Match any Markdown image pattern: ![alt](url)
    image_patterns = re.findall(r'!\[(.*?)\]\((https?://.*?)\)', content)
    
    hero_image = hero_name_hint if hero_name_hint else ""
    processed_content = content
    
    os.makedirs("assets/images/hero", exist_ok=True)
    
    for i, (alt, url) in enumerate(image_patterns):
        # Extract ID from URL for uniqueness
        img_id = re.sub(r'[^a-zA-Z0-9]', '', url.split('/')[-1])[:10]
        
        ext = ".jpg"
        if ".png" in url.lower(): ext = ".png"
        elif ".jpeg" in url.lower(): ext = ".jpeg"
        
        filename = f"issue_{img_id}{ext}"
        
        if i == 0 and not hero_image:
            hero_image = filename
        
        local_path = os.path.join("assets/images/hero", filename)
        
        print(f"Downloading {url} to {local_path}...")
        subprocess.run(["curl", "-L", "-s", "-o", local_path, url])
        
        img_snippet = f'<div class="img img--fullContainer img--14xLeading" style="background-image: url({{{{ site.baseurl_featured_img }}}}{filename});"></div>'
        processed_content = processed_content.replace(f"![{alt}]({url})", img_snippet)

    return processed_content, hero_image

def generate_markdown(data):
    title = data.get('Titel des Posts', 'Untitled')
    author = data.get('Autor', 'Anonymous')
    category = data.get('Kategorie', 'events')
    excerpt = data.get('Kurzbeschreibung (Excerpt)', '')
    content = data.get('Haupt-Text (Markdown)', '')
    hero_hint = data.get('Hero-Bild (Name)', '')
    
    processed_content, hero_image = process_images(content, hero_hint)
    
    date_now = datetime.now()
    date_str = date_now.strftime('%Y-%m-%d %H:%M:%S')
    file_date = date_now.strftime('%Y-%m-%d')
    
    # Safe filename: replace spaces with - and remove special chars
    safe_title = re.sub(r'[^a-zA-Z0-9\s]', '', title).strip().replace(' ', '-')
    filename = f"_posts/{file_date}-{safe_title}.markdown"
    
    # Format categories
    categories = category.strip()
    
    frontmatter = f"""---
layout: post
title:  "{title}"
date:   {date_str}
author: "{author}"
last_modified_at:  {date_str}
excerpt: "{excerpt}"
categories: {categories}
tags:  Back
image:
  feature: {hero_image}
  topPosition: 0px
bgContrast: dark
bgGradientOpacity: darker
syntaxHighlighter: no
---
{processed_content}
"""
    return filename, frontmatter

if __name__ == "__main__":
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as f:
            body = f.read()
    else:
        body = sys.stdin.read()
    
    if not body.strip():
        print("Empty body")
        sys.exit(1)
        
    data = parse_issue(body)
    if not data:
        print("Could not parse issue body. Check format (### Label).")
        sys.exit(1)
        
    filename, markdown = generate_markdown(data)
    with open(filename, 'w') as f:
        f.write(markdown)
    
    print(f"Created {filename}")
    
    if os.path.exists("generate_thumbnails.sh"):
        print("Running generate_thumbnails.sh...")
        subprocess.run(["bash", "generate_thumbnails.sh"])
