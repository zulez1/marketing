from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import CellIsRule, FormulaRule
from openpyxl.utils import get_column_letter

INK, AMBER, PAPER = "0D0F13", "F0B90B", "F3F0E8"
F = lambda **k: Font(name="Arial", **k)
thin = Side(style="thin", color="DAD5C6"); border = Border(left=thin, right=thin, top=thin, bottom=thin)
N, D, S = "Нужно", "Выложено", "—"
W = "Готов"; SHOOT = "Нужно снять"; DATA = "Ждём цифры опроса"; DO = "Нужно сделать"

# (блок, что, формат, рубрика, tg, vk, ig, yt, chat, готовность материала, где файл, что сделать перед публикацией)
rows = [
 ("1. Запуск", "Первое сообщение канала — «визитка» (что это за канал)", "Пост", "Запуск", N,S,S,S,S, W, "content/week-01_28.09-04.10/telegram/00-pervoe-soobschenie-kanala.md", "Опубликовать сразу после создания канала"),
 ("1. Запуск", "Манифест «Не просто послушать. Приехать решить.» + закрепить", "Пост + картинка", "Манифест", N,N,S,S,S, W, "telegram/1-pn-28.09-manifest.md · vk/1-pn-28.09-manifest/cover.png", "Подставить ссылку на канал в VK-версии"),
 ("1. Запуск", "Рассылка по базе ассоциации со ссылкой на канал", "Рассылка", "Привлечение", N,S,S,S,S, W, "telegram/0-rassylka-po-baze-associacii.md", "От имени Р. А. Прокопьева; вставить ссылку на канал"),
 ("1. Запуск", "Карусель «Не просто послушать» (6 слайдов)", "Карусель", "Манифест", S,N,N,S,S, W, "instagram/1-pn-28.09-karusel-manifest/ (slide-1…6 + podpis.md)", ""),
 ("1. Запуск", "Сторис «Мы запустились» + ссылка на канал", "Сторис", "Запуск", S,N,N,S,S, W, "instagram/stories/1-pn-28.09-*.png", "Добавить стикер-ссылку на канал"),
 ("1. Запуск", "Промо-ролик форума (горизонтальный, 23 с)", "Видео", "Промо", N,N,S,N,S, W, "brag-output/brag.mp4", "В ролике есть дата 13–14 ноября — проверить, что актуально"),
 ("1. Запуск", "Дерзкий вертикальный промо «Не ещё одна конференция»", "Рилс", "Промо", N,N,N,S,S, W, "brag-output/brag-vertical.mp4", "В ролике дата и «стартовая цена для первых 50» — проверить"),
 ("2. Кто мы", "Видеообращение Р. А. Прокопьева «Зачем мы делаем РЕШЕНО»", "Видео / рилс", "Организатор", N,N,N,S,S, SHOOT, "Сценарий: instagram/2-vt-29.09-rils-organizator/scenariy.md · обложка там же", "Снять 30–45 с вертикально, с субтитрами"),
 ("2. Кто мы", "Сторис «Готовим РЕШЕНО» + опрос «Были на форуме, который помог?»", "Сторис", "Закулисье", S,N,N,S,S, DO, "instagram/stories/2-vt-*.png", "Нужно фото команды в рамку"),
 ("3. Атмосфера", "Рилс «Полный зал»", "Рилс", "Атмосфера", N,N,N,S,S, W, "reels/reel1-polnyy-zal.mp4 (без музыки: reels/bez-muzyki/)", "Подпись — reels/README.md"),
 ("3. Атмосфера", "Рилс «Как это выглядит» — день форума", "Рилс", "Атмосфера", N,N,N,S,S, W, "reels/reel2-kak-eto-vyglyadit.mp4", ""),
 ("4. Вопросы бизнеса", "Пост «5 вопросов, ради которых стоит приехать» + карточка", "Пост + картинка", "5 вопросов", N,N,S,S,S, W, "telegram/3-sr-30.09-5-voprosov.md · vk/3-sr-30.09-5-voprosov/", ""),
 ("4. Вопросы бизнеса", "Карусель «5 вопросов» (7 слайдов)", "Карусель", "5 вопросов", S,S,N,S,S, W, "instagram/3-sr-30.09-karusel-5-voprosov/", ""),
 ("4. Вопросы бизнеса", "Сторис со стикером-вопросом «Какой вопрос не даёт покоя?»", "Сторис", "5 вопросов", S,N,N,S,S, W, "instagram/stories/3-sr-30.09-vopros.png", "Добавить стикер-вопрос"),
 ("4. Вопросы бизнеса", "Опрос «Что мешает бизнесу расти?» (5 вариантов)", "Опрос", "Опрос", N,N,N,S,S, W, "telegram/4-cht-01.10-opros.md · vk/4-cht-01.10-opros/ · stories/4-cht-*", "Переслать опрос в чаты ассоциации"),
 ("3. Атмосфера", "Рилс «Сцена» — «Минимум сцены. Максимум разбора.»", "Рилс", "Атмосфера", N,N,N,S,S, W, "reels/reel3-scena.mp4", ""),
 ("4. Вопросы бизнеса", "Вопрос недели: «Спортшкола без CRM — через 3 года всё?»", "Пост + рилс", "Future", N,N,N,S,S, SHOOT, "telegram/5-pt-02.10-vopros-nedeli.md · vk/5-pt-02.10-klip-vopros-nedeli/ (обложка, титры, сценарий)", "Снять ролик с человеком в кадре"),
 ("4. Вопросы бизнеса", "Итоги опроса — цифры + диаграмма + карусель", "Пост + карусель", "Опрос", N,N,N,S,S, DATA, "telegram/6-sb-03.10-itogi-oprosa.md · vk/6-sb-03.10-itogi-oprosa/ · instagram/6-sb-03.10-karusel-itogi/", "Прислать результаты — перерисую картинки"),
 ("3. Атмосфера", "Рилс «Hot Seat» — вопросы из зала", "Рилс", "Атмосфера", N,N,N,S,S, W, "reels/reel4-hot-seat.mp4", ""),
 ("5. Форматы", "Business Live: «Три бизнеса. Три проблемы. Три решения.» + набор на разбор", "Пост + картинка", "Business Live", N,N,S,S,S, W, "brag-output/post-business-live.png · текст: brag-output/posts.md (№3)", ""),
 ("5. Форматы", "Карусель «5 вопросов собственнику» с сессиями программы", "Карусель", "5 вопросов", S,N,N,S,S, W, "brag-output/carousel/ (slide-1…7)", "В подписи есть даты — проверить"),
 ("6. Лёгкое", "Мем «Понедельник владельца спортивной школы»", "Пост + картинка", "Лёгкий", N,N,S,S,S, W, "telegram/7-vs-04.10-mem/", ""),
 ("6. Лёгкое", "Сторис: закулисье + анонс следующей темы", "Сторис", "Закулисье", S,N,N,S,S, DO, "instagram/stories/7-vs-04.10-anons.png", "Нужно фото закулисья в рамку"),
 ("7. Чат", "Создать чат и закрепить правила", "Чат", "Чат", S,S,S,S,N, W, "telegram-chat/1-nastroyka.md · 2-pravila-zakrep.md · 3-opisanie.md", ""),
 ("7. Чат", "Лично пригласить 10–15 человек", "Чат", "Чат", S,S,S,S,N, DO, "telegram-chat/5-lichnoe-priglashenie.md (там же таблица приглашённых)", "Составить список людей"),
 ("7. Чат", "Первое сообщение модератора в чате", "Чат", "Чат", S,S,S,S,N, W, "telegram-chat/4-privetstvie.md", ""),
 ("8. YouTube", "Интро, переход и аутро — вставлять в каждый ролик", "Оформление", "YouTube", S,S,S,N,S, W, "youtube/ (intro, stinger, outro + README)", "Не публикуются отдельно — используются при монтаже"),
 ("9. Неделя 2 — спикеры", "Пн 05.10 · Тизер «На этой неделе раскрываем всех спикеров»", "Пост + сторис", "Спикеры", N,N,N,S,S, W, "content/week-02_05.10-11.10/telegram/1-pn-05.10-tizer.md · Figma: «Неделя 2 — спикеры»", ""),
 ("9. Неделя 2 — спикеры", "Вт 06.10 · Спикеры трека MONEY", "Пост + карусель", "Спикеры", N,N,N,S,S, DATA, "content/week-02_05.10-11.10/telegram/2-vt-06.10-money.md · Figma", "Нужны имена, должности, темы, фото, ники; пригласить спикеров соавторами"),
 ("9. Неделя 2 — спикеры", "Ср 07.10 · Спикеры трека CLIENT", "Пост + карусель", "Спикеры", N,N,N,S,S, DATA, "content/week-02_05.10-11.10/telegram/3-sr-07.10-client.md · Figma", "То же"),
 ("9. Неделя 2 — спикеры", "Чт 08.10 · Спикеры трека TEAM", "Пост + карусель", "Спикеры", N,N,N,S,S, DATA, "content/week-02_05.10-11.10/telegram/4-cht-08.10-team.md · Figma", "То же"),
 ("9. Неделя 2 — спикеры", "Пт 09.10 · Спикеры треков GROWTH + FUTURE", "Пост + карусель", "Спикеры", N,N,N,S,S, DATA, "content/week-02_05.10-11.10/telegram/5-pt-09.10-growth-future.md · Figma", "То же"),
 ("9. Неделя 2 — спикеры", "Сб 10.10 · «Все спикеры РЕШЕНО» — закрепить", "Пост + карусель", "Спикеры", N,N,N,S,S, DATA, "content/week-02_05.10-11.10/telegram/6-sb-10.10-vse-spikery.md · Figma", "Открепить манифест, закрепить этот пост"),
 ("9. Неделя 2 — спикеры", "Вс 11.10 · Опрос «Чей разбор ждёте больше всего?»", "Опрос + сторис", "Спикеры", N,N,N,S,S, DATA, "content/week-02_05.10-11.10/telegram/7-vs-11.10-opros.md · Figma", ""),
 ("9. Неделя 2 — спикеры", "Каждый день · Сторис-отсчёт «До форума N дней» + сторис каждого спикера", "Сторис", "Отсчёт", S,N,N,S,S, W, "content/week-02_05.10-11.10/instagram/README.md · Figma", "Вт 38, Ср 37, Чт 36, Пт 35, Сб 34, Вс 33"),
]
PLATS = ["Telegram", "VK", "Instagram", "YouTube", "TG-чат"]

