// Final week 08.11–12.11. Render: node render.mjs w-final.mjs [filter]
// Fill in the venue below and re-render when the team confirms it.
export const dir = '../nedelya-final_08.11-12.11';
const VENUE = '[Название площадки]', ADDRESS = '[Улица, дом]', REG = '[08:30]', CLOSE = '[время]';
const Z = n => `img/zubr-${n}.png`;
const P = { size: 'P', corner: '13–14.11 · Москва', bottom: { l: 'reshenoforum.ru' } };
const S = { size: 'S', corner: '', bottom: { l: 'reshenoforum.ru' } };
const days = n => n === 1 ? 'день' : n < 5 ? 'дня' : 'дней';
const q = (l) => `<span style="position:absolute;left:${l}%;top:4%;transform:translateX(-50%);font-family:Unbounded;font-weight:800;font-size:150px;color:#F0B90B;text-shadow:0 8px 30px rgba(0,0,0,.6)">?</span>`;
const sil = h => ({ type: 'html', html: `<div style="position:relative;height:${h}px;flex-shrink:0;overflow:hidden"><img src="img/siluety.png" style="display:block;width:100%;height:100%;object-fit:contain;object-position:bottom">${[16.6, 38.9, 61.1, 83.3].map(q).join('')}</div>` });
const TOP = [
  ['Роман Ольховский', 'эксперт комитета Госдумы по спорту'],
  ['Дмитрий Крикунов', '«Академия Будущего», 25 объектов в Москве'],
  ['Владислав Перескоков', 'ex-техдиректор Яндекса, Manager 360'],
  ['Ян Ванчайтис', '«Азбука тенниса», 180+ филиалов'],
  ['Георгий Кужим', 'инвестор, Juventus Academy в РФ'],
  ['Дмитрий Кибкало', 'сооснователь 5 бизнесов, «Метеор»'],
  ['Павел Черных', 'Школа CEO СПбГЭУ'],
  ['Андрей Коломеец', 'сеть «Юниор», 450+ филиалов'],
];
const topList = { type: 'html', html: `<div style="display:grid;gap:12px">${TOP.map(([n, r]) => `<div style="display:flex;align-items:center;gap:22px;background:#16181D;border:1.5px solid #2B2E35;border-radius:20px;padding:16px 26px"><span style="width:14px;height:14px;background:#F0B90B;border-radius:3px;transform:rotate(45deg);flex-shrink:0"></span><div><div style="font-family:Unbounded;font-weight:800;font-size:26px;text-transform:uppercase;color:#FAF8F3">${n}</div><div style="font-size:23px;font-weight:600;color:#C9CBD1;margin-top:4px">${r}</div></div></div>`).join('')}</div>` };
const countdown = (d, n, pose, theme) => ({ ...S, out: `storis-otschet/${d}-${n}.png`, theme, valign: 'flex-start', mainBottom: 1000,
  mascot: { src: Z(pose), h: 840, right: 120, bottom: 330, glow: theme === 'ink' },
  blocks: [{ type: 'tag', text: 'До форума' }, { type: 'gap', s: 's' }, { type: 'display', max: 360, lines: [String(n)] },
    { type: 'display', max: 130, lines: [days(n)] }, { type: 'gap', s: 's' }, { type: 'p', size: 32, html: '13–14 ноября · Москва' }] });

