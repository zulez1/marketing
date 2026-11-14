// node shot.mjs page.html out.png [scale]   — one still, 1920x1080 × scale
import { chromium } from 'playwright';
const [page, out, sc] = process.argv.slice(2);
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
const p = await b.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: Number(sc || 1) });
await p.goto('http://127.0.0.1:8767/ekran/src/' + page); await p.evaluate(() => window.ready);
await p.screenshot({ path: out }); await b.close();
