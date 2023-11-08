import time
import cv2
import numpy as np
from lib import *
import threading
import queue
from ultralytics import YOLO


if __name__ == "__main__":
    rtsp1 = "rtsp://admin:tsinb123@thptymb.ddns.net:554"
    rtsp2 = "rtsp://admin:tsinb123@thptymb.ddns.net:555"
    rtsp3 = "rtsp://admin:tsinb123@thptymb.ddns.net:556"
    rtsp4 = 0

    cap1 = cv2.VideoCapture(rtsp1)
    cap2 = cv2.VideoCapture(rtsp2)
    cap3 = cv2.VideoCapture(rtsp3)
    cap4 = cv2.VideoCapture(rtsp4)
    model = YOLO('C:/Users/Truongpc/PycharmProjects/FireWaring/NewFW.pt')
    notify = Notification(json_path="new.json", token=TOKEN)
    while True:
        result_queue1 = queue.Queue()
        thread = threading.Thread(target=process_cam, args=(cap1, model, result_queue1))
        thread.start()
        thread.join()
        frame1, cls1 = result_queue1.get()
        frame1 = cv2.resize(frame1, (300, 300))

        result_queue2 = queue.Queue()
        thread = threading.Thread(target=process_cam, args=(cap2, model, result_queue2))
        thread.start()
        thread.join()
        frame2, cls2 = result_queue2.get()
        frame2 = cv2.resize(frame2, (300, 300))

        result_queue3 = queue.Queue()
        thread = threading.Thread(target=process_cam, args=(cap3, model, result_queue3))
        thread.start()
        thread.join()
        frame3, cls3 = result_queue3.get()
        frame3 = cv2.resize(frame3, (300, 300))

        result_queue4 = queue.Queue()
        thread = threading.Thread(target=process_cam, args=(cap4, model, result_queue4))
        thread.start()
        thread.join()
        frame4, cls4 = result_queue4.get()
        frame4 = cv2.resize(frame4, (300, 300))
        end = time.time()
        frame12 = np.concatenate((frame1, frame2), axis=1)
        frame34 = np.concatenate((frame3, frame4), axis=1)

        frames = np.concatenate((frame12, frame34), axis=0)
        cv2.imshow("frame", frames)

        if len(cls4) - cls4.sum() > 0:
            notify_thread = threading.Thread(target=notify_user, args=(TOKEN_LIST, notify))
            notify_thread.start()

        if cv2.waitKey(1) == 27:
            break
