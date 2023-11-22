import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import cv2
from firebase_admin import messaging
import firebase_admin
from firebase_admin import credentials


TOKEN_LIST = ["your token list"]
DATA1 = {
        "imageUrl":"https://scontent.fhan14-3.fna.fbcdn.net/v/t1.15752-9/377234734_3413410322303677_8758365910479124703_n.png?_nc_cat=104&ccb=1-7&_nc_sid=8cd0a2&_nc_ohc=KnI-b-P5BGIAX9MqraU&_nc_ht=scontent.fhan14-3.fna&oh=03_AdTS1-qHoSo7G0yG4-XLTuCaZT78UVTihm9lOJh-BNn5rQ&oe=65744BAB",  # Thêm URL ảnh vào phần dữ liệu tùy chỉnh
    }
DATA2 = {
    "imageUrl":"https://scontent.fhan20-1.fna.fbcdn.net/v/t1.15752-9/370100027_257199114015509_1128683649524341392_n.png?_nc_cat=100&ccb=1-7&_nc_sid=8cd0a2&_nc_eui2=AeH290_O0GbqyaZl_dy-jr44uyHsYZeUUPi7Iexhl5RQ-LGJFHIf3MfshYqCAjsxqeew7SdqqV3gzFsTCbKijzYl&_nc_ohc=khUkIl6A0KoAX_isPl9&_nc_ht=scontent.fhan20-1.fna&oh=03_AdRZR1NzL516JxmDug1rrQzHG35imNAFltapiNbFDKSHdQ&oe=657465F2"
}

DATA3 = {
    "imageUrl":"https://scontent.fhan20-1.fna.fbcdn.net/v/t1.15752-9/371473185_1475407749964947_8294815324886515897_n.png?_nc_cat=102&ccb=1-7&_nc_sid=8cd0a2&_nc_eui2=AeEdP7vprJkf2_jcUkkSKu9etFVnvgvvxbu0VWe-C-_Fu_wSfr-LRNbjhRwbLuBBHh92KfCW_e0Sv_C18fDYTt1f&_nc_ohc=r95JODmCoz0AX_Sar80&_nc_ht=scontent.fhan20-1.fna&oh=03_AdRAENkDMrSf_a8nBEo6rCmTFoXilCsKotzdJ8WmjtDw6Q&oe=657450B0"
}

DATA4 = {
        "imageUrl": "https://scontent.fhan20-1.fna.fbcdn.net/v/t1.15752-9/398326633_415580800821187_7809818021847975064_n.jpg?_nc_cat=108&ccb=1-7&_nc_sid=8cd0a2&_nc_eui2=AeE08Hpavs6q8Gn7awKplYEhaW4fMaw5Yftpbh8xrDlh-1mHTPb9eLFRFsViCml8kDPXfOiTx28H-rRiZsIup91z&_nc_ohc=-f7k66nU_bkAX9CDLSq&_nc_oc=AQmMxt33WlGk5q5OyPFi2_IGsfICgZI4amj6S23FBem4cxq--5LHVJo1usZP2AH_qF30pGjjZAZexkO28cxkzPzA&_nc_ht=scontent.fhan20-1.fna&oh=03_AdQvaEBMX54NNe-0zErmksjHZcQ8bzND08jP3z4y1xSAIQ&oe=65744D23",  # Thêm URL ảnh vào phần dữ liệu tùy chỉnh
    }


def auto_mail(receiver_email, frame):
    sender_email = 'sender email'
    sender_password = 'sender_token'

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


class Notification:
    def __init__(self, json_path, token, title="Cảnh báo cháy", body="CHÁY", data=DATA4):
        self.json_path = json_path
        self.token = token
        self.title = title
        self.body = body
        self.data = data
        self.message = messaging.Message(notification=messaging.Notification(title=self.title, body=self.body, image="https://pcccpnn.com/wp-content/uploads/2022/08/PNN-1.jpg"),
                                         token=self.token, data=self.data)
        self.cred = credentials.Certificate(self.json_path)
        self.set()

    def set_token(self, tk):
        self.message = messaging.Message(notification=messaging.Notification(title=self.title, body=self.body, image="https://pcccpnn.com/wp-content/uploads/2022/08/PNN-1.jpg"),
                                         token=tk, data=self.data)

    def set_message(self, body, data):
        self.body = body
        self.data = data
        self.message = messaging.Message(notification=messaging.Notification(title=self.title, body=self.body, image="https://pcccpnn.com/wp-content/uploads/2022/08/PNN-1.jpg"),
                                         token=self.token, data=self.data)

    def set(self):
        firebase_admin.initialize_app(self.cred)

    def send(self):
        response = messaging.send(self.message)
        print("Đã gửi", response)


def notify_user(user_list: list, notification: Notification):
    for token in user_list:
        notification.set_token(token)
        notification.send()


def process_frame(frame):
    auto_mail("nhantrong618@gmail.com", frame)


def process_cam(cap, model, queue):
    ret, frame = cap.read()
    result = model.predict(source=frame, conf=0.5)
    boxes = result[0].boxes
    xyxy = boxes.xyxy.cpu().numpy()
    cls = boxes.cls.cpu().numpy()
    frame = plot_box(frame, xyxy, cls)
    queue.put((frame, cls))


if __name__ == "__main__":
    # image = cv2.imread('test.jpg')
    # image = plot_box(image, np.array([[0, 0, 200, 200], [1, 2, 300, 300]]), [1, 0])
    # cv2.imshow("Rectangle", image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    x = Notification(json_path="new.json", token=TOKEN_LIST[0])

    for i in range(3):
        notify_user(user_list=TOKEN_LIST, notification=x)


