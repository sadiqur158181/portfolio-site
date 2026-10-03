import json, re, pathlib
posts = []
for f in sorted(pathlib.Path('posts').glob('*.md')):
    t = f.read_text(encoding='utf-8')
    m = re.match(r'^---\s*\n(.*?)\n---\s*\n', t, re.S)
    if not m:
        continue
    meta = {}
    for line in m.group(1).splitlines():
        if ':' in line:
            k, v = line.split(':', 1)
            meta[k.strip()] = v.strip()
    posts.append({"slug": f.stem, "title": meta.get('title', f.stem), "date": meta.get('date', ''),
                  "summary": meta.get('summary', ''),
                  "tags": [x.strip() for x in meta.get('tags', '').split(',') if x.strip()]})
posts.sort(key=lambda p: p['date'], reverse=True)
pathlib.Path('posts/posts.json').write_text(json.dumps(posts, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
