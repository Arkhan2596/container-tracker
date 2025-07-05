FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    wget unzip curl gnupg ca-certificates fonts-liberation libnss3 libatk-bridge2.0-0 \
    libxss1 libgtk-3-0 libx11-xcb1 libxcomposite1 libxdamage1 libgbm1 libasound2 libxrandr2 \
    chromium chromium-driver && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "--bind", "0.0.0.0:10000", "app:app"]
