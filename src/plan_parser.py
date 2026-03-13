"""Monthly plan parser: text → DeepSeek → CalDAV events pipeline."""

from datetime import datetime, timezone
from typing import Any

from src.calendar_client import CalendarClient
from src.config import AppConfig
from src.deepseek_client import DeepSeekClient
from src.logger import get_logger

logger = get_logger("plan_parser")


class PlanParser:
    """Pipeline: free-form plan text → structured events → calendar entries."""

    def __init__(self, config: AppConfig, deepseek: DeepSeekClient, calendar: CalendarClient) -> None:
        self._config = config
        self._deepseek = deepseek
        self._calendar = calendar
        logger.info("PlanParser initialized")

    def parse_and_create(self, plan_text: str, default_calendar: str | None = None) -> dict[str, Any]:
        """Parse a monthly plan and create calendar events.

        Args:
            plan_text: Free-form plan text from the user.
            default_calendar: Calendar name to use when event doesn't specify one.

        Returns:
            Report dict with 'created', 'failed', and 'total' counts plus details.
        """
        logger.info(
            "Starting plan parse and create pipeline",
            extra={"text_len": len(plan_text), "default_calendar": default_calendar},
        )

        current_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")

        # Step 1: Parse text via DeepSeek
        try:
            events_data = self._deepseek.parse_monthly_plan(plan_text, current_date=current_date)
        except ValueError as e:
            logger.error("Plan parsing failed", extra={"error": str(e)})
            return {"created": 0, "failed": 1, "total": 0, "errors": [str(e)], "events": []}

        logger.info("Plan parsed by DeepSeek", extra={"events_count": len(events_data)})

        # Step 2: Create events in calendar
        created = []
        errors = []

        for i, ev in enumerate(events_data):
            try:
                result = self._create_single_event(ev, default_calendar, index=i)
                created.append(result)
            except Exception as e:
                error_msg = f"Event #{i + 1} '{ev.get('title', '?')}': {e}"
                logger.error("Failed to create event", extra={"index": i, "error": str(e), "event": ev})
                errors.append(error_msg)

        report = {
            "created": len(created),
            "failed": len(errors),
            "total": len(events_data),
            "events": created,
            "errors": errors,
        }

        logger.info(
            "Plan processing complete",
            extra={"created": len(created), "failed": len(errors), "total": len(events_data)},
        )
        return report

    def _create_single_event(
        self,
        event_data: dict[str, Any],
        default_calendar: str | None,
        index: int,
    ) -> dict[str, str]:
        """Create a single calendar event from parsed data.

        Args:
            event_data: Dict with title, date, time_start, time_end, calendar, description.
            default_calendar: Fallback calendar name.
            index: Event index for logging.

        Returns:
            Dict with uid, title, calendar, datetime info.
        """
        title = event_data.get("title", f"Event #{index + 1}")
        date_str = event_data["date"]
        time_start = event_data["time_start"]
        time_end = event_data["time_end"]
        calendar_name = event_data.get("calendar") or default_calendar
        description = event_data.get("description", "")

        if not calendar_name:
            # Use first mapped calendar as fallback
            if self._config.calendar_channels:
                calendar_name = self._config.calendar_channels[0].calendar_name
                logger.debug("Using first mapped calendar as fallback", extra={"calendar": calendar_name})
            else:
                raise ValueError("No calendar specified and no default available")

        logger.debug(
            "Creating single event",
            extra={"title": title, "date": date_str, "start": time_start, "end": time_end, "calendar": calendar_name},
        )

        dtstart = datetime.strptime(f"{date_str} {time_start}", "%Y-%m-%d %H:%M").replace(tzinfo=timezone.utc)
        dtend = datetime.strptime(f"{date_str} {time_end}", "%Y-%m-%d %H:%M").replace(tzinfo=timezone.utc)

        uid = self._calendar.create_event(
            calendar_name=calendar_name,
            summary=title,
            dtstart=dtstart,
            dtend=dtend,
            description=description,
        )

        logger.info("Event created successfully", extra={"uid": uid, "title": title, "calendar": calendar_name})
        return {
            "uid": uid,
            "title": title,
            "calendar": calendar_name,
            "date": date_str,
            "time": f"{time_start}-{time_end}",
        }

    def format_report(self, report: dict[str, Any]) -> str:
        """Format creation report as a human-readable message.

        Args:
            report: Report dict from parse_and_create().

        Returns:
            Formatted text for Telegram.
        """
        lines = [f"Обработано событий: {report['total']}"]
        lines.append(f"Создано: {report['created']}")

        if report["errors"]:
            lines.append(f"Ошибки: {report['failed']}")

        if report["events"]:
            lines.append("\nСозданные события:")
            for ev in report["events"]:
                lines.append(f"  - {ev['title']} ({ev['date']} {ev['time']}) [{ev['calendar']}]")

        if report["errors"]:
            lines.append("\nОшибки:")
            for err in report["errors"]:
                lines.append(f"  - {err}")

        return "\n".join(lines)
