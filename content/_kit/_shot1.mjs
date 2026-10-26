import { chromium } from 'playwright';
const [url, out, w, h] = process.argv.slice(2);
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
const p = await b.newPage({ viewport: { width: +w, height: +h } });
await p.goto(url); await p.evaluate(() => window.ready);
await p.screenshot({ path: out }); await b.close();
