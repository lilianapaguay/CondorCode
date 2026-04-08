import argparse
import cv2
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser(description="Extract frames from a video file")
    parser.add_argument("--video", default="data/raw/videos/contenedores_riobamba.mp4", help="Input video path")
    parser.add_argument("--output", default="data/raw/images", help="Output folder")
    parser.add_argument("--frame-every", type=int, default=20, help="Save one frame every N frames")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    video_path = Path(args.video)
    output_dir = Path(args.output)
    frame_every = max(1, int(args.frame_every))

    if not video_path.exists():
        raise FileNotFoundError(f"Video file not found: {video_path}")

    output_dir.mkdir(parents=True, exist_ok=True)

    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        raise RuntimeError(f"Unable to open video file: {video_path}")

    count = 0
    saved = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if count % frame_every == 0:
            filename = output_dir / f"frame_{saved:05d}.jpg"
            cv2.imwrite(str(filename), frame)
            saved += 1

        count += 1

    cap.release()
    print(f"Frames guardados: {saved}")


if __name__ == "__main__":
    main()