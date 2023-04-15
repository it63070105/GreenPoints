FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

RUN apt-get update && \
    apt-get install -y \
        curl \
        gcc \
        libgl1-mesa-glx \
        libsm6 \
        libxext6 \
        libxrender-dev \
        python3-dev \
        ffmpeg

RUN mkdir -p /root/.cvlib/object_detection/yolo/yolov3

RUN curl -L -o /root/.cvlib/object_detection/yolo/yolov3/yolov3_classes.txt https://github.com/arunponnusamy/object-detection-opencv/raw/master/yolov3.txt

RUN curl -L -o /root/.cvlib/object_detection/yolo/yolov3/yolov4.cfg https://raw.githubusercontent.com/AlexeyAB/darknet/master/cfg/yolov4.cfg

RUN curl -L -o /root/.cvlib/object_detection/yolo/yolov3/yolov4.weights https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v3_optimal/yolov4.weights

COPY . .

# port 80
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8088"]
