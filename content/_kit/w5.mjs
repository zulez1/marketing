// Week 27.10–02.11. Render: node render.mjs w5.mjs
export const dir = '../nedelya-5_27.10-02.11';
const Z = n => `img/zubr-${n}.png`;
export const specs = [
  { size: 'P', out: '01-zubr-sportbiznes/slide-1.png', theme: 'ink', corner: '13–14.11 · Москва', valign: 'flex-start', mainBottom: 760,
    mascot: { src: Z('podmigivaet'), h: 760, right: 300, bottom: -10, glow: true }, bottom: { l: 'reshenoforum.ru' },
    blocks: [{ type: 'display', max: 150, lines: ['Вот такой вот', { t: 'спортбизнес,', c: 'acc' }, 'собачка'] }] },
];