wb = Workbook(); ws = wb.active; ws.title = "План"
head = ["№", "Блок", "Что выкладываем", "Формат", "Рубрика"] + PLATS + ["Статус", "Материал", "Где лежит файл", "Что сделать перед публикацией", "Комментарий"]
ws.append(["Контент-план РЕШЕНО — что за чем идёт"]); ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=len(head))
ws["A1"].font = F(bold=True, size=16, color=AMBER); ws["A1"].fill = PatternFill("solid", fgColor=INK); ws.row_dimensions[1].height = 30
ws["A1"].alignment = Alignment(vertical="center", indent=1)
ws.append(["Идём сверху вниз. В колонках площадок выберите «Выложено», когда пост вышел. «—» — на этой площадке не публикуем. Пути к файлам — от папки content/week-01_28.09-04.10/, если не указано иначе (папки reels/, brag-output/, youtube/ — в корне репозитория)."])
ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=len(head)); ws["A2"].font = F(italic=True, size=10, color="585D66")
ws["A2"].alignment = Alignment(wrap_text=True, vertical="center"); ws.row_dimensions[2].height = 32
ws.append(head); HR = 3
for c in range(1, len(head) + 1):
    cell = ws.cell(HR, c); cell.font = F(bold=True, color="FFFFFF"); cell.fill = PatternFill("solid", fgColor=INK)
    cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True); cell.border = border
