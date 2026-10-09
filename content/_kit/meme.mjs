// Memes with the mascot. Render: node meme.mjs   (kit served on :8766)
import { chromium } from 'playwright';
const Z = n => `img/zubr-${n}.png`;
const specs = [
  { out: '01-drake-forum.png', type: 'rows', tag: 'Мем', rows: [
    { cls: 'no', img: Z('dumaet'), t: 'Ещё один форум, где два дня вдохновляют и рассказывают про мечту' },
    { cls: 'yes', img: Z('priglashaet'), t: 'Два дня разбирать свои цифры с теми, кто уже прошёл этот путь' } ] },
  { out: '02-mozg-uderzhanie.png', type: 'rows', tag: 'Мем', rows: [
    { cls: 'b1', img: Z('dumaet'), t: 'Привести больше учеников', size: 40 },
    { cls: 'b2', img: Z('networking'), t: 'Удержать тех, кто уже пришёл', size: 40 },
    { cls: 'b3', img: Z('flipchart'), t: 'Посчитать, сколько стоит каждый ушедший', size: 40 },
    { cls: 'b4', img: Z('priglashaet'), t: 'Разобрать это с теми, кто уже решил, — на РЕШЕНО', size: 40 } ] },
  { out: '03-roditelskiy-chat.png', type: 'chat', theme: 'ink', tag: 'Жиза владельца', img: Z('dumaet'),
    lines: ['<span>Никто:</span>', '<span>Абсолютно никто:</span>', 'Родительский чат<br>в 23:47:'],
    who: 'Мама Артёма', msg: 'А завтра тренировка точно будет? 🙂' },
];
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
for (const s of specs) {
  const p = await b.newPage({ viewport: { width: 1080, height: 1350 } });
  await p.goto('http://127.0.0.1:8766/meme.html'); await p.evaluate(s => window.build(s), s);
  await p.screenshot({ path: '../memy/' + s.out }); await p.close();
}
await b.close(); console.log('ok', specs.length);
