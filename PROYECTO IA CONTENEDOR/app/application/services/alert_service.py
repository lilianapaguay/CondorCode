from app.domain.entities.alert_result import AlertResult


def _normalize_class_name(raw_name: str) -> str:
    normalized = raw_name.strip().lower().replace(" ", "_").replace("-", "_")
    while "__" in normalized:
        normalized = normalized.replace("__", "_")

    if normalized == "detector_de_basura":
        return "basura_fuera"
    return normalized


def build_alert(detected_classes: list[str]) -> AlertResult:
    detected = {_normalize_class_name(name) for name in detected_classes}

    if not detected:
        return AlertResult(
            alert_level="bajo",
            message="Sin detecciones relevantes.",
            recommended_action="Monitoreo normal.",
        )

    if "contenedor_desbordado" in detected and "basura_fuera" in detected:
        return AlertResult(
            alert_level="alto",
            message="Contenedor desbordado con basura fuera. Riesgo de acumulacion critica.",
            recommended_action="Enviar recoleccion prioritaria e inspeccion.",
        )

    if "contenedor_desbordado" in detected:
        return AlertResult(
            alert_level="alto",
            message="Contenedor desbordado detectado.",
            recommended_action="Priorizar recoleccion en este punto.",
        )

    if "basura_fuera" in detected:
        return AlertResult(
            alert_level="medio",
            message="Basura fuera del contenedor detectada.",
            recommended_action="Programar limpieza y revision del punto.",
        )

    if "contenedor_lleno" in detected:
        return AlertResult(
            alert_level="medio",
            message="Contenedor lleno detectado.",
            recommended_action="Incluir el punto en el siguiente recorrido.",
        )

    return AlertResult(
        alert_level="bajo",
        message="Sin evento crítico.",
        recommended_action="Monitoreo normal.",
    )