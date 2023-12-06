import os
from flask import Flask, request, render_template
import cv2
import torch
import numpy as np
import time


from fileinput import filename 
model = torch.hub.load('ultralytics/yolov5', 'custom', path='best.pt')

videos = []

app = Flask(__name__, '/static')


@app.route('/', methods=['GET', 'POST'])
def upload_file():
     if request.method == 'POST':   
          f = request.files['filename']
          videos.append(f.filename) 
          #f.filename = "static\\test.jpg"
          f.save(f.filename) 
          video = cv2.VideoCapture(f.filename)
          frame_per_second = video.get(cv2.CAP_PROP_FPS)
          frame_count = 0
          while (True):
               #time.sleep(30) # take schreenshot every 5 seconds
               # reading from frame
               ret, frame = video.read()

               if ret:
                    if frame_count > (30*frame_per_second): 
                         frame_count = 0

                         # if video is still left continue creating images
                         name = "static\\test.jpg"

                         # writing the extracted images
                         cv2.imwrite(name, frame)
                         results = model(frame)
                         result_image = np.squeeze(results.render())
                         cv2.imwrite("static\\result.jpg", result_image)
                    else:
                         frame_count += 1

               else:
                    break

          # Release all space and windows once done
          video.release()
          cv2.destroyAllWindows()
        
        
          #return "test"
          return render_template('index.html', videos=videos)
     else:
          return render_template('index.html')
     
if __name__ == '__main__':
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    app.run(debug=True)