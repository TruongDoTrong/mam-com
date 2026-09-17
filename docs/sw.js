// Cho ung dung chay khi mat mang. Uu tien ban moi tren mang, mat mang thi dung ban da luu.
const KHO = "mamcom-v1";
const TEP = ["./", "index.html", "manifest.webmanifest", "icon-192.png", "icon-512.png"];
self.addEventListener("install", e => { e.waitUntil(caches.open(KHO).then(c => c.addAll(TEP))); self.skipWaiting(); });
self.addEventListener("activate", e => { e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== KHO).map(k => caches.delete(k))))); self.clients.claim(); });
self.addEventListener("fetch", e => {
  if (e.request.method !== "GET" || new URL(e.request.url).origin !== location.origin) return;
  e.respondWith(fetch(e.request).then(r => { const b = r.clone(); caches.open(KHO).then(c => c.put(e.request, b)); return r; })
    .catch(() => caches.match(e.request).then(r => r || caches.match("index.html"))));
});
