from app.application.services.alert_service import build_alert
from app.domain.entities.detection_result import DetectionResult


_CLASS_ALIASES = {
    "basura_fuera": "basura_fuera",
    "contenedor_desbordado": "contenedor_desbordado",
    "contenedor_lleno": "contenedor_lleno",
    "contenedor_medio": "contenedor_medio",
    "contenedor_vacio": "contenedor_vacio",
    "detector_de_basura": "basura_fuera",
}


def normalize_class_name(raw_name: str) -> str:
    normalized = raw_name.strip().lower().replace(" ", "_").replace("-", "_")
    while "__" in normalized:
        normalized = normalized.replace("__", "_")
    return _CLASS_ALIASES.get(normalized, normalized)


def extract_detections(results) -> list[DetectionResult]:
    detections: list[DetectionResult] = []

    for result in results:
        names = result.names
        if result.boxes is not None:
            for box in result.boxes:
                class_id = int(box.cls[0].item())
                confidence = float(box.conf[0].item()) if box.conf is not None else 0.0

                if isinstance(names, dict):
                    raw_class_name = str(names.get(class_id, class_id))
                else:
                    raw_class_name = str(names[class_id])

                detections.append(
                    DetectionResult(
                        class_name=normalize_class_name(raw_class_name),
                        confidence=round(confidence, 4),
                    )
                )

    return detections


def extract_detected_classes(results) -> list[str]:
    return [detection.class_name for detection in extract_detections(results)]



def process_detection_results(results):
    detections = extract_detections(results)
    detected_classes = [d.class_name for d in detections]
    alert = build_alert(detected_classes)
    return detections, alert