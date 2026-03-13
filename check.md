Title: Как я стал кодить с Claude в 5 раз эффективнее с AI Factory

URL Source: https://habr.com/ru/articles/995038/

Published Time: 2026-02-12T10:00:21+03:00

Markdown Content:
Как я стал кодить с Claude в 5 раз эффективнее с AI Factory / Хабр
===============

[Реклама](https://yandex.ru/adfox/406261/clickURL?ad-session-id=2286461773398827396&adfox-version=1&erid=F7NfYUJCUneTUTAd6tZY&hash=2af8119d0acd5c07&p1=djueo&p2=joaq&p5=bietqz&pr=gposhjy&puid1=post&puid2=f_popsci&puid3=h_artificial_intelligence&puid4=no&puid5=%2Fru%2Farticles%2F995038%2F&puid6=ru&rand=gopkfzx&rqs=KkNxqRLao0wr67NpT_JqM_YGF1XUkIff&sj=iETiaina1XPxXiHOoo0xZ2xSzHx4GqXxRQwywVwU-ANmAEwdMHzcm6gPDLn8fAtbOMXrrLpaTBVtDUnlfD7nm0rtzX5HQlFvgRfrHx4q3z42EBuPH0V82W4b-EUFq9Oa1r31DsShl9-RFjVXfaPelxKBhfvdmXkD7hglQz2hjSgVSZzyvQGgV0d5yaN2GLpPE-QxE-b_FmUeRA%3D%3D&ybv=0.1304212&ylv=0.1304212&ytt=362838837166085&pf=https%3A%2F%2Fcareer.habr.com%2Fcourses%3Futm_source%3Dhabr%26utm_medium%3Dhead_banner%26utm_campaign%3Dcourses)

[](https://habr.com/ru/feed)[Все потоки](https://habr.com/ru/articles/)

[![Image 1: Курсы для карьерного роста](https://effect.habr.com/a/e-S8_Q7wSJ5ea9i5jNAOoUWm328G_NREjAKtY4TyMUNrrBaVmFzJVS8BM2kmNkxL2orrEEn0ifz98hGCcndRU5L731iUVBbMS-EscWdhssWzHfux30bRWpWTjohlHMSem7Wz3r9ugMc531PUoRXnL1EFdxQu9GVuJivwMPNapCx1raMBVGSpAsUdMw6aI_RsjUHQdgrMgaUSEX5HHwCbf-bJ6I2Gos68) Курсы для карьерного роста](https://effect.habr.com/a/1vwIHcCYHZ-JPyXgWqp6hx4wmEaX0sPbkwxTNU14Nf05GyN3ovvnuFPCu9GRwpAfl9JNFiJ7VgYbSECutSqqkbJ_eKtPIhddHMiu7cD9Q7j6am8zCeHiHpgBZ8sYVSWHwAM_IcN0t9ti2WMAqi-6bGTjcKH6wuub4w2HrXZyn1Z9gGgd9aSkZ8ZTafF9Dqe3Px5g6DPbQjA)

[](https://habr.com/ru/search/)

[](https://habr.com/ru/sandbox/start/)

[Войти](https://habr.com/kek/v1/auth/habrahabr/?back=/ru/articles/995038/&hl=ru)

[![Image 2](https://habrastorage.org/r/w48/getpro/habr/avatars/9a7/175/dca/9a7175dca238510ee177e5e06b5fe8f6.jpg)](https://habr.com/ru/users/Cutcode/)[Cutcode](https://habr.com/ru/users/Cutcode/)12 фев в 07:00

Как я стал кодить с Claude в 5 раз эффективнее с AI Factory
===========================================================

Простой

5 мин

23K

[Искусственный интеллект](https://habr.com/ru/hubs/artificial_intelligence/)

Обзор

Расскажу про инструмент, который я создал для ускорения настройки проекта для его эффективной работы с AI агентом (в моём случае Claude Code). Я долгое время работал с SpecKit - крутой проект ( [даже написал статью про него](https://habr.com/ru/articles/964368) ). Мне он очень помогал в работе и дал понимание работы с LLM. Но со временем я начал замечать недостатки, которые начали напрягать всё сильнее.

Проблема
--------

Перед началом работы с ИИ-агентом над проектом мой стандартный сценарий выглядит так:

**1. Организация работы**

*   Ресерч темы

*   Планирование (я работал с SpecKit): объяснять агенту структуру проекта, описывать стэк и правила работы, составление планов и их проверки

**2. Настройка skills**

*   Искать подходящие skills на skills.sh

*   Копировать в `.claude/skills/`

*   Если нужного skill нет - писать с нуля (ну генерировать если быть точнее)

**3. Конфигурация MCP серверов**

*   Открывать `.claude/settings.local.json` и прописывать MCP серверы

*   Добавлять переменные окружения

**Итог:** 30-60 минут настройки перед началом реальной работы (в смысле вайб-кодинга). Постепенно я стал автоматизировать процессы и это постепенно переросло в проект AI factory.

Что решает AI Factory
---------------------

**Автоматизация настройки:**

*   `ai-factory init` → интерактивно настраивает все за 2-3 минуты

*   Сканирует существующий проект (package.json, composer.json, requirements.txt)

*   Определяет стэк и скачивает подходящие skills с skills.sh

*   Генерирует недостающие skills под ваш проект

*   Конфигурирует MCP серверы по выбору **Результат:** от 30-60 минут настройки до 5-10 минут.

**Единый контекст:**

*   `.ai-factory/DESCRIPTION.md` - всегда актуальная спецификация проекта для контекста агенту - не нужно повторять объяснения над чем работаем в каждом чате

**Структурированный workflow:**

*   Четкие команды: `/task` для быстрых задач, `/feature` для больших фич, `/fix` для багов

*   Автоматические планы и чекпоинты

*   Conventional commits из коробки

**Система обучения:**

*   Каждый фикс создает патч с описанием проблемы

*   Следующие задачи учитывают прошлые ошибки

*   `/evolve` улучшает skills на основе опыта проекта

AI Factory
----------

**Идея проста:** минимум настройки, преимущество использования спецификаций для контекста LLM и качество кода c MCP+суб-агентами со скиллзами. Ну и комфорт работы - всё что нужно уже под рукой!

[GitHub](https://github.com/lee-to/ai-factory)

Что подтолкнуло к созданию? Опыт работы с **SpecKit** и **OpenSpec**. Оба инструмента хороши, но на мой взгляд есть недостатки.

### Опыт работы с SpecKit и OpenSpec

Я активно использовал оба инструмента и столкнулся с конкретными проблемами:

**SpecKit** (от GitHub):

*   **Избыточная документация**: генерирует сотни строк спецификаций, планов и чек-листов. Для небольших задач это overhead

*   **Жесткий workflow**: сложно пропустить шаги вроде тестирования, даже когда это не нужно

*   **Проблемы контекста**: много токенов уходит на работу

*   **Сложность рефакторинга**: когда нужно быстро пофиксить баг, приходится идти через весь цикл `/specify` → `/plan` → `/tasks` → `/implement`

**OpenSpec** (более простой):

*   **Validation баги**: часто показывает ошибки валидации, даже когда все правильно. `openspec validate` и `openspec show` возвращают противоречивые результаты

*   **Проблемы с контролем**: ИИ иногда игнорирует workflow и начинает реализацию без команды `/openspec:apply`

*   **Сложность для больших проектов**: неясно, как применять для существующих крупных кодовых баз

**Общая проблема обоих:**

*   Требуют ручной настройки под каждый проект

*   Требуют предварительного ресерча темы

*   Недостаточная автоматизация генерации skills и подключения MCP

AI Factory учитывает эти моменты и решает их.

Видео обзор AI factory
----------------------

Для тех, кто больше любит контент в формате видео, записал обзор:

Начало работы
-------------

`npm install -g ai-factoryai-factory init`

[Объяснить с![Image 3](https://habr.com/img/sourcecraft-light.bf8f84c1..svg)](https://sourcecraft.dev/)

При инициализации:

*   Интерактивные вопросы о проекте и агенте

*   Автоматическая настройка MCP серверов

*   Создание конфига `.ai-factory.json`

Для нового проекта - спросит о стэке. Для существующего - сам проанализирует код и подберет нужное.

Основные команды
----------------

| Команда | Использование | Ветка? | План? |
| --- | --- | --- | --- |
| `/ai-factory.task` | Быстрые задачи | Нет | `.ai-factory/plan.md` |
| `/ai-factory.feature` | Большие фичи | Да | `.ai-factory/features/<name>.md` |
| `/ai-factory.fix` | Баги и ошибки | Нет | Нет |
| `/ai-factory.implement` | Выполнение плана | - | - |
| `/ai-factory.evolve` | Улучшение skills | - | - |

### Workflow

**Для небольших задач:**

```
/ai-factory.task → план → /ai-factory.implement → готово
```

[Объяснить с![Image 4](https://habr.com/img/sourcecraft-light.bf8f84c1..svg)](https://sourcecraft.dev/)

**Для фич:**

```
/ai-factory.feature → ветка + план → /ai-factory.implement → коммиты → готово
```

[Объяснить с![Image 5](https://habr.com/img/sourcecraft-light.bf8f84c1..svg)](https://sourcecraft.dev/)

**Для багов:**

```
/ai-factory.fix → фикс + логирование + патч → готово
```

[Объяснить с![Image 6](https://habr.com/img/sourcecraft-light.bf8f84c1..svg)](https://sourcecraft.dev/)

Ключевые возможности
--------------------

### 1. /ai-factory - настройка контекста

Анализирует проект, определяет стэк, подбирает skills с skills.sh или генерирует новые, конфигурирует необходимые MCP.

### 2. Feature и Task планирование

`/ai-factory.feature` - для больших задач с веткой и полным планом.

`/ai-factory.task` - для быстрых изменений без ветки.

Оба анализируют требования, изучают кодовую базу, создают задачи с зависимостями.

### 3. /ai-factory.implement - выполнение созданного плана

`/ai-factory.implement 5      # работай с задачей #5 если хотим сделать что-то конкретное`

[Объяснить с![Image 7](https://habr.com/img/sourcecraft-light.bf8f84c1..svg)](https://sourcecraft.dev/)

Перед началом агент прочитает все патчи из `.ai-factory/patches/` - учится на прошлых ошибках.

### 4. /ai-factory.fix - быстрые фиксы

Делаем, если понятно, что проблема небольшая. Агент изучает проблему, применяет фикс с логированием, создает патч для самообучения. Никаких планов - сразу решение и обучение.

### 5. /ai-factory.evolve - самообучение skills

`/ai-factory.evolve           # Все skills/ai-factory.evolve fix       # Конкретный skill`

[Объяснить с![Image 8](https://habr.com/img/sourcecraft-light.bf8f84c1..svg)](https://sourcecraft.dev/)

Анализирует все патчи, находит паттерны ошибок, улучшает skills с вашего одобрения.

### 6. /ai-factory.skill-generator

**Режим обучения** - передайте URL для генерации skills из документации:

`/ai-factory.skill-generator https://fastapi.tiangolo.com/tutorial/`

[Объяснить с![Image 9](https://habr.com/img/sourcecraft-light.bf8f84c1..svg)](https://sourcecraft.dev/)

Изучает источники, обогащает через поиск, генерирует полноценный кастомные skill.

### Система самообучения

Каждый фикс создает **патч** - документ, который помогает избежать подобных ошибок в будущем.

**Цикл обучения:**

```
/fix → баг → фикс → патч → 
следующий /fix или /implement → читает патчи → лучший код
```

[Объяснить с![Image 10](https://habr.com/img/sourcecraft-light.bf8f84c1..svg)](https://sourcecraft.dev/)

**Структура патча:**

*   Проблема и причина

*   Примененное решение

*   Рекомендации по превенции

*   Теги для поиска

Периодически запускайте `/ai-factory.evolve` - инструмент проанализирует накопленные патчи и улучшит skills под ваш проект.

Структура проекта
-----------------

```
project/
├── .claude/skills/          # Skills
├── .ai-factory/
│   ├── DESCRIPTION.md       # Спецификация
│   ├── PLAN.md             # Текущий план
│   ├── features/           # Планы фич
│   ├── patches/            # Патчи для обучения
│   └── evolutions/         # Логи улучшений
└── .ai-factory.json        # Конфиг
```

[Объяснить с![Image 11](https://habr.com/img/sourcecraft-light.bf8f84c1..svg)](https://sourcecraft.dev/)

### MCP серверы

Поддерживаются GitHub, Postgres, Filesystem. Конфигурация в `.claude/settings.local.json`.

### Best Practices

*   **Логирование**: уровни DEBUG/INFO/WARN/ERROR, контроль через `LOG_LEVEL`

*   **Коммиты**: чекпоинты каждые 3-5 задач, conventional commits формат

*   **Тесты**: всегда спрашивается перед планом, не добавляется без согласия

#### Развитие инструмента

После активного использования за несколько дней сделал два релиза (v1.1 и v1.2):

**v1.1:** улучшенный Skill Generator, режим обучения

**v1.2:** система патчей, `/ai-factory.evolve`, организация фич

**v1.3. Безопасность превыше всего!**

 Критически важное обновление - системой защиты от prompt-injection. Скачивая skills с skills.sh, мы доверяем внешним источникам доступ к вашему проекту. Теперь каждый skill проходит обязательное сканирование на 10 категорий угроз - от инъекций и утечек данных до социальной инженерии. Двухуровневая проверка (regex + LLM-анализ намерений) отсекает вредоносный код. `/skill-generator scan` позволяет проверить любой файл вручную.

 Также добавлен новый skill `/ai-factory.improve` для доработки уже созданных планов - когда понимаешь, что план хорош, но чего-то не хватает.

Конечно же для разработки AI factory я использовал AI factory).

Итог
----

AI Factory решает конкретные проблемы разработки с ИИ:

✅ Автоматическая настройка под проект

 ✅ Spec-driven подход с контролем

 ✅ Самообучение на ошибках

 ✅ Простой workflow

### Отлично подойдёт если вы

*   Устали от настроек перед каждым проектом

*   Хотите структурированный подход при работе с AI

*   Работаете над реальными проектами

*   Есть опыт с Claude Code или аналогами

### О будущем

У меня теперь появилась команда помощников - экспертов в разных областях. Я делаю проекты, за которые раньше не взялся бы из-за незнания стэка.

Это инструмент. Опыт разработчика важен - часто приходится корректировать предложенные решения. ИИ - это помощник для специалистов, а не замена разработчику.

Ссылки
------

*   [GitHub](https://github.com/lee-to/ai-factory)

*   [AI чат CutCode](https://t.me/ai_chat_cutcode)

Библиотека бесплатная. Вклад и обратная связь приветствуется.

А у вас есть опыт со spec-driven подходом? Делитесь в комментариях.

Теги:
*   [claude](https://habr.com/ru/search/?target_type=posts&order=relevance&q=[claude])
*   [spec driven development](https://habr.com/ru/search/?target_type=posts&order=relevance&q=[spec+driven+development])
*   [github](https://habr.com/ru/search/?target_type=posts&order=relevance&q=[github])
*   [openspec](https://habr.com/ru/search/?target_type=posts&order=relevance&q=[openspec])
*   [speckit](https://habr.com/ru/search/?target_type=posts&order=relevance&q=[speckit])
*   [claude code](https://habr.com/ru/search/?target_type=posts&order=relevance&q=[claude+code])

Хабы:
*   [Искусственный интеллект](https://habr.com/ru/hubs/artificial_intelligence/)

+23

129

[24](https://habr.com/ru/articles/995038/comments/)[+24](https://habr.com/ru/articles/995038/comments/)

Редакторский дайджест Присылаем лучшие статьи раз в месяц

Подписаться Оставляя почту, я принимаю [Политику конфиденциальности](https://account.habr.com/ru/info/confidential) и даю согласие на получение рассылок

[![Image 12](https://habrastorage.org/getpro/habr/avatars/9a7/175/dca/9a7175dca238510ee177e5e06b5fe8f6.jpg)](https://habr.com/ru/users/Cutcode/)

67

Карма

16.6

Общий рейтинг

Данил Щуцкий[@Cutcode](https://habr.com/ru/users/Cutcode/)

Backend PHP Developer

Подписаться

[Сайт](https://cutcode.dev/)[Сайт](https://moonshine-laravel.com/)[Telegram](https://telegram.me/ai_chat_cutcode)

Поток AI и ML доступен 24/7 благодаря поддержке друзей Хабра

![Image 13: Хабр Карьера Курсы](https://habrastorage.org/webt/qq/ey/pn/qqeypn-py71suynxbusbakjdfjw.png)

Хабр Курсы для всех

РЕКЛАМА

 Практикум, Хекслет, SkyPro, авторские курсы — собрали всех и попросили скидки. Осталось выбрать! 

[Перейти](https://career.habr.com/courses/?erid=2VSb5wDLYUH&utm_source=habr&utm_medium=sponsorship_hub)

[Перейти в поток AI и ML](https://habr.com/ru/flows/ai_and_ml/)

[Комментарии 24](https://habr.com/ru/articles/995038/comments/)

Публикации
----------

Лучшие за сутки Похожие

*   [![Image 14](https://habrastorage.org/r/w48/getpro/habr/avatars/78a/bec/e29/78abece297797d2d6d22d1ee77e2aebf.jpeg)](https://habr.com/ru/users/cyberscoper/)[cyberscoper](https://habr.com/ru/users/cyberscoper/)19 часов назад   
[Как ТСПУ ловит VLESS в 2026 и почему XHTTP — следующий шаг](https://habr.com/ru/articles/1009542/)
---------------------------------------------------------------------------------------------------

Средний 7 мин 43K Аналитика    +127 334[127](https://habr.com/ru/articles/1009542/comments/)[+127](https://habr.com/ru/articles/1009542/comments/)  
*   [![Image 15](https://habrastorage.org/r/w48/getpro/habr/avatars/3a9/a0c/722/3a9a0c722ab0b73193e60b9f84f9a2c0.png)](https://habr.com/ru/users/ntsaplin/)[ntsaplin](https://habr.com/ru/users/ntsaplin/)23 часа назад   
[Как мы отправили сисадмина поставить сервер в Антарктиде](https://habr.com/ru/companies/ruvds/articles/1009366/)
-----------------------------------------------------------------------------------------------------------------

8 мин 13K    +70 27[20](https://habr.com/ru/companies/ruvds/articles/1009366/comments/)[+20](https://habr.com/ru/companies/ruvds/articles/1009366/comments/)  
*   [![Image 16](https://assets.habr.com/habr-web/release_2.306.0/img/avatars/189.png)](https://habr.com/ru/users/interpres/)[interpres](https://habr.com/ru/users/interpres/)21 час назад   
[Анализ плутония из советского датчика дыма](https://habr.com/ru/companies/ruvds/articles/1006518/)
---------------------------------------------------------------------------------------------------

Простой 9 мин 10K Кейс Перевод    +55 21[19](https://habr.com/ru/companies/ruvds/articles/1006518/comments/)[+19](https://habr.com/ru/companies/ruvds/articles/1006518/comments/)  
*   [![Image 17](https://habrastorage.org/r/w48/getpro/habr/avatars/5a7/996/d26/5a7996d26c80c4581a9a0e783646940d.jpg)](https://habr.com/ru/users/vada/)[vada](https://habr.com/ru/users/vada/)4 часа назад   
[Хьюстон, у нас проблемы! Наводим порядок в зоопарке инструментов и возвращаем контроль над продуктом](https://habr.com/ru/companies/simpleone/articles/1009440/)
-----------------------------------------------------------------------------------------------------------------------------------------------------------------

Простой 7 мин 4.2K Обзор    +46 14[1](https://habr.com/ru/companies/simpleone/articles/1009440/comments/)[+1](https://habr.com/ru/companies/simpleone/articles/1009440/comments/)  
*   [![Image 18](https://habrastorage.org/r/w48/getpro/habr/avatars/ee6/cdb/785/ee6cdb7855777d7576810014ec8ba4d0.jpeg)](https://habr.com/ru/users/evgenii_vertii/)[evgenii_vertii](https://habr.com/ru/users/evgenii_vertii/)19 часов назад   
[Застегните ширинки, мамкины киберпанки. Забудьте на хрен про ИИ](https://habr.com/ru/articles/1009544/)
--------------------------------------------------------------------------------------------------------

Простой 2 мин 12K    +45 40[38](https://habr.com/ru/articles/1009544/comments/)[+38](https://habr.com/ru/articles/1009544/comments/)  
*   [![Image 19](https://habrastorage.org/r/w48/getpro/habr/avatars/98e/b11/b26/98eb11b266f2488021151b718c127cb5.jpg)](https://habr.com/ru/users/veselcraft/)[veselcraft](https://habr.com/ru/users/veselcraft/)20 часов назад   
[Как мы отреверсили Агент@Mail.ru и над нами смеялась половина Твиттера](https://habr.com/ru/articles/1009528/)
---------------------------------------------------------------------------------------------------------------

Средний 5 мин 12K Кейс [Из песочницы](https://habr.com/ru/sandbox/)    +31 25[28](https://habr.com/ru/articles/1009528/comments/)[+28](https://habr.com/ru/articles/1009528/comments/)  
*   [![Image 20](https://habrastorage.org/r/w48/getpro/habr/avatars/bd1/ef8/698/bd1ef869856c11faefef406d4189c2a6.png)](https://habr.com/ru/users/ARad/)[ARad](https://habr.com/ru/users/ARad/)17 часов назад   
[Почему они хотят избавиться от инженеров-программистов](https://habr.com/ru/articles/1009570/)
-----------------------------------------------------------------------------------------------

Простой 4 мин 20K Мнение Перевод    +23 34[60](https://habr.com/ru/articles/1009570/comments/)[+60](https://habr.com/ru/articles/1009570/comments/)  
*   [![Image 21](https://assets.habr.com/habr-web/release_2.306.0/img/avatars/092.png)](https://habr.com/ru/users/nastyakopi/)[nastyakopi](https://habr.com/ru/users/nastyakopi/)20 часов назад   
[Добавили флагманские серверы для AI-тренинга и новые образы в AI-маркетплейс: дайджест февральских новостей Selectel](https://habr.com/ru/companies/selectel/articles/1009492/)
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

4 мин 6.1K    +21 5[0](https://habr.com/ru/companies/selectel/articles/1009492/comments/)  
*   [![Image 22](https://habrastorage.org/r/w48/getpro/habr/avatars/b74/878/0b6/b748780b68714225baac6fce502df5ba.png)](https://habr.com/ru/users/oneastok/)[oneastok](https://habr.com/ru/users/oneastok/)2 часа назад   
[Линейка HighFreq или как выжать из облака максимум для инференса, ML и других высоких нагрузок](https://habr.com/ru/companies/selectel/articles/1009450/)
----------------------------------------------------------------------------------------------------------------------------------------------------------

10 мин 3K Обзор    +20 1[0](https://habr.com/ru/companies/selectel/articles/1009450/comments/)  
*   [![Image 23](https://habrastorage.org/r/w48/getpro/habr/avatars/8de/9c5/34a/8de9c534a18a6cb8693270a2b528d4c0.png)](https://habr.com/ru/users/PatientZero/)[PatientZero](https://habr.com/ru/users/PatientZero/)20 часов назад   
[Более быстрый asin()](https://habr.com/ru/articles/1009424/)
-------------------------------------------------------------

Средний 9 мин 7.1K Перевод    +20 20[3](https://habr.com/ru/articles/1009424/comments/)[+3](https://habr.com/ru/articles/1009424/comments/)  

[Сезон Heavy Digital: истории о цифровых двойниках, машинном зрении и IIoT](https://effect.habr.com/a/tNOIiy0opeb_obo1tYpJqXTAzkpch9en4_EtQDEY02q-3lZ333Z0DUja9BzzijczldV2z67Yclny45ow2aS6FxItXIieKxOHGgK6FxMFy5Br6_4nuy2F-nhFKEr3JD28hGVZJ26HYMJl)

Турбо 

Показать еще

Минуточку внимания
------------------

[![Image 24](https://effect.habr.com/a/Eho_lNDVqlWLY3Ux-KKFY8ah_-o1LC5fC3IuY3rfo0D_WXgI0OMZRHs5wLrOFqf3Z1bdVe3bxV0jkP9tlJw1iA8a-_CnvmR_QrHkCpnPY9iWz9kbCX7aCg3Y5C0b2jMm0oChJQzyP6PHjp79VLryYCkwoDJIzzqfW7nADsUdtmIW6Vj_4cGLXOpQud2-sMYF0axi_SNo5FY_xqZPivbmiX4VwLqlcWhfw8pQUm3F) Промо ### Курс Хабра для маркетологов: 600 человек уже прошли](https://effect.habr.com/a/uUvI0LZFh72SG1h6DS-fguIOcypa8Lp9xBo_UEbJT6dBZTV2JMtTIcX6k1UkNj-up2_j8lTok_MLvcBNjEPQcCFhhDnsnNOsHU9b-MO9CG4J7UueDE8YUaDN1nMOxWpdO5nt4BJmMZiXXPGvbaiYVknGPpoHRbG7WLA10DTRQQGkJPxKaKZ3SWhlrytAufGfZczSxIJAjsJ2eN05PyIptA)

[![Image 25](https://effect.habr.com/a/z0QgC3KeNFGV4J_BxgrJAPqvAhEnVjF6werL4fuc5v5l47LnD649Fr85z9LFxpdrZqWpG4qtLyM0xOzYGb5H1kkdLMZxdWlB_pCIxymPf8pGCekv0zt4wsz6JBxis1lmLNze7G4hlGniNkQBmkxdP8gjUpKOD81U6UniGKh_wjwOr53Qbs2Klnwx6exnjyxWlxEBxcvps905MlHX_aE) Событие ### Врываемся в новый год и летим на митапы из Календаря](https://effect.habr.com/a/c3rnnCAXSUutzLWiUNFKTYU1xl23C0tI3EoAca2iUNplM6SYbGbqGiEp9cezORtpxE5Y3LDceFPCJ117AkfU14CIzw4MD0BNiSfNVDQWWMQ0vWh08qlYpqji9eT-PjV1)

[![Image 26](https://effect.habr.com/a/jQDcokY7EUMPH3Lis7TB1ktmbnF3o1X8VcX2Iv4asxpp8lpRmeTwrm3-5s7qGlVClTYUJpqQ7s9ZqLBdOALRt3S7XQ7uS4338f7w8I_FOwduGmjdDkiM80yiNKJ6fALnY5F00sOUSgPsP3CJT8LxCv3lE8Y5B9TXq7MaKXcmcZmbSu5qvjTAwaUk_zUMyhmiGR3GYmEb7qakzRjYxqM) Промо ### В зимние морозы согреваемся тёплыми скидками](https://effect.habr.com/a/89apzIPVvBi4O55JbyF7_UKDT7NDB1_9OnAbz6Czg2wqZU2z0GUqcZZe93gerhHAqWQPjZWNFHEwQ4DFOcUu6h6bJROFtVl5AJBQtKUIr1eQLmqVZxJ-0NLpo04)

[Вопросы и ответы](https://qna.habr.com/questions?utm_campaign=questions_postlist&utm_content=questions&utm_medium=habr_block&utm_source=habr_mob)

*   [Почему не получается собрать сайт на Hugo?](https://qna.habr.com/q/1409180?utm_campaign=questions_postlist&utm_content=question&utm_medium=habr_block&utm_source=habr_mob)CSS Средний 1 ответ 
*   [404я при попытки авторизоваться через шторм в github. Как исправить?](https://qna.habr.com/q/1409144?utm_campaign=questions_postlist&utm_content=question&utm_medium=habr_block&utm_source=habr_mob)GitHub Средний 0 ответов 
*   [Как выложить исполняемый файл на Github?](https://qna.habr.com/q/1408834?utm_campaign=questions_postlist&utm_content=question&utm_medium=habr_block&utm_source=habr_mob)GitHub Простой 4 ответа 
*   [Почему пайплайн ругается на синтаксис?](https://qna.habr.com/q/1408668?utm_campaign=questions_postlist&utm_content=question&utm_medium=habr_block&utm_source=habr_mob)GitHub Простой 0 ответов 
*   [Есть ли рабочие альтернативы yt-dlp?](https://qna.habr.com/q/1407248?utm_campaign=questions_postlist&utm_content=question&utm_medium=habr_block&utm_source=habr_mob)YouTube Простой 2 ответа 

[Больше вопросов на Хабр Q&A](https://qna.habr.com/questions?utm_campaign=questions_postlist&utm_content=questions_all&utm_medium=habr_block&utm_source=habr_mob)

Читают сейчас
-------------

*   [Как ТСПУ ловит VLESS в 2026 и почему XHTTP — следующий шаг](https://habr.com/ru/articles/1009542/)
---------------------------------------------------------------------------------------------------

43K[127](https://habr.com/ru/articles/1009542/comments/)[+127](https://habr.com/ru/articles/1009542/comments/)  
*   [Я 13 лет строил чужой бизнес, потом поставил холодильник и зарабатываю 43 тыс с точки](https://habr.com/ru/companies/moysklad/articles/1008414/)
-------------------------------------------------------------------------------------------------------------------------------------------------

291K[80](https://habr.com/ru/companies/moysklad/articles/1008414/comments/)[+80](https://habr.com/ru/companies/moysklad/articles/1008414/comments/)  
*   [После блокировки мессенджеров Matrix стал единственной альтернативой?](https://habr.com/ru/companies/ruvds/articles/1009268/)
------------------------------------------------------------------------------------------------------------------------------

91K[237](https://habr.com/ru/companies/ruvds/articles/1009268/comments/)[+237](https://habr.com/ru/companies/ruvds/articles/1009268/comments/)  
*   [Учёные обнаружили первые прямые доказательства обмена материалами между двойными астероидами](https://habr.com/ru/articles/1008730/)
-------------------------------------------------------------------------------------------------------------------------------------

53K[10](https://habr.com/ru/articles/1008730/comments/)[+10](https://habr.com/ru/articles/1008730/comments/)  
*   [Claude рисует диаграммы прямо в чате — и это не генерация картинок, а кое-что круче](https://habr.com/ru/news/1009572/)
------------------------------------------------------------------------------------------------------------------------

26K[36](https://habr.com/ru/news/1009572/comments/)[+36](https://habr.com/ru/news/1009572/comments/)  
*   [Сезон Heavy Digital: истории о цифровых двойниках, машинном зрении и IIoT](https://effect.habr.com/a/tNOIiy0opeb_obo1tYpJqXTAzkpch9en4_EtQDEY02q-3lZ333Z0DUja9BzzijczldV2z67Yclny45ow2aS6FxItXIieKxOHGgK6FxMFy5Br6_4nuy2F-nhFKEr3JD28hGVZJ26HYMJl)Турбо   

Истории
-------

![Image 27](https://habrastorage.org/r/w390/getpro/effect/7ee/cc4/9eb/de5/18f/e4c49b3a53793e35627e06c11/_-2.png)![Image 28: author-logo](https://habrastorage.org/getpro/effect/9fd/412/122/2db/450/fde9cf622e997019533ae6fb7/Habr.png)

Просто скажи «th»

![Image 29](https://habrastorage.org/r/w390/getpro/effect/99c/e68/54b/ee0/eed/b810005f1efaf82992f600b5a/erodqyt9msakbi-cpes8vsase3k.jpeg)![Image 30: author-logo](https://habrastorage.org/getpro/effect/9fd/412/122/2db/450/fde9cf622e997019533ae6fb7/Habr.png)

Работать и учиться с умом

![Image 31](https://habrastorage.org/r/w390/getpro/effect/0dc/6a3/0ad/f9d/d52/2d16163c453b286d6974505e1/11.png)![Image 32: author-logo](https://habrastorage.org/getpro/effect/9fd/412/122/2db/450/fde9cf622e997019533ae6fb7/Habr.png)

Праздничная подборка к 8 Марта

![Image 33](https://habrastorage.org/r/w390/getpro/effect/67c/476/9c6/160/009/cf7d7a8019ace58b298558643/6__0.jpg)![Image 34: author-logo](https://habrastorage.org/getpro/effect/9fd/412/122/2db/450/fde9cf622e997019533ae6fb7/Habr.png)

Годнота из блогов компаний

![Image 35](https://habrastorage.org/r/w390/getpro/effect/e9d/4ba/126/584/492/8a5a72e3c7d48d797dc61c239/5.png)![Image 36: author-logo](https://habrastorage.org/getpro/effect/9fd/412/122/2db/450/fde9cf622e997019533ae6fb7/Habr.png)

Кот в доме хозяин

![Image 37](https://habrastorage.org/r/w390/getpro/effect/d35/92f/197/aab/bfb/5e298ddaf2c359d9f5bc77bbe/_1.jpg)![Image 38: author-logo](https://habrastorage.org/getpro/effect/9fd/412/122/2db/450/fde9cf622e997019533ae6fb7/Habr.png)

Схватил за мозг

Ближайшие события
-----------------

[![Image 39](https://habrastorage.org/r/w390/getpro/habr/upload_files/178/af8/4e3/178af84e3106dc65a76ca08c74148615.png)](https://habr.com/ru/events/912/)

26 февраля – 31 марта 

[Авторская рассылка Хабра для бизнеса](https://habr.com/ru/events/912/)

Онлайн

[Больше событий в календаре](https://habr.com/ru/events/#912)

Маркетинг

[![Image 40](https://habrastorage.org/r/w390/getpro/habr/upload_files/93b/ca0/14c/93bca014cd0533ecd9870cb97065926e.jpg)](https://habr.com/ru/events/920/)

3 марта – 9 июня 

[Экспедиция «Рэйдикс»](https://habr.com/ru/events/920/)

Екатеринбург • Новосибирск • Краснодар • Минск • Калининград • Ростов-на-Дону

[Больше событий в календаре](https://habr.com/ru/events/#920)

Разработка

Другое

[![Image 41](https://habrastorage.org/r/w390/getpro/habr/upload_files/e16/ff3/923/e16ff3923b4de6c7ed57cf9f582efaa4.png)](https://habr.com/ru/events/928/)

9 – 31 марта 

[Курс для маркетологов от Хабра — 600 человек уже прошли](https://habr.com/ru/events/928/)

Онлайн

[Больше событий в календаре](https://habr.com/ru/events/#928)

Маркетинг

[![Image 42](https://habrastorage.org/r/w390/getpro/habr/upload_files/e38/dc1/ff6/e38dc1ff688f1177bb4735fd3c930e43.png)](https://habr.com/ru/events/906/)

13 – 14 марта 

[Конференция Femtech Force Jam 2026](https://habr.com/ru/events/906/)

Онлайн

[Больше событий в календаре](https://habr.com/ru/events/#906)

Другое

[![Image 43](https://habrastorage.org/r/w390/getpro/habr/upload_files/9f1/f43/628/9f1f43628549a8250d35f386253cd5b3.png)](https://habr.com/ru/events/916/)

13 марта 

[Конференция «Цифровой Brand Day 2026»](https://habr.com/ru/events/916/)

Москва

[Больше событий в календаре](https://habr.com/ru/events/#916)

Маркетинг

Другое

[![Image 44](https://habrastorage.org/r/w390/getpro/habr/upload_files/a9c/af3/eed/a9caf3eed39a8c778f5079496c7d76dc.png)](https://habr.com/ru/events/932/)

19 марта – 31 декабря 

[Серия вебинаров «Эволюция приложения в облаке»](https://habr.com/ru/events/932/)

Онлайн

[Больше событий в календаре](https://habr.com/ru/events/#932)

Разработка

[![Image 45](https://habrastorage.org/r/w390/getpro/habr/upload_files/1ff/af7/643/1ffaf76435bdacea6f1f53cfd6817233.png)](https://habr.com/ru/events/910/)

19 марта 

[Квартирник по безопасной разработке 2026: обсудим будущее DevSecOps](https://habr.com/ru/events/910/)

Москва

[Больше событий в календаре](https://habr.com/ru/events/#910)

Разработка

Другое

[![Image 46](https://habrastorage.org/r/w390/getpro/habr/upload_files/783/508/6dd/7835086dd3e49409e3690d7c9b3ffda5.png)](https://habr.com/ru/events/864/)

27 марта 

[Публичная защита проектов и Церемония награждения HR Impact](https://habr.com/ru/events/864/)

Москва

[Больше событий в календаре](https://habr.com/ru/events/#864)

Менеджмент

Маркетинг

Другое

[![Image 47](https://habrastorage.org/r/w390/getpro/habr/upload_files/010/410/f65/010410f657c09fa64da1426967623009.jpg)](https://habr.com/ru/events/922/)

2 – 3 апреля 

[DevOpsConf: интеграция разработки, тестирования и эксплуатации](https://habr.com/ru/events/922/)

Москва • Онлайн

[Больше событий в календаре](https://habr.com/ru/events/#922)

Разработка

[![Image 48](https://habrastorage.org/r/w390/getpro/habr/upload_files/012/8aa/ff6/0128aaff68e7a5064543da4b823f34c3.png)](https://habr.com/ru/events/930/)

7 апреля 

[Онлайн-конференция «Сильный медицинский бренд»](https://habr.com/ru/events/930/)

Онлайн

[Больше событий в календаре](https://habr.com/ru/events/#930)

Менеджмент

Маркетинг

Другое

[![Image 49](https://habrastorage.org/r/w390/getpro/habr/upload_files/16e/066/ae1/16e066ae162a09292bbdf8d44e57647d.png)](https://habr.com/ru/events/874/)

9 апреля 

[Deckhouse Conf 2026 — конференция для тех, кто работает с ИТ-инфраструктурой](https://habr.com/ru/events/874/)

Москва

[Больше событий в календаре](https://habr.com/ru/events/#874)

Разработка

[![Image 50](https://habrastorage.org/r/w390/getpro/habr/upload_files/5f8/d78/db8/5f8d78db8fee63434386aac9578360bc.png)](https://habr.com/ru/events/900/)

9 апреля 

[GoCloud 2026 — ежегодная IT-конференция про AI и облака](https://habr.com/ru/events/900/)

Москва • Онлайн

[Больше событий в календаре](https://habr.com/ru/events/#900)

Разработка

Менеджмент

Другое

[![Image 51](https://habrastorage.org/r/w390/getpro/habr/upload_files/4f7/8fa/45d/4f78fa45d141ea67f6ed2c96279f3379.jpg)](https://habr.com/ru/events/904/)

14 апреля 

[K2 Cloud Conf 2026](https://habr.com/ru/events/904/)

Москва • Онлайн

[Больше событий в календаре](https://habr.com/ru/events/#904)

Разработка

Администрирование

Другое

[![Image 52](https://habrastorage.org/r/w390/getpro/habr/upload_files/43a/635/410/43a6354108fc207d3126427044561cd8.jpg)](https://habr.com/ru/events/898/)

17 – 18 апреля 

[Профессиональная IT-конференция Merge Tatarstan 2026](https://habr.com/ru/events/898/)

Иннополис

[Больше событий в календаре](https://habr.com/ru/events/#898)

Разработка

Маркетинг

Другое

[![Image 53](https://habrastorage.org/r/w390/getpro/habr/upload_files/606/e93/c4e/606e93c4e27ce2b8a8079adad4451dee.png)](https://habr.com/ru/events/924/)

20 апреля 

[AiConf — прикладная конференция по data science](https://habr.com/ru/events/924/)

Москва • Онлайн

[Больше событий в календаре](https://habr.com/ru/events/#924)

Разработка

Тестирование

[![Image 54](https://habrastorage.org/r/w390/getpro/habr/upload_files/efc/965/406/efc965406b5969f09138374bf4a0b18c.png)](https://habr.com/ru/events/890/)

3 – 5 июля 

[Летняя антиконференция Summer Merge](https://habr.com/ru/events/890/)

Село Успенское

[Больше событий в календаре](https://habr.com/ru/events/#890)

Разработка

Менеджмент

Другое

[![Image 55](https://habrastorage.org/r/w390/getpro/habr/upload_files/a07/b03/5d5/a07b035d51e9544444ed078d184921be.png)](https://habr.com/ru/events/918/)

5 июля 

[Фестиваль RUNIT by AGIMA](https://habr.com/ru/events/918/)

Москва

[Больше событий в календаре](https://habr.com/ru/events/#918)

Другое

Ваш аккаунт

*   [Войти](https://habr.com/kek/v1/auth/habrahabr/?back=/ru/articles/995038/&hl=ru)
*   [Регистрация](https://habr.com/kek/v1/auth/habrahabr-register/?back=/ru/articles/995038/&hl=ru)

Разделы

*   [Статьи](https://habr.com/ru/articles/)
*   [Новости](https://habr.com/ru/news/)
*   [Хабы](https://habr.com/ru/hubs/)
*   [Компании](https://habr.com/ru/companies/)
*   [Авторы](https://habr.com/ru/users/)
*   [Песочница](https://habr.com/ru/sandbox/)

Информация

*   [Устройство сайта](https://habr.com/ru/docs/help/)
*   [Для авторов](https://habr.com/ru/docs/authors/codex/)
*   [Для компаний](https://habr.com/ru/docs/companies/corpblogs/)
*   [Документы](https://habr.com/ru/docs/docs/transparency/)
*   [Соглашение](https://account.habr.com/info/agreement/?hl=ru_RU)
*   [Конфиденциальность](https://account.habr.com/info/confidential/?hl=ru_RU)

Услуги

*   [Корпоративный блог](https://company.habr.com/ru/corporate-blogs/)
*   [Медийная реклама](https://company.habr.com/ru/advertising/)
*   [Нативные проекты](https://company.habr.com/ru/native-special/)
*   [Образовательные программы](https://company.habr.com/ru/education-programs/)
*   [Стартапам](https://company.habr.com/ru/hello-startup/)

[](https://vk.com/habr)[](https://telegram.me/habr_com)[](http://www.youtube.com/@Habr_com)[](https://dzen.ru/habr)

 Настройка языка[Техническая поддержка](https://habr.com/ru/feedback/)

© 2006–2026,[Habr](https://company.habr.com/)
