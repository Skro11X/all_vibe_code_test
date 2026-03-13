"""DeepSeek API client — OpenAI-compatible wrapper."""

import json

from openai import OpenAI

from src.config import AppConfig
from src.logger import get_logger

logger = get_logger("deepseek")

MONTHLY_PLAN_SYSTEM_PROMPT = """\
Ты — ассистент-планировщик. Пользователь отправляет план на месяц в свободной форме.
Твоя задача — извлечь из текста список событий и вернуть JSON-массив.

Каждый элемент массива:
{
  "title": "Название встречи/события",
  "date": "YYYY-MM-DD",
  "time_start": "HH:MM",
  "time_end": "HH:MM",
  "calendar": "Имя календаря (если указано, иначе null)",
  "description": "Краткое описание (если есть)"
}

Верни ТОЛЬКО валидный JSON-массив, без комментариев и markdown.
Если время окончания не указано, поставь +1 час от начала.
Если дата указана относительно (например, "в понедельник"), рассчитай от текущей даты.
"""

MEETING_PREP_SYSTEM_PROMPT = """\
Ты — ассистент для подготовки к встречам.
На основе контекста из Telegram-канала составь краткий план встречи.

Формат ответа:
📋 **План встречи: {название}**

**Ключевые темы:**
- ...

**Контекст из обсуждений:**
- ...

**Вопросы для обсуждения:**
- ...

**Возможные решения/действия:**
- ...

Будь конкретен, опирайся на фактический контекст. Не выдумывай.
"""


class DeepSeekClient:
    """Wrapper around DeepSeek API using OpenAI SDK."""

    def __init__(self, config: AppConfig) -> None:
        self._config = config.deepseek
        self._client = OpenAI(
            api_key=self._config.api_key,
            base_url=self._config.base_url,
        )
        logger.info(
            "DeepSeek client initialized",
            extra={"model": self._config.model, "base_url": self._config.base_url},
        )

    def _call(self, system_prompt: str, user_message: str) -> str:
        """Make a chat completion request to DeepSeek.

        Args:
            system_prompt: System message defining the assistant's role.
            user_message: User input text.

        Returns:
            Assistant's response text.
        """
        logger.debug(
            "DeepSeek API call",
            extra={"system_prompt_len": len(system_prompt), "user_msg_len": len(user_message)},
        )
        response = self._client.chat.completions.create(
            model=self._config.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
            max_tokens=self._config.max_tokens,
            temperature=self._config.temperature,
        )
        result = response.choices[0].message.content or ""
        logger.debug(
            "DeepSeek API response received",
            extra={"response_len": len(result), "finish_reason": response.choices[0].finish_reason},
        )
        return result

    def parse_monthly_plan(self, plan_text: str, current_date: str = "") -> list[dict]:
        """Parse free-form monthly plan text into structured events.

        Args:
            plan_text: User's monthly plan in free-form text.
            current_date: Current date string (YYYY-MM-DD) for relative date calculation.

        Returns:
            List of event dicts with title, date, time_start, time_end, calendar, description.
        """
        logger.info("Parsing monthly plan", extra={"text_len": len(plan_text)})

        user_msg = plan_text
        if current_date:
            user_msg = f"Текущая дата: {current_date}\n\n{plan_text}"

        raw = self._call(MONTHLY_PLAN_SYSTEM_PROMPT, user_msg)

        # Strip markdown code fences if present
        cleaned = raw.strip()
        if cleaned.startswith("```"):
            lines = cleaned.split("\n")
            lines = lines[1:]  # remove opening fence
            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]
            cleaned = "\n".join(lines)

        try:
            events = json.loads(cleaned)
        except json.JSONDecodeError as e:
            logger.error("Failed to parse DeepSeek response as JSON", extra={"error": str(e), "raw": raw[:500]})
            raise ValueError(f"DeepSeek returned invalid JSON: {e}") from e

        if not isinstance(events, list):
            logger.error("DeepSeek response is not a list", extra={"type": type(events).__name__})
            raise ValueError("Expected a JSON array of events")

        logger.info("Monthly plan parsed", extra={"events_count": len(events)})
        return events

    def generate_meeting_prep(self, meeting_title: str, context_messages: list[str]) -> str:
        """Generate a meeting preparation summary from channel context.

        Args:
            meeting_title: Name of the upcoming meeting.
            context_messages: Relevant messages from the linked Telegram channel.

        Returns:
            Formatted meeting prep text ready to post.
        """
        logger.info(
            "Generating meeting prep",
            extra={"meeting": meeting_title, "context_msgs": len(context_messages)},
        )

        context_block = "\n".join(f"- {msg}" for msg in context_messages)
        user_msg = (
            f"Встреча: {meeting_title}\n\n"
            f"Контекст из канала ({len(context_messages)} сообщений):\n{context_block}"
        )

        result = self._call(MEETING_PREP_SYSTEM_PROMPT, user_msg)
        logger.info("Meeting prep generated", extra={"result_len": len(result)})
        return result

    def chat(self, user_message: str, history: list[dict] | None = None) -> str:
        """Free-form chat with DeepSeek (used for general bot interaction).

        Args:
            user_message: User's message text.
            history: Optional conversation history as list of {role, content} dicts.

        Returns:
            Assistant's response text.
        """
        logger.debug("Chat request", extra={"msg_len": len(user_message), "history_len": len(history or [])})

        messages = [
            {"role": "system", "content": "Ты — полезный ассистент. Отвечай кратко и по существу на русском языке."},
        ]
        if history:
            messages.extend(history)
        messages.append({"role": "user", "content": user_message})

        response = self._client.chat.completions.create(
            model=self._config.model,
            messages=messages,
            max_tokens=self._config.max_tokens,
            temperature=self._config.temperature,
        )
        result = response.choices[0].message.content or ""
        logger.debug("Chat response", extra={"response_len": len(result)})
        return result
