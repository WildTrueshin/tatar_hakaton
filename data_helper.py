import json
from typing import List, Dict, Optional


def load_game() -> Dict[str, object]:
    """Load the persisted game data from ``data.json``.

    Ensures that an ``inventory`` list is always present in the result.
    """
    with open("data.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    data.setdefault("inventory", [])
    return data


def save_game(scene_name: str, inventory: Optional[List[Dict[str, str]]] = None) -> None:
    """Persist the current scene and inventory back to ``data.json``.

    If ``inventory`` is omitted the previously saved inventory is kept.
    """
    data = load_game()
    data["scene"] = scene_name
    if inventory is not None:
        data["inventory"] = inventory
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def load_inventory() -> List[Dict[str, str]]:
    """Return the list of inventory items from the save file."""
    return load_game().get("inventory", [])


def add_inventory_item(word: str, texture_path: str) -> None:
    """Append a new item to the inventory and save it."""
    data = load_game()
    items = data.setdefault("inventory", [])
    items.append({"word": word, "texture_path": texture_path})
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

