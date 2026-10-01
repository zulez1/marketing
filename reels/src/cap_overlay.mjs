// node cap_overlay.mjs overlay.json outdir  -> transparent PNG frames at 30 fps
import { chromium } from 'playwright';
import { mkdirSync, readFileSync } from 'fs';
const [specPath, out] = process.argv.slice(2);
const spec = JSON.parse(readFileSync(specPath, 'utf8'));
mkdirSync(out, { recursive: true });
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
await p.goto('http://127.0.0.1:8767/reels/src/overlay.html'); await p.evaluate(() => window.ready);
await p.evaluate(s => window.setup(s), spec);
const n = Math.round(spec.dur * 30);
for (let i = 0; i < n; i++) {
  await p.evaluate(t => window.render(t), i / 30);
  await p.screenshot({ path: `${out}/f${String(i).padStart(4, '0')}.png`, omitBackground: true });
}
await b.close();
console.log('overlay frames', n);