ws.row_dimensions[HR].height = 30

first = HR + 1
for i, r in enumerate(rows):
    rr = first + i
    blk, what, fmt, rub, *pl, mat, path, todo = r
    pcols = f"F{rr}:J{rr}"
    status = f'=IF(COUNTIF({pcols},"{N}")=0,"Готово","Осталось: "&COUNTIF({pcols},"{N}"))'
    ws.append([i + 1, blk, what, fmt, rub] + pl + [status, mat, path, todo, ""])
    for c in range(1, len(head) + 1):
        cell = ws.cell(rr, c); cell.font = F(size=10); cell.border = border
        cell.alignment = Alignment(vertical="top", wrap_text=True, horizontal="center" if c in (1, 6, 7, 8, 9, 10, 11, 12) else "left")
    ws.cell(rr, 3).font = F(size=10, bold=True)

last = first + len(rows) - 1
dv = DataValidation(type="list", formula1=f'"{N},{D},{S}"', allow_blank=True); ws.add_data_validation(dv); dv.add(f"F{first}:J{last + 50}")
dvm = DataValidation(type="list", formula1=f'"{W},{SHOOT},{DO},{DATA}"', allow_blank=True); ws.add_data_validation(dvm); dvm.add(f"L{first}:L{last + 50}")
rng = f"F{first}:J{last + 50}"
ws.conditional_formatting.add(rng, CellIsRule(operator="equal", formula=[f'"{D}"'], fill=PatternFill("solid", fgColor="CDEBD6"), font=Font(name="Arial", color="1E6B3A", bold=True)))
ws.conditional_formatting.add(rng, CellIsRule(operator="equal", formula=[f'"{N}"'], fill=PatternFill("solid", fgColor="FCEFC2"), font=Font(name="Arial", color="7A5B00")))
ws.conditional_formatting.add(rng, CellIsRule(operator="equal", formula=[f'"{S}"'], font=Font(name="Arial", color="B5B0A3")))
ws.conditional_formatting.add(f"K{first}:K{last + 50}", CellIsRule(operator="equal", formula=['"Готово"'], fill=PatternFill("solid", fgColor="CDEBD6"), font=Font(name="Arial", color="1E6B3A", bold=True)))
ws.conditional_formatting.add(f"L{first}:L{last + 50}", CellIsRule(operator="notEqual", formula=[f'"{W}"'], fill=PatternFill("solid", fgColor="F9D9D3"), font=Font(name="Arial", color="9A2B1A", bold=True)))
# whole row greys out once fully posted
ws.conditional_formatting.add(f"A{first}:E{last}", FormulaRule(formula=[f'$K{first}="Готово"'], font=Font(name="Arial", color="9A9A9A")))

