from scene import *


def home_scene() -> Scene:
    field = StaticObject(
        id='field',
        name='Поле',
        rect=Rect(0, 0, 496, 279),
        solid=False,
        interactable=False,
        texture_path="sprites/backgrounds/home.png",
        z=-1,
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
        texture_path="sprites/objects/house1.png",
        z=2,
    )
    return Scene(
        id="home_scene",
        objects=[field, granny],
        player_pos=(20, 20),
        player_size=(160, 160),
        player_texture_path="sprites/bahtiyar/front.png",
    )


def make_scene_a() -> Scene:
    field = StaticObject(
        id='field',
        name='Поле',
        rect=Rect(0, 0, 496, 279),
        solid=False,
        interactable=False,
        texture_path="sprites/backgrounds/root.png",
        z=-1,
        scale_texture_to_rect=True,
    )
    door = StaticObject(
        id="home_root",
        rect=Rect(200, 100, 250, 150),
        solid=False,
        interactable=True,
        next_scene_factory=home_scene,
        texture_path="sprites/objects/house1.png",
        z=1,
    )

    wall = StaticObject(
        id="wall_1",
        rect=Rect(0, 0, 200, 16),
        solid=True,
        interactable=False,
        texture_path="sprites/objects/house1.png",
        z=0,
        scale_texture_to_rect=True,
    )
    return Scene(
        id="scene_a",
        objects=[field, door, wall],
        player_pos=(30, 90),
        player_size=(16, 16),
        interact_distance=28.0,
        player_texture_path="sprites/bahtiyar/front.png",
        scale_player_texture_to_rect=True,
        player_z=10,
    )


scenes = {
    "menu": make_scene_a()
}
