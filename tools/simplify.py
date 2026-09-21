#!/usr/bin/env python3
"""One-off: four-page site (Home, Work, Studio, Contact). Idempotent."""
import os, re, shutil
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def rd(p): return open(os.path.join(ROOT, p)).read()
def wr(p, s): open(os.path.join(ROOT, p), 'w').write(s)

# nav + footer in assemble.py
a = rd('tools/assemble.py')
a = re.sub(r'<ul>.*?</ul>', '''<ul>
      <li><a href="work.html">Work</a></li>
      <li><a href="studio.html">Studio</a></li>
      <li><a href="contact.html">Contact</a></li>
    </ul>''', a, count=1, flags=re.S)
a = a.replace('<div class="right"><a class="btn sm" href="commission.html">Get a render in 24h</a><button', '<div class="right"><a class="btn sm" href="contact.html">Contact</a><button')
a = re.sub(r'<div class="cols mono">\n      <a href="work.html">Work</a>.*?\n    </div>', '''<div class="cols mono">
      <a href="work.html">Work</a><a href="studio.html">Studio</a><a href="contact.html">Contact</a>
    </div>''', a, count=1, flags=re.S)
a = a.replace("if fn in ('thank-you.html','session.html','private.html'):", "if fn in ('thank-you.html','session.html','private.html','home-v1.html','home-v2.html'):")
wr('tools/assemble.py', a)

# home: CTA to contact
h = rd('tools/pages/index.html')
h = h.replace('<a class="g-cta" href="private.html">Private access</a>', '<a class="g-cta" href="contact.html">Contact</a>')
wr('tools/pages/index.html', h)

# retire pages: move sources to tools/pages/_retired, remove built html
os.makedirs(os.path.join(ROOT, 'tools/pages/_retired'), exist_ok=True)
for fn in ['for-designers.html', 'process.html', 'commission.html', 'home-v1.html', 'home-v2.html']:
    src = os.path.join(ROOT, 'tools/pages', fn)
    if os.path.exists(src): shutil.move(src, os.path.join(ROOT, 'tools/pages/_retired', fn))
    out = os.path.join(ROOT, fn)
    if os.path.exists(out): os.remove(out)

# redirects for retired urls
wr('_redirects', '/for-designers.html /studio.html 301\n/process.html /studio.html 301\n/commission.html /contact.html 301\n/home-v1.html / 301\n/home-v2.html / 301\n')

# sitemap
wr('sitemap.xml', '''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>https://thepolycrafted.com/</loc><changefreq>monthly</changefreq><priority>1.0</priority></url>
  <url><loc>https://thepolycrafted.com/work.html</loc><changefreq>monthly</changefreq><priority>0.8</priority></url>
  <url><loc>https://thepolycrafted.com/studio.html</loc><changefreq>monthly</changefreq><priority>0.8</priority></url>
  <url><loc>https://thepolycrafted.com/contact.html</loc><changefreq>monthly</changefreq><priority>0.8</priority></url>
</urlset>
''')

# thank-you: point links at the four pages
t = rd('tools/pages/thank-you.html')
t = t.replace('for-designers.html', 'studio.html').replace('commission.html', 'contact.html').replace('process.html', 'studio.html')
wr('tools/pages/thank-you.html', t)

# private/session pages stay reachable by code but off the menu; point their public links at contact
for fn in ['private.html', 'session.html']:
    s = rd('tools/pages/' + fn).replace('for-designers.html', 'studio.html').replace('commission.html', 'contact.html')
    wr('tools/pages/' + fn, s)
print('simplified')
