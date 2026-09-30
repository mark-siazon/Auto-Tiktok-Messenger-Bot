import os
from datetime import datetime, timedelta

LOG_PATH = os.path.join("assets", "messaged.csv")


def has_already_messaged(username, now=None, log_path=LOG_PATH):
    if not os.path.exists(log_path):
        return False

    current = now or datetime.now()
    with open(log_path, encoding="utf-8") as handle:
        for line in handle:
            parts = line.strip().split(",")
            if len(parts) != 2:
                continue
            user, timestamp_str = parts
            if user != username:
                continue
            try:
                last_time = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                continue
            if current - last_time < timedelta(hours=12):
                return True
    return False


def save_messaged_user(username, now=None, log_path=LOG_PATH):
    folder = os.path.dirname(log_path)
    if folder:
        os.makedirs(folder, exist_ok=True)
    current = now or datetime.now()
    with open(log_path, "a", encoding="utf-8") as handle:
        handle.write(f"{username},{current.strftime('%Y-%m-%d %H:%M:%S')}\n")
