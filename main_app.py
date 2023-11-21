import os
from flask import Flask, request, render_template
import cv2
import torch
import numpy as np


from fileinput import filename 
model = torch.hub.load('ultralytics/yolov5', 'custom', path='best.pt')

videos = []

app = Flask(__name__, '/static')

@app.route('/', methods=['GET', 'POST'])
def upload_file():
   if request.method == 'POST':   
        f = request.files['filename']
        videos.append(f.filename) 
        f.filename = "static\\test.jpg"
        f.save(f.filename) 
        image = cv2.imread("static\\test.jpg")
        results = model(image)
        result_image = np.squeeze(results.render())
        cv2.imwrite("static\\result.jpg", result_image)
        #return "test"
        return render_template('index.html', videos=videos)
   else:
       return render_template('index.html')