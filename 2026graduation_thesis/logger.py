import csv
from datetime import datetime
from pathlib import Path


CSV_FILE = Path(__file__).with_name("response_times.csv")


def save_response_time(command, response_time_ms):
    """応答時間をCSVへ1行追加する。"""
    file_exists = CSV_FILE.exists()

    with CSV_FILE.open("a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow([
                "timestamp",
                "command",
                "response_time_ms",
            ])

        writer.writerow([
            datetime.now().isoformat(timespec="seconds"),
            command,
            round(response_time_ms, 2),
        ])
