FROM python:3.13.2-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN pip install --no-cache-dir flask-cors python-dotenv

COPY . .

RUN mkdir -p uploads

EXPOSE 5000

ENTRYPOINT ["python", "app.py"]