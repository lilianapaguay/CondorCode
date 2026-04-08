from typing import Any

import cv2


def draw_detection_boxes(frame, result: Any):
	output = frame.copy()
	if result.boxes is None:
		return output

	names = result.names

	for box in result.boxes:
		x1, y1, x2, y2 = [int(v) for v in box.xyxy[0].tolist()]
		class_id = int(box.cls[0].item())
		confidence = float(box.conf[0].item()) if box.conf is not None else 0.0

		label = names.get(class_id, str(class_id)) if isinstance(names, dict) else names[class_id]
		text = f"{label} {confidence:.2f}"

		cv2.rectangle(output, (x1, y1), (x2, y2), (0, 220, 0), 2)
		cv2.putText(output, text, (x1, max(y1 - 10, 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 220, 0), 2)

	return output
