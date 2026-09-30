import ctypes
import json
import os
import shutil
import sqlite3
import sys
import tempfile
from dataclasses import dataclass

BROWSERS = (
    ("Brave", "brave.exe", os.path.join("BraveSoftware", "Brave-Browser", "User Data")),
    ("Chrome", "chrome.exe", os.path.join("Google", "Chrome", "User Data")),
    ("Edge", "msedge.exe", os.path.join("Microsoft", "Edge", "User Data")),
)


@dataclass
class Detection:
    browser: str
    binary: str
    user_data_dir: str
    profile_directory: str
    tiktok_login_found: bool
    message: str


def ensure_windows(platform=None):
    if (platform or sys.platform) != "win32":
        raise RuntimeError("This bot runs on Windows.")


def app_path_from_registry(exe_name):
    if sys.platform != "win32":
        return None
    import winreg

    keys = (
        (winreg.HKEY_CURRENT_USER, rf"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\{exe_name}"),
        (winreg.HKEY_LOCAL_MACHINE, rf"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\{exe_name}"),
        (winreg.HKEY_LOCAL_MACHINE, rf"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\App Paths\{exe_name}"),
    )
    for hive, path in keys:
        try:
            with winreg.OpenKey(hive, path) as key:
                value, _ = winreg.QueryValueEx(key, "")
        except OSError:
            continue
        if value and os.path.isfile(value):
            return value
    return None


def fallback_binary(exe_name):
    local_app_data = os.environ.get("LOCALAPPDATA", "")
    program_files = os.environ.get("PROGRAMFILES", r"C:\Program Files")
    program_files_x86 = os.environ.get("PROGRAMFILES(X86)", r"C:\Program Files (x86)")
    candidates = {
        "brave.exe": (
            os.path.join(program_files, "BraveSoftware", "Brave-Browser", "Application", "brave.exe"),
            os.path.join(local_app_data, "BraveSoftware", "Brave-Browser", "Application", "brave.exe"),
        ),
        "chrome.exe": (
            os.path.join(program_files, "Google", "Chrome", "Application", "chrome.exe"),
            os.path.join(program_files_x86, "Google", "Chrome", "Application", "chrome.exe"),
            os.path.join(local_app_data, "Google", "Chrome", "Application", "chrome.exe"),
        ),
        "msedge.exe": (
            os.path.join(program_files_x86, "Microsoft", "Edge", "Application", "msedge.exe"),
            os.path.join(program_files, "Microsoft", "Edge", "Application", "msedge.exe"),
        ),
    }
    for path in candidates.get(exe_name, ()):
        if path and os.path.isfile(path):
            return path
    return None


def profile_folders(user_data_dir):
    if not os.path.isdir(user_data_dir):
        return []
    names = []
    if os.path.isdir(os.path.join(user_data_dir, "Default")):
        names.append("Default")
    for entry in sorted(os.listdir(user_data_dir)):
        if entry.startswith("Profile ") and os.path.isdir(os.path.join(user_data_dir, entry)):
            names.append(entry)
    return names


def read_shared(path):
    generic_read = 0x80000000
    share = 0x1 | 0x2 | 0x4
    open_existing = 3
    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel32.CreateFileW.restype = ctypes.c_void_p
    kernel32.CreateFileW.argtypes = [
        ctypes.c_wchar_p,
        ctypes.c_uint32,
        ctypes.c_uint32,
        ctypes.c_void_p,
        ctypes.c_uint32,
        ctypes.c_uint32,
        ctypes.c_void_p,
    ]
    kernel32.ReadFile.argtypes = [
        ctypes.c_void_p,
        ctypes.c_void_p,
        ctypes.c_uint32,
        ctypes.POINTER(ctypes.c_ulong),
        ctypes.c_void_p,
    ]
    kernel32.ReadFile.restype = ctypes.c_int
    kernel32.CloseHandle.argtypes = [ctypes.c_void_p]
    handle = kernel32.CreateFileW(path, generic_read, share, None, open_existing, 0, None)
    if not handle or handle == ctypes.c_void_p(-1).value:
        raise OSError(ctypes.get_last_error(), path)
    try:
        chunks = []
        buffer = ctypes.create_string_buffer(1024 * 1024)
        read = ctypes.c_ulong(0)
        while True:
            ok = kernel32.ReadFile(handle, buffer, len(buffer), ctypes.byref(read), None)
            if not ok or read.value == 0:
                break
            chunks.append(buffer.raw[: read.value])
        data = b"".join(chunks)
        if not data:
            raise OSError("Could not read the browser cookie file.")
        return data
    finally:
        kernel32.CloseHandle(handle)


def copy_database(path, destination):
    try:
        shutil.copy2(path, destination)
        if os.path.getsize(destination) > 0:
            return
    except OSError:
        if sys.platform != "win32":
            raise
    with open(destination, "wb") as handle:
        handle.write(read_shared(path))


