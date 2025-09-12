from scene import *

def make_scene_b() -> Scene:
    return Scene(
        id="scene_b",
        objects=[],
        player_pos=(20, 20),
        player_size=(16, 16)
    )


def make_scene_a() -> Scene:
    door = StaticObject(
        id="door_1",
        name="Дверь в сцену B",
        rect=Rect(120, 40, 140, 72),
        solid=False,
        interactable=True,
        next_scene_factory=make_scene_b,
        sprite_id="spr_door"
    )

    wall = StaticObject(
        id="wall_1",
        name="Стена",
        rect=Rect(0, 0, 200, 16),
        solid=True,
        interactable=False,
        sprite_id="spr_wall"
    )

    granny = NPC(
        id="npc_granny",
        name="Әби",
        rect=Rect(60, 60, 76, 92),
        solid=False,
        interactable=True,
        dialog_lines=[
            "Сәлам!",
            "Как настроение?",
            "Учить — свет, не учить — тьма.",
            "Ладно, увидимся позже!"
        ],
        sprite_id="spr_granny",
        repeatable=False,      # после конца диалога NPC перестанет быть интерактивным
        persist_progress=True  # можно отходить и возвращаться — диалог продолжится
    )

    return Scene(
        id="scene_a",
        objects=[door, wall, granny],
        player_pos=(30, 90),
        player_size=(16, 16),
        interact_distance=28.0
    )

scenes = {
    "menu": make_scene_a()
}