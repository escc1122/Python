# 使用官方 Playwright + Python + Chromium 映像
FROM mcr.microsoft.com/playwright/python:v1.51.0-noble

WORKDIR /app

# 複製需要的靜態資源與依賴
COPY requirements.txt ./
COPY .env ./
COPY site_urls.txt ./
COPY logs/ ./logs/

# 安裝 Python 套件
RUN pip install --no-cache-dir -r requirements.txt

# 預設啟動指令（由外部掛入的 update_site.py）
CMD ["python", "main.py"]
