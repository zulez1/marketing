// Weeks 3–4 (12.10–25.10): carousels + countdown stories. Render: node render.mjs w34.mjs [filter]
export const dir = '../nedeli-3-4_12.10-25.10';
const swipe = { r: '<span class="arrow">Листай <i>→</i></span>' };
const next = { r: '<span class="arrow"><i>→</i></span>' };
const D = '13–14 ноября · Москва';
const Z = n => `img/zubr-${n}.png`;
const sub = (b, s) => `${b}<br><span style="font-weight:600;font-size:26px;opacity:.7">${s}</span>`;
const P = (folder, slides) => slides.map((s, i) => ({ size: 'P', corner: `${String(i + 1).padStart(2, '0')} / ${String(slides.length).padStart(2, '0')}`,
  bottom: { l: D, ...(i === 0 ? swipe : i < slides.length - 1 ? next : {}) }, ...s, out: `${folder}/slide-${i + 1}.png` }));

const znakomstvo = P('01-pn-12.10-znakomtes-zubr', [
  { theme: 'ink', mainRight: 450, mascot: { src: Z('priglashaet'), h: 1040, right: -130, bottom: -10, glow: true },
    blocks: [{ type: 'tag', text: 'Знакомьтесь' }, { type: 'gap', s: 'm' },
      { type: 'display', max: 120, lines: ['Это', 'зубр', { t: 'РЕШЕНО', c: 'acc' }] }] },
  { theme: 'paper', mainRight: 440, mascot: { src: Z('ustal'), h: 760, right: -60, bottom: 40 },
    blocks: [{ type: 'display', max: 110, lines: ['Он тоже', 'владелец', { t: 'спортивного', c: 'acc' }, { t: 'бизнеса', c: 'acc' }] }, { type: 'gap', s: 'm' },
      { type: 'p', size: 30, html: 'Отвечает в родительском чате в 23:47, ищет тренеров и считает, куда ушли деньги' }] },
  { theme: 'amber', blocks: [{ type: 'display', max: 120, lines: ['Здесь он', 'будет:'] }, { type: 'gap', s: 'm' },
      { type: 'list', items: [['Шутить', 'про жизнь владельца — без обид, только жиза'], ['Объяснять', 'цифры, формулы и шаблоны, которые можно забрать себе'], ['Звать', 'на РЕШЕНО 13–14 ноября']] }] },
  { theme: 'ink', mainRight: 430, mascot: { src: Z('dumaet'), h: 980, right: -150, bottom: -10, glow: true },
    blocks: [{ type: 'display', max: 120, lines: ['Но у него', { t: 'нет имени', c: 'acc' }] }, { type: 'gap', s: 'm' },
      { type: 'p', html: 'Предлагайте в комментариях — <b>лучшие варианты выставим на голосование</b>' }] },
]);

const klient = P('02-vt-13.10-poteryannyy-klient', [
  { theme: 'ink', mainRight: 420, mascot: { src: Z('v-shoke'), h: 900, right: -60, bottom: -10, glow: true },
    blocks: [{ type: 'tag', text: 'Полезняшка' }, { type: 'gap', s: 'm' },
      { type: 'display', max: 110, lines: ['Сколько', 'стоит', { t: 'потерянный', c: 'acc' }, { t: 'клиент?', c: 'acc' }] }, { type: 'gap', s: 'm' },
      { type: 'p', size: 30, html: 'Спойлер: <b>намного больше</b>, чем один абонемент' }] },
  { theme: 'paper', blocks: [{ type: 'tag', text: 'Формула' }, { type: 'gap', s: 'm' },
      { type: 'display', max: 120, lines: ['Ценность', 'клиента ='] }, { type: 'gap', s: 'm' },
      { type: 'card', size: 40, html: 'Средний чек в месяц × сколько месяцев клиент с вами' }, { type: 'gap', s: 'm' },
      { type: 'p', size: 30, html: 'Это LTV — сколько денег клиент приносит <b>за всё время</b>, а не за один месяц' }] },
  { theme: 'paper', blocks: [{ type: 'tag', text: 'Пример' }, { type: 'gap', s: 'm' },
      { type: 'list', items: [['Абонемент', '6 000 ₽ в месяц'], ['Ходит', 'в среднем 8 месяцев'], ['Ценность', '<b>48 000 ₽</b>']] }, { type: 'gap', s: 'm' },
      { type: 'p', size: 28, html: 'Цифры условные — <b>подставьте свои</b>' }] },
  { theme: 'ink', blocks: [{ type: 'display', max: 120, lines: ['5 человек', 'в месяц', 'не продлили', { t: '= 240 000 ₽', c: 'acc' }] }, { type: 'gap', s: 'm' },
      { type: 'p', html: 'Столько школа <b>недополучает</b> с каждой такой пятёрки. Не за месяц — за всё время, которое они могли бы ходить' }] },
  { theme: 'amber', blocks: [{ type: 'tag', text: 'Что делать' }, { type: 'gap', s: 'm' },
      { type: 'list', items: [['01', 'Позвонить в течение суток после пробного'], ['02', 'Дать родителю обратную связь от тренера'], ['03', 'Назвать понятную цену и следующий шаг']] }] },
  { theme: 'ink', mainRight: 430, mascot: { src: Z('klass'), h: 960, right: -110, bottom: -10, glow: true },
    blocks: [{ type: 'display', max: 120, lines: ['Напишите', { t: 'КЛИЕНТЫ', c: 'acc' }] }, { type: 'gap', s: 'm' },
      { type: 'p', html: 'в комментариях — пришлём чек-лист <b>«12 причин, почему уходят после пробного»</b>' }] },
]);

