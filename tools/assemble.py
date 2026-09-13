#!/usr/bin/env python3
"""Assemble static pages from tools/pages/*.html bodies + shared nav/footer.
Output is plain HTML in the repo root; no runtime build step. Run: python3 tools/assemble.py"""
import os, re, json
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'tools', 'pages')

NAV = '''<nav class="nav" aria-label="Main">
  <div class="wrap">
    <a class="brand" href="index.html">The Polycrafted</a>
    <ul>
      <li><a href="work.html">Work</a></li>
      <li><a href="for-designers.html">For Designers</a></li>
      <li><a href="process.html">Process</a></li>
      <li><a href="studio.html">Studio</a></li>
      <li><a href="contact.html">Contact</a></li>
    </ul>
    <div class="right"><a class="btn sm" href="commission.html">Get a render in 24h</a><button class="nav-toggle" aria-expanded="false">Menu</button></div>
  </div>
</nav>'''

FOOTER = '''<footer>
  <div class="wrap">
    <div>
      <div class="brand">The Polycrafted</div>
      <p class="mono" style="margin-top:12px">Custom art studio, Los Angeles</p>
    </div>
    <div class="cols mono">
      <a href="work.html">Work</a><a href="for-designers.html">For Designers</a><a href="process.html">Process</a><a href="commission.html">Commission</a><a href="studio.html">Studio</a><a href="contact.html">Contact</a>
    </div>
    <div class="cols mono">
      <a href="mailto:info@thepolycrafted.com">info@thepolycrafted.com</a>
      <a href="https://www.instagram.com/thepolycrafted/" rel="noopener" target="_blank">Instagram @thepolycrafted</a>
    </div>
  </div>
  <div class="wrap legal mono"><span>&copy; <span data-year>2026</span> The Polycrafted Art Studio. All rights reserved.</span><span>Los Angeles, California</span></div>
</footer>
<script src="js/main.js"></script>'''

HEAD = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="https://thepolycrafted.com/{canon}">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="https://thepolycrafted.com/{canon}">
<meta property="og:image" content="https://thepolycrafted.com/images/site/{og}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="images/site/favicon.png">
<link rel="stylesheet" href="css/style.css">
{schema}</head>
<body>
'''

for fn in sorted(os.listdir(SRC)):
    if not fn.endswith('.html'): continue
    raw = open(os.path.join(SRC, fn)).read()
    m = re.match(r'---\n(.*?)\n---\n(.*)$', raw, re.S)
    meta = json.loads(m.group(1)); body = m.group(2)
    schema = ''
    if meta.get('schema'):
        schema = '<script type="application/ld+json">\n' + json.dumps(meta['schema'], indent=1) + '\n</script>\n'
    html = HEAD.format(title=meta['title'], description=meta['description'], slug=fn, canon=('' if fn=='index.html' else fn), og=meta.get('og', 'og-home.jpg'), schema=schema)
    if fn == 'thank-you.html': html = html.replace('<link rel="canonical"', '<meta name="robots" content="noindex">\n<link rel="canonical"')
    html += NAV + '\n' + body.strip() + '\n\n' + FOOTER + '\n</body>\n</html>\n'
    assert '—' not in html, fn + ' contains an em dash'
    open(os.path.join(ROOT, fn), 'w').write(html)
    print('wrote', fn)
