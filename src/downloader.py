"""
ماژول دانلودر OSM با استفاده از Overpass API
"""

import time
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Optional, Tuple

import overpy
import requests

# برای احترام به rate limit و تشخیص کاربر
USER_AGENT = "OSM-Downloader/0.1 (https://github.com/yourusername/osm-downloader; your-email@example.com)"


class OSMOverpassDownloader:
    """دانلود داده‌های خام OSM از یک محدوده مستطیلی (bounding box)"""

    def __init__(self, user_agent: str = USER_AGENT):
        self.api = overpy.Overpass(url="https://overpass-api.de/api/interpreter")
        self.api.user_agent = user_agent
        self.user_agent = user_agent

    def _build_bbox_query(self, min_lat: float, min_lon: float, max_lat: float, max_lon: float) -> str:
        """
        ساخت پرس‌وجوی Overpass QL برای دریافت همه چیز داخل یک bounding box.
        این کوئری تمام نودها، راه‌ها و روابط داخل محدوده را می‌گیرد.
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

    def download_as_xml(self, min_lat: float, min_lon: float, max_lat: float, max_lon: float) -> str:
        """
        ارسال درخواست به Overpass API و برگرداندن رشته XML خام (فرمت OSM)
        """
        query = self._build_bbox_query(min_lat, min_lon, max_lat, max_lon)
        print(f"[INFO] ارسال درخواست به Overpass API با محدوده: {min_lat},{min_lon} تا {max_lat},{max_lon}")
        print("[INFO] لطفاً صبر کنید... دانلود ممکن است چند لحظه طول بکشد.")

        # استفاده از requests مستقیم برای کنترل بیشتر
        headers = {"User-Agent": self.user_agent}
        response = requests.post(
            "https://overpass-api.de/api/interpreter",
            data={"data": query},
            headers=headers,
            timeout=300,
        )
        response.raise_for_status()  # خطا اگر وضعیت HTTP ناموفق باشد
        return response.text

    def save_osm_file(self, xml_content: str, output_path: Path) -> None:
        """
        ذخیره محتوای XML در یک فایل با پسوند .osm
        """
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(xml_content)
        print(f"[SUCCESS] فایل OSM ذخیره شد: {output_path}")

    def validate_bbox(self, min_lat: float, min_lon: float, max_lat: float, max_lon: float) -> Tuple[bool, Optional[str]]:
        """اعتبارسنجی ساده محدوده جغرافیایی"""
        if not (-90 <= min_lat <= 90) or not (-90 <= max_lat <= 90):
            return False, "عرض جغرافیایی باید بین -90 و 90 باشد"
        if not (-180 <= min_lon <= 180) or not (-180 <= max_lon <= 180):
            return False, "طول جغرافیایی باید بین -180 و 180 باشد"
        if min_lat >= max_lat:
            return False, "min_lat باید کوچکتر از max_lat باشد"
        if min_lon >= max_lon:
            return False, "min_lon باید کوچکتر از max_lon باشد"
        # هشدار برای محدوده خیلی بزرگ (بیش از 0.5 درجه تقریباً 50 کیلومتر)
        if (max_lat - min_lat) > 1.0 or (max_lon - min_lon) > 1.0:
            print("[WARNING] محدوده بزرگ است – ممکن است زمان دانلود طولانی شود یا Overpass API خطای timeout بدهد.")
        return True, None


# اگر بخواهیم از خط فرمان استفاده کنیم (با click)
import click

@click.command()
@click.option("--min-lat", required=True, type=float, help="عرض جغرافیایی جنوبی")
@click.option("--min-lon", required=True, type=float, help="طول جغرافیایی غربی")
@click.option("--max-lat", required=True, type=float, help="عرض جغرافیایی شمالی")
@click.option("--max-lon", required=True, type=float, help="طول جغرافیایی شرقی")
@click.option("--output", "-o", default="download.osm", type=click.Path(), help="مسیر فایل خروجی (.osm)")
def main(min_lat, min_lon, max_lat, max_lon, output):
    """دانلود داده‌های OSM یک محدوده به صورت فایل .osm"""
    downloader = OSMOverpassDownloader()
    valid, err = downloader.validate_bbox(min_lat, min_lon, max_lat, max_lon)
    if not valid:
        click.echo(f"خطا: {err}", err=True)
        return
    try:
        xml_data = downloader.download_as_xml(min_lat, min_lon, max_lat, max_lon)
        downloader.save_osm_file(xml_data, Path(output))
        click.echo("عملیات با موفقیت پایان یافت.")
    except Exception as e:
        click.echo(f"خطا در دانلود: {e}", err=True)
        raise

if __name__ == "__main__":
    main()