const frazy = [
  ['«Я заметил, что у Миши хорошо получается удар. Хотите, расскажу, над чем поработаем дальше?»', 'Родитель видит, что ребёнка заметили, — и что у занятий есть план'],
  ['«Что для вас главное: результат, дисциплина или чтобы ребёнку было интересно?»', 'Вы узнаёте, за что на самом деле платят, — и говорите об этом дальше'],
  ['«Давайте сразу подберём удобное время — в этой группе есть места во вторник и четверг»', 'Конкретный следующий шаг вместо «подумаем»'],
  ['«Первый месяц — адаптационный: если группа не подойдёт, переведём в другую»', 'Снимаете страх ошибиться с выбором'],
  ['«Можно я напишу вам через неделю и расскажу, как у него дела?»', 'Контакт продолжается, даже если решение не принято сразу'],
];
const udrzh = P('04-cht-15.10-5-fraz-posle-probnogo', [
  { theme: 'paper', mainRight: 430, mascot: { src: Z('podmigivaet'), h: 960, right: -120, bottom: -10 },
    blocks: [{ type: 'tag', text: 'Полезняшка' }, { type: 'gap', s: 'm' },
      { type: 'display', max: 110, lines: ['5 фраз,', 'которые', { t: 'удерживают', c: 'acc' }, { t: 'после', c: 'acc' }, { t: 'пробного', c: 'acc' }] }] },
  ...frazy.map(([f, w], i) => ({ theme: i % 2 ? 'paper' : 'ink', num: `0${i + 1}`, blocks: [{ type: 'tag', text: `Фраза ${i + 1}` }, { type: 'gap', s: 'm' },
      { type: 'card', size: 44, html: f }, { type: 'gap', s: 'm' }, { type: 'p', html: `<b>Почему работает:</b> ${w}` }] })),
  { theme: 'amber', mainRight: 440, mascot: { src: Z('klass'), h: 960, right: -120, bottom: -10 },
    blocks: [{ type: 'display', max: 110, lines: ['Сохраните', { t: 'и отправьте', c: 'acc' }, { t: 'админу', c: 'acc' }] }, { type: 'gap', s: 'm' },
      { type: 'p', html: 'Как клиенты перестают покупать «просто тренировку» — разберём <b>13 ноября на РЕШЕНО</b>' }] },
]);

