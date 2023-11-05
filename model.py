from ultralytics import YOLO


model = YOLO('C:/Users/Truongpc/PycharmProjects/FireWaring/FWm.pt')
model.export(format='onnx')