from firebase_admin import messaging
import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate("new.json")
firebase_admin.initialize_app(cred)


# Tạo một thông báo
message = messaging.Message(
    notification=messaging.Notification(title='Cháy',body='Vị trí cháy ở khu vực 1'),
    token="dZc0l7UcTvaoT8F33cr0Ve:APA91bFv9KIRoP7zn4w598G3Ow9_9OPBp57SDwRGg2JaGUSSOriFdQlvMGkw0RW-3G-zzg9OZa8Mdblz2YHrW8Iob9lbNTh6mPGTlX7Mktb0sgtowTcdOsF1dFOREN61q_376ij0a0MA"

)

# Gửi thông báo
for i in range(2):
    response = messaging.send(message)
    print('Đã gửi thông báo:', response)