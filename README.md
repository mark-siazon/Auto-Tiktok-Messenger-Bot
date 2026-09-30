<p align="center">
  <img src="assets/github-banner.png" width="70%" alt="TikTok Auto Messaging Bot"/>
</p>

<h1 align="center">TikTok Auto Messaging Bot</h1>

<p align="center">
  Sends a short message to your own TikTok chats from the Brave, Chrome, or Edge profile already logged in on this Windows PC.
</p>

## Features

- Finds Brave, Chrome, or Edge from the Windows registry and the usual install folders
- Uses `%LOCALAPPDATA%` for the signed-in Windows user, so the path is not fixed to one account
- Uses the `Default` profile when that is the only profile on the PC
- When extra profiles exist, uses the one that already has TikTok
- When several profiles have TikTok, uses the one Windows marks as most recently used
- Shows the detected browser and profile in the window before you start
- Opens `https://www.tiktok.com/messages`
- Reads the chat list on the regular Messages page
- Reads the chat list inside the Business Suite frame when TikTok redirects there
- Types a short varied message with a delay between characters
- Skips a chat messaged in the last 12 hours
- Sends at most 10 chats in one run, then stops
- Waits 20 to 45 seconds between sends
- Keeps the browser window visible
- Stops if TikTok asks you to log in or verify, and does not retry
- Asks you to close the browser when that profile is already open
- Saves each chat name and time in `assets/messaged.csv`
- `python main.py --once` sends to a single chat and stops
- Selenium Manager fetches the browser driver, so Edge does not need a driver copied by hand

## Requirements

- Windows
- Python 3.14
- One of these browsers, with TikTok already logged in:
  - Brave
  - Chrome
  - Microsoft Edge

```bash
pip install -r requirements.txt
```

## How to run

Close the detected browser first, then:

```bash
python main.py
```

One chat only:

```bash
python main.py --once
```

Tests, with no TikTok session:

```bash
python -m pytest
```

## Project structure

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

## Future improvements

- Message only unread chats
- Show the send log in the window
- Export the log to CSV from the window
- Message templates with a name variable
- A daily summary of who was messaged
- Schedule a run for a set time of day
- Resume a run after a crash
- Pick a browser profile from the window when detection finds none
- More than one TikTok account on the same PC
- A standalone Windows app, so Python is not required
- Update the chat-list hook when TikTok changes the page

## Warnings

- This automates your own TikTok messages
- A finished run means the message was typed and Enter was pressed. Open the chat in TikTok to confirm it is in the thread
- If the message page layout changes, the chat-list hook in `core/messenger.py` has to be updated
