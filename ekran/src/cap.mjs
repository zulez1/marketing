// node cap.mjs stills t1 t2 ...  |  node cap.mjs frames <outdir>   (repo root served on :8767)
import { chromium } from 'playwright';
import { mkdirSync } from 'fs';
const [mode, ...rest] = process.argv.slice(2);
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
await p.goto('http://127.0.0.1:8767/ekran/src/ekran.html'); await p.evaluate(() => window.ready);
if (mode === 'stills') {
  mkdirSync('stills', { recursive: true });
  for (const t of rest.map(Number)) { await p.evaluate(t => window.render(t), t); await p.screenshot({ path: `stills/t-${t.toFixed(1)}.png` }); }
} else {
  const out = rest[0]; mkdirSync(out, { recursive: true });
  const n = Math.round(await p.evaluate(() => window.DURATION) * 30);
  for (let i = 0; i < n; i++) { await p.evaluate(t => window.render(t), i / 30); await p.screenshot({ path: `${out}/f${String(i).padStart(4, '0')}.jpg`, type: 'jpeg', quality: 95 }); }
  console.log(n, 'frames');
}
await b.close();
