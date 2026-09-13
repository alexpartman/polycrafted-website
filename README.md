# The Polycrafted Art Studio website

Static site (HTML, CSS, JS, no build step). Preview on GitHub Pages, production deploy on Netlify (forms use Netlify Forms, same as liveinhomesla.com).

Editing: page bodies live in `tools/pages/*.html`; run `python3 tools/assemble.py` to regenerate the root pages with the shared nav, head and footer.

- `index.html`, `work.html`, `for-designers.html`, `process.html`, `commission.html`, `studio.html`, `contact.html`
- `css/style.css` design tokens and components
- `js/main.js` navigation, forms, gallery
- `images/work` artwork, `images/site` UI assets
- `fonts/` self-hosted woff2 (Syne, IBM Plex Mono, Instrument Serif, OFL)
- `docs/` trade documents (price sheet PDF)

Do not edit the live WordPress site. DNS is switched by Alex after approval.
