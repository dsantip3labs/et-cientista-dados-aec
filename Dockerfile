FROM python:3.13-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    MODEL_PATH=/modelo/modelo.joblib \
    PORT=8000 \
    WORKERS=1

RUN apt-get update \
 && apt-get install -y --no-install-recommends libgomp1 \
 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY api ./api
COPY src ./src

RUN mkdir -p /modelo


EXPOSE 8000
CMD ["sh", "-c", "uvicorn api.main:app --host 0.0.0.0 --port ${PORT} --workers ${WORKERS}"]