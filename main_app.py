import os
from flask import Flask, request, render_template
import cv2
import torch
import numpy as np

from fileinput import filename 
model = torch.hub.load('ultralytics/yolov5', 'custom', path='best.pt')

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
   if request.method == 'POST':   
        f = request.files['file'] 
        f.filename = "test.jpg"
        f.save(f.filename) 
        image = cv2.imread("test.jpg")
        results = model(image)
        result_image = np.squeeze(results.render())
        cv2.imwrite("result.jpg", result_image)
        return render_template('index.html')
   else:
       return render_template('index.html')