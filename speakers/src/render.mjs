import { chromium } from 'playwright';
const A = '../assets/';
const base = { first: 'Имя', last: 'Фамилия', role: 'Должность, компания', topic: 'Название темы — что спикер разберёт на форуме', cta: 'Подробнее — по ссылке' };
const cards = [
  { out: '../post-speaker1.png', story: false, bg: A + 'bg_IMG_2335.jpg', paper: A + 'speaker1_paper.png', photo: A + 'speaker1_cutout.png' },
  { out: '../post-speaker2.png', story: false, bg: A + 'bg_IMG_2378.jpg', paper: A + 'speaker2_paper.png', photo: A + 'speaker2_cutout.png' },
  { out: '../story-speaker1.png', story: true, bg: A + 'bg_IMG_2335_story.jpg', paper: A + 'speaker1_paper.png', photo: A + 'speaker1_cutout.png' },
  { out: '../story-speaker2.png', story: true, bg: A + 'bg_IMG_2345_story.jpg', paper: A + 'speaker2_paper.png', photo: A + 'speaker2_cutout.png' },
];
// colour versions: same layout, colour photo of the speaker
for (const c of [...cards]) cards.push({ ...c, out: c.out.replace('.png', '-color.png'), photo: c.photo.replace('_cutout', '_cutout_color') });
// speakers 3+: colour cards only (post + story)
const BG = ['IMG_2345', 'IMG_2416', 'IMG_2335', 'IMG_2378'];
for (const n of [3, 4, 5, 6]) {
  const bg = BG[(n - 3) % BG.length];
  cards.push({ out: `../post-speaker${n}-color.png`, story: false, bg: A + `bg_${bg}.jpg`, paper: A + `speaker${n}_paper.png`, photo: A + `speaker${n}_cutout_color.png` });
  cards.push({ out: `../story-speaker${n}-color.png`, story: true, bg: A + `bg_${bg}_story.jpg`, paper: A + `speaker${n}_paper.png`, photo: A + `speaker${n}_cutout_color.png` });
}
const only = process.argv[2];
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
for (const c of cards) {
  if (only && !c.out.includes(only)) continue;
  const p = await b.newPage({ viewport: { width: 1080, height: c.story ? 1920 : 1350 } });
  await p.goto('http://127.0.0.1:8767/speakers/src/card.html');
  await p.evaluate(s => window.build(s), { ...base, ...c });
  await p.screenshot({ path: c.out }); await p.close();
}
await b.close(); console.log('ok');