widths = [5, 16, 46, 14, 14, 11, 11, 11, 11, 11, 13, 17, 52, 38, 24]
for i, w in enumerate(widths, 1): ws.column_dimensions[get_column_letter(i)].width = w
ws.freeze_panes = ws.cell(first, 4); ws.auto_filter.ref = f"A{HR}:{get_column_letter(len(head))}{last}"

# ---- Сводка ----
s = wb.create_sheet("Сводка")
s.append(["Сводка по площадкам"]); s["A1"].font = F(bold=True, size=14, color=AMBER); s["A1"].fill = PatternFill("solid", fgColor=INK); s.merge_cells("A1:E1")
s.append(["Площадка", "Запланировано", "Выложено", "Осталось", "Прогресс"])
for c in range(1, 6):
    s.cell(2, c).font = F(bold=True, color="FFFFFF"); s.cell(2, c).fill = PatternFill("solid", fgColor=INK); s.cell(2, c).alignment = Alignment(horizontal="center")
for i, p in enumerate(PLATS):
    col = get_column_letter(6 + i); r = 3 + i
    R = f"План!{col}{first}:{col}{last + 50}"
    s.append([p, f'=COUNTIF({R},"{N}")+COUNTIF({R},"{D}")', f'=COUNTIF({R},"{D}")', f"=B{r}-C{r}", f"=IF(B{r}=0,0,C{r}/B{r})"])
tr = 3 + len(PLATS)
s.append(["Всего публикаций", f"=SUM(B3:B{tr - 1})", f"=SUM(C3:C{tr - 1})", f"=B{tr}-C{tr}", f"=IF(B{tr}=0,0,C{tr}/B{tr})"])
s.append([]); s.append(["Пунктов плана", f'=COUNTA(План!C{first}:C{last + 50})'])
s.append(["Готово целиком", f'=COUNTIF(План!K{first}:K{last + 50},"Готово")'])
s.append(["Материал не готов (снять / сделать / цифры)", f'=COUNTIF(План!L{first}:L{last + 50},"<>{W}")-COUNTBLANK(План!L{first}:L{last + 50})'])
for r in range(3, tr + 5):
    for c in range(1, 6):
        cell = s.cell(r, c); cell.font = F(size=11, bold=(r == tr)); cell.border = border if r <= tr else Border()
    s.cell(r, 5).number_format = "0%"
s.column_dimensions["A"].width = 44
for c in "BCDE": s.column_dimensions[c].width = 15

# ---- Как пользоваться ----
h = wb.create_sheet("Как пользоваться")
lines = [
 ("Как пользоваться таблицей", True),
 ("1. Идём по листу «План» сверху вниз — это рекомендуемый порядок. Даты не жёсткие: порядок можно менять, вырезав и вставив строку.", False),
 ("2. Колонки Telegram / VK / Instagram / YouTube / TG-чат: «Нужно» — надо выложить, «Выложено» — вышло, «—» — на этой площадке не публикуем. Значения выбираются из списка.", False),
 ("3. «Статус» считается сам: «Готово», когда на всех нужных площадках стоит «Выложено», иначе — сколько площадок осталось.", False),
 ("4. «Материал»: «Готов» — можно публиковать; «Нужно снять», «Нужно сделать», «Ждём цифры опроса» — подсвечено красным, сначала доделать.", False),
 ("5. Новый пункт — добавьте строку внизу и выберите значения из списков; на листе «Сводка» он учтётся автоматически.", False),
 ("Пример строки: «Рилс «Полный зал» | Рилс | Атмосфера | Telegram: Нужно | VK: Выложено | Instagram: Выложено | YouTube: — | TG-чат: — | Материал: Готов».", False),
]
for t, b in lines:
    h.append([t]); c = h.cell(h.max_row, 1); c.font = F(size=13 if b else 11, bold=b); c.alignment = Alignment(wrap_text=True, vertical="top")
h.column_dimensions["A"].width = 120
for r in range(2, h.max_row + 1): h.row_dimensions[r].height = 32

from openpyxl.workbook.properties import CalcProperties
wb.calculation = CalcProperties(fullCalcOnLoad=True)
wb.save("kontent-plan-RESHENO.xlsx"); print("rows", len(rows))
