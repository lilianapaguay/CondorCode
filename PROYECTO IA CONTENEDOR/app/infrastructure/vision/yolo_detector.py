from pathlib import Path
from typing import Any, Union

from ultralytics import YOLO


class YoloDetector:
    def __init__(self, model_path: Union[str, Path]):
        self.model_path = Path(model_path)
        if not self.model_path.exists():
            raise FileNotFoundError(f"Model file not found: {self.model_path}")
        self.model = YOLO(str(self.model_path))

    def predict(
        self,
        source: Any,
        conf: float = 0.35,
        save: bool = False,
        show: bool = False,
        project: Union[str, Path, None] = None,
        name: str | None = None,
    ):
        kwargs = {
            "source": source,
            "conf": conf,
            "save": save,
            "show": show,
        }
        if project is not None:
            kwargs["project"] = str(project)
        if name is not None:
            kwargs["name"] = name
        return self.model.predict(**kwargs)

    def predict_image(
        self,
        image_path: Union[str, Path],
        conf: float = 0.35,
        save: bool = False,
        show: bool = False,
        project: Union[str, Path, None] = None,
        name: str | None = None,
    ):
        image = Path(image_path)
        if not image.exists():
            raise FileNotFoundError(f"Image file not found: {image}")
        return self.predict(
            source=str(image),
            conf=conf,
            save=save,
            show=show,
            project=project,
            name=name,
        )

    def predict_video(
        self,
        video_path: Union[str, Path],
        conf: float = 0.35,
        save: bool = True,
        project: Union[str, Path, None] = None,
        name: str | None = None,
    ):
        video = Path(video_path)
        if not video.exists():
            raise FileNotFoundError(f"Video file not found: {video}")
        return self.predict(
            source=str(video),
            conf=conf,
            save=save,
            show=False,
            project=project,
            name=name,
        )