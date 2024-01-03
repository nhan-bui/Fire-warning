import cv2
from ultralytics import YOLO
from lib import *
import threading
import queue
import numpy as np


if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    notify = Notification(json_path="new.json", token=TOKEN_LIST[0])
    model = YOLO('NewFW.pt')
    try:
        while True:
            ret, frame = cap.read()
            result = model.predict(source=frame, conf=0.5)
            boxes = result[0].boxes
            xyxy = boxes.xyxy.cpu().numpy()
            cls = boxes.cls.cpu().numpy()
            frame = plot_box(frame, xyxy, cls)
            cv2.imshow("Camera", frame)
            if len(cls) - cls.sum() > 0:
                notify.set_message(body="Khu vực 4", data=DATA4)
                notify_thread = threading.Thread(target=notify_user, args=(TOKEN_LIST, notify))
                notify_thread.start()

            if cv2.waitKey(1) == 27:
                break

    except Exception as e:
        print(e)

