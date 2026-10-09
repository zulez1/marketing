// Memes for weeks 3–4. Render: node meme.mjs memy-w34.mjs
export const dir = '../nedeli-3-4_12.10-25.10';
const Z = n => `img/zubr-${n}.png`;
const L = (l, t) => `<span><span class="lbl">${l}</span>${t}</span>`;
export const specs = [
  { out: '03-sr-14.10-mem-roditelskiy-chat/mem.png', type: 'chat', theme: 'ink', tag: 'Жиза владельца', img: Z('zlitsya'),
    lines: ['<span>Никто:</span>', '<span>Абсолютно никто:</span>', 'Родительский чат<br>в 23:47:'], who: 'Мама Артёма', msg: 'А завтра тренировка точно будет? 🙂' },
  { out: '05-pt-16.10-mem-net-da/mem.png', type: 'rows', tag: 'Мем', rows: [
    { cls: 'no', img: Z('zakatyvaet-glaza'), t: 'Ещё один форум, где два дня вдохновляют и рассказывают про мечту' },
    { cls: 'yes', img: Z('klass'), t: 'Два дня разбирать свои цифры с теми, кто уже прошёл этот путь' }] },
  { out: '07-vs-18.10-kakoy-ty-zubr/mem.png', type: 'grid', theme: 'ink', tag: 'Вопрос дня',
    title: 'Какой ты зубр <span>сегодня?</span>', cells: [Z('spit'), Z('zlitsya'), Z('ustal'), Z('v-shoke'), Z('smeetsya'), Z('klass')] },
  { out: '09-vt-20.10-mem-ozhidanie-realnost/mem.png', type: 'rows', tag: 'Мем', rows: [
    { cls: 'yes', img: Z('klass'), t: L('Ожидание', 'Открою второй филиал — будет в два раза больше денег') },
    { cls: 'no', img: Z('ustal'), t: L('Реальность', 'В два раза больше чатов, тренеров и отчётов') }] },
  { out: '11-cht-22.10-mem-urovni/mem.png', type: 'rows', tag: 'Мем', rows: [
    { cls: 'b1', img: Z('dumaet'), t: 'Привести больше учеников', size: 40 },
    { cls: 'b2', img: Z('networking'), t: 'Удержать тех, кто уже пришёл', size: 40 },
    { cls: 'b3', img: Z('flipchart'), t: 'Посчитать, сколько стоит каждый ушедший', size: 40 },
    { cls: 'b4', img: Z('aplodiruet'), t: 'Разобрать это с теми, кто уже решил, — на РЕШЕНО', size: 40 }] },
];
