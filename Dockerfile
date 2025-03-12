FROM mcr.microsoft.com/playwright/python:v1.36.0-focal

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Create images directory
RUN mkdir -p images

# Install Playwright browsers
RUN playwright install chromium

CMD ["python", "main.py"] 