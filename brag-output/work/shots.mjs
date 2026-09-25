import { chromium } from 'playwright';
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
const p = await b.newPage({ viewport: { width: 1080, height: 1350 } });
await p.goto('http://127.0.0.1:8765/carousel.html'); await p.evaluate(() => window.ready);
const ids = ['s1','s2','s3','s4','s5','s6','s7','p1'];
for (const [i,id] of ids.entries()) {
  await p.evaluate(id => window.show(id), id);
  const name = id === 'p1' ? '../post-business-live.png' : `../carousel/slide-${i+1}.png`;
  await p.screenshot({ path: name });
}
await b.close();
