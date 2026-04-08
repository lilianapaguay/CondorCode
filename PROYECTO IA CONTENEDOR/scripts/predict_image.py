import argparse
from pathlib import Path

from app.config.settings import settings
from app.infrastructure.vision.yolo_detector import YoloDetector


def parse_args():
	parser = argparse.ArgumentParser(description="Run YOLO prediction on one image")
	parser.add_argument("--source", default=str(settings.test_image_path), help="Path to the input image")
	parser.add_argument("--model", default=str(settings.model_path), help="Path to model weights")
	parser.add_argument("--conf", type=float, default=settings.default_confidence, help="Confidence threshold")
	parser.add_argument("--name", default="image_test", help="Output experiment name")
	return parser.parse_args()


def main() -> None:
	args = parse_args()

	detector = YoloDetector(args.model)
	detector.predict_image(
		image_path=Path(args.source),
		conf=args.conf,
		save=True,
		project=settings.predictions_dir,
		name=args.name,
	)
	print("Prediccion terminada")


if __name__ == "__main__":
	main()