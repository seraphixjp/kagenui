/* カゲヌイ モバイル（アプリ版）の Service Worker
 * ・画面（同じオリジン）は「ネット優先・だめならキャッシュ」→ 更新はpushすれば次に開いたとき反映
 * ・CDNの部品（ZXing・フォント・文字認識など）は「キャッシュ優先」
 * ・データ（script.google.com への POST）には触らない
 */
const V = "km-v1";
const SHELL = ["./", "index.html", "manifest.webmanifest", "icon-192.png", "icon-512.png", "icon-180.png"];

self.addEventListener("install", (e) => {
  e.waitUntil(caches.open(V).then((c) => c.addAll(SHELL)).then(() => self.skipWaiting()));
});
self.addEventListener("activate", (e) => {
  e.waitUntil(caches.keys().then((ks) => Promise.all(ks.filter((k) => k !== V).map((k) => caches.delete(k)))).then(() => self.clients.claim()));
});
self.addEventListener("fetch", (e) => {
  const req = e.request;
  if (req.method !== "GET") return;
  const url = new URL(req.url);
  if (url.hostname.endsWith("google.com") || url.hostname.endsWith("googleusercontent.com")) return;
  if (url.origin === location.origin) {
    e.respondWith(fetch(req).then((res) => {
      if (res.ok) { const cp = res.clone(); caches.open(V).then((c) => c.put(req, cp)); }
      return res;
    }).catch(() => caches.match(req).then((r) => r || caches.match("index.html"))));
    return;
  }
  if (/(jsdelivr\.net|fonts\.googleapis\.com|fonts\.gstatic\.com)$/.test(url.hostname)) {
    e.respondWith(caches.match(req).then((hit) => hit || fetch(req).then((res) => {
      if (res.ok || res.type === "opaque") { const cp = res.clone(); caches.open(V).then((c) => c.put(req, cp)); }
      return res;
    })));
  }
});
