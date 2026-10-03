# Portfolio site

Static site (HTML, CSS, JS). No build step. Hosted on GitHub Pages.

## Add a blog post
1. Create `posts/my-slug.md` (Markdown, no front matter).
2. Add an entry to `posts/posts.json`:
   `{"slug":"my-slug","title":"...","date":"2026-10-03","summary":"...","tags":["oracle"]}`

## Share a PDF or DOCX
1. Put the file in `docs/`.
2. Add to `docs/docs.json`:
   `{"title":"RAC checklist","file":"rac-checklist.pdf","desc":"One-page pre-install checks","date":"2026-10-03"}`

## Before going live
- Replace `YOUR-EMAIL`, `YOUR-GITHUB`, `YOUR-LINKEDIN` in `index.html`.
- Put your real domain in `CNAME` (one line, no https://).

## Deploy
1. Create a GitHub repo, push these files to `main`.
2. Settings > Pages > Deploy from a branch > `main` / root.
3. Settings > Pages > Custom domain: enter your domain, tick Enforce HTTPS.
4. At your domain registrar's DNS:
   - Apex domain (example.com): four A records to 185.199.108.153, 185.199.109.153, 185.199.110.153, 185.199.111.153
   - www: CNAME to `YOUR-GITHUB.github.io`
