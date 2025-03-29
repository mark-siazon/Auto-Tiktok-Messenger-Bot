# 📋 Changelog

All notable changes to this project will be documented here.

---

## [1.0.0] - 2025-03-29

### Added

- Initial working version with TikTok DM auto-messaging via GUI
- Support for Brave browser (Profile 1)
- Human-like message typing + delay simulation
- Skips users messaged within the last 12 hours
- Tracks messaged users in `messaged.csv`
- GUI message input with `tkinter`

---

## [1.1.0] - 2025-03-30

### Added

- Cross-browser support: Brave, Chrome, and Microsoft Edge
- GUI browser picker with "Remember my choice"
- Edge WebDriver check and prompt to download if missing
- Prompt to move `msedgedriver.exe` to correct folder
- Modular folder structure (`core/`, `assets/`, etc.)

### Changed

- Refactored logic into modular components for easier maintenance
- Improved `.gitignore` and README.md formatting

### Fixed

- Graceful handling of browser launch errors
- Edge profile detection error due to missing driver

---

## [Planned]

- Auto-detect unread users only
- GUI log viewer (live and history)
- Multi-account switcher
- .exe build for one-click usage
- TikTok UI selector versioning (fallbacks or patches)
- Message templates with variables (e.g., {name})
- Smart delay system (based on volume/timer)
- Scheduled messaging (e.g., only run at 9–11 AM)
- Crash recovery & resume support
- Edge/Chrome/Brave profile drag-and-drop selector
- System tray / minimize-to-background
- Export logs to Excel/CSV or Google Sheets
- Daily report of who was messaged
