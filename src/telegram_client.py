"""Telegram bot on Telethon with command handlers and free chat."""

from telethon import TelegramClient, events

from src.config import AppConfig
from src.logger import get_logger

logger = get_logger("telegram")

HELP_TEXT = """Доступные команды:

/start — Приветствие
/plan — Отправить план на месяц (в следующем сообщении)
/calendars — Показать список календарей
/upcoming — Ближайшие события
/help — Эта справка

Любое другое сообщение — свободный чат с ассистентом.
"""


class TelegramBot:
    """Telethon-based Telegram bot with command handlers."""

    def __init__(self, config: AppConfig) -> None:
        self._config = config
        self._tg_config = config.telegram
        self._client = TelegramClient(
            "bot_session",
            api_id=self._tg_config.api_id,
            api_hash=self._tg_config.api_hash,
        )

        # These will be set externally after all components are initialized
        self._plan_handler = None
        self._calendar_handler = None
        self._chat_handler = None

        # Track users waiting to send plan text
        self._awaiting_plan: set[int] = set()

        self._register_handlers()
        logger.info("TelegramBot created", extra={"api_id": self._tg_config.api_id})

    def set_plan_handler(self, handler) -> None:
        """Set callback for processing monthly plan text.

        Args:
            handler: Async callable(text: str) -> str (returns report).
        """
        self._plan_handler = handler
        logger.debug("Plan handler set")

    def set_calendar_handler(self, handler) -> None:
        """Set callback for listing calendars / upcoming events.

        Args:
            handler: Object with list_calendars() and get_upcoming_events() methods.
        """
        self._calendar_handler = handler
        logger.debug("Calendar handler set")

    def set_chat_handler(self, handler) -> None:
        """Set callback for free-form chat messages.

        Args:
            handler: Async callable(text: str) -> str.
        """
        self._chat_handler = handler
        logger.debug("Chat handler set")

    def _register_handlers(self) -> None:
        """Register all Telethon event handlers."""
        bot = self._client

        @bot.on(events.NewMessage(pattern="/start"))
        async def on_start(event):
            logger.info("Command /start", extra={"user_id": event.sender_id})
            await event.respond(
                "Привет! Я бот-планировщик.\n"
                "Отправь /plan чтобы загрузить план на месяц,\n"
                "или напиши что угодно для свободного чата.\n\n"
                "Используй /help для списка команд."
            )

        @bot.on(events.NewMessage(pattern="/help"))
        async def on_help(event):
            logger.info("Command /help", extra={"user_id": event.sender_id})
            await event.respond(HELP_TEXT)

        @bot.on(events.NewMessage(pattern="/plan"))
        async def on_plan(event):
            logger.info("Command /plan", extra={"user_id": event.sender_id})
            self._awaiting_plan.add(event.sender_id)
            await event.respond(
                "Отправь план на месяц в следующем сообщении.\n"
                "Формат свободный — я извлеку события и создам их в календаре."
            )

        @bot.on(events.NewMessage(pattern="/calendars"))
        async def on_calendars(event):
            logger.info("Command /calendars", extra={"user_id": event.sender_id})
            if not self._calendar_handler:
                await event.respond("Календарь не подключен.")
                return
            try:
                calendars = self._calendar_handler.list_calendars()
                if not calendars:
                    await event.respond("Календари не найдены.")
                    return
                lines = ["Доступные календари:"]
                for cal in calendars:
                    lines.append(f"  - {cal['name']}")
                await event.respond("\n".join(lines))
            except Exception as e:
                logger.error("Failed to list calendars", extra={"error": str(e)})
                await event.respond(f"Ошибка при получении календарей: {e}")

        @bot.on(events.NewMessage(pattern="/upcoming"))
        async def on_upcoming(event):
            logger.info("Command /upcoming", extra={"user_id": event.sender_id})
            if not self._calendar_handler:
                await event.respond("Календарь не подключен.")
                return
            try:
                all_events = []
                for mapping in self._config.calendar_channels:
                    events_list = self._calendar_handler.get_upcoming_events(
                        mapping.calendar_name, hours_ahead=48
                    )
                    for ev in events_list:
                        ev["calendar"] = mapping.calendar_name
                    all_events.extend(events_list)

                if not all_events:
                    await event.respond("Нет ближайших событий (48 часов).")
                    return

                all_events.sort(key=lambda e: e.get("dtstart") or "")
                lines = ["Ближайшие события (48ч):"]
                for ev in all_events:
                    dt = ev.get("dtstart", "")
                    dt_str = dt.strftime("%d.%m %H:%M") if hasattr(dt, "strftime") else str(dt)
                    lines.append(f"  - {dt_str} | {ev['summary']} [{ev['calendar']}]")
                await event.respond("\n".join(lines))
            except Exception as e:
                logger.error("Failed to get upcoming events", extra={"error": str(e)})
                await event.respond(f"Ошибка: {e}")

        @bot.on(events.NewMessage)
        async def on_message(event):
            # Skip commands
            if event.text and event.text.startswith("/"):
                return

            sender_id = event.sender_id
            logger.debug("Incoming message", extra={"user_id": sender_id, "text_len": len(event.text or "")})

            # Check if user is sending a plan
            if sender_id in self._awaiting_plan:
                self._awaiting_plan.discard(sender_id)
                logger.info("Processing plan from user", extra={"user_id": sender_id})

                if not self._plan_handler:
                    await event.respond("Обработчик планов не настроен.")
                    return

                await event.respond("Обрабатываю план... Это может занять минуту.")
                try:
                    result = await self._plan_handler(event.text)
                    await event.respond(result)
                except Exception as e:
                    logger.error("Plan processing failed", extra={"error": str(e)})
                    await event.respond(f"Ошибка при обработке плана: {e}")
                return

            # Free chat via DeepSeek
            if self._chat_handler:
                try:
                    response = await self._chat_handler(event.text)
                    await event.respond(response)
                except Exception as e:
                    logger.error("Chat handler failed", extra={"error": str(e)})
                    await event.respond(f"Ошибка: {e}")
            else:
                await event.respond("Используй /help для списка команд.")

        logger.debug("All handlers registered")

    async def start(self) -> None:
        """Start the bot (connect and run until disconnected)."""
        logger.info("Starting Telegram bot")
        await self._client.start(bot_token=self._tg_config.bot_token)
        logger.info("Telegram bot started, listening for messages")

    async def run_until_disconnected(self) -> None:
        """Block until the bot is disconnected."""
        await self._client.run_until_disconnected()

    async def stop(self) -> None:
        """Gracefully disconnect the bot."""
        logger.info("Stopping Telegram bot")
        await self._client.disconnect()
        logger.info("Telegram bot stopped")

    @property
    def client(self) -> TelegramClient:
        """Access the underlying Telethon client (for context_reader)."""
        return self._client
