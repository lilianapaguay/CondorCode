from pydantic import BaseModel


class AlertResult(BaseModel):
    alert_level: str
    message: str
    recommended_action: str