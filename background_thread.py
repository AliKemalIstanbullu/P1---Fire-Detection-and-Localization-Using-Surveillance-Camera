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
                    else:
                         frame_count += 1

               else:
                    break

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
