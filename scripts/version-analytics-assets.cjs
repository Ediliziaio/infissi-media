// Build-time only: keep consented analytics on generated public pages and make
// browsers fetch the reviewed JS when a previously cached implementation changes.
const fs = require('node:fs');
const path = require('node:path');
const { createHash } = require('node:crypto');
const root = path.resolve(__dirname, '..');
const tracking = ['analytics-config.js', 'analytics-loader.js', 'consent-adapter.js'];
const config = fs.readFileSync(path.join(root, 'assets/tracking/analytics-config.js'), 'utf8');
const kind = (config.match(/"kind"\s*:\s*"([a-z]+)"/) || [])[1];
const core = { gs: ['styles.css', 'config.js', 'script.js'], ic: ['js/main.js'], ge: [], im: [], ie: ['styles.css', 'config.js', 'tracking.js'] }[kind];
if (!core) throw new Error('Unknown static consent adapter kind');
const assets = [...core, ...tracking.map(name => 'assets/tracking/' + name)];
const hashes = new Map(assets.map(name => {
  const absolute = path.join(root, name);
  return [absolute, createHash('sha256').update(fs.readFileSync(absolute)).digest('hex').slice(0, 12)];
}));
const tags = tracking.map(name => {
  const relative = 'assets/tracking/' + name;
  return `<script defer src="/${relative}?v=${hashes.get(path.join(root, relative))}"></script>`;
}).join('\n') + '\n';
let changed = 0;
function walk(dir) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    if (entry.name.startsWith('.') || ['node_modules', 'dist', 'admin', 'admin-cms', 'scripts', 'tools'].includes(entry.name)) continue;
    const file = path.join(dir, entry.name);
    if (entry.isDirectory()) { walk(file); continue; }
    if (!entry.name.endsWith('.html')) continue;
    const source = fs.readFileSync(file, 'utf8');
    if (!source.includes('</head>')) continue;
    let output = source.replace(/<script\b[^>]*\bsrc=(["'])\/assets\/tracking\/(?:analytics-config|analytics-loader|consent-adapter)\.js(?:\?[^"']*)?\1[^>]*>\s*<\/script>\s*/gi, '');
    output = output.replace('</head>', tags + '</head>');
    output = output.replace(/\b(src|href)=(["'])([^"']+)\2/g, (full, attr, quote, url) => {
      if (/^(?:[a-z]+:|\/\/|#)/i.test(url)) return full;
      const relative = url.split(/[?#]/, 1)[0];
      const asset = relative.startsWith('/') ? path.join(root, relative.slice(1)) : path.resolve(path.dirname(file), relative);
      const hash = hashes.get(asset);
      return hash ? `${attr}=${quote}${relative}?v=${hash}${quote}` : full;
    });
    if (output !== source) { fs.writeFileSync(file, output); changed++; }
  }
}
walk(root);
console.log(`Versioned consent assets on ${changed} public pages; editorial body content is unchanged.`);
