#!/usr/bin/env python3
"""
Randează docs/grafice/grafic.html în PNG 1080×1080.

    python randeaza.py                      # -> grafic.png
    python randeaza.py alerta-netflix.png   # nume de fișier explicit

Cerințe: pip install playwright && playwright install chromium
"""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

HERE = Path(__file__).parent
SRC = HERE / "grafic.html"
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "grafic.png"

if not SRC.exists():
    sys.exit(f"Lipsește {SRC}")

with sync_playwright() as pw:
    browser = pw.chromium.launch()
    page = browser.new_page(viewport={"width": 1080, "height": 1080},
                            device_scale_factor=1)
    page.goto(SRC.resolve().as_uri())
    page.wait_for_timeout(400)          # așteaptă fonturile
    page.screenshot(path=str(OUT))
    browser.close()

print(f"scris: {OUT}")
