from scene import *

def make_scene_b() -> Scene:
    return Scene(
        id="scene_b",
        objects=[],
        player_pos=(20, 20),
        player_size=(16, 16),
        player_texture_path="assets/player/player_idle.png",
    )


def make_scene_a() -> Scene:
    door = StaticObject(
        id="door_1",
        name="Дверь в сцену B",
        rect=Rect(120, 40, 140, 72),
        solid=False,
        interactable=True,
        next_scene_factory=make_scene_b,
        texture_path="assets/props/door.png",
        z=1,
    )

    wall = StaticObject(
        id="wall_1",
        name="Стена",
        rect=Rect(0, 0, 200, 16),
        solid=True,
        interactable=False,
        texture_path="assets/tiles/wall_top.png",
        z=0,
        scale_texture_to_rect=True,
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
        repeatable=False,
        persist_progress=True,
        texture_path="assets/npc/granny.png",
        z=2,
    )

    return Scene(
        id="scene_a",
        objects=[door, wall, granny],
        player_pos=(30, 90),
        player_size=(16, 16),
        interact_distance=28.0,
        player_texture_path="assets/player/player_idle.png",
        scale_player_texture_to_rect=True,
        player_z=10,
    )

scenes = {
    "menu": make_scene_a()
}