import { cpSync, existsSync, mkdirSync, readdirSync, rmSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = dirname(dirname(fileURLToPath(import.meta.url)));
const out = join(root, 'dist');
const directories = new Set(['guide-pratiche', 'speciali-aziende', 'editorial-assets', 'articoli', 'css', 'js', 'assets', 'fonts']);
const publicFile = /\.(html|xml|txt|ico|png|webmanifest)$/i;

// Keep the deploy artifact separate from generators, server code and config.
rmSync(out, { recursive: true, force: true });
mkdirSync(out);
for (const entry of readdirSync(root, { withFileTypes: true })) {
  const include = entry.isDirectory()
    ? directories.has(entry.name)
    : publicFile.test(entry.name) || entry.name === 'eic-lead.js';
  if (include) cpSync(join(root, entry.name), join(out, entry.name), { recursive: true });
}
for (const required of ['index.html', '404.html', 'robots.txt', 'sitemap.xml', 'feed.xml']) {
  if (!existsSync(join(out, required))) throw new Error(`Missing public output: ${required}`);
}
const pages = readdirSync(out, { recursive: true }).filter(file => file.endsWith('.html'));
console.log(`Static build: ${pages.length} complete HTML pages in dist/`);
