FROM python:3.9-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONIOENCODING=utf-8
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

WORKDIR /app

# システムの依存関係とFFmpegのインストール
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsm6 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8080

ENV PORT=8080
ENV HOST=0.0.0.0

CMD streamlit run src/main.py \
    --server.port $PORT \
    --server.address $HOST \
    --server.baseUrlPath ${BASE_URL_PATH:-""} \
    --browser.serverAddress ${SERVER_ADDRESS:-"0.0.0.0"} \
    --server.enableCORS false \
    --server.enableXsrfProtection false