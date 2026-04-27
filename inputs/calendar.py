"""Fetches Google Calendar events for a given date."""
from datetime import datetime, timezone
from googleapiclient.discovery import build
from inputs.google_auth import get_credentials


def _get_service():
    return build("calendar", "v3", credentials=get_credentials())


def get_calendar_events(date):
    """Returns a list of calendar events the user attended on the given date.

    Each event is a dict with: title, start, end, duration_minutes, attendees.
    """
    service = _get_service()

    start_of_day = datetime(date.year, date.month, date.day, 0, 0, 0, tzinfo=timezone.utc).isoformat()
    end_of_day = datetime(date.year, date.month, date.day, 23, 59, 59, tzinfo=timezone.utc).isoformat()

    result = service.events().list(
        calendarId="primary",
        timeMin=start_of_day,
        timeMax=end_of_day,
        singleEvents=True,
        orderBy="startTime",
    ).execute()

    events = []
    for item in result.get("items", []):
        start = item["start"].get("dateTime", item["start"].get("date"))
        end = item["end"].get("dateTime", item["end"].get("date"))

        duration_minutes = None
        if "T" in start and "T" in end:
            fmt = "%Y-%m-%dT%H:%M:%S%z"
            duration_minutes = int(
                (datetime.fromisoformat(end) - datetime.fromisoformat(start)).seconds / 60
            )

        events.append({
            "title": item.get("summary", "No title"),
            "start": start,
            "end": end,
            "duration_minutes": duration_minutes,
            "attendees": [a["email"] for a in item.get("attendees", [])],
        })

    return events