def sqlite_tiktok_status(path):
    temp_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".db") as handle:
            temp_path = handle.name
        copy_database(path, temp_path)
        if os.path.getsize(temp_path) == 0:
            return "unreadable"
        connection = sqlite3.connect(temp_path)
        try:
            row = connection.execute(
                "SELECT 1 FROM cookies WHERE host_key LIKE '%tiktok.com%' LIMIT 1"
            ).fetchone()
        except sqlite3.Error:
            return "unreadable"
        finally:
            connection.close()
        return "yes" if row is not None else "no"
    except OSError:
        return "unreadable"
    finally:
        if temp_path:
            try:
                os.remove(temp_path)
            except OSError:
                pass


def indexeddb_has_tiktok(profile_dir):
    folder = os.path.join(profile_dir, "IndexedDB")
    if not os.path.isdir(folder):
        return False
    return any("tiktok.com" in name.lower() for name in os.listdir(folder))


def cookie_has_tiktok(profile_dir):
    saw_readable_cookie_db = False
    for relative in (os.path.join("Network", "Cookies"), "Cookies"):
        path = os.path.join(profile_dir, relative)
        if not os.path.isfile(path):
            continue
        status = sqlite_tiktok_status(path)
        if status == "yes":
            return True
        if status == "no":
            saw_readable_cookie_db = True
    if saw_readable_cookie_db:
        return False
    return indexeddb_has_tiktok(profile_dir)


def _read_local_state(user_data_dir):
    path = os.path.join(user_data_dir, "Local State")
    if not os.path.isfile(path):
        return {}
    try:
        with open(path, encoding="utf-8") as handle:
            return json.load(handle)
    except (OSError, json.JSONDecodeError):
        return {}


def profile_active_time(user_data_dir, profile_directory):
    info = _read_local_state(user_data_dir).get("profile", {}).get("info_cache", {})
    return info.get(profile_directory, {}).get("active_time", 0) or 0


def most_recent_profile(user_data_dir, folders):
    if not folders:
        return None
    profile = _read_local_state(user_data_dir).get("profile", {})
    last_used = profile.get("last_used")
    if last_used in folders:
        return last_used
    return max(folders, key=lambda name: profile_active_time(user_data_dir, name))


def choose_profile(user_data_dir):
    folders = profile_folders(user_data_dir)
    if not folders:
        return None, False
    if len(folders) == 1:
        only = folders[0]
        return only, cookie_has_tiktok(os.path.join(user_data_dir, only))

    logged_in = [
        name for name in folders if cookie_has_tiktok(os.path.join(user_data_dir, name))
    ]
    if len(logged_in) == 1:
        return logged_in[0], True
    if len(logged_in) > 1:
        return most_recent_profile(user_data_dir, logged_in), True
    if "Default" in folders:
        return "Default", False
    return folders[0], False


def profile_caption(user_data_dir, profile_directory):
    info = _read_local_state(user_data_dir).get("profile", {}).get("info_cache", {})
    label = info.get(profile_directory, {}).get("name")
    if label:
        return f"{profile_directory} ({label})"
    return profile_directory


def detect_browsers(local_app_data, binaries):
    found = []
    for browser, _exe, relative in BROWSERS:
        binary = binaries.get(browser)
        user_data_dir = os.path.join(local_app_data, relative)
        if not binary or not os.path.isfile(binary):
            continue
        if not os.path.isfile(os.path.join(user_data_dir, "Local State")):
            continue
        profile, logged_in = choose_profile(user_data_dir)
        if not profile:
            continue
        found.append(
            Detection(
                browser=browser,
                binary=binary,
                user_data_dir=user_data_dir,
                profile_directory=profile,
                tiktok_login_found=logged_in,
                message="",
            )
        )
    if not found:
        return None

    logged = [item for item in found if item.tiktok_login_found]
    pool = logged or found
    winner = max(pool, key=lambda item: profile_active_time(item.user_data_dir, item.profile_directory))
    if winner.tiktok_login_found:
        caption = profile_caption(winner.user_data_dir, winner.profile_directory)
        winner.message = f"{winner.browser} / {caption}"
    else:
        winner.message = "TikTok login was not found."
    return winner


def installed_binaries():
    binaries = {}
    for browser, exe, _relative in BROWSERS:
        path = app_path_from_registry(exe) or fallback_binary(exe)
        if path:
            binaries[browser] = path
    return binaries


def load_config_override(path="config.json"):
    try:
        with open(path, encoding="utf-8") as handle:
            config = json.load(handle)
    except (OSError, json.JSONDecodeError):
        return None
    binary = config.get("binary")
    user_data_dir = config.get("user_data_dir")
    profile_directory = config.get("profile_directory")
    browser = config.get("browser")
    if not (binary and user_data_dir and profile_directory and browser):
        return None
    if not os.path.isfile(binary) or not os.path.isdir(os.path.join(user_data_dir, profile_directory)):
        return None
    return Detection(
        browser=browser,
        binary=binary,
        user_data_dir=user_data_dir,
        profile_directory=profile_directory,
        tiktok_login_found=False,
        message=f"{browser} / {profile_directory}",
    )


def detect_target():
    ensure_windows()
    local_app_data = os.environ.get("LOCALAPPDATA", "")
    found = detect_browsers(local_app_data, installed_binaries())
    if found is not None:
        return found
    return load_config_override()
