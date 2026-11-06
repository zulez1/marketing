// Post «Выключите телефон на неделю». Render: node render.mjs telefon.mjs
export const dir = '../posty-noyabr';
const Z = n => `img/zubr-${n}.png`;
const base = { theme: 'ink', corner: '13–14.11 · Москва', valign: 'center', mainRight: 400, bottom: { l: 'reshenoforum.ru' } };
const blocks = (p, c) => [{ type: 'tag', text: 'Вопрос владельцу' }, { type: 'gap', s: 'm' },
  { type: 'display', max: 120, lines: ['Выключите', 'телефон', { t: 'на неделю', c: 'acc' }] }, { type: 'gap', s: 'm' },
  { type: 'p', size: p, html: 'Бизнес продолжит работать&nbsp;— <b>или всё держится на&nbsp;вас?</b>' }, { type: 'gap', s: 'm' },
  { type: 'card', size: c, kicker: 'Неделя без вас', html: 'Кто ответит клиенту, закроет смену тренера и проверит деньги?' }, { type: 'gap', s: 'm' },
  { type: 'btn', text: '13–14 ноября · Москва' }];
export const specs = [
  { ...base, size: 'P', out: 'vyklyuchite-telefon/post.png', mascot: { src: Z('v-shoke'), h: 960, right: -60, bottom: -40, glow: true }, blocks: blocks(32, 30) },
  { ...base, size: 'S', out: 'vyklyuchite-telefon/story.png', valign: 'flex-start', mainRight: 420,
    mascot: { src: Z('v-shoke'), h: 1000, right: -70, bottom: -40, glow: true }, blocks: blocks(36, 32) },
];
