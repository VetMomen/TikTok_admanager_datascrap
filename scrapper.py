import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import pandas as pd
import os
from datetime import datetime


from logger import setup_logger

logger = setup_logger(__name__)


def campaigns_scrapper(driver):
    logger.info("Starting to scrap campaign data from the table.")
    campaign_row_data = []
    try:
        table_header = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".pt-header"))
        )
        header_cells = table_header.find_elements(By.CSS_SELECTOR, ".header-cell-wrapper")
        header = [cell.text for cell in header_cells]
        logger.info(f"Table headers found: {header}")

        table_rows = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "div.row.row-item.flex.bg-white")
            )
        )
        logger.info(f"Found {len(table_rows)} rows in the table.")
        
        for row in table_rows:
            cells = row.find_elements(By.CSS_SELECTOR, ".pt-cell.content-cell")
            campaign_row_data.append([cell.text for cell in cells[3:]])
        
        scraped_data = pd.DataFrame(campaign_row_data, columns=header)
        logger.info("Successfully scraped and processed table data.")
        return scraped_data
    except Exception as e:
        logger.error(f"Error during scraping: {e}")
        raise


def close_notification(driver, timeout=50):
    logger.info("Attempting to close notification popover using JavaScript.")
    try:
        # استخدام JavaScript للوصول إلى العنصر داخل shadowRoot
        close_button = driver.execute_script(
            """
            const host = document.querySelector('ks-nux-popover-dyo6q65e');
            if (host && host.shadowRoot) {
                return host.shadowRoot.querySelector('[data-testid="ks-nux-popover-index-aunGbQ"]');
            }
            return null;
        """
        )

        if close_button:
            close_button.click()
            logger.info("Successfully closed the notification popover.")
        else:
            logger.info("Notification popover not found.")

    except Exception as e:
        logger.error(f"Error while attempting to close notification: {e}")
