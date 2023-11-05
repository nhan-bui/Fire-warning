import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import cv2
import numpy as np
from firebase_admin import messaging
import firebase_admin
from firebase_admin import credentials

TOKEN = "dZc0l7UcTvaoT8F33cr0Ve:APA91bFv9KIRoP7zn4w598G3Ow9_9OPBp57SDwRGg2JaGUSSOriFdQlvMGkw0RW-3G-zzg9OZa8Mdblz2YHrW8Iob9lbNTh6mPGTlX7Mktb0sgtowTcdOsF1dFOREN61q_376ij0a0MA"
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
    def __init__(self, json_path, token, title = "FIREWARNING", body = "CHÁY"):
        self.json_path = json_path
        self.token = token
        self.title = title
        self.body = body
        self.message = messaging.Message(notification=messaging.Notification(title=self.title, body=self.body), token=self.token)
        self.cred = credentials.Certificate(self.json_path)
        self.set()
    def set(self):
        firebase_admin.initialize_app(self.cred)

    def send(self):
        response = messaging.send(self.message)
        print("Đã gửi", response)


if __name__ == "__main__":
    # image = cv2.imread('test.jpg')
    # image = plot_box(image, np.array([[0, 0, 200, 200], [1, 2, 300, 300]]), [1, 0])
    # cv2.imshow("Rectangle", image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    x = Notification(json_path="new.json", token=TOKEN)
    x.set()
    for i in range(10):
        x.send()

