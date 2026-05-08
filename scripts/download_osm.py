#!/usr/bin/env python3
import argparse
import sys
import os
import requests

DEFAULT_USER_AGENT = "GitHubAction-OSMDownloader/1.0 (https://github.com/YOUR_USERNAME/osm-downloader; your-email@example.com)"

def build_overpass_query(min_lon, min_lat, max_lon, max_lat):
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
    query = build_overpass_query(min_lon, min_lat, max_lon, max_lat)
    user_agent = os.environ.get('OVERPASS_USER_AGENT', DEFAULT_USER_AGENT)
    headers = {'User-Agent': user_agent}
    print(f"[INFO] Sending request to Overpass API for bounding box: {min_lon}, {min_lat}, {max_lon}, {max_lat}")
    try:
        response = requests.post(
            'https://overpass-api.de/api/interpreter',
            data={'data': query},
            headers=headers,
            timeout=300
        )
        response.raise_for_status()
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(response.text)
        print(f"[SUCCESS] OSM data saved to {output_file}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Failed to download data: {e}")
        return False

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--min-lon', type=float, required=True)
    parser.add_argument('--min-lat', type=float, required=True)
    parser.add_argument('--max-lon', type=float, required=True)
    parser.add_argument('--max-lat', type=float, required=True)
    args = parser.parse_args()
    if not (-180 <= args.min_lon <= 180) or not (-180 <= args.max_lon <= 180):
        print("[ERROR] Longitude out of range")
        sys.exit(1)
    if not (-90 <= args.min_lat <= 90) or not (-90 <= args.max_lat <= 90):
        print("[ERROR] Latitude out of range")
        sys.exit(1)
    if args.min_lat >= args.max_lat or args.min_lon >= args.max_lon:
        print("[ERROR] Invalid bounding box")
        sys.exit(1)
    output_file = "downloaded_data.osm"
    if download_osm_file(args.min_lon, args.min_lat, args.max_lon, args.max_lat, output_file):
        print("[INFO] Script finished successfully.")
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
