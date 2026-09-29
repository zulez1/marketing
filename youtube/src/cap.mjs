// node cap.mjs <scene> stills t1 t2 ...   |   node cap.mjs <scene> frames <outdir>
import { chromium } from 'playwright';
import { mkdirSync } from 'fs';
const [scene, mode, ...rest] = process.argv.slice(2);
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
await p.goto('http://127.0.0.1:8767/youtube/src/yt.html'); await p.evaluate(() => window.ready);
await p.evaluate(n => window.setup(n), scene);
if (mode === 'stills') {
  mkdirSync('stills', { recursive: true });
  for (const t of rest.map(Number)) { await p.evaluate(t => window.render(t), t); await p.screenshot({ path: `stills/${scene}-${t.toFixed(2)}.png`, omitBackground: true }); }
} else {
  const out = rest[0]; mkdirSync(out, { recursive: true });
  const dur = await p.evaluate(() => window.DURATION), n = Math.round(dur * 30);
  for (let i = 0; i < n; i++) { await p.evaluate(t => window.render(t), i / 30); await p.screenshot({ path: `${out}/f${String(i).padStart(4, '0')}.png`, omitBackground: true }); }
  console.log(scene, n, 'frames');
}
await b.close();
