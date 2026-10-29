from unittest.mock import patch
from notifications.services import send_notification


def test_send_notification_no_telegram(monkeypatch):
    monkeypatch.delenv("TELEGRAM_BOT_TOKEN", raising=False)
    monkeypatch.delenv("TELEGRAM_CHAT_ID", raising=False)
    # Should not raise — falls back to log
    send_notification("test message")


@patch("notifications.services.requests.post")
def test_send_notification_with_telegram(mock_post, monkeypatch):
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "t")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "c")
    send_notification("hello")
    mock_post.assert_called_once()