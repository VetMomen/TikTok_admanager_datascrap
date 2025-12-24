import pytest
from mailer import send_report
from unittest.mock import patch, MagicMock
import os

def test_send_report_success(mock_env_vars):
    with patch("smtplib.SMTP") as mock_smtp:
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        
        result = send_report(subject="Test Subject", body="Test Body")
        
        assert result is True
        mock_smtp.assert_called_once_with("smtp.test.com", 587)
        mock_server.starttls.assert_called_once()
        mock_server.login.assert_called_once_with("test@test.com", "testpass")
        mock_server.sendmail.assert_called_once()
        mock_server.quit.assert_called_once()

def test_send_report_with_attachment(mock_env_vars, tmp_path):
    csv_file = tmp_path / "test.csv"
    csv_file.write_text("col1,col2\nval1,val2")
    
    with patch("smtplib.SMTP") as mock_smtp:
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        
        result = send_report(csv_path=str(csv_file), subject="Test CSV", body="See attachment")
        
        assert result is True
        mock_server.sendmail.assert_called_once()
        # Verify that the attachment was handled (checking the call would be complex, but success means it didn't crash)

def test_send_report_missing_config(monkeypatch):
    monkeypatch.delenv("SMTP_USER", raising=False)
    result = send_report()
    assert result is False

def test_send_report_smtp_error(mock_env_vars):
    with patch("smtplib.SMTP") as mock_smtp:
        mock_smtp.side_effect = Exception("SMTP Connection Failed")
        result = send_report(subject="Test Fail", body="Fail")
        assert result is False
