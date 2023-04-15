import io

import urllib
from flask import Flask, render_template, request
import requests
import base64
import matplotlib.pyplot as plt
import numpy as np
import cv2
import json
import datetime

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

    print("POST: " + url + "/detect-image")
    response = requests.post(f"{url}/detect-image", json=payload)
    data = json.loads(response.content)
    # print(data)

    for result in data:
        image_string = result['output_image']
        result['output_image'] = urllib.parse.quote(base64.b64encode(decode_image(image_string).read()).decode())
        if result['found']:
            image_string = result['qrcode']
            result['qrcode'] = urllib.parse.quote(base64.b64encode(decode_image(image_string).read()).decode())
            # Count the occurrences of each item in the label list and exclude 'trash'
            count_items = {item: result['label'].count(item) for item in set(result['label']) if item != 'trash'}

            # Format the output to display as "itemxN"
            result['label'] = [f"{item}x{count}" for item, count in count_items.items()]

    return render_template("index.html", result=data)

@app.route('/records', methods=['GET', 'POST'])
def records():
    # records = requests.get(f"{url}/getrecords")
    # records = json.loads(records.content)
    # for rec in records:
    #     rec[1] = rec[1].split(", ")
    #     rec[2] = datetime.datetime.strptime(rec[2], '%Y-%m-%dT%H:%M:%S')
    #     counts = {}
    #     for obj in rec[1]:
    #         if obj != 'trash':
    #             if obj in counts:
    #                 counts[obj] += 1
    #             else:
    #                 counts[obj] = 1
    #     rec[1] = counts
    # print(records)
    object_filter = None
    if request.method == 'POST':
        object_filter = request.form.get('object')

    records = requests.get(f"{url}/getrecords", json={"object_filter": object_filter})
    print(records.content)
    if not records:
        return render_template("records.html", records=records, data=False)
    elif not json.loads(records.content):
        return render_template("records.html", records=records.content, data=False)
    records = json.loads(records.content)
    for rec in records:
        rec[1] = rec[1].split(", ")
        rec[2] = datetime.datetime.strptime(rec[2], '%Y-%m-%dT%H:%M:%S')
        counts = {}
        for obj in rec[1]:
            if obj != 'trash':
                if obj in counts:
                    counts[obj] += 1
                else:
                    counts[obj] = 1
        rec[1] = counts
    return render_template("records.html", records=records, data=True)

if __name__ == '__main__':
    app.run(host="0.0.0.0",port="8081")
