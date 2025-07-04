#!/bin/bash
python -m playwright install --with-deps
gunicorn app:app --bind 0.0.0.0:10000
chmod +x build.sh
