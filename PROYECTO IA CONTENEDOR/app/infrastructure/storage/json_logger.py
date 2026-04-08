import json
from pathlib import Path
from datetime import datetime
from typing import Any, Optional, Union


def save_alert(alert_data: dict[str, Any], output_dir: Optional[Union[str, Path]] = None):
    output_dir = Path(output_dir) if output_dir is not None else Path("data/alerts")
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    file_path = output_dir / f"alert_{timestamp}.json"

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(alert_data, f, ensure_ascii=False, indent=2)

    return str(file_path)