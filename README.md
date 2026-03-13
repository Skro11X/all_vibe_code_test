# DeepSeek + Yandex Calendar + Telegram Bot

Telegram-бот, который:
1. Принимает план на месяц в свободной форме → создаёт события в Yandex Calendar через CalDAV
2. За 15 минут до каждой встречи генерирует план встречи на основе контекста привязанного TG-канала
3. Постит результат в отдельный саммари-канал

## Архитектура

```
Пользователь → TG бот (/plan) → DeepSeek (парсинг) → Yandex CalDAV (создание событий)
                                                        ↓
Саммари-канал ← DeepSeek (генерация плана) ← Контекст из TG-канала ← APScheduler (за 15 мин)
```

Каждый календарь привязан к конкретному TG-каналу — из него берётся контекст для подготовки к встречам.

## Стек

- **Python 3.12+**
- **Telethon** — Telegram MTProto клиент
- **OpenAI SDK** → DeepSeek API (совместимый)
- **caldav + icalendar** — Yandex Calendar
- **APScheduler** — планировщик проверки событий

## Быстрый старт

```bash
# Клонировать
git clone git@github.com:Skro11X/all_vibe_code_test.git
cd all_vibe_code_test

# Создать виртуальное окружение
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Настроить
cp .env.example .env        # заполнить ключи
cp config.yml.example config.yml  # настроить маппинг

# Запустить
python main.py
```

## Конфигурация

### .env

| Переменная | Описание |
|---|---|
| `DEEPSEEK_API_KEY` | API-ключ DeepSeek |
| `DEEPSEEK_BASE_URL` | URL API (по умолчанию `https://api.deepseek.com`) |
| `TELEGRAM_API_ID` | Telegram API ID (my.telegram.org) |
| `TELEGRAM_API_HASH` | Telegram API Hash |
| `TELEGRAM_BOT_TOKEN` | Токен бота от @BotFather |
| `TELEGRAM_SUMMARY_CHANNEL_ID` | ID канала для саммари |
| `YANDEX_USERNAME` | Логин Яндекса |
| `YANDEX_PASSWORD` | Пароль приложения |
| `LOG_LEVEL` | Уровень логирования (DEBUG, INFO, WARNING) |

### config.yml

```yaml
calendar_channels:
  - calendar_name: "Рабочий"
    channel_id: -100xxxxxxxxxxxx
    context_messages_limit: 50

scheduler:
  check_interval_minutes: 5
  meeting_prep_before_minutes: 15

deepseek:
  model: "deepseek-chat"
  max_tokens: 4096
  temperature: 0.7
```

## Команды бота

| Команда | Описание |
|---|---|
| `/start` | Приветствие |
| `/plan` | Загрузить план на месяц (следующее сообщение) |
| `/calendars` | Список доступных календарей |
| `/upcoming` | Ближайшие события (48ч) |
| `/help` | Справка |
| *любой текст* | Свободный чат с DeepSeek |

## Структура проекта

```
src/
├── main.py             # Точка входа, инициализация, graceful shutdown
├── config.py           # Загрузка .env + config.yml, валидация
├── logger.py           # Структурированное JSON-логирование
├── deepseek_client.py  # DeepSeek API: парсинг планов, генерация, чат
├── calendar_client.py  # Yandex CalDAV: CRUD событий
├── plan_parser.py      # Конвейер: текст → DeepSeek → CalDAV
├── telegram_client.py  # Telethon бот с хендлерами команд
├── context_reader.py   # Чтение контекста из TG-каналов
├── meeting_prep.py     # Генерация плана встречи → саммари-канал
└── scheduler.py        # APScheduler: проверка событий, триггер подготовки
```
