import pytest
import os
from unittest.mock import MagicMock

@pytest.fixture
def mock_env_vars(monkeypatch):
    monkeypatch.setenv("SMTP_HOST", "smtp.test.com")
    monkeypatch.setenv("SMTP_PORT", "587")
    monkeypatch.setenv("SMTP_USER", "test@test.com")
    monkeypatch.setenv("SMTP_PASS", "testpass")
    monkeypatch.setenv("EMAIL_FROM", "test@test.com")
    monkeypatch.setenv("EMAIL_TO", "recipient@test.com")
    monkeypatch.setenv("CHROME_PROFILE_PATH", "/tmp/chrome_profile")
    monkeypatch.setenv("TIKTOK_ADS_URL", "https://ads.tiktok.com/test")
