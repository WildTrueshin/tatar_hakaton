from scene import *

home_b = root_b = False


def home_scene() -> Scene:
    global home_b
    if home_b:
        return scenes["home_scene"]
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
        rect=Rect(110, 160, 200, 250),
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
        texture_path="sprites/objects/grandma.png",
        z=0,
    )
    door = StaticObject(
        id="home_scene",
        rect=Rect(20, 20, 120, 220),
        solid=False,
        interactable=True,
        next_scene_factory=root_scene,
        texture_path="sprites/objects/house1.png",
        z=0,
    )
    home_b = True
    return Scene(
        id="home_scene",
        objects=[field, granny, door],
        player_pos=(20, 20),
        player_size=(120, 120),
        player_texture_path=f"sprites/bahtiyar/down{0}.png",
        player_z=0
    )


def root_scene() -> Scene:
    global root_b
    if root_b:
        return scenes["root_scene"]
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
        solid=True,
        interactable=True,
        next_scene_factory=home_scene,
        texture_path="sprites/objects/house1.png",
        z=0,
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
    root_b = True
    return Scene(
        id="scene_a",
        objects=[field, door, wall],
        player_pos=(30, 90),
        player_size=(16, 16),
        interact_distance=28.0,
        player_texture_path=f"sprites/bahtiyar/down{0}.png",
        scale_player_texture_to_rect=True,
        player_z=0,
    )


scenes = {
    "root_scene": root_scene(),
    "home_scene": home_scene()
}
