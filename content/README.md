# Контент РЕШЕНО

Папка на каждую неделю: `week-NN_ДД.ММ-ДД.ММ/`, внутри — `telegram/`, `telegram-chat/`, `vk/`, `instagram/`. Начинать с `README.md` недели.

## `_kit/` — генератор картинок в фирменном стиле

Все слайды, обложки и сторис рисуются из одного HTML-шаблона (`kit.html`: цвета, шрифты Unbounded/Montserrat, логотип — как на сайте). Картинки недели описаны в `week-NN.mjs`: поменяли текст → перерисовали.

```bash
cd content/_kit
python3 -m http.server 8766 --bind 127.0.0.1 &   # отдать шаблон браузеру
node render.mjs week-01.mjs                      # все картинки недели
node render.mjs week-01.mjs itogi                # только файлы, где в пути есть «itogi»
```

Нужны Node 22 и Playwright с Chromium.
