// Visuals for week 1 (28.09–04.10). Render: node render.mjs week-01.mjs
// Every entry: out (relative to the week folder), size P = 1080×1350 post, S = 1080×1920 story/reel.
export const dir = '../week-01_28.09-04.10';

const swipe = { r: '<span class="arrow">Листай <i>→</i></span>' };
const next = { r: '<span class="arrow"><i>→</i></span>' };
const IG = 'instagram', VK = 'vk', TG = 'telegram';

// ---- Saturday poll results: fill in and re-render on 03.10 ----
export const results = {
  voters: '[N]',
  // [option, percent] — replace with numbers, e.g. ['Клиенты уходят', 34]
  options: [['Не хватает клиентов', '—'], ['Клиенты уходят', '—'], ['Проблемы с тренерами', '—'], ['Не понимаю, как масштабироваться', '—'], ['Выручка есть, прибыли нет', '—']],
  conclusion: '[вывод одной фразой]',
};
const bars = { type: 'bars', items: results.options };

export const specs = [
  // ================= ПН 28.09 — манифест =================
  { out: `${VK}/1-pn-28.09-manifest/cover.png`, size: 'P', theme: 'ink', blocks: [
    { type: 'display', lines: ['Не просто', 'послушать.', { t: 'Приехать', c: 'acc' }, { t: 'решить.', c: 'acc' }] },
    { type: 'gap', s: 'm' }, { type: 'p', html: 'Форум владельцев и руководителей спортивного бизнеса' } ] },
  { out: `${IG}/1-pn-28.09-karusel-manifest/slide-1.png`, size: 'P', theme: 'ink', bottom: swipe, blocks: [
    { type: 'display', lines: [{ t: 'Не просто', c: 'dim' }, { t: 'послушать.', c: 'dim' }, { t: 'Приехать', c: 'acc' }, { t: 'решить.', c: 'acc' }] } ] },
  { out: `${IG}/1-pn-28.09-karusel-manifest/slide-2.png`, size: 'P', theme: 'paper', corner: '02 / 06', bottom: next, blocks: [
    { type: 'tag', text: 'Знакомо?' }, { type: 'gap', s: 'm' },
    { type: 'display', lines: ['Два дня форума,', 'блокнот', 'конспектов —', { t: 'и в понедельник', c: 'acc' }, { t: 'всё как было', c: 'acc' }] } ] },
  { out: `${IG}/1-pn-28.09-karusel-manifest/slide-3.png`, size: 'P', theme: 'ink', corner: '03 / 06', bottom: next, blocks: [
    { type: 'display', lines: [{ t: 'РЕШЕНО —', c: 'acc' }, 'форум', 'для владельцев', 'спортивного', 'бизнеса'] } ] },
  { out: `${IG}/1-pn-28.09-karusel-manifest/slide-4.png`, size: 'P', theme: 'amber', corner: '04 / 06', bottom: next, blocks: [
    { type: 'display', lines: [{ t: 'Меньше', c: 'dim' }, { t: 'докладов.', c: 'dim' }, 'Больше', 'разборов'] },
    { type: 'gap', s: 'm' }, { type: 'p', html: 'конкретно вашей ситуации' } ] },
  { out: `${IG}/1-pn-28.09-karusel-manifest/slide-5.png`, size: 'P', theme: 'ink', corner: '05 / 06', bottom: next, blocks: [
    { type: 'display', lines: [{ t: '200–300', c: 'acc' }, 'человек.', 'Специально', 'мало.'] } ] },
  { out: `${IG}/1-pn-28.09-karusel-manifest/slide-6.png`, size: 'P', theme: 'amber', corner: '06 / 06', bottom: { l: 'Форум владельцев спортивного бизнеса' }, blocks: [
    { type: 'display', lines: ['13–14 ноября', 'Москва'] }, { type: 'gap', s: 'm' },
    { type: 'p', html: 'Ссылка в шапке профиля' }, { type: 'gap', s: 'l' }, { type: 'btn', text: 'Узнать подробнее' } ] },
  { out: `${IG}/stories/1-pn-28.09-a-my-zapustilis.png`, size: 'S', theme: 'ink', blocks: [
    { type: 'display', lines: ['Мы', { t: 'запустились', c: 'acc' }] }, { type: 'gap', s: 'm' },
    { type: 'p', html: 'РЕШЕНО — форум владельцев и руководителей спортивного бизнеса' } ] },
  { out: `${IG}/stories/1-pn-28.09-b-ssylka-na-kanal.png`, size: 'S', theme: 'amber', blocks: [
    { type: 'display', lines: ['Как всё', 'устроено —', 'рассказываем', 'в Telegram'] }, { type: 'gap', s: 'l' },
    { type: 'sticker', text: 'место для стикера-ссылки<br>на Telegram-канал' } ] },

  // ================= ВТ 29.09 — организатор =================
  { out: `${IG}/2-vt-29.09-rils-organizator/oblozhka.png`, size: 'S', theme: 'ink', bottom: false, blocks: [
    { type: 'display', lines: ['Зачем', 'мы делаем', { t: 'РЕШЕНО', c: 'acc' }] }, { type: 'gap', s: 'm' },
    { type: 'p', html: 'Андрей Коломеец,<br>президент Ассоциации руководителей футбольных школ' } ] },
  { out: `${IG}/stories/2-vt-29.09-a-gotovim.png`, size: 'S', theme: 'ink', blocks: [
    { type: 'sticker', h: 900, text: 'место для фото команды<br>или рабочего процесса' }, { type: 'gap', s: 'm' },
    { type: 'display', lines: ['Готовим', { t: 'РЕШЕНО', c: 'acc' }] } ] },
  { out: `${IG}/stories/2-vt-29.09-b-opros.png`, size: 'S', theme: 'paper', blocks: [
    { type: 'display', lines: ['Были', 'на форуме,', 'который', { t: 'реально', c: 'acc' }, { t: 'помог?', c: 'acc' }] }, { type: 'gap', s: 'l' },
    { type: 'sticker', text: 'место для стикера-опроса<br>Да / Нет' } ] },

  // ================= СР 30.09 — 5 вопросов =================
  { out: `${VK}/3-sr-30.09-5-voprosov/kartochka.png`, size: 'P', theme: 'paper', blocks: [
    { type: 'display', max: 90, lines: ['5 вопросов,', 'ради которых', { t: 'стоит приехать', c: 'acc' }] }, { type: 'gap', s: 'm' },
    { type: 'list', items: [['Money', 'Почему выручка есть, а денег нет?'], ['Client', 'Как удерживать клиентов после пробного?'], ['Team', 'Где найти тренеров — и удержать?'], ['Growth', 'Как открыть второй филиал и не развалить первый?'], ['Future', 'Что будет с рынком через 3 года?']] } ] },
  { out: `${IG}/3-sr-30.09-karusel-5-voprosov/slide-1.png`, size: 'P', theme: 'ink', bottom: swipe, blocks: [
    { type: 'display', lines: [{ t: '5 вопросов,', c: 'acc' }, 'которые', 'не дают спать', 'владельцу', 'спортивной школы'] } ] },
  ...[
    ['Money', 'paper', ['Выручка есть,', 'а денег нет.', { t: 'Почему?', c: 'acc' }]],
    ['Client', 'ink', ['Пробное', 'прошли —', 'и пропали.', { t: 'Как удержать?', c: 'acc' }]],
    ['Team', 'amber', ['Хороший тренер', 'ушёл', 'к конкуренту.', { t: 'Опять', c: 'acc' }]],
    ['Growth', 'paper', ['Второй филиал:', 'рост или способ', { t: 'развалить', c: 'acc' }, { t: 'первый?', c: 'acc' }]],
    ['Future', 'ink', ['Что будет', 'с рынком', { t: 'через 3 года?', c: 'acc' }]],
  ].map(([tag, theme, lines], i) => ({
    out: `${IG}/3-sr-30.09-karusel-5-voprosov/slide-${i + 2}.png`, size: 'P', theme, num: `0${i + 1}`, corner: `0${i + 1} / 05`, bottom: next,
    blocks: [{ type: 'tag', text: tag }, { type: 'gap', s: 'm' }, { type: 'display', lines }] })),
  { out: `${IG}/3-sr-30.09-karusel-5-voprosov/slide-7.png`, size: 'P', theme: 'amber', bottom: { l: '13–14 ноября 2026 · Москва' }, blocks: [
    { type: 'display', lines: ['Ответы —', 'на РЕШЕНО'] }, { type: 'gap', s: 'm' },
    { type: 'p', html: 'Какой вопрос ваш? <b>Напишите номер в комментариях</b>' }, { type: 'gap', s: 'l' },
    { type: 'btn', text: 'Узнать подробнее' } ] },
  { out: `${IG}/stories/3-sr-30.09-vopros.png`, size: 'S', theme: 'ink', blocks: [
    { type: 'display', lines: ['Какой вопрос', 'бизнеса', { t: 'не даёт вам', c: 'acc' }, { t: 'покоя?', c: 'acc' }] }, { type: 'gap', s: 'l' },
    { type: 'sticker', text: 'место для стикера-вопроса' } ] },

  // ================= ЧТ 01.10 — опрос =================
  { out: `${IG}/stories/4-cht-01.10-a-opros.png`, size: 'S', theme: 'paper', blocks: [
    { type: 'display', lines: ['Что сейчас', 'больше всего', 'мешает', { t: 'расти?', c: 'acc' }] }, { type: 'gap', s: 'l' },
    { type: 'sticker', text: 'место для стикера-опроса<br>Клиенты / Тренеры / Деньги' } ] },
  { out: `${IG}/stories/4-cht-01.10-b-polnyy-opros.png`, size: 'S', theme: 'amber', blocks: [
    { type: 'display', lines: ['Полный опрос —', 'в Telegram'] }, { type: 'gap', s: 'm' },
    { type: 'p', html: '5 вариантов. Итоги покажем в субботу, а разбирать на форуме будем то, что болит у вас.' }, { type: 'gap', s: 'l' },
    { type: 'sticker', text: 'место для стикера-ссылки' } ] },

  // ================= ПТ 02.10 — вопрос недели =================
  { out: `${VK}/5-pt-02.10-klip-vopros-nedeli/oblozhka.png`, size: 'S', theme: 'ink', bottom: false, blocks: [
    { type: 'tag', text: 'Вопрос недели' }, { type: 'gap', s: 'm' },
    { type: 'display', lines: ['Спортшкола', 'без CRM —', 'через 3 года', { t: 'всё?', c: 'acc' }] } ] },
  { out: `${VK}/5-pt-02.10-klip-vopros-nedeli/titr-1-vopros.png`, size: 'S', theme: 'clear', bottom: false, blocks: [
    { type: 'grow' }, { type: 'card', size: 42, html: 'Через 3 года спортивная школа без CRM, онлайн-оплаты и автоворонки ещё сможет конкурировать?' } ] },
  { out: `${VK}/5-pt-02.10-klip-vopros-nedeli/titr-2-dve-pozicii.png`, size: 'S', theme: 'clear', bottom: false, blocks: [
    { type: 'grow' }, { type: 'vs', items: ['Главное —<br>тренер', 'Без цифры —<br>конец'] } ] },
  { out: `${VK}/5-pt-02.10-klip-vopros-nedeli/titr-3-final.png`, size: 'S', theme: 'amber', bottom: false, blocks: [
    { type: 'display', lines: ['А вы как', 'думаете?'] }, { type: 'gap', s: 'm' }, { type: 'p', html: 'Пишите в комментариях' } ] },
  { out: `${IG}/stories/5-pt-02.10-trener-ili-cifra.png`, size: 'S', theme: 'ink', blocks: [
    { type: 'display', lines: ['Тренер', { t: 'или цифра?', c: 'acc' }] }, { type: 'gap', s: 'l' },
    { type: 'sticker', h: 600, text: 'место для репоста поста из канала<br>+ стикер-опрос «Тренер / Цифра»' } ] },

  // ================= СБ 03.10 — итоги (шаблоны, перерендерить с цифрами) =================
  { out: `${VK}/6-sb-03.10-itogi-oprosa/diagramma.png`, size: 'P', theme: 'ink', blocks: [
    { type: 'display', max: 90, lines: ['Что мешает', { t: 'расти', c: 'acc' }] }, { type: 'gap', s: 's' },
    { type: 'p', size: 30, html: `Проголосовали ${results.voters} владельцев и руководителей` }, { type: 'gap', s: 'm' }, bars ] },
  { out: `${IG}/6-sb-03.10-karusel-itogi/slide-1.png`, size: 'P', theme: 'ink', bottom: swipe, blocks: [
    { type: 'tag', text: 'Итоги опроса' }, { type: 'gap', s: 'm' },
    { type: 'display', lines: ['Что мешает', 'расти', { t: 'спортивному', c: 'acc' }, { t: 'бизнесу', c: 'acc' }] } ] },
  { out: `${IG}/6-sb-03.10-karusel-itogi/slide-2.png`, size: 'P', theme: 'paper', corner: '02 / 03', bottom: next, blocks: [
    { type: 'p', size: 30, html: `Проголосовали <b>${results.voters}</b> владельцев и руководителей` }, { type: 'gap', s: 'm' }, bars ] },
  { out: `${IG}/6-sb-03.10-karusel-itogi/slide-3.png`, size: 'P', theme: 'amber', corner: '03 / 03', blocks: [
    { type: 'tag', text: 'Вывод' }, { type: 'gap', s: 'm' }, { type: 'card', size: 48, html: results.conclusion }, { type: 'gap', s: 'l' },
    { type: 'p', html: 'Этому посвятим отдельный разбор на форуме. <b>Подробности — в Telegram</b>' } ] },
  { out: `${IG}/stories/6-sb-03.10-itogi.png`, size: 'S', theme: 'ink', blocks: [
    { type: 'tag', text: 'Итоги опроса' }, { type: 'gap', s: 'm' }, bars, { type: 'gap', s: 'l' },
    { type: 'sticker', h: 200, text: 'стикер-ссылка «Подробности в Telegram»' } ] },

  // ================= ВС 04.10 — лёгкий пост =================
  { out: `${TG}/7-vs-04.10-mem/ponedelnik-vladelca.png`, size: 'P', theme: 'paper', bottom: { l: 'Узнали себя?' }, blocks: [
    { type: 'display', max: 100, lines: ['Понедельник', { t: 'владельца', c: 'acc' }, { t: 'спортивной школы', c: 'acc' }] }, { type: 'gap', s: 'm' },
    { type: 'list', times: true, items: [['08:00', 'Три тренера заболели'], ['08:15', 'Родители в чате'], ['09:00', 'Аренда подорожала']] } ] },
  { out: `${IG}/stories/7-vs-04.10-anons.png`, size: 'S', theme: 'amber', blocks: [
    { type: 'sticker', h: 800, text: 'место для фото закулисья' }, { type: 'gap', s: 'm' },
    { type: 'p', html: 'На следующей неделе' }, { type: 'display', lines: ['рассказываем', 'про форматы', 'форума'] } ] },
];
