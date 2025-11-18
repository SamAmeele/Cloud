FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY publisher.py .

CMD ["python", "publisher.py", "--host", "mosquitto", "--port", "3500", "--interval", "1.0"]
