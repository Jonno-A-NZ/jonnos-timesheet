"""Fetches Slack messages sent by the user today."""
import os
from datetime import datetime, timezone
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv

load_dotenv()


def _get_client():
    token = os.environ.get("SLACK_USER_TOKEN")
    if not token:
        raise EnvironmentError("SLACK_USER_TOKEN not set in .env")
    return WebClient(token=token)


def get_slack_messages(date):
    """Returns a list of messages sent by the user on the given date.

    Each message is a dict with: channel, text, sent_at.
    """
    client = _get_client()

    start = datetime(date.year, date.month, date.day, 0, 0, 0, tzinfo=timezone.utc).timestamp()
    end = datetime(date.year, date.month, date.day, 23, 59, 59, tzinfo=timezone.utc).timestamp()
    query = f"from:me after:{date.isoformat()} before:{date.isoformat()}"

    try:
        result = client.search_messages(query=query, count=100)
    except SlackApiError as e:
        raise RuntimeError(f"Slack API error: {e.response['error']}")

    messages = []
    for match in result["messages"]["matches"]:
        ts = float(match.get("ts", 0))
        if not (start <= ts <= end):
            continue
        messages.append({
            "channel": match.get("channel", {}).get("name", "unknown"),
            "text": match.get("text", ""),
            "sent_at": datetime.fromtimestamp(ts, tz=timezone.utc).isoformat(),
        })

    return messages
