"""APScheduler-based scheduler: checks upcoming events and triggers meeting prep."""

import asyncio
from datetime import datetime, timedelta, timezone

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from src.calendar_client import CalendarClient
from src.config import AppConfig
from src.logger import get_logger
from src.meeting_prep import MeetingPrep

logger = get_logger("scheduler")


class MeetingScheduler:
    """Periodically checks calendars and triggers meeting prep before events."""

    def __init__(
        self,
        config: AppConfig,
        calendar_client: CalendarClient,
        meeting_prep: MeetingPrep,
    ) -> None:
        self._config = config
        self._calendar = calendar_client
        self._meeting_prep = meeting_prep
        self._scheduler = AsyncIOScheduler()
        self._processed_uids: set[str] = set()

        logger.info(
            "MeetingScheduler initialized",
            extra={
                "check_interval": config.scheduler.check_interval_minutes,
                "prep_before": config.scheduler.meeting_prep_before_minutes,
            },
        )

    def start(self) -> None:
        """Start the scheduler with periodic event checking."""
        interval = self._config.scheduler.check_interval_minutes

        self._scheduler.add_job(
            self._check_upcoming,
            "interval",
            minutes=interval,
            id="check_upcoming_events",
            replace_existing=True,
        )
        self._scheduler.start()
        logger.info("Scheduler started", extra={"interval_minutes": interval})

    def stop(self) -> None:
        """Stop the scheduler gracefully."""
        logger.info("Stopping scheduler")
        self._scheduler.shutdown(wait=False)
        logger.info("Scheduler stopped")

    async def _check_upcoming(self) -> None:
        """Check all mapped calendars for events starting within the prep window."""
        prep_minutes = self._config.scheduler.meeting_prep_before_minutes
        now = datetime.now(timezone.utc)
        window_end = now + timedelta(minutes=prep_minutes + 5)

        logger.debug(
            "Checking upcoming events",
            extra={
                "now": str(now),
                "window_end": str(window_end),
                "prep_minutes": prep_minutes,
            },
        )

        for mapping in self._config.calendar_channels:
            try:
                await self._check_calendar(mapping.calendar_name, now, window_end, prep_minutes)
            except Exception as e:
                logger.error(
                    "Error checking calendar",
                    extra={"calendar": mapping.calendar_name, "error": str(e)},
                )

    async def _check_calendar(
        self,
        calendar_name: str,
        now: datetime,
        window_end: datetime,
        prep_minutes: int,
    ) -> None:
        """Check a single calendar for upcoming events needing prep.

        Args:
            calendar_name: Name of the calendar to check.
            now: Current UTC datetime.
            window_end: End of the lookahead window.
            prep_minutes: Minutes before event to trigger prep.
        """
        logger.debug("Checking calendar", extra={"calendar": calendar_name})

        events = self._calendar.get_upcoming_events(calendar_name, hours_ahead=1)

        for event in events:
            uid = event.get("uid", "")

            # Deduplicate by UID
            if uid in self._processed_uids:
                logger.debug("Event already processed, skipping", extra={"uid": uid})
                continue

            dtstart = event.get("dtstart")
            if dtstart is None:
                continue

            # Ensure timezone-aware
            if dtstart.tzinfo is None:
                dtstart = dtstart.replace(tzinfo=timezone.utc)

            time_until = (dtstart - now).total_seconds() / 60

            if 0 < time_until <= prep_minutes + 5:
                logger.info(
                    "Event within prep window, triggering preparation",
                    extra={
                        "uid": uid,
                        "summary": event.get("summary"),
                        "minutes_until": round(time_until, 1),
                    },
                )

                self._processed_uids.add(uid)
                asyncio.create_task(
                    self._trigger_prep(
                        meeting_title=event.get("summary", "Встреча"),
                        calendar_name=calendar_name,
                    )
                )

    async def _trigger_prep(self, meeting_title: str, calendar_name: str) -> None:
        """Trigger meeting preparation for a specific event.

        Args:
            meeting_title: Title of the meeting.
            calendar_name: Calendar name (for context lookup).
        """
        logger.info(
            "Triggering meeting prep",
            extra={"meeting": meeting_title, "calendar": calendar_name},
        )

        try:
            result = await self._meeting_prep.prepare_and_post(
                meeting_title=meeting_title,
                calendar_name=calendar_name,
            )
            logger.info(
                "Meeting prep completed and posted",
                extra={"meeting": meeting_title, "result_len": len(result)},
            )
        except Exception as e:
            logger.error(
                "Meeting prep failed",
                extra={"meeting": meeting_title, "error": str(e)},
            )
