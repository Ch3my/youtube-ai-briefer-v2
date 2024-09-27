import json

def load_config():
    try:
        with open("config.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            "resumeModel": "gpt-4o-mini",
            "condensaModel": "gpt-4o-mini",
            "resumeChunkSize": 10000,
            "ragModel": "gpt-4o-mini",
            "ragSearchType": "mmr",
            "ragSearchK": 5,
            "ragChunkSize": 1000,
            "useWhisper": "no",
        }