"""Fetches emails sent today from Gmail."""
import base64
from datetime import datetime, timezone
from googleapiclient.discovery import build
from inputs.google_auth import get_credentials


def _get_service():
    return build("gmail", "v1", credentials=get_credentials())


def get_sent_emails(date):
    """Returns a list of emails sent by the user on the given date.

    Each email is a dict with: subject, to, sent_at, snippet.
    """
    service = _get_service()

    start = int(datetime(date.year, date.month, date.day, 0, 0, 0, tzinfo=timezone.utc).timestamp())
    end = int(datetime(date.year, date.month, date.day, 23, 59, 59, tzinfo=timezone.utc).timestamp())
    query = f"in:sent after:{start} before:{end}"

    result = service.users().messages().list(userId="me", q=query).execute()
    messages = result.get("messages", [])

    emails = []
    for msg in messages:
        detail = service.users().messages().get(
            userId="me", id=msg["id"], format="metadata",
            metadataHeaders=["Subject", "To", "Date"]
        ).execute()

        headers = {h["name"]: h["value"] for h in detail["payload"]["headers"]}
        emails.append({
            "subject": headers.get("Subject", "No subject"),
            "to": headers.get("To", ""),
            "sent_at": headers.get("Date", ""),
            "snippet": detail.get("snippet", ""),
        })

    return emails
