// Examples with the mascot (bison). Render: node render.mjs mascot.mjs
export const dir = '../../mascot/primery';
const swipe = { r: '<span class="arrow">Листай <i>→</i></span>' };
const D = '13–14 ноября 2026 · Москва';
export const specs = [
  // смешнявка: жиза владельца
  { out: '1-smeshnoe-zhiza.png', size: 'P', theme: 'paper', corner: 'Жиза владельца', mainRight: 470,
    mascot: { src: 'img/bizon-dumaet.png', h: 1000, right: -150, bottom: -10 },
    bottom: { l: D }, blocks: [
      { type: 'tag', text: 'Родитель' }, { type: 'gap', s: 's' },
      { type: 'display', max: 90, lines: ['«А можно', 'заморозить', 'абонемент', { t: 'на лето?»', c: 'acc' }] },
      { type: 'gap', s: 'l' },
      { type: 'p', html: 'Владелец спортшколы<br><b>в этот момент:</b>' },
    ] },
  // полезняшка: обложка карусели
  { out: '2-polza-oblozhka.png', size: 'P', theme: 'ink', corner: 'Полезняшка', valign: 'flex-start', mainBottom: 700,
    mascot: { src: 'img/bizon-flipchart.png', h: 640, right: 40, bottom: 140, glow: true },
    bottom: { l: 'Сохраните, пригодится', ...swipe }, blocks: [
      { type: 'display', max: 110, lines: ['Сколько стоит', { t: 'потерянный', c: 'acc' }, { t: 'клиент?', c: 'acc' }] },
      { type: 'gap', s: 's' },
      { type: 'p', html: 'Считаем на примере школы — <b>листайте</b>' },
    ] },
  // продажа
  { out: '3-prodazha.png', size: 'P', theme: 'amber', corner: '13–14.11 · Москва', mainRight: 500,
    mascot: { src: 'img/bizon-priglashaet.png', h: 1020, right: -190, bottom: -10 },
    bottom: { l: 'reshenoforum.ru' }, blocks: [
      { type: 'display', max: 120, lines: ['Ваше место', 'на РЕШЕНО', { t: 'уже ждёт', c: 'acc' }] },
      { type: 'gap', s: 'm' },
      { type: 'p', html: '200–300 участников — <b>специально мало</b>' },
      { type: 'gap', s: 'l' },
      { type: 'btn', text: 'Забронировать' },
    ] },
  // сторис: выбираем имя маскоту
  { out: '4-storis-imya.png', size: 'S', theme: 'ink', corner: '', valign: 'flex-start', mainBottom: 1000,
    mascot: { src: 'img/bizon-dumaet.png', h: 860, right: 150, bottom: 330, glow: true },
    bottom: { l: 'Голосуйте в опросе ↓' }, blocks: [
      { type: 'tag', text: 'Знакомьтесь' }, { type: 'gap', s: 's' },
      { type: 'display', max: 130, lines: ['Как его', { t: 'назовём?', c: 'acc' }] },
    ] },
];
