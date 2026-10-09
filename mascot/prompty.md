# Промпты для новых поз зубра

## Как генерировать, чтобы персонаж не «поплыл»

- **Всегда прикладывайте референс** — исходную картинку зубра (лучше `zubr-priglashaet.png` в полный рост).
  - ChatGPT / GPT-image: загрузить картинку + «Сделай этого же персонажа…» + промпт.
  - Midjourney: `--cref <ссылка на картинку> --cw 100` (или `--oref` в новых версиях) — держит внешность и одежду.
  - Другие (Kandinsky, Шедеврум, Leonardo, Flux): режим «по референсу» / «character reference».
- **Бейдж с символикой форума обязателен** — он уже прописан в основе: жёлтый бейдж, на нём чёрный ромб и надпись РЕШЕНО, жёлтый шнурок с чёрными ромбиками, жёлтый значок-ромб на лацкане. Если генератор напишет «РЕШЕНО» с ошибкой или нарисует не тот знак — не страшно: присылайте, я заменю бейдж на правильный логотип при вырезке.
- **Белый фон** — я потом вырежу его в прозрачный PNG.
- Генерируйте по 3–4 варианта и берите тот, где морда и рога ближе всего к оригиналу.
- Английские промпты обычно дают более точный результат; в ChatGPT можно и по-русски (ниже есть русский вариант основы).

## Основа (вставлять в начало каждого промпта)

**EN:**
> The same character as in the reference image: an anthropomorphic European bison (zubr) mascot, Pixar-style 3D render, fluffy curly dark-brown fur, short curved cream-coloured horns, brown eyes, friendly confident smile. He wears an oversized black blazer, a white crew-neck t-shirt, wide black trousers, grey chunky sneakers, a small yellow diamond-shaped pin on the left lapel, and a yellow lanyard with small black diamond icons holding a yellow rectangular badge; on the badge: a black diamond (a square rotated 45°) with the bold black word «РЕШЕНО» below it, exactly as in the reference. POSE: [ПОЗА]. Full body, centered, plain pure white background, soft studio lighting, high detail, no text, no watermark.

**RU (для ChatGPT):**
> Тот же персонаж, что на картинке: антропоморфный зубр-маскот, 3D в стиле Pixar, пушистая кудрявая тёмно-коричневая шерсть, короткие изогнутые светлые рога, карие глаза, дружелюбная уверенная улыбка. Одет в свободный чёрный пиджак, белую футболку, широкие чёрные брюки, серые массивные кроссовки, на лацкане маленький жёлтый значок-ромб, на шее жёлтый шнурок с чёрными ромбиками и жёлтым прямоугольным бейджем: на бейдже чёрный ромб (квадрат, повёрнутый на 45°) и под ним жирная чёрная надпись «РЕШЕНО» — как на референсе. ПОЗА: [поза]. В полный рост, по центру, чистый белый фон, мягкий студийный свет, высокая детализация, без текста.

## Позы — подставить вместо [ПОЗА]

### Эмоции (для мемов)
| # | Что | POSE (EN) |
|---|---|---|
| 1 | Смеётся до слёз | laughing out loud with tears in his eyes, holding his belly, head tilted back |
| 2 | В шоке | shocked, eyes wide open, mouth open, both hands pressed to his cheeks |
| 3 | Фейспалм | facepalm, one hand covering his eyes, disappointed sigh |
| 4 | Закатывает глаза | rolling his eyes, arms crossed, unimpressed expression |
| 5 | Злится на телефон | angry, frowning, steam coming out of his ears, glaring at a smartphone in his hand |
| 6 | Устал | exhausted, sitting on the floor, head in his hands, slumped shoulders |
| 7 | «Класс» | big happy grin, two thumbs up |
| 8 | Подмигивает | winking at the camera, pointing at the viewer with a finger gun |
| 9 | Хитрый план | sly smile, narrowed eyes, rubbing his hands together |
| 10 | Спит над ноутбуком | asleep at a desk, head resting on a laptop keyboard, a coffee cup nearby |

### Жизнь владельца
| # | Что | POSE (EN) |
|---|---|---|
| 11 | 99+ сообщений | staring at a smartphone with a stressed face, the screen shows a huge pile of chat notifications |
| 12 | Пустая табличка | holding a large blank white sign with both hands in front of his chest |
| 13 | Считает | using a big calculator, focused expression, receipts in the other hand |
| 14 | Тренер | holding a soccer ball under one arm and a whistle in his mouth, coach stance |
| 15 | Утро понедельника | holding a big coffee mug with both hands, sleepy half-closed eyes |
| 16 | Графики | sitting at a desk with a laptop showing growing charts, pleased smile |
| 17 | Нервный звонок | talking on the phone, worried expression, hand on his forehead |
| 18 | Пустые карманы | pulling out empty trouser pockets, awkward smile, shrugging |

### Форум
| # | Что | POSE (EN) |
|---|---|---|
| 19 | Едет на форум | walking confidently, pulling a small travel suitcase |
| 20 | Селфи | taking a selfie with a smartphone held at arm's length, cheerful |
| 21 | Протягивает билет | holding a yellow ticket out toward the viewer, inviting smile |
| 22 | Рукопожатие | stretching out his hand for a handshake toward the viewer |
| 23 | Аплодирует | clapping his hands enthusiastically, big smile |
| 24 | С микрофоном | speaking into a handheld microphone, other hand gesturing, confident |

### Для сторис и вёрстки
| # | Что | POSE (EN) |
|---|---|---|
| 25 | Указывает вниз | pointing down with both index fingers, excited face |
| 26 | Указывает вверх | pointing up with one finger, "idea!" expression |
| 27 | Выглядывает сбоку | peeking in from the right edge of the frame, only half of his body visible, curious face |
| 28 | Сидит в кресле | sitting in a modern armchair, legs crossed, relaxed and confident |
| 29 | Портрет по пояс | waist-up portrait, looking straight at the camera, warm smile (заменить «Full body» на «waist-up») |
| 30 | Со спины | seen from behind, looking at a big stage with yellow lights |

После генерации пришлите картинки — вырежу фон, при необходимости поправлю бейдж и добавлю в `png/`.
