from datetime import datetime
from pathlib import Path

from fastapi import APIRouter
from fastapi import HTTPException

from app.config.settings import settings
from app.infrastructure.vision.yolo_detector import YoloDetector
from app.application.services.detection_service import process_detection_results
from app.infrastructure.storage.json_logger import save_alert

router = APIRouter()


def _resolve_image_path(image_path: str | None) -> Path:
    if image_path is None:
        return settings.test_image_path

    path = Path(image_path)
    if not path.is_absolute():
        path = Path.cwd() / path
    return path


@router.get("/vision/test")
def vision_test(image_path: str | None = None, conf: float | None = None):
    confidence = conf if conf is not None else settings.default_confidence
    if confidence <= 0 or confidence > 1:
        raise HTTPException(status_code=422, detail="conf must be between 0 and 1")

    try:
        detector = YoloDetector(settings.model_path)
        target_image = _resolve_image_path(image_path)
        results = detector.predict_image(target_image, conf=confidence)
        detections, alert = process_detection_results(results)
        detected_classes = [d.class_name for d in detections]

        payload = {
            "timestamp": datetime.now().isoformat(),
            "model_path": str(settings.model_path),
            "image_path": str(target_image),
            "detected_classes": detected_classes,
            "detections": [d.model_dump() for d in detections],
            "alert_level": alert.alert_level,
            "message": alert.message,
            "recommended_action": alert.recommended_action,
        }
        saved_path = save_alert(payload, output_dir=settings.alerts_dir)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Vision pipeline failed: {exc}") from exc

    return {
        "detected_classes": detected_classes,
        "detections": [d.model_dump() for d in detections],
        "alert": alert.model_dump(),
        "saved_path": saved_path,
    }