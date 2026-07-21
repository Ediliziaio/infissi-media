/**
 * Infissi Media — zero-dependency static dev server.
 * Usage: npm run dev [-- --port 7100 --host 0.0.0.0]
 * Forwards --port / --host CLI arguments.
 */
const http = require('http');
const fs = require('fs');
const path = require('path');

const argv = process.argv.slice(2);
function arg(name, fallback) {
  const i = argv.indexOf('--' + name);
  if (i > -1 && argv[i + 1]) return argv[i + 1];
  const eq = argv.find(a => a.startsWith('--' + name + '='));
  if (eq) return eq.split('=')[1];
  return fallback;
}

const PORT = parseInt(arg('port', '7100'), 10);
const HOST = arg('host', '0.0.0.0');
const ROOT = __dirname;

const MIME = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'application/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.xml': 'application/xml; charset=utf-8',
  '.txt': 'text/plain; charset=utf-8',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.webp': 'image/webp',
  '.svg': 'image/svg+xml',
  '.ico': 'image/x-icon',
  '.woff2': 'font/woff2',
  '.webmanifest': 'application/manifest+json'
};

http.createServer((req, res) => {
  try {
    let urlPath = decodeURIComponent(req.url.split('?')[0]);
    if (urlPath.endsWith('/')) urlPath += 'index.html';
    if (!path.extname(urlPath)) urlPath += '.html';
    const filePath = path.join(ROOT, path.normalize(urlPath));
    if (!filePath.startsWith(ROOT)) { res.writeHead(403); res.end('Forbidden'); return; }
    fs.readFile(filePath, (err, data) => {
      if (err) { res.writeHead(404, { 'Content-Type': 'text/html; charset=utf-8' }); res.end('<h1>404 — Pagina non trovata</h1><p><a href="/">Torna alla home</a></p>'); return; }
      res.writeHead(200, { 'Content-Type': MIME[path.extname(filePath).toLowerCase()] || 'application/octet-stream', 'Cache-Control': 'no-cache' });
      res.end(data);
    });
  } catch (e) {
    res.writeHead(500); res.end('Server error');
  }
}).listen(PORT, HOST, () => {
  console.log(`Infissi Media dev server → http://localhost:${PORT}/`);
});
