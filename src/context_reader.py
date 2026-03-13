"""Read context messages from Telegram channels linked to calendars."""

from telethon import TelegramClient

from src.config import AppConfig, CalendarChannel
from src.logger import get_logger

logger = get_logger("context_reader")


class ContextReader:
    """Reads messages from Telegram channels to build meeting context."""

    def __init__(self, config: AppConfig, client: TelegramClient) -> None:
        self._config = config
        self._client = client
        self._channel_map: dict[str, CalendarChannel] = {
            ch.calendar_name: ch for ch in config.calendar_channels
        }
        logger.info(
            "ContextReader initialized",
            extra={"mapped_calendars": list(self._channel_map.keys())},
        )

    async def get_context(
        self,
        calendar_name: str,
        keywords: list[str] | None = None,
    ) -> list[str]:
        """Get context messages from the channel linked to a calendar.

        Strategy:
        1. If keywords provided — search for messages containing them.
        2. Fallback — return last N messages from the channel.

        Args:
            calendar_name: Name of the calendar to find linked channel.
            keywords: Optional keywords to filter messages.

        Returns:
            List of message texts.
        """
        mapping = self._channel_map.get(calendar_name)
        if not mapping:
            logger.warning("No channel mapped for calendar", extra={"calendar": calendar_name})
            return []

        channel_id = mapping.channel_id
        limit = mapping.context_messages_limit

        logger.info(
            "Reading context from channel",
            extra={
                "calendar": calendar_name,
                "channel_id": channel_id,
                "limit": limit,
                "keywords": keywords,
            },
        )

        if keywords:
            messages = await self._search_by_keywords(channel_id, keywords, limit)
            if messages:
                logger.info("Found messages by keywords", extra={"count": len(messages)})
                return messages
            logger.debug("No keyword matches, falling back to recent messages")

        messages = await self._get_recent_messages(channel_id, limit)
        logger.info("Context messages collected", extra={"count": len(messages)})
        return messages

    async def _search_by_keywords(
        self,
        channel_id: int,
        keywords: list[str],
        limit: int,
    ) -> list[str]:
        """Search channel messages by keywords.

        Args:
            channel_id: Telegram channel ID.
            keywords: Keywords to search for.
            limit: Max messages to return.

        Returns:
            List of matching message texts.
        """
        logger.debug("Searching by keywords", extra={"channel_id": channel_id, "keywords": keywords})

        results = []
        for keyword in keywords:
            async for message in self._client.iter_messages(
                channel_id, search=keyword, limit=limit
            ):
                if message.text and message.text not in results:
                    results.append(message.text)
                if len(results) >= limit:
                    break
            if len(results) >= limit:
                break

        logger.debug("Keyword search results", extra={"count": len(results)})
        return results[:limit]

    async def _get_recent_messages(self, channel_id: int, limit: int) -> list[str]:
        """Get the most recent messages from a channel.

        Args:
            channel_id: Telegram channel ID.
            limit: Max messages to return.

        Returns:
            List of message texts (newest first).
        """
        logger.debug("Fetching recent messages", extra={"channel_id": channel_id, "limit": limit})

        messages = []
        async for message in self._client.iter_messages(channel_id, limit=limit):
            if message.text:
                messages.append(message.text)

        logger.debug("Recent messages fetched", extra={"count": len(messages)})
        return messages
