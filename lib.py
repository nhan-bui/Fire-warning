import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import cv2
import numpy as np
from firebase_admin import messaging
import firebase_admin
from firebase_admin import credentials

TOKEN = "dzGV42xAQVSGIFHzBY-mFo:APA91bGgawNwBt4okVtLncZ3VhvnmTGPjpcx2qE4fhRnhiSTgHcXjYqFFjRklQxbg6WkMS4ftWfZZ0B-cdjYu5skIPutCTQvoaHBuOwNbrEfV0RuDc1fFblZU6XgvYh6BdaWJBHOdPyO"
DATA = {
        "image": "https://pcccpnn.com/wp-content/uploads/2022/08/PNN-1.jpg",  # Thêm URL ảnh vào phần dữ liệu tùy chỉnh
    }

def auto_mail(receiver_email, frame):
    sender_email = 'tnhan1901.work@gmail.com'
    sender_password = 'ctddvjxhycfbpkwb'

    # Thông tin người nhận email

    # Tạo đối tượng MIMEMultipart để tạo email
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = 'FIRE WARNING'

    # Thêm nội dung email
    message.attach(MIMEText('Fire warning.', 'plain'))

    # Đính kèm tệp vào email

    _, image_data = cv2.imencode(".jpg", frame)
    image_bytes = image_data.tobytes()

    # Đính kèm ảnh vào email
    image_mime = MIMEImage(image_bytes, name="image.jpg")
    message.attach(image_mime)
    # Gửi email
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(message)
        print('Email sent successfully!')
    except Exception as e:
        print('Error sending email:', str(e))


def plot_box(image, xyxy, cls):
    for i in range(xyxy.shape[0]):
        color = (0, 0, 0)
        p1 = (int(xyxy[i][0]), int(xyxy[i][1]))
        p2 = (int(xyxy[i][2]), int(xyxy[i][3]))
        if cls[i] == 1:
            color = (93, 108, 96)
        else:
            color = (71, 205, 130)
        cv2.rectangle(image, p1, p2, color=color, thickness=2)
    return image


class Notification():
    def __init__(self, json_path, token, title = "FIREWARNING", body = "CHÁY", data=DATA):
        self.json_path = json_path
        self.token = token
        self.title = title
        self.body = body
        self.data = data
        self.message = messaging.Message(notification=messaging.Notification(title=self.title, body=self.body, image="https://pcccpnn.com/wp-content/uploads/2022/08/PNN-1.jpg"), token=self.token, data=self.data)
        self.cred = credentials.Certificate(self.json_path)
        self.set()
    def set(self):
        firebase_admin.initialize_app(self.cred)

    def send(self):
        response = messaging.send(self.message)
        print("Đã gửi", response)

def process_frame(frame):
        auto_mail("nhantrong618@gmail.com", frame)


if __name__ == "__main__":
    # image = cv2.imread('test.jpg')
    # image = plot_box(image, np.array([[0, 0, 200, 200], [1, 2, 300, 300]]), [1, 0])
    # cv2.imshow("Rectangle", image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    x = Notification(json_path="new.json", token=TOKEN)
    for i in range(3):
        x.send()

