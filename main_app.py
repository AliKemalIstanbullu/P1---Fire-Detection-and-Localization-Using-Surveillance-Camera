import os
from flask import Flask, request, render_template
import cv2
import torch
import numpy as np
import time
import signal

from background_thread import BackgroundThreadFactory, TASKS_QUEUE


from fileinput import filename 
model = torch.hub.load('ultralytics/yolov5', 'custom', path='best.pt')

videos = []

app = Flask(__name__, '/static')


@app.route('/', methods=['GET', 'POST'])
def upload_file():
     if request.method == 'POST':   
          
          
                    
          if 'steamurl' in request.form:
               feed = request.form['streamurl']
               name = request.form['filename']
               TASKS_QUEUE.put({'name':name, 'address':feed}) 
               notification_thread = BackgroundThreadFactory.create('stream')
               notification_thread.start()
          
               videos.append(name) 
          else:
               f = request.files['filename']
               f.save(f.filename) 
               TASKS_QUEUE.put(f.filename) 
               notification_thread = BackgroundThreadFactory.create('video')
               notification_thread.start()
               videos.append(f.filename) 
          
          return render_template('index.html', videos=videos)
     else:
          return render_template('index.html', videos=videos)
     
if __name__ == '__main__':
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    app.run(debug=True)