from ultralytics import YOLO

MODEL_PATH = "data/models/contenedores_v1/weights/best.pt"

model = YOLO(MODEL_PATH)
results = model.predict(source=0, show=True, conf=0.35)