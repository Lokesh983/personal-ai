import json
import os

DATA_PATH = os.path.join("data", "memory.json")


def load_all_records():
    if not os.path.exists(DATA_PATH):
        return []
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def append_record(record):
    records = load_all_records()
    records.append(record)
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2)
