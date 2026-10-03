const fmt=d=>new Date(d).toLocaleDateString('en-GB',{day:'numeric',month:'short',year:'numeric'});
const esc=s=>String(s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
async function getJSON(u){try{const r=await fetch(u);if(!r.ok)throw 0;return await r.json()}catch(e){return null}}

async function renderPosts(el){
  const posts=await getJSON('posts/posts.json');
  const limit=+el.dataset.limit||99;
  if(!posts||!posts.length){el.innerHTML='<div class="empty">No posts yet. Add one in <code>posts/</code> and list it in <code>posts/posts.json</code>.</div>';return}
  el.innerHTML=posts.sort((a,b)=>b.date.localeCompare(a.date)).slice(0,limit).map(p=>
   `<a class="item" href="post.html?p=${encodeURIComponent(p.slug)}"><small>${fmt(p.date)}</small><h3>${esc(p.title)}</h3><p>${esc(p.summary||'')}</p><div style="margin-top:8px">${(p.tags||[]).map(t=>`<span class="tag">${esc(t)}</span>`).join('')}</div></a>`).join('');
}
async function renderDocs(el){
  const docs=await getJSON('docs/docs.json');
  if(!docs||!docs.length){el.innerHTML='<div class="empty">No documents yet. Drop a PDF or DOCX in <code>docs/</code> and list it in <code>docs/docs.json</code>.</div>';return}
  el.innerHTML=docs.map(d=>`<a class="item" href="docs/${encodeURI(d.file)}" download><small>${esc((d.file.split('.').pop()||'').toUpperCase())}${d.date?' · '+fmt(d.date):''}</small><h3>${esc(d.title)}</h3><p>${esc(d.desc||'')}</p></a>`).join('');
}
async function renderPost(){
  const slug=new URLSearchParams(location.search).get('p');
  const host=document.getElementById('post');
  const posts=await getJSON('posts/posts.json')||[];
  const meta=posts.find(p=>p.slug===slug);
  if(!meta){host.innerHTML='<h1>Post not found</h1><p><a href="blog.html">Back to all posts</a></p>';return}
  const md=(await (await fetch(`posts/${encodeURIComponent(slug)}.md`)).text()).replace(/^---[\s\S]*?\n---\s*/,'');
  document.title=meta.title+' | Sadiqur Rahman';
  host.innerHTML=`<small>${fmt(meta.date)}</small><h1>${esc(meta.title)}</h1><div>${(meta.tags||[]).map(t=>`<span class="tag">${esc(t)}</span>`).join('')}</div>${marked.parse(md)}`;
  if(window.hljs)host.querySelectorAll('pre code').forEach(b=>hljs.highlightElement(b));
}
document.querySelectorAll('[data-posts]').forEach(renderPosts);
document.querySelectorAll('[data-docs]').forEach(renderDocs);
if(document.getElementById('post'))renderPost();
document.querySelectorAll('[data-year]').forEach(e=>e.textContent=new Date().getFullYear());
