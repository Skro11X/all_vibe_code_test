"""Configuration loader: .env + config.yml with validation."""

import os
import sys
from dataclasses import dataclass, field
from pathlib import Path

import yaml
from dotenv import load_dotenv

from src.logger import get_logger

logger = get_logger("config")


@dataclass
class CalendarChannel:
    """Mapping of a Yandex Calendar to a Telegram channel."""

    calendar_name: str
    channel_id: int
    context_messages_limit: int = 50


@dataclass
class SchedulerConfig:
    """Scheduler settings."""

    check_interval_minutes: int = 5
    meeting_prep_before_minutes: int = 15


@dataclass
class DeepSeekConfig:
    """DeepSeek API settings."""

    api_key: str = ""
    base_url: str = "https://api.deepseek.com"
    model: str = "deepseek-chat"
    max_tokens: int = 4096
    temperature: float = 0.7


@dataclass
class TelegramConfig:
    """Telegram credentials."""

    api_id: int = 0
    api_hash: str = ""
    bot_token: str = ""
    summary_channel_id: int = 0


@dataclass
class YandexConfig:
    """Yandex CalDAV credentials."""

    caldav_url: str = "https://caldav.yandex.ru"
    username: str = ""
    password: str = ""


@dataclass
class AppConfig:
    """Root application configuration."""

    deepseek: DeepSeekConfig = field(default_factory=DeepSeekConfig)
    telegram: TelegramConfig = field(default_factory=TelegramConfig)
    yandex: YandexConfig = field(default_factory=YandexConfig)
    scheduler: SchedulerConfig = field(default_factory=SchedulerConfig)
    calendar_channels: list[CalendarChannel] = field(default_factory=list)


_REQUIRED_ENV = [
    "DEEPSEEK_API_KEY",
    "TELEGRAM_API_ID",
    "TELEGRAM_API_HASH",
    "TELEGRAM_BOT_TOKEN",
    "TELEGRAM_SUMMARY_CHANNEL_ID",
    "YANDEX_USERNAME",
    "YANDEX_PASSWORD",
]


def _validate_env() -> None:
    """Check that all required environment variables are set."""
    missing = [var for var in _REQUIRED_ENV if not os.getenv(var)]
    if missing:
        logger.error("Missing required env vars", extra={"missing": missing})
        sys.exit(f"Missing required environment variables: {', '.join(missing)}")
    logger.debug("All required env vars present")


def _load_yaml(path: Path) -> dict:
    """Load YAML config file. Returns empty dict if file is missing."""
    if not path.exists():
        logger.warning("Config file not found, using defaults", extra={"path": str(path)})
        return {}
    with open(path) as f:
        data = yaml.safe_load(f) or {}
    logger.info("YAML config loaded", extra={"path": str(path), "keys": list(data.keys())})
    return data


def load_config(env_path: str = ".env", yaml_path: str = "config.yml") -> AppConfig:
    """Load full application config from .env and config.yml.

    Args:
        env_path: Path to .env file.
        yaml_path: Path to YAML config file.

    Returns:
        Populated AppConfig dataclass.
    """
    logger.info("Loading configuration", extra={"env_path": env_path, "yaml_path": yaml_path})

    load_dotenv(env_path)
    _validate_env()

    yml = _load_yaml(Path(yaml_path))

    # DeepSeek
    ds_yml = yml.get("deepseek", {})
    deepseek = DeepSeekConfig(
        api_key=os.getenv("DEEPSEEK_API_KEY", ""),
        base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com"),
        model=ds_yml.get("model", "deepseek-chat"),
        max_tokens=ds_yml.get("max_tokens", 4096),
        temperature=ds_yml.get("temperature", 0.7),
    )

    # Telegram
    telegram = TelegramConfig(
        api_id=int(os.getenv("TELEGRAM_API_ID", "0")),
        api_hash=os.getenv("TELEGRAM_API_HASH", ""),
        bot_token=os.getenv("TELEGRAM_BOT_TOKEN", ""),
        summary_channel_id=int(os.getenv("TELEGRAM_SUMMARY_CHANNEL_ID", "0")),
    )

    # Yandex CalDAV
    yandex = YandexConfig(
        caldav_url=os.getenv("YANDEX_CALDAV_URL", "https://caldav.yandex.ru"),
        username=os.getenv("YANDEX_USERNAME", ""),
        password=os.getenv("YANDEX_PASSWORD", ""),
    )

    # Scheduler
    sched_yml = yml.get("scheduler", {})
    scheduler = SchedulerConfig(
        check_interval_minutes=sched_yml.get("check_interval_minutes", 5),
        meeting_prep_before_minutes=sched_yml.get("meeting_prep_before_minutes", 15),
    )

    # Calendar → Channel mapping
    channels_yml = yml.get("calendar_channels", [])
    calendar_channels = [
        CalendarChannel(
            calendar_name=ch["calendar_name"],
            channel_id=int(ch["channel_id"]),
            context_messages_limit=ch.get("context_messages_limit", 50),
        )
        for ch in channels_yml
    ]

    config = AppConfig(
        deepseek=deepseek,
        telegram=telegram,
        yandex=yandex,
        scheduler=scheduler,
        calendar_channels=calendar_channels,
    )

    logger.info(
        "Configuration loaded successfully",
        extra={
            "calendars_mapped": len(calendar_channels),
            "deepseek_model": deepseek.model,
            "scheduler_interval": scheduler.check_interval_minutes,
        },
    )
    return config
