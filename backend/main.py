import cv2
import cvlib as cv
from cvlib.object_detection import draw_bbox
from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
import cv2
import base64
from typing import List
import psycopg2
import datetime
from typing import Optional

app = FastAPI()

db_host = "db"

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
    print("RECEIVE: request")
    recycle = ['bottle', 'cup', 'paper', 'can']
    images = image_request.images
    result = []
    found = False
    qrcode = ''
    
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
            if label[j] in recycle and found != True:
                found = True
                with open('./qrcode.jpg', 'rb') as f:
                    image_data = f.read()
                    image_np = np.frombuffer(image_data, np.uint8)
                    image_cv = cv2.imdecode(image_np, cv2.IMREAD_COLOR)
                    qrcode = encode_image(image_cv)
        
        result.append({'image_name': images[i].image_name, 'label': label, 'output_image': output_image, 'found': found, 'qrcode': qrcode})
        if found:
            conn = psycopg2.connect(
                host=db_host,
                database="greenpointsdb",
                user="postgres",
                password="postgres"
            )
            cur = conn.cursor()
            try:
                objects_str = ', '.join(label)
                now_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                query = "INSERT INTO records (objects, time) VALUES ('" + objects_str + "', '" + now_str + "');"
                cur.execute(query)
                conn.commit()
            except psycopg2.Error as e:
                print(e)
                conn.rollback()
                return False
            finally:
                cur.close()
                conn.close()

        # print(result)
        
    return result

@app.get("/getrecords")
async def getrecords(object_filter: Optional[str] = None):
    conn = psycopg2.connect(
        host=db_host,
        database="greenpointsdb",
        user="postgres",
        password="postgres"
    )
    cur = conn.cursor()
    try:
        if object_filter:
            query = "SELECT * FROM records WHERE objects LIKE %s ORDER BY time DESC;"
            cur.execute(query, ('%' + object_filter + '%',))
        else:
            query = "SELECT * FROM records ORDER BY time DESC;"
            cur.execute(query)
            
        records = cur.fetchall()
        return records
    except Exception as e:
        print(e)
        return False
    finally:
        cur.close()
        conn.close()
