#!/usr/bin/env python3
"""
اسکریپت کمکی برای اجرای سریع دانلودر از پوشه scripts
"""

import sys
from pathlib import Path

# اضافه کردن مسیر src به sys.path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from downloader import main

if __name__ == "__main__":
    main()
