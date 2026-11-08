import { readFileSync, writeFileSync, readdirSync, existsSync } from 'node:fs';
import { join, resolve, relative } from 'node:path';
const root = process.cwd();
const policy = JSON.parse(readFileSync(join(root, 'editorial-length-policy.json'), 'utf8'));
const output = resolve(root, process.argv[2] || 'dist');
if (!existsSync(output)) throw new Error(`Missing production HTML directory: ${relative(root, output)}`);
const required = new Set(policy.requiredSlugs);
const seen = new Set();
const reports = [];
const problems = [];
const decode = s => s.replace(/&(?:amp|lt|gt|quot|apos|nbsp|#39|#x27);/gi, m => ({'&amp;':'&','&lt;':'<','&gt;':'>','&quot;':'"','&apos;':"'",'&nbsp;':' ','&#39;':"'",'&#x27;':"'"}[m.toLowerCase()] || m)).replace(/&#(\d+);/g, (_,n) => String.fromCodePoint(Number(n))).replace(/&#x([\da-f]+);/gi, (_,n) => String.fromCodePoint(parseInt(n,16)));
function attrs(tag) {
 const out = {};
 for (const m of tag.matchAll(/([\w:-]+)(?:\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s>]+)))?/g)) out[m[1].toLowerCase()] = decode(m[2] ?? m[3] ?? m[4] ?? '');
 return out;
}
function articleDates(html) {
 const dates = [];
 function visit(v) {
  if (!v || typeof v !== 'object') return;
  if (Array.isArray(v)) { v.forEach(visit); return; }
  const types = Array.isArray(v['@type']) ? v['@type'] : [v['@type']];
  if (types.some(t => ['Article','NewsArticle','BlogPosting','TechArticle'].includes(t)) && typeof v.datePublished === 'string') dates.push(v.datePublished.slice(0,10));
  if (v['@graph']) visit(v['@graph']);
 }
 for (const m of html.matchAll(/<script\b[^>]*type=["']application\/ld\+json["'][^>]*>([\s\S]*?)<\/script>/gi)) {
  try { visit(JSON.parse(m[1])); } catch { /* Other metadata validation checks malformed JSON-LD. */ }
 }
 return dates;
}
function bodyHTML(clean) {
 const open = clean.match(/<([a-z][\w:-]*)\b[^>]*\bdata-editorial-body(?=\s|=|>)[^>]*>/i);
 if (!open) return null;
 const tag = open[1].toLowerCase();
 const start = open.index + open[0].length;
 const scanner = /<\/?([a-z][\w:-]*)\b[^>]*>/gi;
 scanner.lastIndex = start;
 let depth = 1, m;
 while ((m = scanner.exec(clean))) {
  if (m[1].toLowerCase() !== tag) continue;
  if (/^<\//.test(m[0])) depth--;
  else if (!/\/\s*>$/.test(m[0])) depth++;
  if (!depth) return clean.slice(start, m.index);
 }
 throw new Error('Unclosed data-editorial-body container');
}
const voidTags = new Set(['area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr']);
const omitted = new Set(['aside','nav','figure','form','footer','button','iframe']);
function bodyText(html) {
 const stack = [];
 const parts = [];
 for (const m of html.matchAll(/<[^>]*>|[^<]+/g)) {
  const token = m[0];
  if (!token.startsWith('<')) { if (!stack.at(-1)?.omit) parts.push(decode(token)); continue; }
  const tag = token.match(/^<\/?([a-z][\w:-]*)/i)?.[1]?.toLowerCase();
  if (!tag) continue;
  if (/^<\//.test(token)) {
   const index = stack.map(x => x.tag).lastIndexOf(tag);
   if (index >= 0) stack.length = index;
   continue;
  }
  const a = attrs(token);
  const omit = !!stack.at(-1)?.omit || omitted.has(tag) || /pubblicit|advertisement|sponsored placement/i.test(a['aria-label'] || '') || /(?:^|\s)(?:ad-slot|ad-placeholder|ad-container|ad-label)(?:\s|$)/.test(a.class || '') || 'data-ad-slot' in a;
  if (!voidTags.has(tag) && !/\/\s*>$/.test(token)) stack.push({tag,omit});
 }
 return parts.join(' ').replace(/\s+/g,' ').trim();
}
function walk(dir) {
 for (const item of readdirSync(dir,{withFileTypes:true})) {
  const file = join(dir,item.name);
  if (item.isDirectory()) { walk(file); continue; }
  if (!item.name.endsWith('.html')) continue;
  const html = readFileSync(file,'utf8');
  const clean = html.replace(/<!--[^]*?-->/g,' ').replace(/<(script|style|noscript)\b[^>]*>[\s\S]*?<\/\1>/gi,' ');
  const metas = [...clean.matchAll(/<meta\b[^>]*>/gi)].map(m => attrs(m[0]));
  if (metas.some(a => (a['http-equiv'] || '').toLowerCase() === 'refresh') && metas.some(a => (a.name || '').toLowerCase() === 'robots' && /noindex/i.test(a.content || ''))) continue;
  const canonical = [...clean.matchAll(/<link\b[^>]*>/gi)].map(m => attrs(m[0])).find(a => (a.rel || '').split(/\s+/).includes('canonical'))?.href;
  if (!canonical) continue;
  let slug;
  try { slug = new URL(canonical).pathname.split('/').filter(Boolean).at(-1)?.replace(/\.html$/,''); } catch { continue; }
  const dates = articleDates(html);
  if (!dates.length && metas.some(a => (a.name || "").toLowerCase() === "robots" && /noindex/i.test(a.content || ""))) continue;
  if (!required.has(slug) && !dates.some(d => d >= policy.enforcePublishedOnOrAfter)) continue;
  if (required.has(slug)) seen.add(slug);
  let body;
  try { body = bodyHTML(clean); } catch(e) { problems.push(`${slug}: ${e.message}`); continue; }
  if (body === null) { problems.push(`${slug}: missing data-editorial-body marker`); continue; }
  const text = bodyText(body);
  const words = text.split(/\s+/).filter(w => /[\p{L}\p{N}]/u.test(w)).length;
  reports.push({slug,canonical,words,file:relative(root,file)});
  if (words < policy.minimumWords) problems.push(`${slug}: ${words} words; minimum ${policy.minimumWords}`);
 }
}
walk(output);
for (const slug of required) if (!seen.has(slug)) problems.push(`${slug}: missing production article HTML`);
writeFileSync(join(root,'.editorial-length-report.json'),JSON.stringify({minimumWords:policy.minimumWords,articles:reports,errors:problems},null,2)+'\n');
for (const row of reports) console.log(`Editorial length: ${row.slug}: ${row.words} words`);
if (problems.length) throw new Error(`Editorial word-count check failed:\n${problems.join('\n')}`);
console.log(`Editorial minimum verified: ${reports.length} articles, at least ${policy.minimumWords} body words each.`);
