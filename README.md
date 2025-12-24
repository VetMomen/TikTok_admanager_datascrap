# TikTok Ads Manager Scraper

Automated tool to scrape campaign and ad group data from TikTok Ads Manager and email it as a CSV report.

## Setup

1. **Environment Variables**:
   Update the `.env` file with your SMTP credentials and preferred Chrome profile path.
   ```bash
   SMTP_HOST=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USER=your_email@gmail.com
   SMTP_PASS=your_app_password
   EMAIL_FROM=your_email@gmail.com
   EMAIL_TO=recipient_email@gmail.com
   CHROME_PROFILE_PATH="/home/mint/Share Point/Programming_Projects/Automation_first_steps/chrome_profile"
   ```

2. **Manual Login (First Time Only)**:
   TikTok requires manual login for the first time or if the session expires. Run:
   ```bash
   ./venv/bin/python run_tiktok_scraper.py --login
   ```
   A browser will open. Log in to TikTok Ads Manager manually, then press **Enter** in the terminal to close the browser. This saves your session.

## Usage

### Run Scraper
To run the scraper and send the email:
```bash
./venv/bin/python run_tiktok_scraper.py
```

### Scheduling (Cron)
To run every 12 hours, add this to your `crontab -e`:
```bash
0 */12 * * * cd "/home/mint/Share Point/Programming_Projects/TikTok_Ads_Automation" && ./venv/bin/python run_tiktok_scraper.py >> logs/cron.log 2>&1
```

## Project Structure
- `tiktok_scraper.py`: Core logic for browser automation.
- `mailer.py`: SMTP email sending module.
- `run_tiktok_scraper.py`: Main entry point and orchestrator.
- `data/`: Directory where CSV reports are saved.
- `logs/`: Scraper and orchestrator logs.
