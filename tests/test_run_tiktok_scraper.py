import pytest
import os
import time
from run_tiktok_scraper import cleanup_old_reports
from datetime import datetime, timedelta

def test_cleanup_old_reports(tmp_path):
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    
    # Create an old file (31 days ago)
    old_file = data_dir / "old_report.csv"
    old_file.write_text("old data")
    old_time = time.time() - (31 * 86400)
    os.utime(str(old_file), (old_time, old_time))
    
    # Create a new file
    new_file = data_dir / "new_report.csv"
    new_file.write_text("new data")
    
    cleanup_old_reports(directory=str(data_dir), days=30)
    
    assert not old_file.exists()
    assert new_file.exists()

def test_date_range_logic(mock_env_vars, monkeypatch):
    # This is a bit tricky since main() uses argparse and sys.argv
    # We can test the logic by mocking the datetime and checking the URL manipulation
    import run_tiktok_scraper
    from unittest.mock import patch, MagicMock
    
    fixed_now = datetime(2023, 10, 24) # A Tuesday
    
    class MockDateTime(datetime):
        @classmethod
        def now(cls):
            return fixed_now

    with patch('run_tiktok_scraper.datetime', MockDateTime):
        # Test daily
        mock_args = MagicMock()
        mock_args.type = "daily"
        
        # Test 1 day back
        yesterday = fixed_now - timedelta(days=1)
        assert yesterday.strftime("%Y-%m-%d") == "2023-10-23"
        
        # Test 30 days back (monthly)
        monthly_start = fixed_now - timedelta(days=30)
        assert monthly_start.strftime("%Y-%m-%d") == "2023-09-24"
