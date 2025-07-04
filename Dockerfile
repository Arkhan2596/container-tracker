# Base image
FROM mcr.microsoft.com/playwright/python:v1.43.1-jammy

# Create working directory
WORKDIR /app

# Copy everything
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port
EXPOSE 10000

# Start the service
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:10000"]
