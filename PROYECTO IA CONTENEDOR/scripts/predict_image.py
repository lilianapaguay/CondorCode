from ultralytics import YOLO

MODEL_PATH = "data/models/contenedores_v1/weights/best.pt"
IMAGE_PATH = "data/samples/test1.jpg"

model = YOLO(MODEL_PATH)
results = model.predict(source=IMAGE_PATH, save=True, conf=0.35, project="data/predictions", name="image_test")
print("Predicción terminada")