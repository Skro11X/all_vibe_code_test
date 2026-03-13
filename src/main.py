"""Main entry point: initializes all components, runs event loop with graceful shutdown."""

import asyncio
import signal

from src.calendar_client import CalendarClient
from src.config import load_config
from src.context_reader import ContextReader
from src.deepseek_client import DeepSeekClient
from src.logger import get_logger, setup_logging
from src.meeting_prep import MeetingPrep
from src.plan_parser import PlanParser
from src.scheduler import MeetingScheduler
from src.telegram_client import TelegramBot

logger = get_logger("main")


async def main() -> None:
    """Initialize all components and run the bot."""
    setup_logging()
    logger.info("Application starting")

    # Load config
    config = load_config()
    logger.info("Configuration loaded")

    # Initialize components
    deepseek = DeepSeekClient(config)
    calendar = CalendarClient(config)
    calendar.connect()

    bot = TelegramBot(config)
    await bot.start()

    context_reader = ContextReader(config, bot.client)
    meeting_prep = MeetingPrep(config, deepseek, context_reader, bot.client)
    plan_parser = PlanParser(config, deepseek, calendar)
    scheduler = MeetingScheduler(config, calendar, meeting_prep)

    # Wire up bot handlers
    async def handle_plan(text: str) -> str:
        report = plan_parser.parse_and_create(text)
        return plan_parser.format_report(report)

    async def handle_chat(text: str) -> str:
        return deepseek.chat(text)

    bot.set_plan_handler(handle_plan)
    bot.set_calendar_handler(calendar)
    bot.set_chat_handler(handle_chat)

    # Start scheduler
    scheduler.start()
    logger.info("All components initialized, bot is running")

    # Graceful shutdown
    loop = asyncio.get_event_loop()
    stop_event = asyncio.Event()

    def shutdown_handler(sig: int, frame) -> None:
        sig_name = signal.Signals(sig).name
        logger.info("Received shutdown signal", extra={"signal": sig_name})
        stop_event.set()

    signal.signal(signal.SIGINT, shutdown_handler)
    signal.signal(signal.SIGTERM, shutdown_handler)

    # Wait for shutdown signal or bot disconnect
    try:
        await stop_event.wait()
    except asyncio.CancelledError:
        pass
    finally:
        logger.info("Shutting down...")
        scheduler.stop()
        await bot.stop()
        logger.info("Application stopped")


def run() -> None:
    """Entry point for running the application."""
    asyncio.run(main())


if __name__ == "__main__":
    run()
