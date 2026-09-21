#!/usr/bin/env python3
"""One-off: switch the site to the light Inter theme. Idempotent."""
import os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def rd(p): return open(os.path.join(ROOT, p)).read()
def wr(p, s): open(os.path.join(ROOT, p), 'w').write(s)

# 1. style.css: Inter 400 face + light override block
css = rd('css/style.css')
if 'inter-latin-400' not in css:
    css = css.replace("@font-face{font-family:'Inter';font-weight:500",
        "@font-face{font-family:'Inter';font-weight:400;font-display:swap;src:url('../fonts/inter-latin-400-normal.woff2') format('woff2')}\n@font-face{font-family:'Inter';font-weight:500", 1)
MARK = '/* ===== Light theme, Inter (Sep 2026) ===== */'
if MARK not in css:
    css += '\n' + MARK + '''
:root{
  --bg:#EFECE6; --panel:#E6E2DA; --panel-2:#F6F4EF;
  --ink:#1A1917; --ink-2:#5E5B56; --ink-3:#8E8B84; --line:#D9D5CD;
  --accent:#1A1917;
  --display:'Inter',Helvetica,Arial,sans-serif;
  --mono:'Inter',Helvetica,Arial,sans-serif;
  --serif:'Inter',Helvetica,Arial,sans-serif;
}
html{color-scheme:light}
::selection{background:var(--ink);color:var(--bg)}
.mono,.nav ul,.nav-toggle,.ticker span,.note,.field label,.form-status,.form-note,.field .hint,.tag,.table th,.index-row .n,.index-row .s,.work-card .cap span,.steps li::before{font-weight:600;letter-spacing:.14em}
.mono{font-size:11px}
.table{font-family:var(--display);font-size:14px}
.table th{font-size:11px}
h1,.h1{font-weight:700;letter-spacing:-.035em}
h2,.h2{font-weight:600;letter-spacing:-.03em}
h3,.h3{font-weight:600}
h1 i,h2 i,.serif-i{font-family:var(--display);font-style:normal;font-weight:500;color:var(--ink-2);letter-spacing:inherit}
.lede{color:var(--ink-2)}
.nav{background:rgba(239,236,230,.92);border-bottom:1px solid var(--line)}
.nav .brand{font-size:18px;letter-spacing:.02em;font-weight:700}
.nav ul{color:var(--ink);font-size:12px}
.nav ul a{opacity:.8;border-bottom:0}
.nav ul a:hover,.nav ul a[aria-current=page]{opacity:1;border-bottom:0}
.btn{font-weight:600;letter-spacing:.14em;font-size:11px}
.tag{background:rgba(239,236,230,.92);color:var(--ink);font-size:11px}
.ticker span::before{background:var(--ink)}
.index-row:hover{background:var(--panel-2)}
.panel{background:var(--panel-2);border-color:var(--line)}
.panel-dark{background:var(--panel)}
.field input,.field select,.field textarea{background:#fff}
.form-status.err{color:#B3261E}
footer .brand{letter-spacing:.02em;font-size:16px;font-weight:700}
'''
wr('css/style.css', css)

# 2. home: CTA pill over the image
h = rd('tools/pages/index.html')
if 'g-cta' not in h:
    h = h.replace('.g-bar .cap{opacity:.6;font-weight:500}',
        '.g-bar .cap{opacity:.6;font-weight:500}\n.g-cta{position:absolute;right:28px;bottom:28px;z-index:2;background:#1A1917;color:#EFECE6;padding:15px 22px;font-family:var(--sans);font-weight:600;font-size:11px;letter-spacing:.16em;text-transform:uppercase;border:1px solid #1A1917;transition:background .2s,color .2s}\n.g-cta:hover{background:#EFECE6;color:#1A1917}\n@media(max-width:820px){.g-cta{right:16px;bottom:16px;padding:13px 18px}}')
    h = h.replace('</figure>\n</div>', '</figure>\n  <a class="g-cta" href="private.html">By invitation &rarr;</a>\n</div>', 1)
    h = h.replace('<div class="r"><a href="private.html">By invitation</a><span id="g-n">Los Angeles</span></div>',
                  '<div class="r"><a href="work.html">Selected work</a><span id="g-n">Los Angeles</span></div>')
wr('tools/pages/index.html', h)

