import pytest
from tiktok_scraper import TikTokAdsScraper
from unittest.mock import patch, MagicMock
import os
import pandas as pd

@pytest.fixture
def scraper(mock_env_vars):
    return TikTokAdsScraper()

def test_scraper_init(scraper):
    assert scraper.profile_path == "/tmp/chrome_profile"
    assert scraper.ads_url == "https://ads.tiktok.com/test"

def test_save_to_csv(scraper, tmp_path, monkeypatch):
    # Mock 'data' directory creation or existence
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    
    # Temporarily change directory to tmp_path so it saves into the mock data dir
    monkeypatch.chdir(tmp_path)
    
    test_data = [{"Name": "Ad1", "Status": "Active", "Cost (التكلفة)": "100"}]
    csv_file = scraper.save_to_csv(test_data)
    
    assert csv_file is not None
    assert os.path.exists(csv_file)
    df = pd.read_csv(csv_file)
    assert df.iloc[0]["Name"] == "Ad1"

def test_save_to_csv_empty(scraper):
    result = scraper.save_to_csv([])
    assert result is None

@patch("undetected_chromedriver.Chrome")
@patch("tiktok_scraper.stealth")
def test_init_driver(mock_stealth, mock_chrome, scraper):
    scraper.init_driver(headless=True)
    assert scraper.driver is not None
    mock_chrome.assert_called_once()
    mock_stealth.assert_called_once()

@patch("tiktok_scraper.time.sleep", return_value=None)
def test_is_logged_in_true(mock_sleep, scraper):
    scraper.driver = MagicMock()
    scraper.driver.current_url = "https://ads.tiktok.com/i18n/dashboard"
    
    assert scraper.is_logged_in() is True
    scraper.driver.get.assert_called_with(scraper.ads_url)

@patch("tiktok_scraper.time.sleep", return_value=None)
def test_is_logged_in_false(mock_sleep, scraper):
    scraper.driver = MagicMock()
    scraper.driver.current_url = "https://ads.tiktok.com/i18n/login"
    
    assert scraper.is_logged_in() is False
