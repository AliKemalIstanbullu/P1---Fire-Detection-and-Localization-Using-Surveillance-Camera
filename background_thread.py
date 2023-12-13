import logging
import queue
import threading
import time
from queue import Queue
from abc import abstractmethod, ABC
from typing import Dict
import cv2
import torch
import numpy as np
import os
import smtplib
from email.message import EmailMessage

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

def sendAlert(filename):
    file1 = open('config.txt', 'r')
    lines = file1.readlines()
    file1.close()

    stripped = filename.split('.', 1)[0]

    send_user = lines[0].strip()
    send_password = lines[1].strip()
    receive_user = lines[2].strip()

    msg = MIMEMultipart()
    msg['Subject'] = 'fire Alert in ' + filename
    msg['From'] = send_user
    msg['To'] = receive_user

    text = MIMEText('<p>fire detected in : ' + filename + '</p><img src="cid:image1">', 'html')
    msg.attach(text)

    image = MIMEImage(open("static\\"+stripped+"\\result.jpg", 'rb').read())

    # Define the image's ID as referenced in the HTML body above
    image.add_header('Content-ID', '<image1>')
    msg.attach(image)


    s = smtplib.SMTP("smtp-mail.outlook.com",587)
    s.ehlo() # Hostname to send for this command defaults to the fully qualified domain name of the local host.
    s.starttls() #Puts connection to SMTP server in TLS mode
    s.ehlo()
    s.login(send_user, send_password)
    s.send_message(msg)
    s.quit()

TASKS_QUEUE = Queue()

model = torch.hub.load('ultralytics/yolov5', 'custom', path='best.pt')

class BackgroundThread(threading.Thread, ABC):
    def __init__(self):
        super().__init__()
        self._stop_event = threading.Event()

    def stop(self) -> None:
        self._stop_event.set()

    def _stopped(self) -> bool:
        return self._stop_event.is_set()

    @abstractmethod
    def startup(self) -> None:
        """
        Method that is called before the thread starts.
        Initialize all necessary resources here.
        :return: None
        """
        raise NotImplementedError()

    @abstractmethod
    def shutdown(self) -> None:
        """
        Method that is called shortly after stop() method was called.
        Use it to clean up all resources before thread stops.
        :return: None
        """
        raise NotImplementedError()

    @abstractmethod
    def handle(self) -> None:
        """
        Method that should contain business logic of the thread.
        Will be executed in the loop until stop() method is called.
        Must not block for a long time.
        :return: None
        """
        raise NotImplementedError()

    def run(self) -> None:
        """
        This method will be executed in a separate thread
        when start() method is called.
        :return: None
        """
        self.startup()
        while not self._stopped():
            self.handle()
        self.shutdown()


class NotificationThread(BackgroundThread):
    def startup(self) -> None:
        logging.info('NotificationThread started')

    def shutdown(self) -> None:
        logging.info('NotificationThread stopped')

    def handle(self) -> None:
        try:
            task = TASKS_QUEUE.get(block=False)
            stripped = task.split('.', 1)[0]
            os.makedirs('static\\'+stripped, exist_ok=True)
            video = cv2.VideoCapture(task)
            frame_per_second = video.get(cv2.CAP_PROP_FPS)
            frame_count = 0
            object_count = 0
            while (True):
 
               # reading from frame
               ret, frame = video.read()

               if ret:
                    if frame_count > (30*frame_per_second): 
                         frame_count = 0

                         # if video is still left continue creating images
                         name = "static\\"+stripped+"\\test.jpg"

                         # writing the extracted images
                         cv2.imwrite(name, frame)
                         results = model(frame)
                         result_image = np.squeeze(results.render())
                         cv2.imwrite("static\\"+stripped+"\\result.jpg", result_image)
                         detected_objects = results.pandas().xyxy[0] 
                         object_count = len(detected_objects)
                         if object_count > 0:
                             sendAlert(task)
                             break
                         
                    else:
                         frame_count += 1

               else:
                    break
            f = open("static\\"+stripped+"\\result.txt", "w")
            f.write(str(object_count))
            f.close()
            # Release all space and windows once done
            video.release()
            cv2.destroyAllWindows()
            self.stop()
        except queue.Empty:
            time.sleep(1)


class BackgroundThreadFactory:
    @staticmethod
    def create(thread_type: str) -> BackgroundThread:
        if thread_type == 'notification':
            return NotificationThread()

        # if thread_type == 'some_other_type':
        #     return SomeOtherThread()

        raise NotImplementedError('Specified thread type is not implemented.')