const den = P('06-sb-17.10-den-na-reshno', [
  { theme: 'ink', mainRight: 480, mascot: { src: Z('priglashaet'), h: 1000, right: -170, bottom: -10, glow: true },
    blocks: [{ type: 'tag', text: '13 ноября' }, { type: 'gap', s: 'm' },
      { type: 'display', max: 110, lines: ['Как', 'выглядит', 'день', { t: 'на РЕШЕНО', c: 'acc' }] }, { type: 'gap', s: 'm' },
      { type: 'p', size: 30, html: 'Главный вопрос дня: <b>где деньги?</b>' }] },
  { theme: 'paper', blocks: [{ type: 'tag', text: 'Утро' }, { type: 'gap', s: 'm' },
      { type: 'list', times: true, items: [['08:30', sub('Business Arrival', 'регистрация, кофе, знакомства')], ['09:00', 'Business Breakfast'], ['10:00', sub('Открытие', 'Sport Business Index — что происходит с рынком')]] }] },
  { theme: 'ink', blocks: [{ type: 'tag', text: 'До обеда' }, { type: 'gap', s: 'm' },
      { type: 'list', times: true, items: [['10:20', sub('Панель', 'Как на самом деле зарабатывает спортивный бизнес')], ['11:05', sub('Debate', 'Больше клиентов или больше денег с клиента?')], ['11:50', 'Business Speed Networking'], ['12:20', sub('Sales', 'Где теряются клиенты?')]] }] },
  { theme: 'paper', blocks: [{ type: 'tag', text: 'После обеда' }, { type: 'gap', s: 'm' },
      { type: 'list', times: true, items: [['13:10', 'Business Lunch'], ['14:10', sub('Client', 'Клиент больше не покупает просто тренировку')], ['15:00', sub('Hot Seat', 'Вопрос, который вы боитесь задать')], ['15:45', 'Coffee + Find Your Partner']] }] },
  { theme: 'ink', blocks: [{ type: 'tag', text: 'Вечер' }, { type: 'gap', s: 'm' },
      { type: 'list', times: true, items: [['16:15', sub('Money', 'Как увеличить прибыль без увеличения количества клиентов?')], ['17:00', sub('Business Live #1', 'Почему этот бизнес не растёт? — разбор перед залом')], ['19:00', sub('Sport Business Night', 'Networking + Business Stories')]] }] },
  { theme: 'amber', mainRight: 430, mascot: { src: Z('aplodiruet'), h: 960, right: -120, bottom: -10 },
    blocks: [{ type: 'display', max: 110, lines: ['А 14 ноября —', { t: 'как вырасти', c: 'acc' }] }, { type: 'gap', s: 'm' },
      { type: 'p', html: 'Owner vs Owner, Team, Finance, Future и ещё два Business Live. <b>Программа — на сайте</b>' }, { type: 'gap', s: 'l' },
      { type: 'btn', text: 'Участвовать' }] },
]);

const cifry = [
  ['01 · Выручка за неделю', 'Сравнивайте с той же неделей месяц назад, а не с прошлой — так видна сезонность'],
  ['02 · Активные клиенты', 'Не «записанные», а те, кто был хотя бы раз за последние 2 недели'],
  ['03 · Отток', 'Сколько ушли и не продлили. Главная цифра, которую обычно не считают'],
  ['04 · Конверсия пробного', 'Из 10 пришедших на пробное — сколько купили абонемент'],
  ['05 · Заполняемость групп', 'Пустое место в группе — потерянная выручка при тех же расходах'],
  ['06 · Доля зарплат в выручке', 'Если растёт быстрее выручки — прибыль тает, даже когда клиентов больше'],
];
const ponedelnik = P('08-pn-19.10-6-cifr-ponedelnika', [
  { theme: 'ink', valign: 'flex-start', mainBottom: 720, mascot: { src: Z('flipchart'), h: 640, right: 40, bottom: 140, glow: true },
    blocks: [{ type: 'tag', text: 'Полезняшка' }, { type: 'gap', s: 's' },
      { type: 'display', max: 110, lines: ['6 цифр,', 'которые владелец', { t: 'смотрит каждый', c: 'acc' }, { t: 'понедельник', c: 'acc' }] }] },
  ...[0, 2, 4].map((k, i) => ({ theme: i % 2 ? 'ink' : 'paper', blocks: [
      { type: 'card', size: 38, kicker: cifry[k][0], html: cifry[k][1] }, { type: 'gap', s: 'm' },
      { type: 'card', size: 38, kicker: cifry[k + 1][0], html: cifry[k + 1][1] }] })),
  { theme: 'amber', mainRight: 430, mascot: { src: Z('klass'), h: 960, right: -120, bottom: -10 },
    blocks: [{ type: 'display', max: 110, lines: ['Сохраните', { t: 'на понедельник', c: 'acc' }] }, { type: 'gap', s: 'm' },
      { type: 'p', html: 'Эти цифры разбираем на сессии <b>Finance 14 ноября</b>: «Цифры, которые собственник должен видеть каждую неделю»' }] },
]);

