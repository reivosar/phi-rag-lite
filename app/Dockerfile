FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /app/data && touch /app/data/docs.txt

CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port 8000"]