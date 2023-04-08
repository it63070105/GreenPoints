import cv2
import cvlib as cv
from cvlib.object_detection import draw_bbox
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
import cv2
import base64
from typing import List

app = FastAPI()

# from keras.models import load_model
# import numpy as np
#tensorflow

# Load the trained model
# model = load_model('./trained_model.h5')

# Create a dictionary of class labels
# labels = ['Plastic', 'Glass', 'Metal', 'Trash', 'Paper', 'Cardboard']

# images = ['./backend/images/1.jpg', './backend/images/2.jpg', './backend/images/3.jpg', './backend/images/4.jfif', './backend/images/5.jfif', './backend/images/6.jpg']
class ImageInfo(BaseModel):
    image_name : str
    encode_image : str

class ImageRequest(BaseModel):
    images: List[ImageInfo]


# encode image as base64 string
def encode_image(image):
    _, encoded_image = cv2.imencode(".jpg", image)
    return "data:image/jpeg;base64," + base64.b64encode(encoded_image).decode()

# decode base64 string to image
def decode_image(image_string):
    encoded_data = image_string.split(',')[1]
    nparr = np.frombuffer(base64.b64decode(encoded_data), np.uint8)
    return cv2.imdecode(nparr, cv2.IMREAD_COLOR)

@app.post("/detect-image")
async def process_image(image_request: ImageRequest):
    
    recycle = ['bottle', 'cup', 'paper', 'can']
    images = image_request.images
    result = []
    
    # create video capture object
    for i in range(0, len(images)):
        im = decode_image(images[i].encode_image)
        # cap = cv2.imread(im)
        bbox, label, conf = cv.detect_common_objects(im)

        # h, w, c = cap.shape
        # draw bounding boxes around detected objects
        output_image = draw_bbox(im, bbox, label, conf)
        # output_image = cv2.resize(output_image, (int(w/4), int(h/3)))
        output_image = encode_image(output_image)

        for j in range(0, len(label)):
            if label[j] not in recycle:
                label[j] = 'trash'
        result.append({'image_name': images[i].image_name, 'label': label, 'output_image': output_image})
        print(result)
        
    return result
