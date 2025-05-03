# Stamp loading, filtering, and selection
import json
import os


def load_stamps():
    path = "data/stamps.json"
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return []
