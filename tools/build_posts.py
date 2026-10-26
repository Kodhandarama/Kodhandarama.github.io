"""Write a shareable page for every human-written reflection in index.html.

Each <article data-webpage=... data-slug=...> inside the Reflections window becomes
reflections/<slug>/index.html, and reflections/index.html lists them all.
Run from the repo root after adding or editing a reflection:  python3 tools/build_posts.py
"""
import html
import pathlib
import re

root = pathlib.Path(__file__).resolve().parent.parent
page = (root / "index.html").read_text(encoding="utf-8")

ARTICLE = re.compile(
    r'<article data-webpage="(?P<id>[\w-]+)" data-slug="(?P<slug>[\w-]+)" data-short="(?P<short>[^"]+)" '
    r'data-title="(?P<title>[^"]+)" data-desc="(?P<desc>[^"]+)" hidden>(?P<inner>.*?)</article>',
    re.S,
)

CSS = """
:root { --web-bg: #cbcbc6; --ink: #17171c; --ink-2: #3a3a3a; --paper: #fbfaf4; --chrome: #ebe7da; --link: #0000ee; --visited: #551a8b; color-scheme: light; }
* { box-sizing: border-box; }
html { background: var(--web-bg); }
body { margin: 0; background: var(--web-bg); color: #111111; font: 20px/1.65 "Times New Roman", Times, Georgia, serif; padding-block: env(safe-area-inset-top, 0px) env(safe-area-inset-bottom, 0px); }
.bar { position: sticky; top: 0; display: flex; justify-content: space-between; align-items: center; gap: 12px; padding: 10px max(16px, env(safe-area-inset-right, 0px)) 10px max(16px, env(safe-area-inset-left, 0px)); background: var(--chrome); border-bottom: 1px solid var(--ink); font: 500 16px "Pixelify Sans", ui-monospace, monospace; }
.bar a { color: var(--ink); }
main { max-width: 700px; margin: 0 auto; padding: 28px max(18px, env(safe-area-inset-right, 0px)) 56px max(18px, env(safe-area-inset-left, 0px)); }
h1 { margin: 0 0 10px; font: 700 36px/1.15 "Times New Roman", Times, Georgia, serif; text-wrap: balance; }
.meta, .crumb { font: 16px "Pixelify Sans", ui-monospace, monospace; color: var(--ink-2); }
p { margin: 0 0 18px; }
.aside { font-style: italic; color: var(--ink-2); }
a { color: var(--link); }
a:visited { color: var(--visited); }
hr { margin: 26px 0; border: 0; border-top: 1px solid #8a8a86; border-bottom: 1px solid #f2f2ee; }
.foot { display: flex; flex-wrap: wrap; align-items: center; gap: 10px 18px; font: 16px "Pixelify Sans", ui-monospace, monospace; }
.btn { padding: 8px 14px; border: 1px solid var(--ink); border-radius: 7px; background: var(--paper); color: var(--ink); font: 500 16px "Pixelify Sans", ui-monospace, monospace; cursor: pointer; }
.btn:active { background: var(--ink); color: var(--paper); }
.list { padding-left: 22px; list-style: square; }
.list li { margin-bottom: 18px; }
@media (max-width: 700px) { body { font-size: 18px; } h1 { font-size: 30px; } }
"""

SHARE_JS = """
const btn = document.getElementById('share'), msg = document.getElementById('share-msg');
const url = location.href.split('#')[0];
const phone = () => !!navigator.share && matchMedia('(max-width: 700px)').matches;
if (phone()) btn.textContent = 'Share';
btn.addEventListener('click', async () => {
  if (phone()) {
    try { await navigator.share({ title: document.title, url }); return; } catch (err) { if (err && err.name === 'AbortError') return; }
  }
  try { await navigator.clipboard.writeText(url); msg.textContent = 'Link copied'; }
  catch (err) { msg.textContent = url; }
});
"""


def shell(title, desc, og_type, depth, bar_right, body):
    up = "../" * depth
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta property="og:type" content="{og_type}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:site_name" content="Shreeram Chandra">
<meta name="twitter:card" content="summary">
<link rel="icon" href="{up}favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Pixelify+Sans:wght@400..700&display=swap">
<style>{CSS}</style>
</head>
<body>
<header class="bar"><a href="{up}">◀ Shreeram's desktop</a><span>{bar_right}</span></header>
<main>
{body}
</main>
</body>
</html>
"""


posts = []
for m in ARTICLE.finditer(page):
    inner = m["inner"]
    meta = re.search(r'<p class="meta">(.*?)</p>', inner, re.S).group(1)
    start = inner.index("</p>", inner.index('<p class="meta">')) + len("</p>")
    body = inner[start:inner.index("<hr>")].strip()
    title, desc, slug = m["title"], m["desc"], m["slug"]
    posts.append((slug, title, desc))
    out = root / "reflections" / slug
    out.mkdir(parents=True, exist_ok=True)
    (out / "index.html").write_text(shell(
        title, desc, "article", 2, "Human-written reflections",
        f"""<p class="crumb"><a href="../">Human-written reflections</a> › {m["short"]}</p>
<article>
<h1>{title}</h1>
<p class="meta">{meta}</p>
{body}
</article>
<hr>
<div class="foot"><a href="../">◀ All reflections</a><button class="btn" id="share">Copy link</button><span id="share-msg" role="status"></span><a href="../../#reflections/{slug}">Open on the desktop ↗</a></div>
<script>{SHARE_JS}</script>"""), encoding="utf-8")

items = "\n".join(
    f'<li><a href="{slug}/">{title}</a><br>{desc}</li>' for slug, title, desc in posts
)
(root / "reflections").mkdir(exist_ok=True)
(root / "reflections" / "index.html").write_text(shell(
    "Human-written reflections · Shreeram Chandra",
    "A growing series of essays and notes on research, the PhD, and everything in between.",
    "website", 1, "Shreeram Chandra",
    f"""<h1>Human-written reflections</h1>
<p>A growing series of essays and notes on research, the PhD, and everything in between.</p>
<hr>
<ul class="list">
{items}
</ul>"""), encoding="utf-8")
print("wrote", len(posts), "post page(s):", ", ".join(slug for slug, _, _ in posts))
