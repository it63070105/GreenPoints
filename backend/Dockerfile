FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 curl -y

# download YOLOv4 configuration file
RUN curl -L -o yolov4.cfg https://raw.githubusercontent.com/AlexeyAB/darknet/master/cfg/yolov4.cfg

# download YOLOv4 weights file
RUN curl -L -o yolov4.weights https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v3_optimal/yolov4.weights

# download YOLOv3 classes file
RUN curl -L -o yolov3_classes.txt https://github.com/arunponnusamy/object-detection-opencv/raw/master/yolov3.txt

COPY . .

# port 80
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8088"]
