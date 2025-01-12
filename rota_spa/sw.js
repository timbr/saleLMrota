const CACHE_NAME = 'sale-lm-rota-v1';
const urlsToCache = [
  '/saleLMrota/',
  '/saleLMrota/index.html',
  '/saleLMrota/styles.css',
  '/saleLMrota/app.js',
  '/saleLMrota/manifest.json'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => cache.addAll(urlsToCache))
  );
});

self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request)
      .then((response) => response || fetch(event.request))
  );
});
