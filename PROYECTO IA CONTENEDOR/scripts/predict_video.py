import argparse
from pathlib import Path

from app.config.settings import settings
from app.infrastructure.vision.yolo_detector import YoloDetector


def parse_args():
	parser = argparse.ArgumentParser(description="Run YOLO prediction on a video file")
	parser.add_argument("--source", default="data/raw/videos/contenedores_riobamba.mp4", help="Path to input video")
	parser.add_argument("--model", default=str(settings.model_path), help="Path to model weights")
	parser.add_argument("--conf", type=float, default=settings.default_confidence, help="Confidence threshold")
	parser.add_argument("--name", default="video_test", help="Output experiment name")
	return parser.parse_args()


def main() -> None:
	args = parse_args()

	detector = YoloDetector(args.model)
	detector.predict_video(
		video_path=Path(args.source),
		conf=args.conf,
		save=True,
		project=settings.predictions_dir,
		name=args.name,
	)
	print("Prediccion sobre video terminada")


if __name__ == "__main__":
	main()