# TikTok Ads Automation - دليل المشروع الشامل

## 1. فكرة المشروع (Project Concept)
هذا المشروع هو أداة متكاملة لأتمتة سحب البيانات (Web Scraping) من منصات إعلانات TikTok (TikTok Ads Manager). يهدف المشروع إلى توفير الوقت والجهد في مراقبة أداء الحملات الإعلانية من خلال استخراج البيانات بشكل دوري، تنظيمها في ملفات Excel، وإرسال تقارير تلقائية عبر البريد الإلكتروني.

---

## 2. الغرض من المشروع (Purpose)
الغرض الأساسي هو تحويل عملية مراقبة الإعلانات اليدوية إلى عملية تلقائية ذكية:
- **توفير الوقت:** بدلاً من الدخول اليومي وتحميل التقارير يدوياً.
- **الدقة:** تجنب الأخطاء البشرية في نقل البيانات.
- **المتابعة المستمرة:** الحصول على تحديثات دورية (كل 12 ساعة مثلاً) مباشرة في بريدك الإلكتروني.

---

## 3. الميزات الأساسية (Core Features)
- **تجاوز الحماية (Anti-Detection):** يستخدم تقنية `undetected-chromedriver` لتجنب اكتشاف البوتات من قبل تيك توك.
- **سحب بيانات متعدد المستويات:** يسحب بيانات (الحملات الإعلانية، المجموعات الإعلانية، والإعلانات الفردية).
- **التخصيص التلقائي للجداول:** يقوم البوت بضبط إعدادات الأعمدة (Core Metrics) داخل TikTok Ads Manager لضمان سحب البيانات المطلوبة فقط.
- **تصدير Excel:** يتم حفظ البيانات في ملفات Excel منظمة بترتيب زمني.
- **التقارير البريدية:** إرسال التقارير فور الانتهاء إلى البريد الإلكتروني المحدد.
- **الجدولة (Scheduling):** نظام مدمج للتشغيل التلقائي كل عدد معين من الساعات.

---

## 4. متطلبات التشغيل (Requirements)
- **لغة البرمجة:** Python 3.10+
- **المتصفح:** Google Chrome مثبت على الجهاز.
- **المكتبات الأساسية:**
  - `selenium` & `undetected-chromedriver` (للتحكم في المتصفح).
  - `pandas` & `openpyxl` (لمعالجة البيانات والـ Excel).
  - `python-dotenv` (لإدارة المتغيرات البيئية).
  - `click` (لواجهة سطر الأوامر).

---

## 5. خطوات التثبيت (Installation Guide)
1. **تحميل المشروع:** قم بتحميل الكود المصدري وفك الضغط عنه.
2. **إنشاء بيئة وهمية (اختياري ولكن مفضل):**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. **تثبيت المكتبات:**
   ```bash
   pip install -r requirements.txt
   ```
4. **فتح المتصفح يدوياً:** يجب فتح متصفح Chrome مرة واحدة لإنشاء ملف تعريف (Profile) والتأكد من تسجيل الدخول إلى تيك توك في المسار المحدد في `browser_manager.py`.

---

## 6. الإعدادات الضرورية (Configuration)
يتم التحكم في المشروع عبر ملف `.env`. يجب التأكد من وجود القيم التالية:
- `campains_url`: الرابط الأساسي للحملات.
- `adgroup_url`: الرابط الأساسي للمجموعات الإعلانية.
- `ad_url`: الرابط الأساسي للإعلانات.
- `smtp_host`, `smtp_port`, `smtp_user`, `smtp_password`: إعدادات خادم البريد (GMAIL مثلاً).
- `smtp_to`: الحساب الذي سيستلم التقارير.

---

## 7. طريقة التشغيل (How to Use)
### أ. التشغيل المباشر:
لتشغيل عملية السحب الآن:
```bash
python3 main.py
```

### ب. التشغيل المجدول:
لتشغيل الجدولة التلقائية (تتفحص كل 12 ساعة):
```bash
python3 scheduler.py
```

---

## 8. هيكل الملفات (File Structure)
```text
├── main.py             # الملف الرئيسي المتحكم في سير العمل
├── scrapper.py         # يحتوي على خوارزميات سحب البيانات من العناصر
├── browser_manager.py  # إدارة المتصفح والملحقات
├── mailer.py           # إدارة إرسال التقارير البريدية
├── logger.py           # نظام تسجيل الأحداث والأخطاء الموحد
├── scheduler.py        # إدارة التوقيت والتشغيل التكراري
├── log/                # مجلد يحتوي على ملفات السجل (logfile.log)
├── data/               # مجلد تخزين ملفات Excel الناتجة
└── .env                # ملف الإعدادات السرية
```

---

