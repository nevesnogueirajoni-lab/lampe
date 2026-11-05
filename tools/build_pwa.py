#!/usr/bin/env python3
"""Construit la version autonome de Lampe (PWA) dans pwa/ : index.html, qb.js, config.js, manifest, service worker, icônes."""
import re, subprocess, pathlib, os, json, hashlib, math
from PIL import Image, ImageDraw
ESB = '/opt/npm-tools/node_modules/esbuild/bin/esbuild'
base = pathlib.Path(__file__).resolve().parent.parent
out = base / 'pwa'; out.mkdir(exist_ok=True)

def esb(code, loader):
    r = subprocess.run([ESB, f'--loader={loader}', '--minify', '--target=es2020', '--legal-comments=none', '--charset=utf8'],
                       input=code.encode(), capture_output=True)
    if r.returncode:
        raise SystemExit(r.stderr.decode())
    return r.stdout.decode().strip()

h = (base / 'index.html').read_text(encoding='utf-8')
# aucune donnée personnelle dans le code public
h = re.sub(r"let SETUP = \{[^}]*\};", "let SETUP = { prenom:'', langue:'fr', enfant:false, kprenom:'', kage:6, garde:false, jour:0, heure:'18:00', ici:null, vm:3, tg:6 };", h, count=1)
head = '''<meta name="theme-color" content="#d62976">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<meta name="apple-mobile-web-app-title" content="Lampe">
<link rel="manifest" href="manifest.webmanifest">
<link rel="apple-touch-icon" href="icon-180.png">
<link rel="icon" href="icon-192.png">
<script src="config.js"></script>
'''
h = h.replace('<title>', head + '<title>', 1)
h = h.replace('</body>', '''<script>if ('serviceWorker' in navigator) addEventListener('load', () => navigator.serviceWorker.register('sw.js').catch(() => {}));</script>
</body>''', 1)
h = re.sub(r'<style>([\s\S]*?)</style>', lambda m: '<style>' + esb(m.group(1), 'css') + '</style>', h, count=1)
h = re.sub(r'<script>([\s\S]*?)</script>', lambda m: '<script>' + esb(m.group(1), 'js').replace('</script', '<\\/script') + '</script>', h, count=1)
h = re.sub(r'<!--(?!\[)[\s\S]*?-->', '', h)
(out / 'index.html').write_text(h, encoding='utf-8')
(out / 'qb.js').write_text(esb((base / 'qb.js').read_text(encoding='utf-8'), 'js'), encoding='utf-8')
cfg = base / 'firebase-config.json'
conf = json.loads(cfg.read_text()) if cfg.exists() else None
(out / 'config.js').write_text('window.LAMPE_FB = ' + (json.dumps(conf) if conf else 'null') + ';\n', encoding='utf-8')
(out / '.nojekyll').write_text('')

# ---------- icônes ----------
def icon(size, path, pad=0.0):
    S = size * 4
    im = Image.new('RGB', (S, S))
    px = im.load()
    c1, c2, c3 = (250, 126, 30), (214, 41, 118), (150, 47, 191)
    for y in range(S):
        for x in range(S):
            t = (x + y) / (2 * S)
            a, b, u = (c1, c2, t / 0.5) if t < 0.5 else (c2, c3, (t - 0.5) / 0.5)
            px[x, y] = tuple(int(a[i] + (b[i] - a[i]) * u) for i in range(3))
    d = ImageDraw.Draw(im)
    cx, cy, r = S / 2, S * 0.56, S * 0.21 * (1 - pad)
    # flamme
    pts = []
    for k in range(0, 361, 4):
        th = math.radians(k)
        rr = r * (1 + 0.0 * math.cos(th))
        x = cx + rr * math.sin(th) * 0.78
        y = cy - rr * math.cos(th)
        if math.cos(th) > 0:  # partie haute étirée en pointe
            y = cy - rr * math.cos(th) * (1.9 - 0.9 * abs(math.sin(th)))
        pts.append((x, y))
    d.polygon(pts, fill=(255, 255, 255))
    ri = r * 0.45
    pts2 = [(cx + ri * math.sin(math.radians(k)) * 0.78, cy + r * 0.35 - (ri * math.cos(math.radians(k)) * ((1.9 - 0.9 * abs(math.sin(math.radians(k)))) if math.cos(math.radians(k)) > 0 else 1))) for k in range(0, 361, 4)]
    d.polygon(pts2, fill=(255, 200, 80))
    # coupe de la lampe
    d.rounded_rectangle([cx - S * 0.25, cy + r * 1.05, cx + S * 0.25, cy + r * 1.05 + S * 0.07], radius=S * 0.035, fill=(255, 255, 255))
    im = im.resize((size, size), Image.LANCZOS)
    im.save(out / path)
for s, n in ((180, 'icon-180.png'), (192, 'icon-192.png'), (512, 'icon-512.png')):
    icon(s, n)
icon(512, 'icon-maskable.png', pad=0.25)

manifest = {
    'name': 'Lampe — études bibliques en famille', 'short_name': 'Lampe', 'lang': 'fr', 'start_url': './', 'scope': './',
    'display': 'standalone', 'background_color': '#ffffff', 'theme_color': '#d62976',
    'icons': [{'src': 'icon-192.png', 'sizes': '192x192', 'type': 'image/png'},
              {'src': 'icon-512.png', 'sizes': '512x512', 'type': 'image/png'},
              {'src': 'icon-maskable.png', 'sizes': '512x512', 'type': 'image/png', 'purpose': 'maskable'}]}
(out / 'manifest.webmanifest').write_text(json.dumps(manifest, ensure_ascii=False, indent=1), encoding='utf-8')

files = ['./', 'index.html', 'qb.js', 'config.js', 'manifest.webmanifest', 'icon-180.png', 'icon-192.png', 'icon-512.png']
ver = hashlib.sha1(b''.join((out / f).read_bytes() for f in files[1:])).hexdigest()[:10]
sw = '''const V = 'lampe-%s'; const SHELL = %s; const FBV = 'https://www.gstatic.com/firebasejs/';
self.addEventListener('install', e => { e.waitUntil(caches.open(V).then(c => c.addAll(SHELL)).then(() => self.skipWaiting())); });
self.addEventListener('activate', e => { e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== V && k !== 'lampe-fb').map(k => caches.delete(k)))).then(() => self.clients.claim())); });
self.addEventListener('fetch', e => {
  const u = new URL(e.request.url); if (e.request.method !== 'GET') return;
  if (u.href.startsWith(FBV)) { e.respondWith(caches.open('lampe-fb').then(c => c.match(e.request).then(r => r || fetch(e.request).then(n => { if (n.ok) c.put(e.request, n.clone()); return n; })))); return; }
  if (u.origin !== location.origin) return;
  /* l'app : réseau d'abord (mises à jour), cache si hors ligne */
  e.respondWith(fetch(e.request).then(n => { if (n.ok) caches.open(V).then(c => c.put(e.request, n.clone())); return n; }).catch(() => caches.match(e.request, { ignoreSearch: true }).then(r => r || caches.match('index.html'))));
});
''' % (ver, json.dumps(files))
(out / 'sw.js').write_text(sw, encoding='utf-8')
for f in sorted(os.listdir(out)):
    print(f, os.path.getsize(out / f))
print('config Firebase :', 'oui' if conf else 'non (mode local)')
