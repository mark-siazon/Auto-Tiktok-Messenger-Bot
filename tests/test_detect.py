import json
import os
import sqlite3

import pytest

from core.detect import (
    choose_profile,
    detect_browsers,
    ensure_windows,
    load_config_override,
    profile_folders,
)


def write_cookies(profile_dir, hosts):
    network = os.path.join(profile_dir, "Network")
    os.makedirs(network, exist_ok=True)
    connection = sqlite3.connect(os.path.join(network, "Cookies"))
    connection.execute("CREATE TABLE cookies (host_key TEXT)")
    for host in hosts:
        connection.execute("INSERT INTO cookies (host_key) VALUES (?)", (host,))
    connection.commit()
    connection.close()


def write_local_state(user_data, last_used, active_times):
    os.makedirs(user_data, exist_ok=True)
    info = {name: {"active_time": stamp} for name, stamp in active_times.items()}
    payload = {"profile": {"last_used": last_used, "info_cache": info}}
    with open(os.path.join(user_data, "Local State"), "w", encoding="utf-8") as handle:
        json.dump(payload, handle)


def test_non_windows_is_refused():
    with pytest.raises(RuntimeError, match="Windows"):
        ensure_windows("linux")


def test_only_default_profile_is_used(tmp_path):
    user_data = tmp_path / "User Data"
    default = user_data / "Default"
    write_cookies(default, [".tiktok.com"])
    write_local_state(user_data, "Default", {"Default": 1})

    assert profile_folders(user_data) == ["Default"]
    assert "Profile 1" not in profile_folders(user_data)
    assert choose_profile(str(user_data)) == ("Default", True)


def test_locked_cookies_fall_back_to_tiktok_storage(tmp_path):
    user_data = tmp_path / "User Data"
    default = user_data / "Default"
    indexed = default / "IndexedDB"
    indexed.mkdir(parents=True)
    (indexed / "https_www.tiktok.com_0.indexeddb.leveldb").mkdir()
    write_local_state(user_data, "Default", {"Default": 1})

    assert choose_profile(str(user_data)) == ("Default", True)


def test_tiktok_cookie_selects_that_profile(tmp_path):
    user_data = tmp_path / "User Data"
    write_cookies(user_data / "Default", ["example.com"])
    write_cookies(user_data / "Profile 1", [".tiktok.com"])
    write_local_state(user_data, "Default", {"Default": 10, "Profile 1": 1})

    assert choose_profile(str(user_data)) == ("Profile 1", True)


def test_several_logged_in_profiles_use_the_most_recent(tmp_path):
    user_data = tmp_path / "User Data"
    write_cookies(user_data / "Default", [".tiktok.com"])
    write_cookies(user_data / "Profile 2", [".www.tiktok.com"])
    write_local_state(
        user_data,
        "Profile 2",
        {"Default": 10, "Profile 2": 3},
    )

    assert choose_profile(str(user_data)) == ("Profile 2", True)


def test_no_tiktok_login_uses_default(tmp_path):
    user_data = tmp_path / "User Data"
    write_cookies(user_data / "Default", ["example.com"])
    write_cookies(user_data / "Profile 1", ["example.org"])
    write_local_state(user_data, "Profile 1", {"Default": 1, "Profile 1": 9})

    binary = tmp_path / "brave.exe"
    binary.write_text("", encoding="utf-8")
    local_app = tmp_path / "local"
    brave_data = local_app / "BraveSoftware" / "Brave-Browser" / "User Data"
    write_cookies(brave_data / "Default", ["example.com"])
    write_cookies(brave_data / "Profile 1", ["example.org"])
    write_local_state(brave_data, "Profile 1", {"Default": 1, "Profile 1": 9})

    found = detect_browsers(str(local_app), {"Brave": str(binary)})
    assert found.profile_directory == "Default"
    assert found.tiktok_login_found is False
    assert found.message == "TikTok login was not found."


def test_logged_in_browser_wins(tmp_path):
    local_app = tmp_path / "local"
    brave = tmp_path / "brave.exe"
    edge = tmp_path / "msedge.exe"
    brave.write_text("", encoding="utf-8")
    edge.write_text("", encoding="utf-8")

    brave_data = local_app / "BraveSoftware" / "Brave-Browser" / "User Data"
    edge_data = local_app / "Microsoft" / "Edge" / "User Data"
    write_cookies(brave_data / "Default", ["example.com"])
    write_local_state(brave_data, "Default", {"Default": 100})
    write_cookies(edge_data / "Default", [".tiktok.com"])
    write_local_state(edge_data, "Default", {"Default": 1})

    found = detect_browsers(str(local_app), {"Brave": str(brave), "Edge": str(edge)})
    assert found.browser == "Edge"
    assert found.profile_directory == "Default"
    assert found.tiktok_login_found is True


def test_config_override_requires_a_real_profile(tmp_path):
    missing = tmp_path / "missing.json"
    missing.write_text("{}", encoding="utf-8")
    assert load_config_override(missing) is None

    binary = tmp_path / "brave.exe"
    binary.write_text("", encoding="utf-8")
    profile = tmp_path / "User Data" / "Default"
    profile.mkdir(parents=True)
    config = tmp_path / "config.json"
    config.write_text(
        json.dumps(
            {
                "browser": "Brave",
                "binary": str(binary),
                "user_data_dir": str(profile.parent),
                "profile_directory": "Default",
            }
        ),
        encoding="utf-8",
    )
    found = load_config_override(config)
    assert found.browser == "Brave"
    assert found.profile_directory == "Default"
