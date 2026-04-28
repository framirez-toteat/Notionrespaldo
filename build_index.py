import os
import json
import re

content_dir = os.path.join(os.path.dirname(__file__), "content")
pages = []

for root, dirs, files in os.walk(content_dir):
    for file in sorted(files):
        if not file.endswith('.html'):
            continue
        full_path = os.path.join(root, file)
        rel_path = os.path.relpath(full_path, os.path.dirname(__file__)).replace('\\', '/')
        title = re.sub(r'\s+[a-f0-9]{32}(-[a-f0-9-]+)?$', '', os.path.splitext(file)[0]).strip()
        folder = os.path.relpath(root, content_dir).replace('\\', '/')
        if folder == '.':
            folder = ''
        pages.append({'title': title, 'path': rel_path, 'folder': folder})

pages.sort(key=lambda x: (x['folder'].lower(), x['title'].lower()))

out_json = os.path.join(os.path.dirname(__file__), "pages.json")
with open(out_json, 'w', encoding='utf-8') as f:
    json.dump(pages, f, ensure_ascii=False, indent=2)

out_js = os.path.join(os.path.dirname(__file__), "pages.js")
with open(out_js, 'w', encoding='utf-8') as f:
    f.write("var PAGES = ")
    json.dump(pages, f, ensure_ascii=False)
    f.write(";\n")

print(f"Generados pages.json y pages.js con {len(pages)} páginas.")
