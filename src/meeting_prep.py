"""Meeting preparation: context → DeepSeek → summary channel."""

from telethon import TelegramClient

from src.config import AppConfig
from src.context_reader import ContextReader
from src.deepseek_client import DeepSeekClient
from src.logger import get_logger

logger = get_logger("meeting_prep")


class MeetingPrep:
    """Generates meeting prep from channel context and posts to summary channel."""

    def __init__(
        self,
        config: AppConfig,
        deepseek: DeepSeekClient,
        context_reader: ContextReader,
        tg_client: TelegramClient,
    ) -> None:
        self._config = config
        self._deepseek = deepseek
        self._context_reader = context_reader
        self._tg_client = tg_client
        self._summary_channel_id = config.telegram.summary_channel_id
        logger.info(
            "MeetingPrep initialized",
            extra={"summary_channel": self._summary_channel_id},
        )

    async def prepare_and_post(
        self,
        meeting_title: str,
        calendar_name: str,
        keywords: list[str] | None = None,
    ) -> str:
        """Generate meeting prep and post to summary channel.

        Args:
            meeting_title: Title of the upcoming meeting.
            calendar_name: Calendar name (to find linked context channel).
            keywords: Optional keywords to search context.

        Returns:
            The generated prep text.
        """
        logger.info(
            "Preparing meeting",
            extra={
                "meeting": meeting_title,
                "calendar": calendar_name,
                "keywords": keywords,
            },
        )

        # Step 1: Get context from linked channel
        context_messages = await self._context_reader.get_context(
            calendar_name=calendar_name,
            keywords=keywords or self._extract_keywords(meeting_title),
        )

        if not context_messages:
            logger.warning("No context messages found", extra={"calendar": calendar_name})
            context_messages = ["(Контекст не найден — канал пуст или не привязан)"]

        logger.info("Context collected", extra={"messages_count": len(context_messages)})

        # Step 2: Generate prep via DeepSeek
        prep_text = self._deepseek.generate_meeting_prep(
            meeting_title=meeting_title,
            context_messages=context_messages,
        )

        logger.info("Prep text generated", extra={"length": len(prep_text)})

        # Step 3: Post to summary channel
        await self._post_to_summary(prep_text)

        return prep_text

    async def _post_to_summary(self, text: str) -> None:
        """Send formatted prep text to the summary Telegram channel.

        Args:
            text: Meeting prep text to post.
        """
        logger.info("Posting to summary channel", extra={"channel_id": self._summary_channel_id})

        try:
            await self._tg_client.send_message(self._summary_channel_id, text)
            logger.info("Posted to summary channel successfully")
        except Exception as e:
            logger.error(
                "Failed to post to summary channel",
                extra={"channel_id": self._summary_channel_id, "error": str(e)},
            )
            raise

    @staticmethod
    def _extract_keywords(meeting_title: str) -> list[str]:
        """Extract search keywords from meeting title.

        Simple heuristic: split title, keep words longer than 3 chars.

        Args:
            meeting_title: The meeting title string.

        Returns:
            List of keyword strings.
        """
        stop_words = {"встреча", "совещание", "обсуждение", "планёрка", "митинг", "созвон", "with", "the", "and"}
        words = meeting_title.lower().split()
        keywords = [w for w in words if len(w) > 3 and w not in stop_words]
        logger.debug("Extracted keywords", extra={"title": meeting_title, "keywords": keywords})
        return keywords
