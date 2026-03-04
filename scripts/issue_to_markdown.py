import sys
import re
import os
import subprocess
from datetime import datetime

def parse_issue(body):
    # The specific labels from our issue_template/new_post.yml
    labels = [
        "Titel des Posts",
        "Autor",
        "Kategorie",
        "Kurzbeschreibung (Excerpt)",
        "Haupt-Text (Markdown)",
        "Hero-Bild (Name)"
    ]
    
    data = {}
    # Find positions of all known labels
    positions = []
    for label in labels:
        # Search for "### Label" at the start of a line
        match = re.search(f'^### {re.escape(label)}', body, re.MULTILINE)
        if match:
            positions.append((match.start(), label))
    
    # Sort positions by their occurrence in the body
    positions.sort()
    
    for i in range(len(positions)):
        start_idx, label = positions[i]
        # Content starts after the label line
        content_start = body.find('\n', start_idx) + 1
        
        # Content ends at the start of the next label or end of string
        if i < len(positions) - 1:
            end_idx = positions[i+1][0]
        else:
            end_idx = len(body)
            
        data[label] = body[content_start:end_idx].strip()
        
    return data

def process_images(content, hero_name_hint):
    # Match Markdown images: ![alt](url)
    markdown_images = re.findall(r'!\[(.*?)\]\((https?://.*?)\)', content)
    # Match HTML images: <img ... src="url" ... />
    html_images = re.findall(r'<img [^>]*src="(https?://[^"]+)"[^>]*>', content)
    
    # Standardize image list: (alt, url, full_match_string)
    images = []
    for alt, url in markdown_images:
        images.append((alt, url, f"![{alt}]({url})"))
    for url in html_images:
        # Find the full <img> tag to replace it later
        full_tag_match = re.search(f'<img [^>]*src="{re.escape(url)}"[^>]*>', content)
        if full_tag_match:
            full_tag = full_tag_match.group(0)
            images.append(("Image", url, full_tag))
    
    hero_image = ""
    processed_content = content
    downloaded_filenames = []
    
    os.makedirs("assets/images/hero", exist_ok=True)
    
    for i, (alt, url, full_match) in enumerate(images):
        # Determine extension
        ext = ".jpg"
        if ".png" in url.lower(): ext = ".png"
        elif ".jpeg" in url.lower(): ext = ".jpeg"
        elif ".svg" in url.lower(): ext = ".svg"
        
        # Use hero_name_hint for the first image if provided
        if i == 0 and hero_name_hint:
            filename = hero_name_hint
            if "." not in filename:
                filename += ext
            hero_image = filename
        else:
            img_id = re.sub(r'[^a-zA-Z0-9]', '', url.split('/')[-1])[:10]
            filename = f"issue_{img_id}{ext}"
            if i == 0:
                hero_image = filename
        
        local_path = os.path.join("assets/images/hero", filename)
        
        print(f"Downloading {url} to {local_path}...")
        subprocess.run(["curl", "-L", "-s", "-o", local_path, url])
        downloaded_filenames.append(filename)
        
        # Replace the original tag with the Jekyll div snippet
        img_snippet = f'<div class="img img--fullContainer img--14xLeading" style="background-image: url({{{{ site.baseurl_featured_img }}}}{filename});"></div>'
        processed_content = processed_content.replace(full_match, img_snippet)

    return processed_content, hero_image, downloaded_filenames

def generate_markdown(data):
    title = data.get('Titel des Posts', 'Untitled')
    author = data.get('Autor', 'Anonymous')
    category = data.get('Kategorie', 'events')
    excerpt = data.get('Kurzbeschreibung (Excerpt)', '')
    content = data.get('Haupt-Text (Markdown)', '')
    hero_hint = data.get('Hero-Bild (Name)', '')
    
    processed_content, hero_image, downloaded_filenames = process_images(content, hero_hint)
    
    date_now = datetime.now()
    date_str = date_now.strftime('%Y-%m-%d %H:%M:%S')
    file_date = date_now.strftime('%Y-%m-%d')
    
    safe_title = re.sub(r'[^a-zA-Z0-9\s]', '', title).strip().replace(' ', '-')
    filename = f"_posts/{file_date}-{safe_title}.markdown"
    
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
    return filename, frontmatter, downloaded_filenames

if __name__ == "__main__":
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as f:
            body = f.read()
    else:
        body = sys.stdin.read()
    
    if not body.strip():
        sys.exit(1)
        
    data = parse_issue(body)
    if not data:
        sys.exit(1)
        
    filename, markdown, downloaded_files = generate_markdown(data)
    with open(filename, 'w') as f:
        f.write(markdown)
    
    print(f"Created {filename}")
    
    if os.path.exists("generate_thumbnails.sh"):
        for img_file in downloaded_files:
            print(f"Running generate_thumbnails.sh for {img_file}...")
            subprocess.run(["bash", "generate_thumbnails.sh", img_file])
