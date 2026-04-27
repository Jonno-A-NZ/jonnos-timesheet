"""Entry point — runs the full timesheet workflow."""
from datetime import date

from inputs.gmail import get_sent_emails
from inputs.slack import get_slack_messages
from inputs.calendar import get_calendar_events
from process import group_activities
from output import write_summary


def run():
    today = date.today()

    # Input
    emails = get_sent_emails(service=None, date=today)
    messages = get_slack_messages(client=None, date=today)
    events = get_calendar_events(service=None, date=today)

    # Process
    activities = group_activities(emails, messages, events)

    # Output
    write_summary(activities)
    print(f"Timesheet written for {today}")


if __name__ == "__main__":
    run()
