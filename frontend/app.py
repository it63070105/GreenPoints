import io

import urllib
from flask import Flask, render_template, request
import requests
import base64
import matplotlib.pyplot as plt
import numpy as np
import cv2
import json

app = Flask(__name__,template_folder="")

# encode image as base64 string
def encode_image(image):
    _, encoded_image = cv2.imencode(".jpg", image)
    return "data:image/jpeg;base64," + base64.b64encode(encoded_image).decode()

# decode base64 string to image
def decode_image(image_string):
    encoded_data = image_string.split(',')[1]
    decoded_data = base64.b64decode(encoded_data)
    return io.BytesIO(decoded_data)

url = "http://localhost:8088"

@app.route('/', methods=['GET'])
def home():
    return render_template("index.html")

@app.route('/post_images', methods=['POST'])
def post_images():
    payload = {
        "images" : []
    }
    
    request_images = request.files.getlist('images')

    for i in range(0, len(request_images)):   
        image = request_images[i].read()
        image_np = np.frombuffer(image, np.uint8)
        image_cv = cv2.imdecode(image_np, cv2.IMREAD_COLOR)
        image_string = encode_image(image_cv)
        payload.get('images').append({'image_name': request_images[i].filename, 'encode_image': image_string})  

    response = requests.post(f"{url}/detect-image", json=payload)
    data = json.loads(response.content)
    # print(data)

    for result in data:
        image_string = result['output_image']
        result['output_image'] = urllib.parse.quote(base64.b64encode(decode_image(image_string).read()).decode())
        if result['found']:
            image_string = result['qrcode']
            result['qrcode'] = urllib.parse.quote(base64.b64encode(decode_image(image_string).read()).decode())

    return render_template("index.html", result=data)

if __name__ == '__main__':
    app.run(host="0.0.0.0",port="8081")
