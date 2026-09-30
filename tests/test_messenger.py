import pytest

from core.messenger import StopRun, run_messages


class Element:
    def __init__(self, text, browser):
        self.text = text
        self.browser = browser

    def click(self):
        self.browser.clicks.append(self.text)

    def send_keys(self, value):
        self.browser.keys.append(value)


class Browser:
    def __init__(self, names, page_source="", url="https://www.tiktok.com/messages"):
        self.names = list(names)
        self.page_source = page_source
        self.current_url = url
        self.screenshots = []
        self.clicks = []
        self.keys = []
        self.name_index = 0

    def get(self, url):
        self.current_url = url

    def find_elements(self, _by, selector):
        if "chat-list-item" in selector:
            return [Element(name, self) for name in self.names]
        if "chat-nickname" in selector and self.name_index < len(self.names):
            element = Element(self.names[self.name_index], self)
            self.name_index += 1
            return [element]
        if "message-input" in selector or "contenteditable" in selector or "Draft" in selector:
            return [Element("composer", self)]
        return []

    def execute_script(self, *_args):
        return None

    def save_screenshot(self, path):
        self.screenshots.append(path)
        with open(path, "wb") as handle:
            handle.write(b"png")


def noop():
    return None


def test_missing_chat_list_stops_once(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    browser = Browser([])

    with pytest.raises(StopRun, match="Chat list"):
        run_messages(browser, settle=noop, pause=noop)

    assert browser.clicks == []
    assert browser.screenshots == ["missing_hook.png"]


def test_verification_page_stops_before_send(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    browser = Browser(["ada", "bea"], page_source="Verify to continue")

    with pytest.raises(StopRun, match="verification"):
        run_messages(browser, settle=noop, pause=noop)

    assert browser.clicks == []
    assert browser.screenshots == ["challenge.png"]


def test_normal_run_stops_at_ten_sends(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    names = [f"user{index}" for index in range(12)]
    browser = Browser(names)

    summary = run_messages(browser, settle=noop, pause=noop, type_text=lambda element, text: element.send_keys(text))

    sent_names = [name for name in browser.clicks if name in names]
    assert sent_names == names[:10]
    assert summary == "Sent 10 messages. Cap reached."
