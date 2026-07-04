راهنمای راه‌اندازی ریپوزیتوری گیت برای پروژه PKI X.509
=========================================================

سلام! این فایل شامل تمام مراحل برای آماده‌کردن پروژه خود برای GitHub است.

📋 خلاصه آنچه آماده شده است:
================================

✅ README.md - توضیحات جامع پروژه
✅ .gitignore - فایل‌های که نباید کمیت شوند
✅ 8 کمیت حرفه‌ای و معنادار
✅ setup_git.bat - اسکریپت Windows
✅ setup_git.ps1 - اسکریپت PowerShell

🚀 نحوه اجرای تنظیمات:
========================

**بر روی Windows (گزینه 1 - Batch):**
1. فولدر پروژه را در Explorer باز کنید
2. روی setup_git.bat راست‌کلیک کنید
3. "Run with PowerShell" یا "Run as Administrator" را کلیک کنید
4. انتظار بکشید تا تمام کمیت‌ها انجام شوند

**بر روی PowerShell (گزینه 2 - توصیه شده):**
1. PowerShell را باز کنید (Windows PowerShell یا PowerShell 7+)
2. به فولدر پروژه بروید:
   cd "C:\Users\Nine\Downloads\git\PKI_X.509"

3. اجازه اجرای اسکریپت را دهید:
   Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process

4. اسکریپت را اجرا کنید:
   .\setup_git.ps1

5. گزینه‌ی [Y] را برای تایید کلیک کنید

⚠️ مهم - پیش از اجرا:
========================

اطمینان حاصل کنید که Git نصب است:
- برای بررسی: git --version را در PowerShell/CMD بنویسید
- اگر نصب نیست: https://git-scm.com/download/win را دانلود و نصب کنید

👤 تنظیم اطلاعات کاربری Git:
如果 اسکریپت به‌طور خودکار انجام نمی‌دهد، دستی اجرا کنید:

git config user.name "نام شما"
git config user.email "your.email@example.com"

📊 ساختار کمیت‌ها:
===================

این 8 کمیت، تطور منطقی پروژه را نشان می‌دهند:

1️⃣ Commit 1: Core Infrastructure
   - ساختار پایه‌ای و توابع کمکی
   - مسیرهای ذخیره‌سازی

2️⃣ Commit 2: Certificate Authority
   - ایجاد و تنظیم CA
   - تولید کلید RSA-3072
   - تنظیمات X.509

3️⃣ Commit 3: CSR Generation
   - تولید درخواست امضای گواهی
   - پشتیبانی SAN برای دامنه‌ها
   - تولید کلید‌های خصوصی

4️⃣ Commit 4: RA Approval Workflow
   - تایید درخواست‌ها
   - اعتبارسنجی هویت
   - ذخیره‌سازی ریکورد‌های تایید

5️⃣ Commit 5: CA Signing
   - امضای گواهی‌ها
   - تنظیمات دوره اعتبار
   - اضافه کردن اکسทنشن‌های X.509

6️⃣ Commit 6: EKU & Advanced Features
   - Extended Key Usage (EKU)
   - حفظ SAN اکسทنشن
   - تایید امضای RSA

7️⃣ Commit 7: Revocation & CRL
   - لغو گواهی‌ها
   - تولید CRL
   - مدیریت علل لغو

8️⃣ Commit 8: Documentation
   - README جامع
   - .gitignore برای فایل‌های تولید‌شده
   - دستورالعمل‌های کامل

🔄 چگونه به GitHub وصل کنید:
==============================

بعد از اجرای اسکریپت، مراحل زیر را انجام دهید:

1. یک ریپوزیتوری جدید بر روی GitHub ایجاد کنید:
   - به https://github.com/new بروید
   - نام ریپوزیتوری را وارد کنید (مثلاً: PKI_X.509)
   - "Public" یا "Private" را انتخاب کنید
   - "Create" را کلیک کنید

2. لینک ریپوزیتوری را کپی کنید (فرمت HTTPS یا SSH)

3. مراحل زیر را در PowerShell یا CMD اجرا کنید:

   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
   git branch -M main
   git push -u origin main

   توضیح:
   - YOUR_USERNAME را با نام‌کاربری GitHub خود جایگزین کنید
   - YOUR_REPO را با نام ریپوزیتوری خود جایگزین کنید

4. بعد از push، همه کمیت‌ها و توضیحات بر روی GitHub ظاهر می‌شوند!

✅ بررسی اینکه همه چیز درست است:
================================

بعد از Commit کردن، اجرا کنید:

git log --oneline

باید کمیت‌هایی مانند این جملات مشاهده کنید:
- feat: initial project structure with core infrastructure
- feat: add Certificate Authority (CA) creation functionality
- feat: implement CSR generation with SAN support
- feat: add RA certificate request approval process
- feat: implement certificate signing by CA
- feat: implement Extended Key Usage and advanced certificate features
- feat: implement certificate revocation and CRL management
- docs: add comprehensive README and project documentation

🔍 فایل‌های موجود:
===================

بعد از راه‌اندازی، فولدر پروژه شامل این موارد خواهد بود:

pki_lab.py .................. کد اصلی پروژه
README.md ................... توضیحات جامع
.gitignore ................. فایل‌های نادیده‌گیری
setup_git.bat .............. اسکریپت Windows Batch
setup_git.ps1 .............. اسکریپت PowerShell
.git/ ...................... فولدر git (نمایش‌داده نمی‌شود)

💡 نکات مهم:
=============

✓ تمام کمیت‌ها به‌صورت محلی ایجاد می‌شوند (push نمی‌شوند)
✓ فقط یک بار اسکریپت را اجرا کنید
✓ بعد از آن می‌توانید اضافه کمیت کنید: git commit -m "پیام"
✓ تمام کمیت‌ها یکجا به GitHub push می‌شوند

❓ مشکلات متداول:
==================

مشکل: "git: The term 'git' is not recognized"
حل: Git را نصب کنید: https://git-scm.com/download/win

مشکل: "Permission denied" هنگام اجرای اسکریپت
حل: PowerShell را "Run as Administrator" باز کنید

مشکل: "authentication failed" هنگام push
حل: Personal Access Token استفاده کنید:
     - به https://github.com/settings/tokens بروید
     - Token جدید بسازید
     - آن را در هنگام درخواست رمز برای push کپی کنید

📞 پیام نهایی:
==============

اسکریپت تمام مراحل را خودکار انجام می‌دهد!

1. تنها کاری که باید بکنید:
   - اسکریپت را اجرا کنید
   - منتظر تمام کمیت‌ها بمانید
   - یک ریپوزیتوری GitHub بسازید
   - دستورات git remote add و push را اجرا کنید

2. همه کمیت‌ها یکجا اضافه می‌شوند!

3. README توضیحات کامل پروژه را فراهم می‌کند

4. .gitignore تمام فایل‌های حساس را نادیده می‌گیرد

✨ اکنون آماده‌اید! موفق باشید! ✨

---

آخرین بروزرسانی: مهر 1405
