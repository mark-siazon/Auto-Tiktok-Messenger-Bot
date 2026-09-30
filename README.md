# TikTok Auto Messaging Bot 💬

  <p align="center">
    <img src="assets/github-banner.png" alt="TikTok Bot Banner" width="60%">
  </p>

This bot sends short messages to your TikTok chats from the Brave, Chrome, or Edge profile already logged in on this Windows PC.

---

## Features

- Finds Brave, Chrome, or Edge from Windows, including a PC that only has the `Default` profile
- Uses the profile that already has a TikTok login
- Skips chats messaged in the last 12 hours
- Sends at most 10 chats per run, with a pause between them
- Stops when TikTok shows a login or verification page
- `python main.py --once` sends a single message

---

## Requirements

- Windows
- Python 3.14
- Brave, Chrome, or Edge, with TikTok logged in

```bash
pip install -r requirements.txt
```

---

## How to Run

Close the detected browser if it is already open, then:

```bash
python main.py
```

The window shows the browser and profile it found. Start messaging from there.

```bash
python -m pytest
python main.py --once
```

---

## Project Structure

```
Auto-Tiktok-Messenger-Bot/
├── main.py
├── core/
│   ├── detect.py
│   ├── browser.py
│   ├── messenger.py
│   ├── message_gen.py
│   ├── user_tracker.py
│   └── utils.py
├── tests/
└── assets/messaged.csv
```

---

## Warnings

- This automates your own TikTok messages. A run stops at 10 sends, and it stops if TikTok asks you to log in or verify.
- If the message page layout changes, the chat list hook has to be updated.
