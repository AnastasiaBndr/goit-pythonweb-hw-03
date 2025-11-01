from urllib.parse import parse_qs
from datetime import datetime
import json


def write_JSON(post_data, path):
    parsed_data = parse_qs(post_data)

    username = parsed_data.get('username', [''])[0]
    message = parsed_data.get('message', [''])[0]
    
    try:
        with open(path, "r", encoding='utf-8') as f:
            messages = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        messages = {}

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    messages[timestamp] = {
        "username": username,
        "message": message
    }

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(messages, f, ensure_ascii=False, indent=2)
