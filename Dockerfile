# ---- Base image ----
FROM python:3.10-slim

# ---- Set environment ----
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# ---- Set working directory ----
WORKDIR /app

# ---- Install system dependencies ----
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    libxml2-dev \
    libxslt1-dev \
    libjpeg-dev \
    zlib1g-dev \
    libglib2.0-0 \
    libnss3 \
    libgconf-2-4 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
    libxshmfence1 \
    libx11-xcb1 \
    && apt-get clean

# ---- Copy requirements and install ----
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# ---- Copy project files ----
COPY . .

# ---- Expose port ----
EXPOSE 10000

# ---- Start app ----
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:10000"]
