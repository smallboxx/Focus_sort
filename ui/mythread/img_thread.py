import pickle
import struct

from PyQt5.QtCore import QThread, pyqtSignal, QWaitCondition, QMutex
# from hkcamera.run import grab_img, WORKQUEUE
import cv2

import threading


class MyThread_Image(QThread):
    valueChangeSignal = pyqtSignal(dict)

    def __init__(self):
        super(MyThread_Image, self).__init__()
        self._isPause = True
        self._value = 1

        self.cond = QWaitCondition()
        self.mutex = QMutex()
        # self.camera_thread = threading.Thread(target=grab_img, args=(0, 2))
        

    def pause(self):
        print("线程休眠")
        self._isPause = True
        print(self.currentThreadId())

    def resume(self):
        print("线程启动")
        self._isPause = False
        self.cond.wakeAll()
        self.camera_thread.start()
        self.start()

    def run(self):
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        while True:
            # img_dict = WORKQUEUE.get()
            data = pickle.dumps(frame)
            self.valueChangeSignal.emit(struct.pack("L", len(data)) + data)


