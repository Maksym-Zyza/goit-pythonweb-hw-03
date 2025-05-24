from datetime import datetime
from pathlib import Path
import json


def save_to_storage(data_dict):
    timestamp = str(datetime.now())

    storage_path = Path("storage/data.json")
    storage_path.parent.mkdir(parents=True, exist_ok=True)

    if storage_path.exists():
        with open(storage_path, "r", encoding="utf-8") as f:
            try:
                all_data = json.load(f)
            except json.JSONDecodeError:
                all_data = {}
    else:
        all_data = {}

    all_data[timestamp] = data_dict

    with open(storage_path, "w", encoding="utf-8") as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)
