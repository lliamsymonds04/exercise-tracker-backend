FROM python:3.12-slim

WORKDIR /app

# Install build dependencies, including PostgreSQL development headers
RUN apt-get update && apt-get install -y build-essential libpq-dev

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000
CMD ["python", "app.py"]