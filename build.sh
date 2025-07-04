#!/bin/bash

echo "📦 Installing dependencies..."
pip install -r requirements.txt

echo "🌐 Installing Playwright browsers..."
python -m playwright install

echo "✅ Build complete"
