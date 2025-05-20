from ultralytics import YOLO
from pathlib import Path

def analyze_cracks_with_yolo(image_path: str):
    model = YOLO("models/best.pt")
    results = model(image_path)

    original_path = Path(image_path)
    annotated_dir = original_path.parent
    annotated_name = f"annotated_{original_path.name}"
    save_path = annotated_dir / annotated_name

    annotated_dir.mkdir(parents=True, exist_ok=True)
    results[0].save(filename=str(save_path))

    num_cracks = len(results[0].boxes.data)

    return str(save_path), num_cracks
