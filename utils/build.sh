#!/bin/bash

# Playwright browser-ləri quraşdır (lazımlı native deps-lərlə birlikdə)
python -m playwright install --with-deps

# Flask app-i Gunicorn ilə başlat
gunicorn app:app --bind 0.0.0.0:10000
