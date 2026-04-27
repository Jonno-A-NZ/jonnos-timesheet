"""Writes the timesheet summary to a text file."""
import os
from datetime import date

OUTPUT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "output"))


def _safe_path(filename):
    """Raises an error if the file is outside OUTPUT_DIR or not a .txt file."""
    if not filename.endswith(".txt"):
        raise ValueError(f"Only .txt files are allowed. Got: {filename}")

    abs_path = os.path.abspath(filename)
    if not abs_path.startswith(OUTPUT_DIR + os.sep):
        raise ValueError(f"Writes are only allowed inside '{OUTPUT_DIR}'. Got: {abs_path}")

    return abs_path


def write_summary(activities, output_dir=OUTPUT_DIR):
    """Writes grouped activities to a dated text file in the output folder."""
    os.makedirs(output_dir, exist_ok=True)
    filename = os.path.join(output_dir, f"timesheet-{date.today()}.txt")
    safe = _safe_path(filename)

    with open(safe, "w") as f:
        # TODO: implement summary formatting
        f.write("")