# 3. private gate: light
p = rd('tools/pages/private.html')
rep = [
 ('.pv-gate{position:relative;min-height:100vh;display:grid;place-items:center;padding:140px var(--gutter) 100px;overflow:hidden;background:#000}',
  '.pv-gate{position:relative;min-height:100vh;display:grid;place-items:center;padding:140px var(--gutter) 100px;overflow:hidden;background:var(--bg)}'),
 ('center/cover;opacity:.28;transform:scale(1.04)}', 'center/cover;opacity:.10;filter:grayscale(1);transform:scale(1.04)}'),
 ('background:radial-gradient(ellipse at center,rgba(0,0,0,.2),rgba(0,0,0,.85) 75%)}', 'background:radial-gradient(ellipse at center,rgba(239,236,230,.2),rgba(239,236,230,.92) 75%)}'),
 ('.pv-gate .box{position:relative;text-align:center;max-width:560px;color:#fff}', '.pv-gate .box{position:relative;text-align:center;max-width:600px;color:var(--ink)}'),
 ('.pv-gate .mono{color:rgba(255,255,255,.65);margin-bottom:28px}', '.pv-gate .mono{color:var(--ink-2);margin-bottom:28px}'),
 ('.pv-gate h1{font-family:var(--serif);font-weight:400;font-size:clamp(40px,6vw,84px);line-height:1;letter-spacing:-.02em;max-width:none}', '.pv-gate h1{font-size:clamp(40px,6vw,84px);line-height:1;max-width:none}'),
 ('.pv-gate h1 i{font-style:italic}\n', ''),
 ('.pv-gate p.lede{margin:28px auto 0;max-width:46ch;color:rgba(255,255,255,.8);font-size:17px;line-height:1.6}', '.pv-gate p.lede{margin:28px auto 0;max-width:46ch;font-size:17px;line-height:1.6}'),
 ('.pv-code .in{display:flex;border:1px solid rgba(255,255,255,.35);background:rgba(0,0,0,.35)}', '.pv-code .in{display:flex;border:1px solid var(--ink);background:#fff}'),
 ('.pv-code input{flex:1;background:transparent;border:0;color:#fff;font-family:var(--mono);font-size:16px;letter-spacing:.22em;', '.pv-code input{flex:1;background:transparent;border:0;color:var(--ink);font-family:var(--mono);font-weight:600;font-size:15px;letter-spacing:.2em;'),
 ('.pv-code input::placeholder{color:rgba(255,255,255,.35);letter-spacing:.12em}', '.pv-code input::placeholder{color:var(--ink-3);letter-spacing:.12em;font-weight:500}'),
 ('.pv-code button{background:#fff;color:#000;border:0;padding:0 26px;font-family:var(--mono);font-size:12px;letter-spacing:.12em;text-transform:uppercase;cursor:pointer}', '.pv-code button{background:var(--ink);color:var(--bg);border:0;padding:0 26px;font-family:var(--mono);font-weight:600;font-size:11px;letter-spacing:.14em;text-transform:uppercase;cursor:pointer}'),
 ('.pv-code button:hover{background:var(--accent);color:#fff}', '.pv-code button:hover{background:#3A3835}'),
 ('.pv-code .msg{margin-top:14px;font-family:var(--mono);font-size:12px;letter-spacing:.05em;color:var(--accent);min-height:16px}', '.pv-code .msg{margin-top:14px;font-family:var(--mono);font-weight:600;font-size:11px;letter-spacing:.1em;color:#B3261E;min-height:16px}'),
 ('.pv-gate .foot{margin-top:56px;font-family:var(--mono);font-size:12px;letter-spacing:.05em;color:rgba(255,255,255,.55)}', '.pv-gate .foot{margin-top:56px;font-family:var(--mono);font-weight:500;font-size:12px;letter-spacing:.08em;color:var(--ink-2)}'),
 ('.pv-gate .foot a{color:#fff}', '.pv-gate .foot a{color:var(--ink);border-bottom:1px solid var(--ink)}'),
 ('<h1>The studio works with <i>a few.</i></h1>', '<h1>The studio works with a few.</h1>'),
 ("m.style.color='#fff'; m.textContent='Welcome.'", "m.style.color='var(--ink)'; m.textContent='Welcome.'"),
]
for a, b in rep:
    if a in p: p = p.replace(a, b)
wr('tools/pages/private.html', p)
print('theme applied')
