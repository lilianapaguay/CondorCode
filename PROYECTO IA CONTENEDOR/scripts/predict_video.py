from ultralytics import YOLO

MODEL_PATH = "data/models/contenedores_v1/weights/best.pt"
VIDEO_PATH = "data/raw/videos/contenedores_riobamba.mp4"

model = YOLO(MODEL_PATH)
results = model.predict(source=VIDEO_PATH, save=True, conf=0.35, project="data/predictions", name="video_test")
print("Predicción sobre video terminada")