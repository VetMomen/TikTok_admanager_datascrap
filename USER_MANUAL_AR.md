# دليل استخدام سكربت أتمتة تقارير TikTok Ads Manager 📊

هذا السكربت مصمم لسحب بيانات الحملات (Campaigns) والمجموعات الإعلانية (Ad Groups) من TikTok Ads Manager بشكل آلي، وتصديرها كملف CSV، ثم إرسالها إلى بريدك الإلكتروني كل 12 ساعة.

---

## 🚀 الخطوة 1: إعداد البيئة والبيانات
يجب ضبط الإعدادات الأساسية في ملف `.env` ليعمل السكربت بشكل صحيح.

1. افتح ملف [.env](file:///home/mint/Share%20Point/Programming_Projects/Automation_first_steps/.env).
2. قم بتعبئة البيانات التالية:
   - **SMTP_USER**: بريدك الإلكتروني (الذي سيرسل التقارير).
   - **SMTP_PASS**: كلمة مرور التطبيقات (App Password) - *إذا كنت تستخدم Gmail، يجب إنشاء App Password من إعدادات حساب جوجل*.
   - **EMAIL_TO**: البريد الذي تود استقبال التقارير عليه.
   - **CHROME_PROFILE_PATH**: اترك المسار كما هو إلا إذا أردت تغييره، هذا المجلد سيحفظ جلسة دخولك.

---

## 🔑 الخطوة 2: تسجيل الدخول (للمرة الأولى فقط)
بما أن تيك توك لديه حماية قوية، نحتاج لتسجيل الدخول يدويًا "مرة واحدة" لحفظ الجلسة.

1. افتح الطرفية (Terminal) في مجلد المشروع.
2. قم بتشغيل الأمر التالي:
   ```bash
   ./venv/bin/python run_tiktok_scraper.py --login
   ```
3. ستفتح نافذة متصفح Chrome. قم بتسجيل الدخول إلى حساب TikTok Ads Manager الخاص بك بشكل طبيعي.
4. بعد الدخول وظهور جدول الحملات، ارجع إلى الطرفية واضغط **Enter**.
5. سيتم إغلاق المتصفح وحفظ الجلسة بنجاح.

---

## 📈 الخطوة 3: تشغيل السكربت يدويًا
للتأكد من أن كل شيء يعمل (سحب البيانات + إرسال الإيميل)، شغّل السكربت بدون أي إضافات:

```bash
./venv/bin/python run_tiktok_scraper.py
```

- سيقوم السكربت بفتح المتصفح (في الخلفية أو بشكل مرئي حسب الإعداد)، سحب البيانات، وحفظها في مجلد `data/`.
- سيصلك إيميل يحتوي على ملف الـ CSV.

---

## ⏰ الخطوة 4: الجدولة الآلية (كل 12 ساعة)
لجعل السكربت يعمل تلقائيًا مرتين في اليوم على نظام Linux:

1. اكتب في الطرفية: `crontab -e`.
2. في نهاية الملف، أضف السطر التالي (تأكد من تعديل المسارات إذا لزم الأمر):
   ```bash
   0 */12 * * * cd "/home/mint/Share Point/Programming_Projects/Automation_first_steps" && ./venv/bin/python run_tiktok_scraper.py >> logs/cron.log 2>&1
   ```
3. احفظ واخرج. الآن سيعمل السكربت كل 12 ساعة تلقائيًا.

---

### 3. أنواع التقارير المتاحة
السكربت الآن يدعم استخراج التقارير لفترات زمنية مختلفة آلياً:

*   **تقرير يومي (Daily):** يأتي بنتائج يوم أمس فقط.
    ```bash
    ./venv/bin/python run_tiktok_scraper.py --type daily
    ```
*   **تقرير 3 أيام (3-Day):** نتائج آخر 3 أيام تراكمياً.
    ```bash
    ./venv/bin/python run_tiktok_scraper.py --type 3days
    ```
*   **تقرير أسبوعي (Weekly):** نتائج آخر 7 أيام.
    ```bash
    ./venv/bin/python run_tiktok_scraper.py --type weekly
    ```
*   **تقرير شهري (Monthly):** نتائج آخر 30 يوم.
    ```bash
    ./venv/bin/python run_tiktok_scraper.py --type monthly
    ```

### 4. الجدولة التلقائية (Cron Job)
لإرسال التقارير بشكل آلي في مواعيد محددة، قم بفتح محرر الجدولة:
```bash
crontab -e
```

ثم أضف الأسطر التالية (تأكد من تعديل المسارات للمسار الكامل للمشروع):

```cron
# تقرير يومي الساعة 9 صباحاً (لنتائج أمس)
0 9 * * * /home/mint/Share\ Point/Programming_Projects/Automation_first_steps/venv/bin/python /home/mint/Share\ Point/Programming_Projects/Automation_first_steps/run_tiktok_scraper.py --type daily

# تقرير كل 3 أيام الساعة 9:05 صباحاً
5 9 */3 * * /home/mint/Share\ Point/Programming_Projects/Automation_first_steps/venv/bin/python /home/mint/Share\ Point/Programming_Projects/Automation_first_steps/run_tiktok_scraper.py --type 3days

# تقرير أسبوعي كل يوم اثنين الساعة 9:10 صباحاً
10 9 * * 1 /home/mint/Share\ Point/Programming_Projects/Automation_first_steps/venv/bin/python /home/mint/Share\ Point/Programming_Projects/Automation_first_steps/run_tiktok_scraper.py --type weekly

# تقرير شهري يوم 1 من كل شهر الساعة 9:15 صباحاً
15 9 1 * * /home/mint/Share\ Point/Programming_Projects/Automation_first_steps/venv/bin/python /home/mint/Share\ Point/Programming_Projects/Automation_first_steps/run_tiktok_scraper.py --type monthly
```

---

## الملاحظات الهامة
*   **بيانات الدخول:** يجب تشغيل السكربت بخيار `--login` مرة واحدة على الأقل أو في حال تعطل الجلسة.
*   **الإحصائيات:** السكربت يركز الآن على (التكلفة، CPM، النتائج، تكلفة النتيجة، CTR).
*   **التواريخ:** السكربت يقوم بتحديث التواريخ في الرابط آلياً بناءً على نوع التقرير.

## 📁 هيكل المشروع
- `data/`: يحتوي على ملفات التقرير (يتم الاحتفاظ بآخر 30 يوم فقط).
- `logs/`: يحتوي على ملفات السجل (Logs) لمتابعة العمليات أو تشخيص الأخطاء.
- `run_tiktok_scraper.py`: الملف الرئيسي للتشغيل.

---

## 🛠️ استكشاف الأخطاء وإصلاحها
- **فشل تسجيل الدخول**: إذا وصلك إيميل بعنوان "Login Required"، كرر الخطوة رقم 2.
- **تنبيه خطأ بالبريد**: إذا واجه السكربت مشكلة تقنية، سيرسل لك إيميل يحتوي على تفاصيل الخطأ (Error Message).
- **تحديث المكتبات**: إذا توقف السكربت بعد فترة، قد تحتاج لتحديث متصفح Chrome أو مكتبة `undetected-chromedriver`.

---
*تم إعداد هذا السكربت بواسطة Antigravity لمساعدتك في أتمتة أعمالك.* 🚀
