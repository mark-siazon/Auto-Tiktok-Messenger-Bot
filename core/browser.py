from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.support.ui import WebDriverWait

from core.detect import detect_target


def init_browser(target=None):
    target = target or detect_target()
    if target is None:
        raise RuntimeError("No Brave, Chrome, or Edge profile was found on this PC.")

    if target.browser == "Edge":
        options = EdgeOptions()
        driver = webdriver.Edge
    else:
        options = Options()
        driver = webdriver.Chrome

    options.binary_location = target.binary
    options.add_argument(f"--user-data-dir={target.user_data_dir}")
    options.add_argument(f"--profile-directory={target.profile_directory}")
    options.add_argument("--start-maximized")

    try:
        browser = driver(options=options)
    except Exception as exc:
        text = str(exc).lower()
        if "already in use" in text or "devtoolsactiveport" in text or "session not created" in text:
            raise RuntimeError(
                f"Close {target.browser} and start again. That profile is already open."
            ) from exc
        raise

    return browser, WebDriverWait(browser, 20), target
