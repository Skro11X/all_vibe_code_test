# Implementation Plan: DeepSeek + Yandex Calendar + Telegram Bot

Branch: none (fast mode)
Created: 2026-03-13

## Settings
- Testing: no
- Logging: verbose
- Docs: no

## Research Context
Source: .ai-factory/RESEARCH.md (Active Summary)

Goal: TG бот, который (1) принимает план на месяц, (2) создаёт события в Yandex Calendar через CalDAV, (3) за 15 минут до каждой встречи генерит план встречи на основе контекста привязанного TG канала, (4) постит результат в отдельный саммари-канал
Constraints:
- Yandex Calendar — только CalDAV (нет REST API)
- Telegram каналы приватные, бот будет админом
- DeepSeek API (OpenAI-compatible)
- Telethon (MTProto) для Telegram
- Хостинг на собственном сервере
- Решение для одного пользователя
Decisions:
- Интерфейс взаимодействия с DeepSeek — через TG бота (не веб)
- Доставка планов встреч — в отдельный приватный TG канал (саммари-канал)
- Маппинг: каждый календарь привязан к конкретному TG каналу с контекстом

## Commit Plan
- **Commit 1** (after tasks 1-3): "feat: project structure, config, and DeepSeek client"
- **Commit 2** (after tasks 4-5): "feat: Yandex CalDAV integration and plan parser"
- **Commit 3** (after tasks 6-8): "feat: Telegram bot, context reader, and meeting prep"
- **Commit 4** (after tasks 9-10): "feat: scheduler and main entry point"

## Tasks

### Phase 1: Foundation
- [x] Task 1: Структура проекта и зависимости
  - Создать src/ с модулями, requirements.txt, .env.example, config.yml.example
  - Настроить базовый logging
- [x] Task 2: Система конфигурации (depends on 1)
  - src/config.py — загрузка .env + config.yml
  - Валидация обязательных переменных
  - Маппинг календарь↔канал из YAML
- [x] Task 3: DeepSeek API клиент (depends on 2)
  - src/deepseek_client.py — обёртка через openai SDK
  - Методы: parse_monthly_plan(), generate_meeting_prep(), chat()
<!-- Commit checkpoint: tasks 1-3 -->

### Phase 2: Calendar Integration
- [ ] Task 4: Yandex Calendar CalDAV клиент (depends on 2)
  - src/calendar_client.py — подключение, CRUD событий
  - list_calendars(), get_upcoming_events(), create_event()
- [ ] Task 5: Парсинг плана на месяц и создание событий (depends on 3, 4)
  - src/plan_parser.py — конвейер: текст → DeepSeek → CalDAV события
  - Обработка ошибок, отчёт о создании
<!-- Commit checkpoint: tasks 4-5 -->

### Phase 3: Telegram Integration
- [ ] Task 6: Telethon клиент и базовые хендлеры (depends on 2)
  - src/telegram_client.py — бот на Telethon
  - Команды: /start, /plan, /calendars, /upcoming, /help
  - Свободный чат → DeepSeek
- [ ] Task 7: Чтение контекста из TG каналов (depends on 6)
  - src/context_reader.py — чтение сообщений из привязанного канала
  - Поиск по ключевым словам + fallback на последние N сообщений
- [ ] Task 8: Генерация плана встречи и отправка в саммари-канал (depends on 3, 7)
  - src/meeting_prep.py — контекст → DeepSeek → форматированный план → саммари-канал
<!-- Commit checkpoint: tasks 6-8 -->

### Phase 4: Orchestration
- [ ] Task 9: Планировщик APScheduler (depends on 4, 8)
  - src/scheduler.py — проверка ближайших событий каждые 5 мин
  - Триггер подготовки за 15 мин до встречи
  - Дедупликация по UID
- [ ] Task 10: Главный модуль: запуск и graceful shutdown (depends on 5, 6, 9)
  - src/main.py — инициализация всех компонентов, event loop
  - Обработка SIGINT/SIGTERM
  - Обновить корневой main.py
<!-- Commit checkpoint: tasks 9-10 -->
