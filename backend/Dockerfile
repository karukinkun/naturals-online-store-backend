FROM python:3.11-slim

WORKDIR /app

# uvインストール
RUN pip install --no-cache-dir uv

ENV UV_PYTHON=3.11

# 依存だけ先にコピー（キャッシュ効かせる）
COPY pyproject.toml uv.lock ./

# 本番用依存インストール
RUN uv sync --no-dev

# アプリコピー
COPY . .

# ポート公開
EXPOSE 8000

# 起動
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]