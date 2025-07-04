# Playwright-in rəsmi imici (Python + Chromium ilə hazır gəlir)
FROM mcr.microsoft.com/playwright/python:v1.43.1-jammy

# İş qovluğunu qur
WORKDIR /app

# Faylları konteynerə kopyala
COPY . .

# Lazımi Python paketlərini quraşdır
RUN pip install --no-cache-dir -r requirements.txt

# Portu aç
EXPOSE 10000

# Flask serverini başlat
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:10000"]