## 9. استكشاف الأخطاء وإصلاحها (Troubleshooting)
- **ModuleNotFoundError:** تأكد من تفعيل البيئة الوهمية وتثبيت `requirements.txt`.
- **Chrome Not Reachable:** تأكد من إغلاق جميع نوافذ Chrome التي قد تستخدم نفس الـ User Profile قبل البدء.
- **SMTP Authentication Error:** تأكد من تفعيل "App Passwords" في حساب Gmail إذا كنت تستخدمه.
- **TimeoutException:** قد يكون الإنترنت بطيئاً أو واجهة تيك توك قد تغيرت؛ تحقق من `logfile.log`.

---

## 10. أفضل الممارسات وحدود المشروع
- **أفضل الممارسات:** يفضل تشغيل السكربت على خادم (VPS) يعمل بنظام لينكس لضمان الاستمرارية.
- **الحدود:** المشروع مصمم لواجهة تيك توك الحالية؛ أي تغيير جذري في تصميم الموقع قد يتطلب تحديث الـ Selectors في `scrapper.py`.
- **الصيانة:** يوصى بتحديث `undetected-chromedriver` بانتظام لمواكبة تحديثات جوجل كروم.

---

**تم إعداد هذا الدليل لمساعدة المستخدمين والمطورين على البدء فوراً في استخدام المشروع بكفاءة.**

---

# TikTok Ads Automation - Comprehensive Project Guide

## 1. Project Concept
This project is an integrated tool for automating Web Scraping from TikTok Ads Manager. It aims to save time and effort in monitoring ad campaign performance by periodically extracting data, organizing it into Excel files, and sending automated reports via email.

---

## 2. Project Purpose
The primary purpose is to transform the manual ad monitoring process into a smart automated process:
- **Save Time:** Instead of daily manual logins and report downloads.
- **Accuracy:** Avoid human error in data entry.
- **Continuous Monitoring:** Get periodic updates (e.g., every 12 hours) directly in your email.

---

## 3. Core Features
- **Anti-Detection:** Uses `undetected-chromedriver` to avoid bot detection by TikTok.
- **Multi-Level Scraping:** Scrapes data for Campaigns, Ad Groups, and individual Ads.
- **Auto Table Customization:** The bot automatically adjusts column settings (Core Metrics) within TikTok Ads Manager to ensure only the required data is scraped.
- **Excel Export:** Data is saved in organized Excel files with timestamps.
- **Email Reporting:** Reports are sent immediately to the specified email upon completion.
- **Scheduling:** Built-in system for automatic execution every set number of hours.

---

## 4. Requirements
- **Language:** Python 3.10+
- **Browser:** Google Chrome installed.
- **Core Libraries:**
  - `selenium` & `undetected-chromedriver` (Browser control).
  - `pandas` & `openpyxl` (Data processing & Excel).
  - `python-dotenv` (Environment variables management).

---

## 5. Installation Guide
1. **Download Project:** Download and extract the source code.
2. **Create Virtual Environment (Optional but Recommended):**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Manual Browser Setup:** Open Chrome once to create a profile and ensure you are logged into TikTok at the path specified in `browser_manager.py`.

---

## 6. Necessary Configuration
The project is controlled via the `.env` file. Ensure the following values are set:
- `campains_url`: Primary campaign URL.
- `adgroup_url`: Primary ad group URL.
- `ad_url`: Primary ad URL.
- `smtp_host`, `smtp_port`, `smtp_user`, `smtp_password`: SMTP server settings (e.g., GMAIL).
- `smtp_to`: Recipient email address.

---

## 7. How to Use
### A. Direct Execution:
To start the scraping process immediately:
```bash
python3 main.py
```

### B. Scheduled Execution:
To run the automatic scheduler (checks every 12 hours):
```bash
python3 scheduler.py
```

---

## 8. File Structure
```text
├── main.py             # Main entry point for the workflow
├── scrapper.py         # Scraping algorithms and element selectors
├── browser_manager.py  # Browser and profile management
├── mailer.py           # Email report management
├── logger.py           # Unified logging system
├── scheduler.py        # Timing and repetitive execution management
├── log/                # Directory containing logs (logfile.log)
├── data/               # Directory for storing generated Excel files
└── .env                # Secret configuration file
```

---

## 9. Troubleshooting
- **ModuleNotFoundError:** Ensure the virtual environment is active and `requirements.txt` is installed.
- **Chrome Not Reachable:** Ensure all Chrome windows using the same User Profile are closed before starting.
- **SMTP Authentication Error:** Enable "App Passwords" in your Gmail account settings if applicable.
- **TimeoutException:** Likely due to slow internet or TikTok UI changes; check `logfile.log`.

---

## 10. Best Practices and Limitations
- **Best Practices:** It is recommended to run the script on a Linux VPS for continuity.
- **Limitations:** Designed for the current TikTok UI; major design changes might require updating selectors in `scrapper.py`.
- **Maintenance:** Regularly update `undetected-chromedriver` to match Google Chrome updates.

---

**This guide was prepared to help users and developers get started efficiently with the project.**
# TikTok_admanager_datascrap
