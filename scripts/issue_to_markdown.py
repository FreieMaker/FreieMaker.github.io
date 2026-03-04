import sys
import re
from datetime import datetime

def parse_issue(body):
    # Regex to find sections: ### Label\n(Content)
    # The content is until the next section marker (### ) or end of string.
    # Using raw string and escaping backslashes for the regex
    sections = re.findall(r'### (.*?)\r?\n(.*?)(?=\r?\n### |\Z)', body, re.DOTALL)
    data = {}
    for label, content in sections:
        data[label.strip()] = content.strip()
    return data

def generate_markdown(data):
    title = data.get('Titel des Posts', 'Untitled')
    author = data.get('Autor', 'Anonymous')
    category = data.get('Kategorie', 'events')
    excerpt = data.get('Kurzbeschreibung (Excerpt)', '')
    content = data.get('Haupt-Text (Markdown)', '')
    hero_image = data.get('Hero-Bild (Name)', '')
    
    date_now = datetime.now()
    date_str = date_now.strftime('%Y-%m-%d %H:%M:%S')
    file_date = date_now.strftime('%Y-%m-%d')
    
    # Safe filename: replace spaces with - and remove special chars
    safe_title = re.sub(r'[^a-zA-Z0-9\s]', '', title).strip().replace(' ', '-')
    filename = f"_posts/{file_date}-{safe_title}.markdown"
    
    # Format categories (it's often single word but can be list in YAML)
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
{content}
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
        # Print first 50 chars of body to debug
        print(f"Body snippet: {body[:50]}")
        sys.exit(1)
        
    filename, markdown = generate_markdown(data)
    with open(filename, 'w') as f:
        f.write(markdown)
    print(f"Created {filename}")