export const specs = [
  // Вс 08.11 — локация
  { ...P, out: '01-vs-08.11-lokaciya/post.png', theme: 'amber', valign: 'flex-start', mainRight: 400,
    mascot: { src: Z('priglashaet'), h: 820, right: -130, bottom: -30 },
    blocks: [{ type: 'tag', text: 'Локация есть' }, { type: 'gap', s: 'm' },
      { type: 'display', max: 110, lines: ['Где мы', { t: 'встретимся?', c: 'acc' }] }, { type: 'gap', s: 'm' },
      { type: 'card', size: 40, kicker: 'Площадка', html: VENUE }, { type: 'gap', s: 's' },
      { type: 'card', size: 34, kicker: 'Адрес', html: ADDRESS }, { type: 'gap', s: 'm' },
      { type: 'p', size: 30, html: '<b>13–14 ноября.</b> Удобная логистика, современный зал и всё для продуктивной работы' }] },
  { ...S, out: '01-vs-08.11-lokaciya/storis-marshrut.png', theme: 'ink', valign: 'flex-start', mainBottom: 760,
    mascot: { src: Z('dumaet'), h: 620, right: 470, bottom: 300, glow: true },
    blocks: [{ type: 'tag', text: 'Локация' }, { type: 'gap', s: 's' },
      { type: 'display', max: 120, lines: ['Строим', 'маршрут', { t: 'заранее', c: 'acc' }] }, { type: 'gap', s: 's' },
      { type: 'p', size: 34, html: `<b>${VENUE}</b><br>${ADDRESS}` }] },
  countdown('08.11', 5, 'priglashaet', 'amber'),

  // Пн 09.11 — альтернативная стоимость
  { ...P, out: '02-pn-09.11-cena-oshibki/post.png', theme: 'ink', valign: 'flex-start', mainRight: 90,
    blocks: [{ type: 'tag', text: 'Альтернативная стоимость' }, { type: 'gap', s: 'm' },
      { type: 'display', max: 130, lines: ['Сколько', 'стоит', { t: 'ошибка?', c: 'acc' }] }, { type: 'gap', s: 'm' },
      { type: 'card', size: 34, kicker: 'Неверная стратегия', html: 'Месяцы работы и упущенная прибыль' }, { type: 'gap', s: 's' },
      { type: 'card', size: 34, kicker: 'Билет на РЕШЕНО', html: 'Как одна консультация, <span style="color:#F0B90B">которая может сэкономить год</span>' }] },
  { ...S, out: '02-pn-09.11-cena-oshibki/storis-vopros.png', theme: 'ink', valign: 'flex-start', mainBottom: 700,
    mascot: { src: Z('facepalm'), h: 700, right: 160, bottom: 300, glow: true },
    blocks: [{ type: 'tag', text: 'Вопрос' }, { type: 'gap', s: 's' },
      { type: 'display', max: 92, lines: ['Сколько стоила', 'ваша самая', { t: 'дорогая ошибка?', c: 'acc' }] }, { type: 'gap', s: 'm' },
      { type: 'sticker', h: 230, text: 'Сюда — стикер «Вопрос»' }] },
  countdown('09.11', 4, 'dumaet', 'ink'),

  // Вт 10.11 — спикер, которого вы не знали
  { ...P, out: '03-vt-10.11-spiker-zagadka/post.png', theme: 'ink', valign: 'flex-start', mainRight: 90, mainBottom: 150,
    blocks: [{ type: 'tag', text: 'Угадайте спикера' }, { type: 'gap', s: 'm' },
      { type: 'display', max: 92, lines: ['Кто из них', 'работал с ООН', { t: 'и Всемирным банком?', c: 'acc' }] }, { type: 'gap', s: 's' }, { type: 'p', size: 30, html: 'А кто — доктор наук по управлению коллективным бессознательным? <b>Узнаете лично</b>' }, { type: 'grow' }, sil(620)] },
  countdown('10.11', 3, 'podmigivaet', 'amber'),

  // Ср 11.11 — топ-спикеры + как подготовиться
  { ...P, out: '04-sr-11.11-top-spikery/post.png', theme: 'ink', valign: 'flex-start', mainRight: 90,
    blocks: [{ type: 'display', max: 72, lines: ['Те, ради кого', { t: 'стоит ехать в Москву', c: 'acc' }] }, { type: 'gap', s: 's' }, topList] },
  { ...P, out: '04-sr-11.11-top-spikery/post-podgotovka.png', theme: 'paper', valign: 'flex-start', mainRight: 90, mainBottom: 560,
    mascot: { src: Z('flipchart'), h: 520, right: 60, bottom: 40 },
    blocks: [{ type: 'tag', text: 'Чек-лист' }, { type: 'gap', s: 's' },
      { type: 'display', max: 100, lines: ['Как подготовиться', { t: 'за 2 дня', c: 'acc' }] }, { type: 'gap', s: 's' },
      { type: 'list', items: [['01', 'Сформулируйте главный бизнес-вопрос'], ['02', 'Возьмите визитки'], ['03', 'Блокнот и хорошее настроение']] }] },
  countdown('11.11', 2, 'klass', 'ink'),

  // Чт 12.11 — завтра старт
  { ...P, out: '05-cht-12.11-zavtra-start/post.png', theme: 'amber', valign: 'flex-start', mainRight: 300,
    mascot: { src: Z('aplodiruet'), h: 620, right: -40, bottom: -20 },
    blocks: [{ type: 'tag', text: 'Готовы на 99%' }, { type: 'gap', s: 'm' },
      { type: 'display', max: 170, lines: ['Завтра', { t: 'старт', c: 'acc' }] }, { type: 'gap', s: 'm' },
      { type: 'list', items: [['Где', `${VENUE}`], ['Когда', `13.11, регистрация с ${REG}`], ['Билеты', `закрываются сегодня в ${CLOSE}`]] },
      ] },
  countdown('12.11', 1, 'aplodiruet', 'amber'),
];
