import argparse

from app.config.settings import settings
from app.infrastructure.vision.yolo_detector import YoloDetector


def _parse_source(value: str):
	cleaned = value.strip()
	if cleaned.isdigit():
		return int(cleaned)
	return cleaned


def parse_args():
	parser = argparse.ArgumentParser(description="Run YOLO prediction on webcam/IP stream")
	parser.add_argument("--source", default=str(settings.default_camera_source), help="Camera index or stream URL")
	parser.add_argument("--model", default=str(settings.model_path), help="Path to model weights")
	parser.add_argument("--conf", type=float, default=settings.default_confidence, help="Confidence threshold")
	return parser.parse_args()


def main() -> None:
	args = parse_args()

	detector = YoloDetector(args.model)
	detector.predict(
		source=_parse_source(args.source),
		conf=args.conf,
		save=False,
		show=True,
	)


if __name__ == "__main__":
	main()