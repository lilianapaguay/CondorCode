import cv2
from pathlib import Path

VIDEO_PATH = "data/raw/videos/contenedores_riobamba.mp4"
OUTPUT_DIR = Path("data/raw/images")
FRAME_EVERY = 20  # guarda 1 imagen cada 20 frames

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

cap = cv2.VideoCapture(VIDEO_PATH)

count = 0
saved = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    if count % FRAME_EVERY == 0:
        filename = OUTPUT_DIR / f"frame_{saved:05d}.jpg"
        cv2.imwrite(str(filename), frame)
        saved += 1

    count += 1

cap.release()
print(f"Frames guardados: {saved}")