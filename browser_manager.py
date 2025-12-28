import time
import undetected_chromedriver as uc
import os
from dotenv import load_dotenv

from logger import setup_logger

logger = setup_logger(__name__)

# استيراد متغيرات البيئة
load_dotenv()
tiktok_campaign_url = os.getenv("campains_url")

if not tiktok_campaign_url:
    logger.error("الرابط غير موجود في البيئة، رجاء اضافته أولا!")
    raise Exception("الرابط غير موجود في البيئة، رجاء اضافته أولا!")


def run_chrome():
    try:
        logger.info("Initializing Chrome browser with custom profile.")
        # اضافة خيارات التشغيل
        options = uc.ChromeOptions()

        # إنشاء ملف جوجل كروم محلي لتخزين الجلسات
        chrome_profile = "/home/mint/Share Point/Programming_Projects/TikTok_Automation_manual/chrome_profile"
        os.makedirs(chrome_profile, exist_ok=True)

        # تحديد ملف جوجل كروم ثابت
        options.add_argument(f"--user-data-dir={chrome_profile}")
        options.add_argument("--profile-directory=Default")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--disable-infobars")
        options.add_experimental_option(
            "prefs", {"profile.default_content_setting_values.notifications": 2}
        )
        options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument(
            "--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
        )

        # فتح الـ متصفح
        driver = uc.Chrome(options=options, use_subprocess=True)
        logger.info("Chrome browser started successfully.")
        return driver
    except Exception as e:
        logger.error(f"Failed to start Chrome: {e}")
        return None