const voprosy = [
  ['«Почему ушли с прошлого места?»', 'Слушайте не причину, а как он говорит о бывшем руководителе — так же будет говорить и о вас'],
  ['«Как работаете с ребёнком, который не хочет тренироваться?»', 'Проверяете педагогику, а не только спортивный уровень'],
  ['«Что скажете родителю, который недоволен?»', 'Для родителя тренер — лицо школы. Важно, умеет ли он разговаривать'],
  ['«Где вы видите себя через 2 года?»', '«Своя школа» — не минус. Обсудите, как он может расти внутри вашей'],
  ['«Проведите 10 минут тренировки прямо сейчас»', 'Покажет больше любого резюме'],
];
const trener = P('10-sr-21.10-sobesedovanie-trenera', [
  { theme: 'paper', valign: 'flex-start', mainBottom: 700, mascot: { src: Z('dumaet'), h: 640, right: 60, bottom: 140 },
    blocks: [{ type: 'tag', text: 'Полезняшка' }, { type: 'gap', s: 's' },
      { type: 'display', max: 110, lines: ['5 вопросов', 'тренеру', { t: 'на собеседовании', c: 'acc' }] }, { type: 'gap', s: 's' },
      { type: 'p', size: 30, html: 'Чтобы он <b>не ушёл через полгода</b>' }] },
  ...voprosy.map(([q, w], i) => ({ theme: i % 2 ? 'paper' : 'ink', num: `0${i + 1}`, blocks: [{ type: 'tag', text: `Вопрос ${i + 1}` }, { type: 'gap', s: 'm' },
      { type: 'card', size: 48, html: q }, { type: 'gap', s: 'm' }, { type: 'p', html: `<b>Зачем:</b> ${w}` }] })),
  { theme: 'amber', mainRight: 430, mascot: { src: Z('podmigivaet'), h: 960, right: -120, bottom: -10 },
    blocks: [{ type: 'display', max: 110, lines: ['Команда,', 'которая', { t: 'работает', c: 'acc' }, { t: 'без вас', c: 'acc' }] }, { type: 'gap', s: 'm' },
      { type: 'p', html: 'Разбираем на сессии <b>Team 14 ноября</b> на РЕШЕНО' }] },
]);

const live = P('12-pt-23.10-business-live', [
  { theme: 'amber', valign: 'flex-start', mainBottom: 720, mascot: { src: Z('flipchart'), h: 640, right: 40, bottom: 140 },
    blocks: [{ type: 'tag', text: 'Business Live' }, { type: 'gap', s: 's' },
      { type: 'display', max: 110, lines: ['Ваш бизнес', 'могут разобрать', { t: 'перед залом', c: 'acc' }] }] },
  { theme: 'ink', blocks: [{ type: 'tag', text: 'Как это работает' }, { type: 'gap', s: 'm' },
      { type: 'list', items: [['01', 'Вы присылаете заявку и цифры'], ['02', 'Эксперты и зал задают вопросы'], ['03', 'Ищем решения вживую, по цифрам'], ['04', 'Вы уезжаете с планом действий']] }] },
  { theme: 'paper', blocks: [{ type: 'display', max: 110, lines: ['Три бизнеса.', 'Три проблемы.', { t: 'Три решения.', c: 'acc' }] }, { type: 'gap', s: 'm' },
      { type: 'list', times: true, items: [['#01', sub('Почему этот бизнес не растёт?', '13 ноября · 17:00')], ['#02', sub('Где этот бизнес теряет деньги?', '14 ноября · 15:30')], ['#03', sub('Как вырасти в 3 раза?', '14 ноября · 17:10')]] }] },
  { theme: 'ink', mainRight: 430, mascot: { src: Z('podmigivaet'), h: 960, right: -120, bottom: -10, glow: true },
    blocks: [{ type: 'display', max: 110, lines: ['Хотите', 'разбор', { t: 'своего', c: 'acc' }, { t: 'бизнеса?', c: 'acc' }] }, { type: 'gap', s: 'm' },
      { type: 'p', html: 'Три бизнеса выбираются заранее из заявок. <b>Заявка — на сайте</b>' }, { type: 'gap', s: 'l' }, { type: 'btn', text: 'Подать заявку' }] },
]);

