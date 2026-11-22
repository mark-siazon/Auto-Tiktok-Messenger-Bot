# AGENTS.md

## Scope
- Automated TikTok/Messenger Python bot (`mark-siazon/Auto-Tiktok-Messenger-Bot`, branch `main`).
- Follow root `C:\Codes Local\AGENTS.md` first, then this file.

## Environment / Stack
- Python 3.11 (`.venv`), `selenium==4.52.0`, `pytest==9.2.0` (`requirements.txt`, `pytest.ini`).

## Project Layout
- `main.py` — primary bot entrypoint
- `core/` — automation modules
- `tests/` — pytest test suite

## Key Commands
- `.\.venv\Scripts\python.exe -m pip check` — verify Python dependency consistency
- `.\.venv\Scripts\python.exe -m pytest -q tests` — run test suite
- `.\.venv\Scripts\python.exe main.py` — run bot entrypoint

## Secrets / Env
- Never commit browser session profiles, cookies, or account credentials.
