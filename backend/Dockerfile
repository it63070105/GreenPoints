FROM python:3.9-slim-buster

WORKDIR /app

COPY ./backend/requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# port 80
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8088"]
