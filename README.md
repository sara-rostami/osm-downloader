# OSM Downloader

ابزاری حرفه‌ای برای دانلود فایل کامل `.osm` یک محدوده جغرافیایی از OpenStreetMap با استفاده از Overpass API.

## ویژگی‌ها

- دریافت تمام نودها، راه‌ها و روابط درون یک bounding box
- خروجی به فرمت استاندارد OSM (XML)
- احترام به Rate Limit و معرفی User-Agent
- رابط خط فرمان با استفاده از Click
- اعتبارسنجی محدوده جغرافیایی

## نصب و راه‌اندازی

```bash
git clone https://github.com/yourusername/osm-downloader.git
cd osm-downloader
python -m venv venv
source venv/bin/activate   # (Linux/Mac) یا venv\Scripts\activate (Windows)
pip install -r requirements.txt
