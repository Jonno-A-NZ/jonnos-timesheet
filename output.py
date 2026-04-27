"""Writes the timesheet summary to a text file."""
import os
from datetime import date


def write_summary(activities, output_dir="output"):
    """Writes grouped activities to a dated text file."""
    os.makedirs(output_dir, exist_ok=True)
    filename = os.path.join(output_dir, f"timesheet-{date.today()}.txt")
    # TODO: implement summary formatting and write
    pass
