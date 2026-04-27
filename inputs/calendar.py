"""Fetches Google Calendar events for a given date."""
import os
from datetime import datetime, timezone
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]
CREDENTIALS_FILE = os.path.join(os.path.dirname(__file__), "..", "credentials.json")
TOKEN_FILE = os.path.join(os.path.dirname(__file__), "..", "token.json")


def _get_service():
    """Authenticates and returns a Google Calendar service client."""
    creds = None

    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, "w") as f:
            f.write(creds.to_json())

    return build("calendar", "v3", credentials=creds)


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
