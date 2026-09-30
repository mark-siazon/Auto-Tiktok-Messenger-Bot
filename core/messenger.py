import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from core.browser import init_browser
from core.message_gen import generate_human_message
from core.user_tracker import has_already_messaged, save_messaged_user
from core.utils import human_delay, type_like_human

MESSAGES_URL = "https://www.tiktok.com/messages"
MAX_SENDS = 10
CHAT_LIST_SELECTORS = (
    "[data-e2e='dm-new-conversation-item']",
    "[data-e2e='chat-list-item']",
)
NAME_SELECTORS = (
    "[data-e2e='dm-new-chat-nickname']",
    "[data-e2e='chat-nickname']",
)
COMPOSER_SELECTORS = (
    "[data-e2e='dm-new-input-editor'] div[contenteditable='true']",
    "[data-e2e='message-input-area'] div[contenteditable='true']",
    "div.public-DraftEditor-content",
    "div.public-DraftStyleDefault-block",
)
CHALLENGE_MARKERS = (
    "verify to continue",
    "confirm it's you",
    "confirm it’s you",
    "drag the puzzle",
    "captcha",
)


class StopRun(Exception):
    pass


def visible_text(browser):
    script = getattr(browser, "execute_script", None)
    if callable(script):
        try:
            text = script("return document.body ? document.body.innerText : ''")
        except Exception:
            text = None
        if text:
            return text
    return getattr(browser, "page_source", "") or ""


def challenge_reason(browser):
    url = (getattr(browser, "current_url", "") or "").lower()
    if "/login" in url:
        return "TikTok is asking you to log in."
    source = visible_text(browser).lower()
    for marker in CHALLENGE_MARKERS:
        if marker in source:
            return "TikTok is asking for verification."
    return None


def _chat_rows(browser):
    for selector in CHAT_LIST_SELECTORS:
        found = browser.find_elements(By.CSS_SELECTOR, selector)
        if found:
            return found
    return []


def _one(browser, selectors):
    for selector in selectors:
        found = browser.find_elements(By.CSS_SELECTOR, selector)
        if found:
            return found[0]
    return None


def _chat_rows_anywhere(browser):
    switch = getattr(browser, "switch_to", None)
    if switch is not None:
        try:
            switch.default_content()
        except Exception:
            pass
    rows = _chat_rows(browser)
    if rows:
        return rows
    if switch is None:
        return []
    try:
        frames = browser.find_elements(By.CSS_SELECTOR, "iframe")
    except Exception:
        return []
    for frame in frames:
        try:
            switch.default_content()
            switch.frame(frame)
        except Exception:
            continue
        rows = _chat_rows(browser)
        if rows:
            return rows
    try:
        switch.default_content()
    except Exception:
        pass
    return []


def wait_for_chats(browser, timeout):
    deadline = time.monotonic() + timeout
    while True:
        reason = challenge_reason(browser)
        if reason:
            return [], reason
        rows = _chat_rows_anywhere(browser)
        if rows or time.monotonic() >= deadline:
            return rows, None
        time.sleep(0.5)


def _stop(browser, message, screenshot):
    browser.save_screenshot(screenshot)
    raise StopRun(message)


def run_messages(browser, *, once=False, pause=None, settle=None, type_text=None, on_status=None, chat_timeout=20):
    def report(message):
        if on_status:
            on_status(message)

    pause = pause or (lambda: human_delay(20, 45))
    settle = settle or (lambda: human_delay(5, 7))
    type_text = type_text or type_like_human
    limit = 1 if once else MAX_SENDS

    report("Opening TikTok messages.")
    browser.get(MESSAGES_URL)
    settle()

    chats, reason = wait_for_chats(browser, chat_timeout)
    if reason:
        _stop(browser, reason, "challenge.png")
    if not chats:
        _stop(browser, "Chat list was not found.", "missing_hook.png")

    sent = 0
    for user in chats:
        if sent >= limit:
            report("Cap reached.")
            break

        reason = challenge_reason(browser)
        if reason:
            _stop(browser, reason, "challenge.png")

        browser.execute_script("arguments[0].scrollIntoView();", user)
        user.click()
        settle()

        reason = challenge_reason(browser)
        if reason:
            _stop(browser, reason, "challenge.png")

        name_element = _one(browser, NAME_SELECTORS)
        if name_element is None:
            _stop(browser, "Chat name was not found.", "missing_hook.png")
        username = name_element.text.strip()
        if not username:
            continue
        if has_already_messaged(username):
            report(f"Skipped {username}.")
            continue

        composer = _one(browser, COMPOSER_SELECTORS)
        if composer is None:
            _stop(browser, "Message box was not found.", "missing_hook.png")

        if sent:
            pause()

        composer.click()
        message = generate_human_message()
        type_text(composer, message)
        composer.send_keys(Keys.RETURN)
        save_messaged_user(username)
        sent += 1
        report(f"Sent to {username}.")

    if sent >= limit and not once:
        return f"Sent {sent} messages. Cap reached."
    if sent == 0:
        return "No new messages sent."
    return f"Sent {sent} message." if sent == 1 else f"Sent {sent} messages."


def start_bot(once=False, on_status=None):
    browser, _wait, target = init_browser()
    if on_status:
        on_status(target.message)
    try:
        return run_messages(browser, once=once, on_status=on_status)
    except Exception as exc:
        if not isinstance(exc, StopRun):
            try:
                browser.save_screenshot("critical_error.png")
            except Exception:
                pass
        raise
    finally:
        browser.quit()
