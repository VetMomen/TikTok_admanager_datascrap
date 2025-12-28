import time
import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
import os
from dotenv import load_dotenv
from browser_manager import run_chrome
from scrapper import campaigns_scrapper, close_notification
import pandas as pd
from datetime import datetime
import openpyxl
from selenium.webdriver.common.by import By
from mailer import tiktok_sd_mail
from logger import setup_logger

logger = setup_logger("main")

load_dotenv()

tiktok_campaign_url = f"{os.getenv('campains_url')}&{os.getenv('yesterday_suffix')}"
tiktok_adgroup_url = f"{os.getenv('adgroup_url')}&{os.getenv('yesterday_suffix')}"
tiktok_ad_url = f"{os.getenv('ad_url')}&{os.getenv('yesterday_suffix')}"

logger.info("Environment variables loaded.")


def start_chrome():
    logger.info("Starting the TikTok automation process.")
    driver = None
    try:
        driver = run_chrome()
        if not driver:
            logger.error("Failed to initialize Chrome driver.")
            return

        driver.get("about:blank")
        time.sleep(2)

        # Scrap Campaigns
        logger.info(f"Navigating to campaign URL: {tiktok_campaign_url}")
        driver.get(tiktok_campaign_url)

        logger.info("Waiting for the campaign table to load.")
        # time.sleep(15000)
        try:
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".pt-header"))
            )
            logger.info("Campaign table page opened successfully.")
        except TimeoutException:
            logger.error("Timed out waiting for the campaign table to appear.")

        logger.info("Customizing table columns (Core Metrics)...")
        eclick = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "div.table-customization-text > div")
            )
        )
        time.sleep(1)
        eclick.click()

        eclick = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (
                    By.CSS_SELECTOR,
                    "div:nth-of-type(3) [data-testid='customization-customize-columns-5UHdhV'] > span",
                )
            )
        )
        time.sleep(1)
        eclick.click()

        eclick = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (
                    By.CSS_SELECTOR,
                    "[data-testid='common-metrics-select-panel-dSP5QH']",
                )
            )
        )
        time.sleep(1)
        eclick.click()

        eclick = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (
                    By.CSS_SELECTOR,
                    "[data-testid='message-box-main-bAxqDR'] > span",
                )
            )
        )
        time.sleep(1)
        eclick.click()

        eclick = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (
                    By.CSS_SELECTOR,
                    "[data-testid='common-metrics-select-area-pSAFdS-2'] [data-testid='common-metrics-select-area-eGTnDd'] > span.vi-checkbox__input > span",
                )
            )
        )
        time.sleep(1)
        eclick.click()

        eclick = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (
                    By.CSS_SELECTOR,
                    "[data-testid='common-custom-columns-modal-b9GZsJ'] > span",
                )
            )
        )
        time.sleep(1)
        eclick.click()

        logger.info("Core Metrics selected successfully.")

        logger.info("Waiting for the table to fully reload after customization.")
        try:
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".pt-header"))
            )
            logger.info("Table reloaded.")
        except TimeoutException:
            logger.error("Timed out waiting for the table to reload.")

        try:
            campaign_data = campaigns_scrapper(driver)
            logger.info("Campaign data scraped.")
        except Exception as e:
            logger.error(f"Failed to scrap campaign data: {e}")
            campaign_data = pd.DataFrame()  # Avoid unbound local error

        time.sleep(2)

        # scrap Ad groups
        logger.info(f"Navigating to Ad Group URL: {tiktok_adgroup_url}")
        driver.get(tiktok_adgroup_url)
        try:
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".pt-header"))
            )
            logger.info("Ad Group table loaded.")
        except TimeoutException:
            logger.error("Timed out waiting for Ad Group table.")

        adGroup_data = campaigns_scrapper(driver)
        logger.info("Ad Group data scraped.")
        time.sleep(2)

        # scrap Ads
        logger.info(f"Navigating to Ads URL: {tiktok_ad_url}")
        driver.get(tiktok_ad_url)

        try:
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".pt-header"))
            )
            logger.info("Ads table loaded.")
        except TimeoutException:
            logger.error("Timed out waiting for Ads table.")

        ad_data = campaigns_scrapper(driver)
        logger.info("Ads data scraped.")

        time.sleep(2)

        # Saving Data
        logger.info("Saving scraped data to Excel file.")
        dataFile_dir = os.path.join(os.getcwd(), "data")
        os.makedirs(dataFile_dir, exist_ok=True)

        now_time = datetime.now().strftime("%d%m%y")
        data_file = os.path.join(dataFile_dir, f"tiktok_scraped_data_{now_time}.xlsx")

        try:
            with pd.ExcelWriter(data_file) as writer:
                campaign_data.to_excel(writer, sheet_name="campaigns", index=False)
                adGroup_data.to_excel(writer, sheet_name="ad_groups", index=False)
                ad_data.to_excel(writer, sheet_name="ads", index=False)
            logger.info(f"Data saved successfully to {data_file}")

            logger.info("Initiating email report sending.")
            tiktok_sd_mail(data_file, datetime.now())
        except Exception as e:
            logger.error(f"Error while saving data or sending mail: {e}")

    except Exception as e:
        logger.error(f"An unexpected error occurred in the automation process: {e}")

    finally:
        logger.info("Closing Chrome browser.")
        if driver:
            driver.quit()


if __name__ == "__main__":
    start_chrome()
