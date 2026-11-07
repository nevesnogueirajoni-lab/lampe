const V = 'lampe-5ea9e30167'; const SHELL = ["./", "index.html", "qb.js", "config.js", "manifest.webmanifest", "icon-180.png", "icon-192.png", "icon-512.png"]; const FBV = 'https://www.gstatic.com/firebasejs/';
self.addEventListener('install', e => { e.waitUntil(caches.open(V).then(c => c.addAll(SHELL)).then(() => self.skipWaiting())); });
self.addEventListener('activate', e => { e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== V && k !== 'lampe-fb').map(k => caches.delete(k)))).then(() => self.clients.claim())); });
self.addEventListener('fetch', e => {
  const u = new URL(e.request.url); if (e.request.method !== 'GET') return;
  if (u.href.startsWith(FBV)) { e.respondWith(caches.open('lampe-fb').then(c => c.match(e.request).then(r => r || fetch(e.request).then(n => { if (n.ok) c.put(e.request, n.clone()); return n; })))); return; }
  if (u.origin !== location.origin) return;
  /* l'app : réseau d'abord (mises à jour), cache si hors ligne */
  e.respondWith(fetch(e.request).then(n => { if (n.ok) caches.open(V).then(c => c.put(e.request, n.clone())); return n; }).catch(() => caches.match(e.request, { ignoreSearch: true }).then(r => r || caches.match('index.html'))));
});
