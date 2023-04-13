FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

COPY . .

# port 80
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8088"]
