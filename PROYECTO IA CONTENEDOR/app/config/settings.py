from dataclasses import dataclass
import os
from pathlib import Path
from typing import Union

from dotenv import load_dotenv


ROOT_DIR = Path(__file__).resolve().parents[2]
load_dotenv(ROOT_DIR / ".env")


def _resolve_path(path_value: str) -> Path:
	path = Path(path_value)
	if not path.is_absolute():
		path = ROOT_DIR / path
	return path


def _parse_camera_source(raw_value: str) -> Union[int, str]:
	value = raw_value.strip()
	if value.isdigit():
		return int(value)
	return value


@dataclass(frozen=True)
class Settings:
	model_path: Path
	test_image_path: Path
	alerts_dir: Path
	predictions_dir: Path
	default_confidence: float
	default_camera_source: Union[int, str]


def load_settings() -> Settings:
	model_path = _resolve_path(
		os.getenv("MODEL_PATH", "data/models/contenedores_v1/weights/best.pt")
	)
	test_image_path = _resolve_path(
		os.getenv("TEST_IMAGE_PATH", "data/samples/test1.jpg")
	)
	alerts_dir = _resolve_path(os.getenv("ALERTS_DIR", "data/alerts"))
	predictions_dir = _resolve_path(os.getenv("PREDICTIONS_DIR", "data/predictions"))

	conf_raw = os.getenv("CONFIDENCE_THRESHOLD", "0.35")
	try:
		default_confidence = float(conf_raw)
	except ValueError:
		default_confidence = 0.35
	default_confidence = max(0.01, min(default_confidence, 1.0))

	default_camera_source = _parse_camera_source(os.getenv("CAMERA_SOURCE", "0"))

	return Settings(
		model_path=model_path,
		test_image_path=test_image_path,
		alerts_dir=alerts_dir,
		predictions_dir=predictions_dir,
		default_confidence=default_confidence,
		default_camera_source=default_camera_source,
	)


settings = load_settings()
