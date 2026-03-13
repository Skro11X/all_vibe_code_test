"""Yandex Calendar client via CalDAV protocol."""

from datetime import datetime, timedelta, timezone
from typing import Any

import caldav
from icalendar import Calendar, Event

from src.config import AppConfig
from src.logger import get_logger

logger = get_logger("calendar")


class CalendarClient:
    """CalDAV client for Yandex Calendar."""

    def __init__(self, config: AppConfig) -> None:
        self._config = config.yandex
        self._client: caldav.DAVClient | None = None
        self._principal: caldav.Principal | None = None
        logger.info(
            "CalendarClient created",
            extra={"url": self._config.caldav_url, "user": self._config.username},
        )

    def connect(self) -> None:
        """Establish connection to Yandex CalDAV server."""
        logger.info("Connecting to CalDAV server", extra={"url": self._config.caldav_url})
        self._client = caldav.DAVClient(
            url=self._config.caldav_url,
            username=self._config.username,
            password=self._config.password,
        )
        self._principal = self._client.principal()
        logger.info("Connected to CalDAV server successfully")

    def _ensure_connected(self) -> None:
        """Connect if not already connected."""
        if self._principal is None:
            self.connect()

    def list_calendars(self) -> list[dict[str, str]]:
        """List all available calendars.

        Returns:
            List of dicts with 'name' and 'url' keys.
        """
        self._ensure_connected()
        assert self._principal is not None

        calendars = self._principal.calendars()
        result = []
        for cal in calendars:
            name = cal.name or str(cal.url)
            result.append({"name": name, "url": str(cal.url)})
            logger.debug("Found calendar", extra={"name": name, "url": str(cal.url)})

        logger.info("Calendars listed", extra={"count": len(result)})
        return result

    def _find_calendar(self, calendar_name: str) -> caldav.Calendar:
        """Find a calendar by name.

        Args:
            calendar_name: Name of the calendar to find.

        Returns:
            caldav.Calendar object.

        Raises:
            ValueError: If calendar not found.
        """
        self._ensure_connected()
        assert self._principal is not None

        for cal in self._principal.calendars():
            if cal.name == calendar_name:
                logger.debug("Calendar found", extra={"name": calendar_name})
                return cal

        available = [c.name for c in self._principal.calendars()]
        logger.error(
            "Calendar not found",
            extra={"requested": calendar_name, "available": available},
        )
        raise ValueError(f"Calendar '{calendar_name}' not found. Available: {available}")

    def get_upcoming_events(
        self,
        calendar_name: str,
        hours_ahead: int = 24,
    ) -> list[dict[str, Any]]:
        """Get upcoming events from a specific calendar.

        Args:
            calendar_name: Name of the calendar.
            hours_ahead: How many hours ahead to look.

        Returns:
            List of event dicts with uid, summary, dtstart, dtend, description.
        """
        logger.info(
            "Fetching upcoming events",
            extra={"calendar": calendar_name, "hours_ahead": hours_ahead},
        )

        cal = self._find_calendar(calendar_name)
        now = datetime.now(timezone.utc)
        end = now + timedelta(hours=hours_ahead)

        results = cal.search(start=now, end=end, event=True, expand=True)
        events = []

        for item in results:
            ical = Calendar.from_ical(item.data)
            for component in ical.walk():
                if component.name != "VEVENT":
                    continue
                event = {
                    "uid": str(component.get("uid", "")),
                    "summary": str(component.get("summary", "")),
                    "dtstart": component.get("dtstart").dt if component.get("dtstart") else None,
                    "dtend": component.get("dtend").dt if component.get("dtend") else None,
                    "description": str(component.get("description", "")),
                }
                events.append(event)
                logger.debug(
                    "Event found",
                    extra={"uid": event["uid"], "summary": event["summary"], "dtstart": str(event["dtstart"])},
                )

        logger.info("Upcoming events fetched", extra={"calendar": calendar_name, "count": len(events)})
        return events

    def create_event(
        self,
        calendar_name: str,
        summary: str,
        dtstart: datetime,
        dtend: datetime,
        description: str = "",
    ) -> str:
        """Create a new event in a calendar.

        Args:
            calendar_name: Target calendar name.
            summary: Event title.
            dtstart: Start datetime (timezone-aware).
            dtend: End datetime (timezone-aware).
            description: Optional event description.

        Returns:
            UID of the created event.
        """
        logger.info(
            "Creating event",
            extra={
                "calendar": calendar_name,
                "summary": summary,
                "dtstart": str(dtstart),
                "dtend": str(dtend),
            },
        )

        cal = self._find_calendar(calendar_name)

        event = Event()
        event.add("summary", summary)
        event.add("dtstart", dtstart)
        event.add("dtend", dtend)
        if description:
            event.add("description", description)
        event.add("dtstamp", datetime.now(timezone.utc))

        ical = Calendar()
        ical.add("prodid", "-//DeepSeek Bot//Yandex Calendar//RU")
        ical.add("version", "2.0")
        ical.add_component(event)

        created = cal.save_event(ical.to_ical().decode("utf-8"))
        uid = str(event.get("uid", ""))

        logger.info("Event created", extra={"uid": uid, "summary": summary, "calendar": calendar_name})
        return uid

    def delete_event(self, calendar_name: str, uid: str) -> bool:
        """Delete an event by UID.

        Args:
            calendar_name: Calendar containing the event.
            uid: UID of the event to delete.

        Returns:
            True if deleted, False if not found.
        """
        logger.info("Deleting event", extra={"calendar": calendar_name, "uid": uid})

        cal = self._find_calendar(calendar_name)
        try:
            event = cal.event_by_uid(uid)
            event.delete()
            logger.info("Event deleted", extra={"uid": uid})
            return True
        except caldav.lib.error.NotFoundError:
            logger.warning("Event not found for deletion", extra={"uid": uid})
            return False
