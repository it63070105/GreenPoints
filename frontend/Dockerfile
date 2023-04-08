FROM python:3.9-slim-buster

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8081
CMD ["python", "app.py", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]