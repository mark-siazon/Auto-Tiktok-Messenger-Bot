# Contributions

## Setup

- Windows
- Python 3.14
- Brave, Chrome, or Edge

```bash
pip install -r requirements.txt
python -m pytest
```

Close the detected browser before `python main.py`.

## Pull requests

- Branch from `main`
- Open the pull request into `main`
- Run `python -m pytest` before you push
- Describe what changed and how you checked it

## Do not commit

- `assets/messaged.csv`
- `config.json`
- `.env`
- `missing_hook.png`, `challenge.png`, or `critical_error.png`
- A Windows username, a profile path, a chat name, or a cookie file
- Browser user-data folders

## Code

- Keep browser and profile discovery in `core/detect.py`
- Keep the regular Messages page and the Business Suite frame in `core/messenger.py`
- A PC with only `Default` must still work
- Add a test when you change detection, the send cap, the 12-hour skip, or the chat-list hooks
- Tests use temp folders and a fake browser. They do not open TikTok and they do not send a message

## Ideas

Larger ideas belong in the Future improvements list in `README.md` until they are built.
