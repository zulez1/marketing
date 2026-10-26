import { chromium } from 'playwright';
const P = (i) => ({ id: 'speaker' + i, name: 'Имя<br>Фамилия', role: 'Должность, компания' });
const specs = [
  { out: '../nedelya-5_27.10-02.11/03-spikery-vmeste/slide-6.png', title: '<i>6 спикеров</i><br>РЕШЕНО', people: [1, 2, 3, 4, 5, 6].map(P) },
  { out: '../nedelya-5_27.10-02.11/03-spikery-vmeste/slide-2.png', title: 'Спикеры<br><i>РЕШЕНО</i>', people: [1, 2].map(P) },
];
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
for (const s of specs) { const p = await b.newPage({ viewport: { width: 1080, height: 1350 } });
  await p.goto('http://127.0.0.1:8767/content/_kit/speakers.html'); await p.evaluate(s => window.build(s), s); await p.screenshot({ path: s.out }); await p.close(); }
await b.close(); console.log('ok');
