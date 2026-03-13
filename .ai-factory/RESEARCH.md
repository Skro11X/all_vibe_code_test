# Research

Updated: 2026-03-13 14:00
Status: active

## Active Summary (input for /aif-plan)
<!-- aif:active-summary:start -->
Topic: Интеграция DeepSeek + Yandex Calendar + Telegram
Goal: TG бот, который (1) принимает план на месяц, (2) создаёт события в Yandex Calendar через CalDAV, (3) за 15 минут до каждой встречи генерит план встречи на основе контекста привязанного TG канала, (4) постит результат в отдельный саммари-канал
Constraints:
- Yandex Calendar — только CalDAV (нет REST API)
- Telegram каналы приватные, бот будет админом
- DeepSeek API (OpenAI-compatible)
- Хостинг на собственном сервере
- Решение для одного пользователя
Decisions:
- Интерфейс взаимодействия с DeepSeek — через TG бота (не веб)
- Доставка планов встреч — в отдельный приватный TG канал (саммари-канал)
- Маппинг: каждый календарь привязан к конкретному TG каналу с контекстом
Open questions:
- Стек: aiogram vs python-telegram-bot
- Как именно искать релевантный контекст в канале (последние N сообщений? поиск по ключевым словам?)
- Формат плана на месяц (свободный текст? структурированный?)
- Нужна ли БД (SQLite) для хранения маппинга и состояния?
- Scheduler: APScheduler внутри бота или системный cron?
Success signals:
- Пользователь пишет план в TG → события появляются в Yandex Calendar
- За 15 мин до встречи → саммари-канал получает план встречи с контекстом
Next step: /aif-plan для декомпозиции на задачи
<!-- aif:active-summary:end -->

## Sessions
<!-- aif:sessions:start -->
### 2026-03-13 14:00 — Первичная проработка архитектуры
What changed:
- Определена общая архитектура: TG бот (Python) как центральный хаб
- Выбраны интеграции: DeepSeek API, Yandex CalDAV, Telegram Bot API
- Решено: вся коммуникация через Telegram (бот + саммари-канал)
- Маппинг календарь↔канал — ключевая конфигурация
Key notes:
- Yandex Calendar работает через CalDAV (библиотеки: caldav + icalendar)
- DeepSeek API совместим с OpenAI SDK — можно использовать openai Python клиент
- Для чтения приватных каналов бот должен быть админом
- Однопользовательское решение — можно обойтись без сложной авторизации
Links (paths):
- .ai-factory/DESCRIPTION.md — описание проекта
- main.py — текущая точка входа (заглушка)
<!-- aif:sessions:end -->
