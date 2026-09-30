<p align="center">
  <img src="assets/github-banner.png" width="70%" alt="TikTok Auto Messaging Bot"/>
</p>

<h1 align="center">TikTok Auto Messaging Bot</h1>

<p align="center">
  Sends a short message to your own TikTok chats from the Brave, Chrome, or Edge profile already logged in on this Windows PC.
</p>

## What it does

Close that browser, then start the app. It finds the installed browser and the profile that already has TikTok. A PC with only `Default` uses that profile. Extra profiles are used only when those folders exist.

The run opens `https://www.tiktok.com/messages`. Some accounts stay on that page. Others are sent to Business Suite, where the chat list is inside a frame. The bot reads the list in either place.

Each run:

- Skips a chat that was messaged in the last 12 hours
- Sends at most 10 chats, then stops
- Waits 20 to 45 seconds between sends
- Stops if TikTok asks you to log in or verify

The names and times are saved in `assets/messaged.csv`.

## Run

Windows, Python 3.14, and Brave, Chrome, or Edge with TikTok already logged in.

```bash
pip install -r requirements.txt
python main.py
```

The window shows the browser and profile it found. Start from there.

One chat only:

```bash
python main.py --once
```

Tests, with no TikTok session:

```bash
python -m pytest
```

## Layout

```
Auto-Tiktok-Messenger-Bot/
├── main.py                 # Window
├── core/
│   ├── detect.py           # Windows browser and profile
│   ├── browser.py          # Visible browser launch
│   ├── messenger.py        # Regular inbox and Business Suite
│   ├── message_gen.py      # Message text
│   ├── user_tracker.py     # 12-hour log
│   └── utils.py            # Typing delay
├── tests/
└── assets/messaged.csv
```

## Before you rely on a run

A finished run means the message was typed and Enter was pressed. Open the chat in TikTok to confirm it is in the thread. If the message page layout changes, the chat-list hook in `core/messenger.py` has to be updated.
