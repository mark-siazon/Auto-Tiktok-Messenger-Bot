from datetime import datetime, timedelta

from core.user_tracker import has_already_messaged, save_messaged_user


def test_log_is_created_and_twelve_hour_skip_applies(tmp_path):
    log_path = tmp_path / "assets" / "messaged.csv"
    now = datetime(2026, 9, 30, 12, 0, 0)
    save_messaged_user("ada", now=now, log_path=str(log_path))

    assert log_path.exists()
    assert has_already_messaged("ada", now=now + timedelta(hours=11), log_path=str(log_path))
    assert not has_already_messaged("ada", now=now + timedelta(hours=13), log_path=str(log_path))
