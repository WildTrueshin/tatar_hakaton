import json

def load_game():
    with open("data.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    return data

def save_game(scene_name):
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump({"scene": scene_name}, f, indent=4)