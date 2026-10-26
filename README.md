# Shreeram Chandra's website

A retro Mac desktop. The site is `index.html` (markup, styles and script) plus images in `photo.jpg`, `wallpaper*.jpg`,
`projects/` and `logos/`. GitHub Pages serves the `main` branch at https://kodhandarama.github.io.

## Human-written reflections

Each post is an `<article data-webpage=... data-slug=...>` inside the Reflections window in `index.html`.
Every post also has its own shareable page at `reflections/<slug>/`. After adding or editing a post, regenerate those pages:

    python3 tools/build_posts.py

Then add the post's entry to the `PAGES` list in the script part of `index.html` and to the list on the Reflections home page.

## Moving to your own domain

1. Add a file named `CNAME` containing just the domain, for example `shreeramchandra.com`.
2. At your DNS provider, point the domain at GitHub Pages (A records for the apex, or a CNAME record to `kodhandarama.github.io` for a subdomain).
3. In the repo's Settings > Pages, confirm the domain and turn on "Enforce HTTPS".
