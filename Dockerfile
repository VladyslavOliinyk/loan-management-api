FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["bash", "-c", "for i in $(seq 1 15); do python scripts/load_csv.py && break || sleep 2; done && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
