import json, re, pathlib, html, markdown
SITE = 'https://sadiqurrahman.site'
AUTHOR = 'Sadiqur Rahman'
posts = []
bodies = {}
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
    p = {"slug": f.stem, "title": meta.get('title', f.stem), "date": meta.get('date', ''),
         "summary": meta.get('summary', ''),
         "tags": [x.strip() for x in meta.get('tags', '').split(',') if x.strip()]}
    posts.append(p)
    bodies[f.stem] = t[m.end():]
posts.sort(key=lambda p: p['date'], reverse=True)
pathlib.Path('posts/posts.json').write_text(json.dumps(posts, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')

NAV = ('<header class="top"><div class="wrap"><a class="brand" href="/index.html">Sadiqur Rahman</a><nav>'
       '<a href="/index.html#experience">Experience</a><a href="/blog.html">Blog</a>'
       '<a href="/index.html#library">Library</a><a href="/index.html#contact">Contact</a></nav></div></header>')
TPL = '''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} | Sadiqur Rahman</title><meta name="description" content="{desc}">
<link rel="canonical" href="{url}"><meta property="og:type" content="article"><meta property="og:title" content="{title}"><meta property="og:description" content="{desc}"><meta property="og:url" content="{url}">
<script type="application/ld+json">{ld}</script>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,700;12..96,800&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Serif:wght@400;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/style.css"><link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/github-dark.min.css"></head>
<body>{nav}<article class="post"><small>{date}</small><h1>{title}</h1><div>{tags}</div>{body}
<p><a href="/blog.html">All posts</a></p></article>
<footer><div class="wrap">© {year} Sadiqur Rahman · Dhaka, Bangladesh</div></footer>
<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script><script>hljs.highlightAll()</script></body></html>'''
for p in posts:
    url = f"{SITE}/blog/{p['slug']}/"
    ld = json.dumps({"@context": "https://schema.org", "@type": "BlogPosting", "headline": p['title'],
                     "datePublished": p['date'], "description": p['summary'], "url": url,
                     "author": {"@type": "Person", "name": AUTHOR, "url": SITE + "/"}}, ensure_ascii=False)
    body = markdown.markdown(bodies[p['slug']], extensions=['fenced_code', 'tables'])
    out = pathlib.Path('blog') / p['slug']
    out.mkdir(parents=True, exist_ok=True)
    (out / 'index.html').write_text(TPL.format(
        title=html.escape(p['title']), desc=html.escape(p['summary'] or p['title']), url=url, ld=ld, nav=NAV,
        date=p['date'], year=(p['date'] or '2026')[:4], body=body,
        tags=''.join(f'<span class="tag">{html.escape(x)}</span>' for x in p['tags'])), encoding='utf-8')

urls = [(SITE + '/', ''), (SITE + '/blog.html', '')] + [(f"{SITE}/blog/{p['slug']}/", p['date']) for p in posts]
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for u, d in urls:
    sm += f'<url><loc>{u}</loc>' + (f'<lastmod>{d}</lastmod>' if d else '') + '</url>\n'
pathlib.Path('sitemap.xml').write_text(sm + '</urlset>\n', encoding='utf-8')
