// node cap_zubr.mjs outdir dur  -> frames of zubr.html at 30 fps
import { chromium } from 'playwright';
import { mkdirSync } from 'fs';
const [out, dur] = [process.argv[2], +process.argv[3]];
mkdirSync(out, { recursive: true });
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
await p.goto('http://127.0.0.1:8767/reels/src/zubr.html'); await p.evaluate(() => window.ready);
const n = Math.round(dur * 30);
for (let i = 0; i < n; i++) {
  await p.evaluate(t => window.render(t), i / 30);
  await p.evaluate(() => Promise.all([...document.images].map(i => i.decode().catch(() => {}))));
  await p.screenshot({ path: `${out}/f${String(i).padStart(4, '0')}.png` });
}
await b.close(); console.log('frames', n);
