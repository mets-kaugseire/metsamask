import json
import os

def load_json(file_path):
    """Load a JSON file and return its content."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)
