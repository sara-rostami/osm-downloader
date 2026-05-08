import pytest
from pathlib import Path
import tempfile
from downloader import OSMOverpassDownloader

def test_validate_bbox():
    d = OSMOverpassDownloader()
    # valid
    valid, msg = d.validate_bbox(35.0, 51.0, 35.1, 51.1)
    assert valid is True
    # invalid lat
    valid, msg = d.validate_bbox(100, 0, 101, 1)
    assert valid is False
    # invalid lon range
    valid, msg = d.validate_bbox(35, 51, 34, 52)
    assert valid is False