const prodazha = P('13-sb-24.10-ne-bilet', [
  { theme: 'ink', mainRight: 430, mascot: { src: Z('podmigivaet'), h: 1000, right: -110, bottom: -10, glow: true },
    blocks: [{ type: 'display', max: 120, lines: ['Вы покупаете', { t: 'не билет', c: 'acc' }] }, { type: 'gap', s: 'm' },
      { type: 'p', html: 'А доступ к людям, решениям и новым возможностям' }] },
  { theme: 'paper', blocks: [{ type: 'tag', text: 'Что внутри' }, { type: 'gap', s: 'm' },
      { type: 'list', items: [['2 дня', 'программа, разборы, Hot Seat и дебаты'], ['Match', 'список полезных контактов ещё до форума'], ['Tables', 'собственники в узком кругу по вашему вопросу'], ['Night', 'вечер знакомств без регламента']] }] },
  { theme: 'amber', mainRight: 440, mascot: { src: Z('aplodiruet'), h: 960, right: -130, bottom: -10 },
    blocks: [{ type: 'display', max: 110, lines: ['Приезжайте', { t: 'командой', c: 'acc' }] }, { type: 'gap', s: 'm' },
      { type: 'p', html: 'Пакеты на 3 и 5 человек: <b>чем больше людей — тем больше скидка</b>' }] },
  { theme: 'ink', mainRight: 480, mascot: { src: Z('priglashaet'), h: 980, right: -170, bottom: -10, glow: true },
    blocks: [{ type: 'display', max: 110, lines: ['Стартовая', 'цена —', { t: 'для первых 50', c: 'acc' }] }, { type: 'gap', s: 'l' },
      { type: 'btn', text: 'Забронировать' }, { type: 'url', text: 'reshenoforum.ru' }] },
]);

const objasni = [{ size: 'P', out: '14-vs-25.10-objasni/slide-1.png', theme: 'paper', corner: 'Вопрос недели', mainRight: 430,
  mascot: { src: Z('smeetsya-2'), h: 1000, right: -150, bottom: -10 }, bottom: { l: D },
  blocks: [{ type: 'display', max: 100, lines: ['Объясните,', 'что вы', { t: 'владелец', c: 'acc' }, { t: 'спортшколы,', c: 'acc' }, 'не говоря', 'об этом'] }, { type: 'gap', s: 'm' },
    { type: 'p', size: 30, html: 'Лучшие ответы <b>соберём в карусель</b>' }] }];

// countdown stories: 12.10 → 32 days … 25.10 → 19 days
const days = n => (n % 10 === 1 && n % 100 !== 11) ? 'день' : ([2, 3, 4].includes(n % 10) && ![12, 13, 14].includes(n % 100)) ? 'дня' : 'дней';
const poses = ['priglashaet', 'v-shoke', 'zlitsya', 'klass', 'podmigivaet', 'aplodiruet', 'smeetsya', 'dumaet', 'ustal', 'facepalm', 'zakatyvaet-glaza', 'flipchart', 'smeetsya-2', 'spit'];
const dates = ['12.10', '13.10', '14.10', '15.10', '16.10', '17.10', '18.10', '19.10', '20.10', '21.10', '22.10', '23.10', '24.10', '25.10'];
const otschet = dates.map((d, i) => { const n = 32 - i, pose = poses[i % poses.length], wide = ['spit', 'flipchart', 'ustal'].includes(pose);
  return { size: 'S', out: `storis-otschet/${d}-${n}.png`, theme: i % 2 ? 'ink' : 'amber', corner: '', valign: 'flex-start', mainBottom: 1000, bottom: { l: 'reshenoforum.ru' },
    mascot: { src: Z(pose), h: wide ? 640 : 840, right: wide ? 40 : 120, bottom: 330, glow: i % 2 === 1 },
    blocks: [{ type: 'tag', text: 'До форума' }, { type: 'gap', s: 's' }, { type: 'display', max: 360, lines: [String(n)] },
      { type: 'display', max: 130, lines: [days(n)] }, { type: 'gap', s: 's' }, { type: 'p', size: 32, html: D }] }; });

export const specs = [...znakomstvo, ...klient, ...udrzh, ...den, ...ponedelnik, ...trener, ...live, ...prodazha, ...objasni, ...otschet];
