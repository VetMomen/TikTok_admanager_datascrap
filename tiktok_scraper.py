import os
import time
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
import undetected_chromedriver as uc
from selenium_stealth import stealth
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/scraper.log"),
        logging.StreamHandler()
    ]
)

load_dotenv()

class TikTokAdsScraper:
    def __init__(self):
        self.profile_path = os.getenv("CHROME_PROFILE_PATH")
        self.ads_url = os.getenv("TIKTOK_ADS_URL", "https://ads.tiktok.com/business/Redirect?to=/campaign")
        self.driver = None

    def init_driver(self, headless=False):
        """Initializes the undetected chromedriver."""
        options = uc.ChromeOptions()
        if headless:
            options.add_argument("--headless")
        
        # User Data Directory to persist session
        if self.profile_path:
            options.add_argument(f"--user-data-dir={self.profile_path}")
            options.add_argument("--profile-directory=Default")

        # Disable automation detection
        options.add_argument("--disable-blink-features=AutomationControlled")
        
        # Disable protocol handler popups (like "wants to open this application")
        prefs = {
            "protocol_handler.allowed_origin_protocol_pairs": {
                "https://ads.tiktok.com": {
                    "af-open": True,
                    "tiktok": True,
                    "ms-windows-store": True
                }
            },
            "protocol_handler.excluded_schemes": {
                "af-open": True,
                "tiktok": True,
                "ms-windows-store": True,
                "mailto": True,
                "tel": True
            },
            "profile.default_content_setting_values.notifications": 2,
        }
        options.add_experimental_option("prefs", prefs)

        try:
            self.driver = uc.Chrome(options=options)
            
            # Apply selenium-stealth to further hide automation
            stealth(self.driver,
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True,
            )
            logging.info("Driver initialized successfully.")
        except Exception as e:
            logging.error(f"Failed to initialize driver: {e}")
            raise

    def is_logged_in(self):
        """Checks if the user is currently logged in by looking for common dashboard elements."""
        logging.info(f"Checking login status via: {self.ads_url}")
        self.driver.get(self.ads_url)
        time.sleep(10) # Give it more time to resolve
        # If we are redirected to a login page or see a login button, we are not logged in
        if "login" in self.driver.current_url.lower() or "signup" in self.driver.current_url.lower():
            logging.warning("Redirected to login/signup page. Session might be expired.")
            return False
        return True

    def login_manual(self):
        """Opens the login page and waits for user to log in manually."""
        logging.info("Opening TikTok Ads Manager for manual login...")
        self.driver.get("https://ads.tiktok.com/i18n/login")
        logging.info("Please log in manually in the browser window.")
        input(">>> Press Enter here AFTER you have logged in and can see your campaigns table...")
        if self.is_logged_in():
            logging.info("Successfully verified login session.")
        else:
            logging.error("Failed to verify login session. Please try again.")

    def close_popups(self):
        """Detects and closes common TikTok Ads Manager pop-ups."""
        popups = [
            # NUX Popovers (New User Experience)
            "//button[contains(@data-testid, 'ks-nux-popover-index-aunGbQ')]",
            # Copilot Popover "Not now"
            "//button[contains(@data-testid, 'common-copilot-reporting-popover-3T98jG')]",
            # General Close buttons inside KS popovers
            "//div[contains(@class, 'ks-nux-popover')]//button",
            # "Not now" or "Close" text-based buttons
            "//*[text()='Not now']",
            "//*[text()='Got it']",
        ]
        
        for xpath in popups:
            try:
                elements = self.driver.find_elements(By.XPATH, xpath)
                for el in elements:
                    if el.is_displayed():
                        logging.info(f"Closing pop-up: {xpath}")
                        el.click()
                        time.sleep(1)
            except Exception:
                pass

    def navigate_to_campaigns(self):
        """Navigates to the campaigns page."""
        logging.info(f"Navigating to Campaigns: {self.ads_url}")
        self.driver.get(self.ads_url)
        self.close_popups()
        self._wait_for_table()

    def navigate_to_ad_groups(self):
        """Navigates to the Ad Groups tab."""
        logging.info("Switching to Ad Groups tab...")
        try:
            # Based on user recording: data-testid='tab-index-nRwmKw-ad' (Commonly used for Ad Group level)
            ad_group_tab = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//*[@data-testid='tab-index-nRwmKw-ad']"))
            )
            ad_group_tab.click()
            time.sleep(2)
            self.close_popups()
            self._wait_for_table()
        except Exception as e:
            logging.error(f"Failed to switch to Ad Group tab: {e}")

    def navigate_to_ads(self):
        """Navigates to the Ads tab."""
        logging.info("Switching to Ads tab...")
        try:
            # Based on user recording: data-testid='tab-index-nRwmKw-creative'
            ads_tab = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//*[@data-testid='tab-index-nRwmKw-creative']"))
            )
            ads_tab.click()
            time.sleep(2)
            self.close_popups()
            self._wait_for_table()
        except Exception as e:
            logging.error(f"Failed to switch to Ads tab: {e}")

    def _wait_for_table(self):
        """Generic wait for table or data rows."""
        logging.info("Waiting for table content to appear...")
        for _ in range(5): # Try 5 times with pop-up closing in between
            try:
                # Wait for either a table or a common div row class
                WebDriverWait(self.driver, 15).until(
                    EC.presence_of_element_located((By.XPATH, "//table | //div[contains(@id, 'manage')]//div[contains(@class, 'table-row')] | //div[contains(@class, 'vx-table-row')]"))
                )
                logging.info("Table content found.")
                time.sleep(5) # Final render wait
                return
            except Exception:
                logging.info("Table not found yet, checking for pop-ups...")
                self.close_popups()
                time.sleep(2)
        
        logging.error("Timed out waiting for table content.")
        self.driver.save_screenshot(f"logs/timeout_{datetime.now().strftime('%H%M%S')}.png")

    def scrape_table(self, level="Campaign"):
        """Specific scraper for TikTok Ads Manager tables."""
        logging.info(f"Scraping {level} table...")
        rows_data = []
        try:
            # Row selector based on provided HTML
            rows = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'row-item')]")
            
            if not rows:
                logging.warning(f"No rows found for {level}. Checking for alternative selectors...")
                rows = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'vx-table-row')] | //tr")

            logging.info(f"Found {len(rows)} rows.")

            for row in rows:
                try:
                    # Specific selectors based on user's HTML input
                    name_el = row.find_elements(By.XPATH, ".//span[contains(@class, 'item-content')]")
                    status_el = row.find_elements(By.XPATH, ".//div[contains(@class, 'primary-status')]//span")
                    
                    if not name_el: continue # Skip if no name (could be a summary row)
                    
                    data = {
                        "Run Date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "Level": level,
                        "Name": name_el[0].text.strip(),
                        "Status": status_el[0].text.strip() if status_el else "N/A",
                    }

                    # Map metrics using the 'prop' attribute in the HTML
                    # Focusing on user's requested metrics:
                    # 1- التكلفة (Cost), 2- CPM, 3- النتايج (Results), 4- تكلفة النتيجة (CPA), 5- CTR
                    metrics_map = {
                        "Cost (التكلفة)": "stat_cost",
                        "CPM": "cpm",
                        "Results (النتائج)": "time_attr_convert_cnt",
                        "Cost per Result (تكلفة النتيجة)": "time_attr_conversion_cost",
                        "CTR": "ctr"
                    }

                    for label, prop_val in metrics_map.items():
                        metric_el = row.find_elements(By.XPATH, f".//div[@prop='{prop_val}']//span")
                        data[label] = metric_el[0].text.strip() if metric_el else "0"

                    rows_data.append(data)
                except Exception as row_err:
                    logging.debug(f"Row skip error: {row_err}")
            
            logging.info(f"Successfully scraped {len(rows_data)} rows from {level}.")
            return rows_data
        except Exception as e:
            logging.error(f"Error during scraping {level}: {e}")
            return []


    def save_to_csv(self, data):
        """Saves the scraped data to a CSV file."""
        if not data:
            logging.warning("No data to save.")
            return None
        
        df = pd.DataFrame(data)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        filename = f"data/tiktok_ads_report_{timestamp}.csv"
        df.to_csv(filename, index=False)
        logging.info(f"Data saved to {filename}")
        return filename

    def close(self):
        """Closes the driver."""
        if self.driver:
            self.driver.quit()
            logging.info("Driver closed.")

if __name__ == "__main__":
    scraper = TikTokAdsScraper()
    try:
        scraper.init_driver()
        # For the first run, uncomment scraper.login_manual()
        # scraper.login_manual() 
        scraper.navigate_to_campaigns()
        data = scraper.scrape_data()
        scraper.save_to_csv(data)
    finally:
        scraper.close()
