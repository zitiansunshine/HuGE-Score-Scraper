FROM mcr.microsoft.com/playwright/python:v1.42.0-jammy

WORKDIR /app

COPY requirements.txt .
RUN pip uninstall -y playwright && \
    pip install --no-cache-dir -r requirements.txt && \
    playwright install chromium

COPY . .

CMD ["python", "scraper.py"]
