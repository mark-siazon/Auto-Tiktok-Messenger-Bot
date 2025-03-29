# TikTok Auto Messaging Bot 💬

This bot automatically sends human-like, casual messages to your TikTok contacts using your logged-in **Brave**, **Chrome**, or **Edge** browser profile.

Designed to simulate real user behavior — random delays, varied message formats, and skips users already messaged recently.

---

## ✅ Features

- Uses your logged-in **Profile 1** (Brave, Chrome, or Edge)
- Skips users messaged in the last **12 hours**
- Auto-generates **human-like streak messages**
- Fully **GUI-based** — no terminal required
- Clean, modular Python architecture
- Remembers your browser choice for next run
- Edge WebDriver install prompt if not found

---

### 🚧 Planned / Optional Improvements

- [ ] Auto-detect unread users only
- [ ] Limit daily message count (e.g. max 10 per run)
- [ ] GUI log viewer (table of who was messaged & when)
- [ ] Export logs to Excel/CSV
- [ ] Support multiple TikTok accounts (profile switcher in GUI)
- [ ] Add profile picker (select Brave/Chrome/Edge + user data folder)
- [ ] Add cross-browser support (Brave, Chrome, Edge)
- [ ] Clipboard-paste workaround for emoji support (ChromeDriver BMP fix)
- [ ] Build .exe version for standalone use
- [ ] Auto-update DOM selectors when TikTok layout changes

---

## 🛠 Requirements

- Python 3.10 or higher
- [undetected-chromedriver](https://github.com/ultrafunkamsterdam/undetected-chromedriver)
- One of the following browsers installed with TikTok already logged in (Profile 1):
  - Brave
  - Chrome
  - Microsoft Edge

Install dependencies:

```bash
pip install undetected-chromedriver selenium
```

---

## 🚀 How to Run

```bash
python main.py
```

Make sure your selected browser is **completely closed** before running the bot.

If using **Edge**, ensure `msedgedriver.exe` is placed at:

```
C:\Program Files (x86)\Microsoft\Edge\Application\msedgedriver.exe
```

---

## 📁 Project Structure

```
tiktok-bot/
├── main.py
├── core/
│   ├── browser.py         # Launches Brave, Chrome, or Edge using selected profile
│   ├── messenger.py       # Core logic: who to message and when
│   ├── message_gen.py     # Generates natural random messages
│   ├── user_tracker.py    # Tracks last message timestamp per user
│   └── utils.py           # Typing delays and human-like behavior
├── assets/
│   └── messaged.csv       # Log of messaged users + timestamp
├── .gitignore
└── config.json            # Stores browser choice for future use
```

---

## ⚠️ Warnings

- This bot simulates real behavior but still **automates interaction**. Use responsibly.
- TikTok’s layout may change — inspect HTML and update selectors if needed.
- If using Edge, ensure **msedgedriver.exe** is installed and placed in the correct directory.
