from app.domain.entities.alert_result import AlertResult


def build_alert(detected_classes: list[str]) -> AlertResult:
    detected = set(detected_classes)

    if "contenedor_desbordado" in detected and "basura_fuera" in detected:
        return AlertResult(
            alert_level="alto",
            message="Contenedor desbordado con basura fuera. Riesgo de acumulación crítica.",
            recommended_action="Enviar recolección prioritaria e inspección."
        )

    if "contenedor_desbordado" in detected:
        return AlertResult(
            alert_level="alto",
            message="Contenedor desbordado detectado.",
            recommended_action="Priorizar recolección en este punto."
        )

    if "contenedor_lleno" in detected:
        return AlertResult(
            alert_level="medio",
            message="Contenedor lleno detectado.",
            recommended_action="Incluir el punto en el siguiente recorrido."
        )

    return AlertResult(
        alert_level="bajo",
        message="Sin evento crítico.",
        recommended_action="Monitoreo normal."
    )