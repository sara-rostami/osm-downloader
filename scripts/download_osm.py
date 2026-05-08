#!/usr/bin/env python3
"""
دانلودر OSM برای اجرا در GitHub Actions
"""

import argparse
import sys
import os
import requests

# یک User-Agent معتبر برای احترام به قوانین اوپن‌استریت‌مپ
DEFAULT_USER_AGENT = "GitHubAction-OSMDownloader/1.0 (https://github.com/YOUR_USERNAME/REPO_NAME; your-email@example.com)"


def build_overpass_query(min_lon, min_lat, max_lon, max_lat):
    """
    ساخت کوئری Overpass QL برای دانلود تمام داده‌های یک محدوده
    مستطیلی (bounding box).
    """
    bbox = f"({min_lat},{min_lon},{max_lat},{max_lon})"
    query = f"""
    [out:xml][timeout:300];
    (
      node{bbox};
      way{bbox};
      relation{bbox};
    );
    out body;
    """
    return query


def download_osm_file(min_lon, min_lat, max_lon, max_lat, output_file):
    """ارسال درخواست به Overpass API و ذخیره خروجی."""
    query = build_overpass_query(min_lon, min_lat, max_lon, max_lat)

    # دریافت User-Agent از متغیر محیطی یا استفاده از مقدار پیش‌فرض
    user_agent = os.environ.get('OVERPASS_USER_AGENT', DEFAULT_USER_AGENT)
    headers = {'User-Agent': user_agent}

    print(f"[INFO] Sending request to Overpass API for bounding box: {min_lon}, {min_lat}, {max_lon}, {max_lat}")

    try:
        # ارسال درخواست POST به Overpass API
        response = requests.post(
            'https://overpass-api.de/api/interpreter',
            data={'data': query},
            headers=headers,
            timeout=300  # ۵ دقیقه زمان انتظار
        )
        response.raise_for_status()  # در صورت خطای HTTP (مثل ۴۰۰ یا ۵۰۰) خطا می‌دهد

        # ذخیره محتوای پاسخ در فایل
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(response.text)

        print(f"[SUCCESS] OSM data saved to {output_file}")
        return True

    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Failed to download data: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description='Download OSM data for a bounding box')
    parser.add_argument('--min-lon', type=float, required=True, help='Minimum longitude')
    parser.add_argument('--min-lat', type=float, required=True, help='Minimum latitude')
    parser.add_argument('--max-lon', type=float, required=True, help='Maximum longitude')
    parser.add_argument('--max-lat', type=float, required=True, help='Maximum latitude')

    args = parser.parse_args()

    # اعتبارسنجی ساده محدوده
    if not (-180 <= args.min_lon <= 180) or not (-180 <= args.max_lon <= 180):
        print("[ERROR] Longitude out of range (-180 to 180)")
        sys.exit(1)
    if not (-90 <= args.min_lat <= 90) or not (-90 <= args.max_lat <= 90):
        print("[ERROR] Latitude out of range (-90 to 90)")
        sys.exit(1)
    if args.min_lat >= args.max_lat or args.min_lon >= args.max_lon:
        print("[ERROR] Invalid bounding box: min > max")
        sys.exit(1)

    # مسیر فایل خروجی ثابت است تا آپلود آرتیفکت ساده شود
    output_file = "downloaded_data.osm"

    if download_osm_file(args.min_lon, args.min_lat, args.max_lon, args.max_lat, output_file):
        print("[INFO] Script finished successfully.")
    else:
        print("[ERROR] Script failed.")
        sys.exit(1)


if __name__ == "__main__":
    main()
