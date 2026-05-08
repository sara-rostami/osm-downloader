from setuptools import setup, find_packages

setup(
    name="osm-downloader",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "overpy",
        "requests",
        "click",
    ],
    entry_points={
        "console_scripts": [
            "osm-download=downloader:main",
        ],
    },
    author="Your Name",
    description="Download complete OSM data for a geographic bounding box",
    license="MIT",
)
