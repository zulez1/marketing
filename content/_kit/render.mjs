// Usage: node render.mjs week-01.mjs   (needs the kit served: python3 -m http.server 8766 in this folder)
import { chromium } from 'playwright';
import { mkdirSync } from 'fs';
import { dirname, resolve } from 'path';
const mod = await import('./' + process.argv[2]);
const only = process.argv[3];
const SIZES = { P: [1080, 1350], S: [1080, 1920], Q: [1080, 1080] };
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
const bad = [];
for (const s of mod.specs) {
  if (only && !s.out.includes(only)) continue;
  const [w, h] = SIZES[s.size];
  const p = await b.newPage({ viewport: { width: w, height: h } });
  if (s.theme === 'clear') await p.addStyleTag({ content: 'html,body{background:transparent!important}' }).catch(()=>{});
  await p.goto('http://127.0.0.1:8766/kit.html'); await p.evaluate(() => window.ready);
  await p.evaluate(s => window.renderSpec(s), s);
  if (await p.evaluate(() => window.OVERFLOW)) bad.push(s.out);
  const out = resolve(mod.dir, s.out); mkdirSync(dirname(out), { recursive: true });
  await p.screenshot({ path: out, omitBackground: s.theme === 'clear' }); await p.close();
}
await b.close();
console.log('rendered', mod.specs.length, bad.length ? 'OVERFLOW: ' + bad.join(', ') : 'no overflow');
