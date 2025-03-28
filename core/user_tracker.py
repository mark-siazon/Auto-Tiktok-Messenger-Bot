import os
from datetime import datetime, timedelta

def has_already_messaged(username):
    # Check if the user is in the CSV and last message was within 12 hours
    if not os.path.exists('assets/messaged.csv'):
        return False

    with open('assets/messaged.csv', 'r') as file:
        lines = file.readlines()
        for line in lines:
            parts = line.strip().split(',')
            if len(parts) != 2:
                continue  # skip malformed lines

            user, timestamp_str = parts
            if user == username:
                try:
                    last_time = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
                    if datetime.now() - last_time < timedelta(hours=12):
                        return True
                except:
                    continue  # skip broken timestamps

    return False

def save_messaged_user(username):
    # Append the username and current timestamp to the CSV
    with open('assets/messaged.csv', 'a') as file:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file.write(f"{username},{timestamp}\n")
