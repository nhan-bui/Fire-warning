import cv2
from ultralytics import YOLO
from lib import auto_mail, plot_box, Notification, TOKEN, process_frame, TOKEN_LIST, notify_user
import threading
import asyncio


if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    notify = Notification(json_path="new.json", token=TOKEN)
    model = YOLO('C:/Users/Truongpc/PycharmProjects/FireWaring/NewFW.pt')
    num_frame = 0
    try:
        while True:
            ret, frame = cap.read()
            result = model.predict(source=frame, conf=0.5)
            boxes = result[0].boxes
            xyxy = boxes.xyxy.cpu().numpy()
            cls = boxes.cls.cpu().numpy()
            frame = plot_box(frame, xyxy, cls)
            cv2.imshow("Camera", frame)
            if len(cls) - cls.sum() > 0 and num_frame % 30 == 0:
                # frame_thread = threading.Thread(target=process_frame, args=(frame,))
                # frame_thread.start()

                notify_thread = threading.Thread(target=notify_user, args=(TOKEN_LIST, notify))
                notify_thread.start()
                print(num_frame)
            num_frame += 1

            if cv2.waitKey(1) == 27:
                break
    except Exception as e:
        print(e)

