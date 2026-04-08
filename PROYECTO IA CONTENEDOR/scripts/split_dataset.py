import argparse
import random
import shutil
from pathlib import Path

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".webp", ".tif", ".tiff"}


def _ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def _move_all_files(src_dir: Path, dst_dir: Path) -> int:
    _ensure_dir(dst_dir)
    moved = 0
    for file_path in src_dir.glob("*"):
        if file_path.is_file():
            shutil.move(str(file_path), str(dst_dir / file_path.name))
            moved += 1
    return moved


def _collect_train_pairs(train_images: Path, train_labels: Path) -> list[tuple[Path, Path]]:
    pairs: list[tuple[Path, Path]] = []
    for image_path in sorted(train_images.glob("*")):
        if not image_path.is_file() or image_path.suffix.lower() not in IMAGE_EXTS:
            continue
        label_path = train_labels / f"{image_path.stem}.txt"
        if label_path.exists():
            pairs.append((image_path, label_path))
    return pairs


def split_train_valid(dataset_root: Path, val_ratio: float, seed: int, force: bool, dry_run: bool) -> None:
    train_images = dataset_root / "train" / "images"
    train_labels = dataset_root / "train" / "labels"
    valid_images = dataset_root / "valid" / "images"
    valid_labels = dataset_root / "valid" / "labels"

    if not train_images.exists() or not train_labels.exists():
        raise FileNotFoundError("No se encontraron train/images y train/labels en el dataset.")

    if force:
        if valid_images.exists():
            moved_back_images = _move_all_files(valid_images, train_images)
            print(f"[force] Moved back {moved_back_images} images from valid to train")
        if valid_labels.exists():
            moved_back_labels = _move_all_files(valid_labels, train_labels)
            print(f"[force] Moved back {moved_back_labels} labels from valid to train")

    existing_valid_files = 0
    if valid_images.exists():
        existing_valid_files += len([p for p in valid_images.glob("*") if p.is_file()])
    if valid_labels.exists():
        existing_valid_files += len([p for p in valid_labels.glob("*") if p.is_file()])

    if existing_valid_files > 0 and not force:
        raise RuntimeError(
            "valid ya contiene archivos. Usa --force para reconstruir el split sin duplicar datos."
        )

    pairs = _collect_train_pairs(train_images, train_labels)
    total = len(pairs)
    if total < 2:
        raise RuntimeError("Se necesitan al menos 2 pares imagen-label para crear validacion.")

    if not (0.0 < val_ratio < 1.0):
        raise ValueError("val_ratio debe estar entre 0 y 1 (ejemplo: 0.2)")

    val_count = int(round(total * val_ratio))
    val_count = max(1, min(val_count, total - 1))

    rng = random.Random(seed)
    rng.shuffle(pairs)
    valid_pairs = pairs[:val_count]

    print(f"Dataset root: {dataset_root}")
    print(f"Total train pairs found: {total}")
    print(f"Validation pairs to move: {val_count}")

    if dry_run:
        print("Dry run enabled, no files were moved.")
        return

    _ensure_dir(valid_images)
    _ensure_dir(valid_labels)

    moved = 0
    for image_path, label_path in valid_pairs:
        shutil.move(str(image_path), str(valid_images / image_path.name))
        shutil.move(str(label_path), str(valid_labels / label_path.name))
        moved += 1

    print(f"Moved {moved} image+label pairs to valid/")
    print("Split completed successfully.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Split train data into train/valid for YOLO datasets")
    parser.add_argument("--dataset-root", default="data/exports/contenedores_rf", help="Dataset root path")
    parser.add_argument("--val-ratio", type=float, default=0.2, help="Validation ratio (0 < ratio < 1)")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    parser.add_argument("--force", action="store_true", help="Rebuild split by moving valid back into train first")
    parser.add_argument("--dry-run", action="store_true", help="Preview split without moving files")

    args = parser.parse_args()
    split_train_valid(
        dataset_root=Path(args.dataset_root),
        val_ratio=args.val_ratio,
        seed=args.seed,
        force=args.force,
        dry_run=args.dry_run,
    )


if __name__ == "__main__":
    main()
