import logging
import os
import time
from tiktok_scraper import TikTokAdsScraper
from mailer import send_report
from datetime import datetime, timedelta
import re

# Set up logging for the main orchestrator
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/orchestrator.log"),
        logging.StreamHandler()
    ]
)

import argparse

def cleanup_old_reports(directory="data", days=30):
    """
    Deletes files older than N days in the specified directory.
    """
    if not os.path.exists(directory):
        return
    now = time.time()
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            if os.stat(filepath).st_mtime < now - (days * 86400):
                os.remove(filepath)
                logging.info(f"Deleted old report: {filename}")

def main():
    parser = argparse.ArgumentParser(description="TikTok Ads Scraper")
    parser.add_argument("--login", action="store_true", help="Manual login mode to save session")
    parser.add_argument(
        "--type", 
        choices=["daily", "3days", "weekly", "monthly"], 
        default="daily", 
        help="Type of report to generate (default: daily)"
    )
    args = parser.parse_args()

    scraper = TikTokAdsScraper()
    csv_file = None
    
    try:
        logging.info(f"Starting TikTok Ads Scraper Orchestrator (Type: {args.type})...")
        
        # Calculate Date Range based on report type
        today = datetime.now()
        yesterday = today - timedelta(days=1)
        
        if args.type == "daily":
            st_date = yesterday.strftime("%Y-%m-%d")
            et_date = yesterday.strftime("%Y-%m-%d")
            report_label = "Daily (Yesterday)"
            relative_time = "1" # Yesterday
        elif args.type == "3days":
            st_date = (today - timedelta(days=3)).strftime("%Y-%m-%d")
            et_date = yesterday.strftime("%Y-%m-%d")
            report_label = "3-Day (Average)"
            relative_time = "3" 
        elif args.type == "weekly":
            st_date = (today - timedelta(days=7)).strftime("%Y-%m-%d")
            et_date = yesterday.strftime("%Y-%m-%d")
            report_label = "Weekly (Last 7 Days)"
            relative_time = "4" # Usually 7 days
        elif args.type == "monthly":
            st_date = (today - timedelta(days=30)).strftime("%Y-%m-%d")
            et_date = yesterday.strftime("%Y-%m-%d")
            report_label = "Monthly (Last 30 Days)"
            relative_time = "5" # Usually 30 days
        
        # Inject dates and relative_time into the URL
        if "st=" in scraper.ads_url and "et=" in scraper.ads_url:
            scraper.ads_url = re.sub(r"st=\d{4}-\d{2}-\d{2}", f"st={st_date}", scraper.ads_url)
            scraper.ads_url = re.sub(r"et=\d{4}-\d{2}-\d{2}", f"et={et_date}", scraper.ads_url)
            scraper.ads_url = re.sub(r"relative_time=\d+", f"relative_time={relative_time}", scraper.ads_url)
            logging.info(f"URL updated: {st_date} to {et_date} (relative_time={relative_time})")

        # Initialize driver
        scraper.init_driver(headless=False)
        
        if args.login:
            scraper.login_manual()
            return

        # Verify login session
        if not scraper.is_logged_in():
            logging.error("Not logged in. Please run with --login flag first.")
            send_report(
                subject=f"TikTok Ads Scraper - Login Required ({args.type})",
                body="The scraper could not detect an active session. Please run the script manually with the --login flag."
            )
            return

        # Scrape all levels
        scraper.navigate_to_campaigns()
        campaign_data = scraper.scrape_table(level="Campaign")
        
        scraper.navigate_to_ad_groups()
        adgroup_data = scraper.scrape_table(level="AdGroup")
        
        scraper.navigate_to_ads()
        ads_data = scraper.scrape_table(level="Ads")
        
        all_data = campaign_data + adgroup_data + ads_data
        
        if all_data:
            csv_file = scraper.save_to_csv(all_data)
            logging.info(f"Scraping completed. File: {csv_file}")

            # Send Email
            if csv_file and os.path.exists(csv_file):
                timestamp = today.strftime("%Y-%m-%d")
                subject = f"TikTok Ads {report_label} Report - {timestamp}"
                body = f"Please find the attached {report_label} report for TikTok Ads.\nDate Range: {st_date} to {et_date}"
                success = send_report(csv_file, subject, body)
                if success:
                    logging.info(f"{report_label} report emailed successfully.")
                else:
                    logging.error(f"Failed to email {report_label} report.")
        else:
            logging.warning(f"No data was scraped for {report_label}. Check session or date range.")
            
    except Exception as e:
        error_msg = f"An error occurred during {args.type} scraping: {str(e)}"
        logging.critical(error_msg)
        send_report(
            subject=f"TikTok Ads Scraper FAILED - {args.type}",
            body=f"The script encountered an error during {args.type} report run:\n\n{error_msg}"
        )
    finally:
        scraper.close()
        cleanup_old_reports()
        logging.info("Orchestrator finished.")

if __name__ == "__main__":
    main()
