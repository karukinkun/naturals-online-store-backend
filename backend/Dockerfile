FROM python:3.11-slim

WORKDIR /app

# 依存コピー
COPY requirements.txt .

# インストール
RUN pip install --no-cache-dir -r requirements.txt

# ソースコピー
COPY . 

# 起動
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]