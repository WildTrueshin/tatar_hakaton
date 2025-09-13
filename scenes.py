"""Game scenes implementing the full quest storyline.

Scene order:
1. Walk to the highlighted grandfather.
2. Talk with grandfather.
3. Walk to the highlighted grandmother.
4. Talk with grandmother (asks for a flower).
5. Walk to the highlighted flower.
6. Talk with flower (learn the word).
7. Return to highlighted grandmother.
8. Final dialog with grandmother.

Interacting with a highlighted object adds the corresponding word and
placeholder image to the player's inventory.
"""

from scene import Scene, StaticObject, NPC, Rect, SceneFactory
from typing import Optional


def make_house_scene(
    id: str,
    outside_factory: SceneFactory,
    highlight: bool = False,
    next_scene_factory: Optional[SceneFactory] = None,
) -> Scene:
    """Generic interior of the left house with grandma."""
    background = StaticObject(
        id="bg",
        rect=Rect(0, 0, 496, 279),
        solid=False,
        interactable=False,
        texture_path="sprites/backgrounds/home.png",
        z=0,
        scale_texture_to_rect=True,
    )
    door = StaticObject(
        id="door_exit",
        rect=Rect(60, 80, 120, 200),
        solid=False,
        interactable=True,
        next_scene_factory=outside_factory,
        texture_path=None,
        z=-1,
    )
    grandma_texture = (
        "sprites/objects/grandma_highlited.png"
        if highlight
        else "sprites/objects/grandma.png"
    )
    ebi = StaticObject(
        id="ebi",
        name="Әби",
        rect=Rect(158, 208, 194, 264),
        solid=False,
        interactable=highlight,
        next_scene_factory=next_scene_factory,
        texture_path=grandma_texture,
        z=1,
    )
    return Scene(
        id=id,
        objects=[background, door, ebi],
        player_pos=(230, 220),
        player_size=(70, 70),
        interact_distance=28.0,
        player_texture_path="sprites/bahtiyar/down0.png",
        scale_player_texture_to_rect=True,
        player_z=2,
    )


def scene1() -> Scene:
    """Walking scene with highlighted grandfather."""
    background = StaticObject(
        id="bg",
        rect=Rect(0, 0, 496, 279),
        solid=False,
        interactable=False,
        texture_path="sprites/backgrounds/root.png",
        z=0,
        scale_texture_to_rect=True,
    )
    house1 = StaticObject(
        id="house1",
        rect=Rect(85, 35, 220, 160),
        solid=False,
        interactable=False,
        texture_path="sprites/objects/house1.png",
        z=1,
    )
    house2 = StaticObject(
        id="house2",
        rect=Rect(330, 110, 475, 240),
        solid=False,
        interactable=False,
        texture_path="sprites/objects/house2.png",
        z=1,
    )
    babay = StaticObject(
        id="babay",
        name="Бабай",
        rect=Rect(360, 212, 390, 255),
        solid=False,
        interactable=True,
        next_scene_factory=scene2,
        texture_path="sprites/objects/grandpa_highlited.png",
        z=1,
    )
    door = StaticObject(
        id="door",
        rect=Rect(85, 35, 220, 160),
        solid=False,
        interactable=True,
        next_scene_factory=lambda: scene1_house(),
        texture_path=None,
        z=1,
    )
    flower = StaticObject(
        id="flower",
        name="Чәчәк",
        rect=Rect(238, 212, 258, 236),
        solid=False,
        interactable=False,
        texture_path="sprites/objects/flower.png",
        z=1,
    )
    well = StaticObject(
        id="well",
        rect=Rect(40, 160, 100, 240),
        solid=False,
        interactable=False,
        texture_path="sprites/bahtiyar/down0.png",
        z=1,
    )
    bucket = StaticObject(
        id="bucket",
        rect=Rect(392, 212, 424, 244),
        solid=False,
        interactable=False,
        texture_path="sprites/bahtiyar/down0.png",
        z=2,
    )
    return Scene(
        id="scene1",
        objects=[background, house1, house2, door, babay, flower, well, bucket],
        player_pos=(150, 170),
        player_size=(35, 35),
        interact_distance=28.0,
        player_texture_path="sprites/bahtiyar/down0.png",
        scale_player_texture_to_rect=True,
        player_z=1,
    )


def scene2() -> Scene:
    """Dialog with grandfather teaching the word 'бабай'."""
    background = StaticObject(
        id="bg",
        rect=Rect(0, 0, 496, 279),
        solid=False,
        interactable=False,
        texture_path="sprites/backgrounds/root.png",
        z=0,
        scale_texture_to_rect=True,
    )
    house1 = StaticObject(
        id="house1",
        rect=Rect(85, 35, 220, 160),
        solid=False,
        interactable=False,
        texture_path="sprites/objects/house1.png",
        z=1,
    )
    house2 = StaticObject(
        id="house2",
        rect=Rect(330, 110, 475, 240),
        solid=False,
        interactable=False,
        texture_path="sprites/objects/house2.png",
        z=1,
    )
    flower = StaticObject(
        id="flower",
        rect=Rect(238, 212, 258, 236),
        solid=False,
        interactable=False,
        texture_path="sprites/objects/flower.png",
        z=1,
    )
    well = StaticObject(
        id="well",
        rect=Rect(40, 160, 100, 240),
        solid=False,
        interactable=False,
        texture_path="sprites/bahtiyar/down0.png",
        z=1,
    )
    bucket = StaticObject(
        id="bucket",
        rect=Rect(392, 212, 424, 244),
        solid=False,
        interactable=False,
        texture_path="sprites/bahtiyar/down0.png",
        z=2,
    )
    babay_big = NPC(
        id="babay_big",
        name="Бабай",
        rect=Rect(40, 212, 70, 255),
        solid=False,
        interactable=True,
        dialog_lines=["Сәлам!"],
        repeatable=False,
        persist_progress=True,
        texture_path="sprites/objects/grandpa.png",
        z=1,
        reward=("бабай", "sprites/objects/grandpa.png"),
        next_scene_factory=scene3,
    )
    scene = Scene(
        id="scene2",
        objects=[background, house1, house2, flower, well, bucket, babay_big],
        player_pos=(-100, -100),
        player_size=(35, 35),
        player_texture_path="sprites/bahtiyar/down0.png",
        player_z=1,
    )
    scene.start_dialog_with(babay_big)
    return scene


def scene3() -> Scene:
    """Walking scene leading to grandmother's house."""
    background = StaticObject(
        id="bg",
        rect=Rect(0, 0, 496, 279),
        solid=False,
        interactable=False,
        texture_path="sprites/backgrounds/root.png",
        z=0,
        scale_texture_to_rect=True,
    )
    house1 = StaticObject(
        id="house1",
        rect=Rect(85, 35, 220, 160),
        solid=False,
        interactable=False,
        texture_path="sprites/objects/house_highlited.png",
        z=1,
    )
    house2 = StaticObject(
        id="house2",
        rect=Rect(330, 110, 475, 240),
        solid=False,
        interactable=False,
        texture_path="sprites/objects/house2.png",
        z=1,
    )
    babay = StaticObject(
        id="babay",
        rect=Rect(360, 212, 390, 255),
        solid=False,
        interactable=False,
        texture_path="sprites/objects/grandpa.png",
        z=1,
    )
    door = StaticObject(
        id="door",
        rect=Rect(85, 35, 220, 160),
        solid=False,
        interactable=True,
        next_scene_factory=lambda: scene3_house(),
        texture_path=None,
        z=1,
    )
    flower = StaticObject(
        id="flower",
        rect=Rect(238, 212, 258, 236),
        solid=False,
        interactable=False,
        texture_path="sprites/objects/flower.png",
        z=1,
    )
    well = StaticObject(
        id="well",
        rect=Rect(40, 160, 100, 240),
        solid=False,
        interactable=False,
        texture_path="sprites/bahtiyar/down0.png",
        z=1,
    )
    bucket = StaticObject(
        id="bucket",
        rect=Rect(392, 212, 424, 244),
        solid=False,
        interactable=False,
        texture_path="sprites/bahtiyar/down0.png",
        z=2,
    )
    return Scene(
        id="scene3",
        objects=[background, house1, house2, door, babay, flower, well, bucket],
        player_pos=(150, 170),
        player_size=(35, 35),
        interact_distance=28.0,
        player_texture_path="sprites/bahtiyar/down0.png",
        scale_player_texture_to_rect=True,
        player_z=1,
    )


def scene4() -> Scene:
    """Dialog with grandmother asking for a flower."""
    background = StaticObject(
        id="bg",
        rect=Rect(0, 0, 496, 279),
        solid=False,
        interactable=False,
        texture_path="sprites/backgrounds/home.png",
        z=0,
        scale_texture_to_rect=True,
    )
    ebi_big = NPC(
        id="ebi_big",
        name="Әби",
        rect=Rect(40, 190, 90, 280),
       solid=False,
        interactable=True,
        dialog_lines=["Исәнмесез, бир миңа чәчәк"],
        repeatable=False,
        persist_progress=True,
        texture_path="sprites/objects/grandma.png",
        z=1,
        reward=("әби", "sprites/objects/grandma.png"),
        next_scene_factory=scene5_house,
    )
    scene = Scene(
        id="scene4",
        objects=[background, ebi_big],
        player_pos=(-100, -100),
        player_size=(90, 90),
        player_texture_path="sprites/bahtiyar/down0.png",
        player_z=1,
    )
    scene.start_dialog_with(ebi_big)
    return scene


def scene5() -> Scene:
    """Walking scene with highlighted flower."""
    background = StaticObject(
        id="bg",
        rect=Rect(0, 0, 496, 279),
        solid=False,
        interactable=False,
        texture_path="sprites/backgrounds/root.png",
        z=0,
        scale_texture_to_rect=True,
    )
    house1 = StaticObject(
        id="house1",
        rect=Rect(85, 35, 220, 160),
        solid=False,
        interactable=False,
        texture_path="sprites/objects/house1.png",
        z=1,
    )
    house2 = StaticObject(
        id="house2",
        rect=Rect(330, 110, 475, 240),
        solid=False,
        interactable=False,
        texture_path="sprites/objects/house2.png",
        z=1,
    )
    babay = StaticObject(
        id="babay",
        rect=Rect(360, 212, 390, 255),
        solid=False,
        interactable=False,
        texture_path="sprites/objects/grandpa.png",
        z=1,
    )
    door = StaticObject(
        id="door",
        rect=Rect(85, 35, 220, 160),
        solid=False,
        interactable=True,
        next_scene_factory=lambda: scene5_house(),
        texture_path=None,
        z=1,
    )
    flower = StaticObject(
        id="flower",
        name="Чәчәк",
        rect=Rect(238, 212, 258, 236),
        solid=False,
        interactable=True,
        next_scene_factory=scene6,
        texture_path="sprites/objects/flower_highlited.png",
        z=1,
    )
    well = StaticObject(
        id="well",
        rect=Rect(40, 160, 100, 240),
        solid=False,
        interactable=False,
        texture_path="sprites/bahtiyar/down0.png",
        z=1,
    )
    bucket = StaticObject(
        id="bucket",
        rect=Rect(392, 212, 424, 244),
        solid=False,
        interactable=False,
        texture_path="sprites/bahtiyar/down0.png",
        z=2,
    )
    return Scene(
        id="scene5",
        objects=[background, house1, house2, door, babay, flower, well, bucket],
        player_pos=(150, 170),
        player_size=(35, 35),
        interact_distance=28.0,
        player_texture_path="sprites/bahtiyar/down0.png",
        scale_player_texture_to_rect=True,
        player_z=1,
    )


def scene6() -> Scene:
    """Dialog with flower teaching the word 'чәчәк'."""
    background = StaticObject(
        id="bg",
        rect=Rect(0, 0, 496, 279),
        solid=False,
        interactable=False,
        texture_path="sprites/backgrounds/root.png",
        z=0,
        scale_texture_to_rect=True,
    )
    house1 = StaticObject(
        id="house1",
        rect=Rect(85, 35, 220, 160),
        solid=False,
        interactable=False,
        texture_path="sprites/objects/house1.png",
        z=1,
    )
    house2 = StaticObject(
        id="house2",
        rect=Rect(330, 110, 475, 240),
        solid=False,
        interactable=False,
        texture_path="sprites/objects/house2.png",
        z=1,
    )
    babay = StaticObject(
        id="babay",
        rect=Rect(360, 212, 390, 255),
        solid=False,
        interactable=False,
        texture_path="sprites/objects/grandpa.png",
        z=1,
    )
    well = StaticObject(
        id="well",
        rect=Rect(40, 160, 100, 240),
        solid=False,
        interactable=False,
        texture_path="sprites/bahtiyar/down0.png",
        z=1,
    )
    bucket = StaticObject(
        id="bucket",
        rect=Rect(392, 212, 424, 244),
        solid=False,
        interactable=False,
        texture_path="sprites/bahtiyar/down0.png",
        z=2,
    )
    flower_big = NPC(
        id="flower_big",
        name="Чәчәк",
        rect=Rect(238, 212, 258, 236),
        solid=False,
        interactable=True,
        dialog_lines=["Чәчәк"],
        repeatable=False,
        persist_progress=True,
        texture_path="sprites/objects/flower.png",
        z=1,
        reward=("чәчәк", "sprites/objects/flower.png"),
        next_scene_factory=scene7,
    )
    scene = Scene(
        id="scene6",
        objects=[background, house1, house2, babay, well, bucket, flower_big],
        player_pos=(-100, -100),
        player_size=(35, 35),
        player_texture_path="sprites/bahtiyar/down0.png",
        player_z=1,
    )
    scene.start_dialog_with(flower_big)
    return scene


def scene7() -> Scene:
    """Walking scene returning to grandmother with the flower."""
    background = StaticObject(
        id="bg",
        rect=Rect(0, 0, 496, 279),
        solid=False,
        interactable=False,
        texture_path="sprites/backgrounds/root.png",
        z=0,
        scale_texture_to_rect=True,
    )
    house1 = StaticObject(
        id="house1",
        rect=Rect(85, 35, 220, 160),
        solid=False,
        interactable=False,
        texture_path="sprites/objects/house_highlited.png",
        z=1,
    )
    house2 = StaticObject(
        id="house2",
        rect=Rect(330, 110, 475, 240),
        solid=False,
        interactable=False,
        texture_path="sprites/objects/house2.png",
        z=1,
    )
    babay = StaticObject(
        id="babay",
        rect=Rect(360, 212, 390, 255),
        solid=False,
        interactable=False,
        texture_path="sprites/objects/grandpa.png",
        z=1,
    )
    door = StaticObject(
        id="door",
        rect=Rect(85, 35, 220, 160),
        solid=False,
        interactable=True,
        next_scene_factory=lambda: scene7_house(),
        texture_path=None,
        z=1,
    )
    well = StaticObject(
        id="well",
        rect=Rect(40, 160, 100, 240),
        solid=False,
        interactable=False,
        texture_path="sprites/bahtiyar/down0.png",
        z=1,
    )
    bucket = StaticObject(
        id="bucket",
        rect=Rect(392, 212, 424, 244),
        solid=False,
        interactable=False,
        texture_path="sprites/bahtiyar/down0.png",
        z=2,
    )
    return Scene(
        id="scene7",
        objects=[background, house1, house2, door, babay, well, bucket],
        player_pos=(150, 170),
        player_size=(35, 35),
        interact_distance=28.0,
        player_texture_path="sprites/bahtiyar/down0.png",
        scale_player_texture_to_rect=True,
        player_z=1,
    )


def scene8() -> Scene:
    """Final dialog where grandmother thanks the player."""
    background = StaticObject(
        id="bg",
        rect=Rect(0, 0, 496, 279),
        solid=False,
        interactable=False,
        texture_path="sprites/backgrounds/home.png",
        z=0,
        scale_texture_to_rect=True,
    )
    ebi_big = NPC(
        id="ebi_big_final",
        name="Әби",
        rect=Rect(38, 190, 90, 280),
        solid=False,
        interactable=True,
        dialog_lines=["Рәхмәт"],
        repeatable=False,
        persist_progress=True,
        texture_path="sprites/objects/grandma.png",
        z=1,
        next_scene_factory=scene9,
    )
    scene = Scene(
        id="scene8",
        objects=[background, ebi_big],
        player_pos=(-100, -100),
        player_size=(80, 80),
        player_texture_path="sprites/bahtiyar/down0.png",
        player_z=1,
    )
    scene.start_dialog_with(ebi_big)
    return scene


def scene9() -> Scene:
    """Walking scene with highlighted door leading to the next quest."""
    background = StaticObject(
        id="bg",
        rect=Rect(0, 0, 496, 279),
        solid=False,
        interactable=False,
        texture_path="sprites/backgrounds/root.png",
        z=0,
        scale_texture_to_rect=True,
    )
    house1 = StaticObject(
        id="house1",
        rect=Rect(85, 35, 220, 160),
        solid=False,
        interactable=False,
        texture_path="sprites/objects/house_highlited.png",
        z=1,
    )
    house2 = StaticObject(
        id="house2",
        rect=Rect(330, 110, 475, 240),
        solid=False,
        interactable=False,
        texture_path="sprites/objects/house2.png",
        z=1,
    )
    babay = StaticObject(
        id="babay",
        rect=Rect(360, 212, 390, 255),
        solid=False,
        interactable=False,
        texture_path="sprites/objects/grandpa.png",
        z=1,
    )
    ebi = StaticObject(
        id="ebi",
        name="Әби",
        rect=Rect(158, 208, 194, 264),
        solid=False,
        interactable=False,
        texture_path="sprites/objects/grandma.png",
        z=1,
    )
    door = StaticObject(
        id="door",
        rect=Rect(85, 35, 220, 160),
        solid=False,
        interactable=True,
        next_scene_factory=scene10,
        texture_path="sprites/bahtiyar/down0.png",
        z=1,
    )
    well = StaticObject(
        id="well",
        rect=Rect(40, 160, 100, 240),
        solid=False,
        interactable=False,
        texture_path="sprites/bahtiyar/down0.png",
        z=1,
    )
    bucket = StaticObject(
        id="bucket",
        name="Су",
        rect=Rect(392, 212, 424, 244),
        solid=False,
        interactable=False,
        texture_path="sprites/bahtiyar/down0.png",
        z=2,
    )
    return Scene(
        id="scene9",
        objects=[background, house1, house2, door, babay, ebi, well, bucket],
        player_pos=(150, 170),
        player_size=(35, 35),
        interact_distance=28.0,
        player_texture_path="sprites/bahtiyar/down0.png",
        scale_player_texture_to_rect=True,
        player_z=1,
    )


def scene10() -> Scene:
    """Dialog at the door teaching the word 'ишек'."""
    background = StaticObject(
        id="bg",
        rect=Rect(0, 0, 496, 279),
        solid=False,
        interactable=False,
        texture_path="sprites/backgrounds/root.png",
        z=0,
        scale_texture_to_rect=True,
    )
    well = StaticObject(
        id="well",
        rect=Rect(40, 160, 100, 240),
        solid=False,
        interactable=False,
        texture_path="sprites/bahtiyar/down0.png",
        z=1,
    )
    bucket = StaticObject(
        id="bucket",
        rect=Rect(392, 212, 424, 244),
        solid=False,
        interactable=False,
        texture_path="sprites/bahtiyar/down0.png",
        z=2,
    )
    door_big = NPC(
        id="door_big",
        name="Ишек",
        rect=Rect(40, 180, 140, 280),
        solid=False,
        interactable=True,
        dialog_lines=["Ишек", "Өйгә рәхим ит!"],
        repeatable=False,
        persist_progress=True,
        texture_path="sprites/bahtiyar/down0.png",
        z=1,
        reward=("ишек", "sprites/bahtiyar/down0.png"),
        next_scene_factory=scene11,
    )
    scene = Scene(
        id="scene10",
        objects=[background, well, bucket, door_big],
        player_pos=(-100, -100),
        player_size=(80, 80),
        player_texture_path="sprites/bahtiyar/down0.png",
        player_z=1,
    )
    scene.start_dialog_with(door_big)
    return scene


def scene11() -> Scene:
    """House interior with highlighted book."""
    background = StaticObject(
        id="bg",
        rect=Rect(0, 0, 496, 279),
        solid=False,
        interactable=False,
        texture_path="sprites/backgrounds/home.png",
        z=0,
        scale_texture_to_rect=True,
    )
    door_exit = StaticObject(
        id="door_exit",
        rect=Rect(60, 80, 120, 200),
        solid=False,
        interactable=True,
        next_scene_factory=scene9,
        texture_path=None,
        z=-1,
    )
    book = StaticObject(
        id="book",
        name="Китап",
        rect=Rect(340, 170, 380, 210),
        solid=False,
        interactable=True,
        next_scene_factory=scene12,
        texture_path="sprites/bahtiyar/down0.png",
        z=1,
    )
    ebi = StaticObject(
        id="ebi",
        name="Әби",
        rect=Rect(158, 208, 194, 264),
        solid=False,
        interactable=False,
        texture_path="sprites/objects/grandma.png",
        z=1,
    )
    samovar = StaticObject(
        id="samovar",
        rect=Rect(60, 200, 92, 232),
        solid=False,
        interactable=False,
        texture_path="sprites/bahtiyar/down0.png",
        z=1,
    )
    return Scene(
        id="scene11",
        objects=[background, door_exit, book, ebi, samovar],
        player_pos=(230, 220),
        player_size=(70, 70),
        interact_distance=28.0,
        player_texture_path="sprites/bahtiyar/down0.png",
        scale_player_texture_to_rect=True,
        player_z=2,
    )


def scene12() -> Scene:
    """Dialog with the book teaching the word 'китап'."""
    background = StaticObject(
        id="bg",
        rect=Rect(0, 0, 496, 279),
        solid=False,
        interactable=False,
        texture_path="sprites/backgrounds/home.png",
        z=0,
        scale_texture_to_rect=True,
    )
    book_big = NPC(
        id="book_big",
        name="Китап",
        rect=Rect(40, 180, 140, 280),
        solid=False,
        interactable=True,
        dialog_lines=["Китап"],
        repeatable=False,
        persist_progress=True,
        texture_path="sprites/bahtiyar/down0.png",
        z=1,
        reward=("китап", "sprites/bahtiyar/down0.png"),
        next_scene_factory=scene14,
    )
    scene = Scene(
        id="scene12",
        objects=[background, book_big],
        player_pos=(-100, -100),
        player_size=(80, 80),
        player_texture_path="sprites/bahtiyar/down0.png",
        player_z=1,
    )
    scene.start_dialog_with(book_big)
    return scene


def scene13() -> Scene:
    """House interior after grandmother's request for water."""
    background = StaticObject(
        id="bg",
        rect=Rect(0, 0, 496, 279),
        solid=False,
        interactable=False,
        texture_path="sprites/backgrounds/home.png",
        z=0,
        scale_texture_to_rect=True,
    )
    door_exit = StaticObject(
        id="door_exit",
        rect=Rect(60, 80, 120, 200),
        solid=False,
        interactable=True,
        next_scene_factory=scene15,
        texture_path=None,
        z=-1,
    )
    ebi = StaticObject(
        id="ebi",
        name="Әби",
        rect=Rect(158, 208, 194, 264),
        solid=False,
        interactable=False,
        texture_path="sprites/objects/grandma.png",
        z=1,
    )
    samovar = StaticObject(
        id="samovar",
        rect=Rect(60, 200, 92, 232),
        solid=False,
        interactable=False,
        texture_path="sprites/bahtiyar/down0.png",
        z=1,
    )
    return Scene(
        id="scene13",
        objects=[background, door_exit, ebi, samovar],
        player_pos=(230, 220),
        player_size=(70, 70),
        interact_distance=28.0,
        player_texture_path="sprites/bahtiyar/down0.png",
        scale_player_texture_to_rect=True,
        player_z=2,
    )


def scene14() -> Scene:
    """Dialog where grandmother asks for water."""
    background = StaticObject(
        id="bg",
        rect=Rect(0, 0, 496, 279),
        solid=False,
        interactable=False,
        texture_path="sprites/backgrounds/home.png",
        z=0,
        scale_texture_to_rect=True,
    )
    ebi_big = NPC(
        id="ebi_big_water",
        name="Әби",
        rect=Rect(38, 190, 90, 280),
        solid=False,
        interactable=True,
        dialog_lines=["Миңа су алып кил әле"],
        repeatable=False,
        persist_progress=True,
        texture_path="sprites/objects/grandma.png",
        z=1,
        next_scene_factory=scene13,
    )
    scene = Scene(
        id="scene14",
        objects=[background, ebi_big],
        player_pos=(-100, -100),
        player_size=(80, 80),
        player_texture_path="sprites/bahtiyar/down0.png",
        player_z=1,
    )
    scene.start_dialog_with(ebi_big)
    return scene


def scene15() -> Scene:
    """Yard scene with bucket near the grandfather."""
    background = StaticObject(
        id="bg",
        rect=Rect(0, 0, 496, 279),
        solid=False,
        interactable=False,
        texture_path="sprites/backgrounds/root.png",
        z=0,
        scale_texture_to_rect=True,
    )
    house1 = StaticObject(
        id="house1",
        rect=Rect(85, 35, 220, 160),
        solid=False,
        interactable=False,
        texture_path="sprites/objects/house1.png",
        z=1,
    )
    house2 = StaticObject(
        id="house2",
        rect=Rect(330, 110, 475, 240),
        solid=False,
        interactable=False,
        texture_path="sprites/objects/house2.png",
        z=1,
    )
    well = StaticObject(
        id="well",
        rect=Rect(40, 160, 100, 240),
        solid=False,
        interactable=False,
        texture_path="sprites/bahtiyar/down0.png",
        z=1,
    )
    bucket = StaticObject(
        id="bucket",
        name="Су",
        rect=Rect(392, 212, 424, 244),
        solid=False,
        interactable=True,
        next_scene_factory=scene16,
        texture_path="sprites/bahtiyar/down0.png",
        z=2,
    )
    babay = StaticObject(
        id="babay",
        rect=Rect(360, 212, 390, 255),
        solid=False,
        interactable=False,
        texture_path="sprites/objects/grandpa.png",
        z=1,
    )
    door = StaticObject(
        id="door",
        rect=Rect(85, 35, 220, 160),
        solid=False,
        interactable=True,
        next_scene_factory=scene17,
        texture_path="sprites/bahtiyar/down0.png",
        z=1,
    )
    return Scene(
        id="scene15",
        objects=[background, house1, house2, door, well, bucket, babay],
        player_pos=(150, 170),
        player_size=(35, 35),
        interact_distance=28.0,
        player_texture_path="sprites/bahtiyar/down0.png",
        scale_player_texture_to_rect=True,
        player_z=1,
    )


def scene16() -> Scene:
    """Dialog with bucket teaching the word 'су'."""
    background = StaticObject(
        id="bg",
        rect=Rect(0, 0, 496, 279),
        solid=False,
        interactable=False,
        texture_path="sprites/backgrounds/root.png",
        z=0,
        scale_texture_to_rect=True,
    )
    bucket_big = NPC(
        id="bucket_big",
        name="Су",
        rect=Rect(40, 180, 140, 280),
        solid=False,
        interactable=True,
        dialog_lines=["Су"],
        repeatable=False,
        persist_progress=True,
        texture_path="sprites/bahtiyar/down0.png",
        z=1,
        reward=("су", "sprites/bahtiyar/down0.png"),
        next_scene_factory=scene15,
    )
    scene = Scene(
        id="scene16",
        objects=[background, bucket_big],
        player_pos=(-100, -100),
        player_size=(80, 80),
        player_texture_path="sprites/bahtiyar/down0.png",
        player_z=1,
    )
    scene.start_dialog_with(bucket_big)
    return scene


def scene17() -> Scene:
    """House interior returning with water."""
    background = StaticObject(
        id="bg",
        rect=Rect(0, 0, 496, 279),
        solid=False,
        interactable=False,
        texture_path="sprites/backgrounds/home.png",
        z=0,
        scale_texture_to_rect=True,
    )
    door_exit = StaticObject(
        id="door_exit",
        rect=Rect(60, 80, 120, 200),
        solid=False,
        interactable=True,
        next_scene_factory=scene15,
        texture_path=None,
        z=-1,
    )
    bucket = StaticObject(
        id="bucket",
        rect=Rect(240, 180, 272, 212),
        solid=False,
        interactable=False,
        texture_path="sprites/bahtiyar/down0.png",
        z=1,
    )
    ebi = StaticObject(
        id="ebi",
        name="Әби",
        rect=Rect(158, 208, 194, 264),
        solid=False,
        interactable=True,
        next_scene_factory=scene18,
        texture_path="sprites/objects/grandma_highlited.png",
        z=1,
    )
    samovar = StaticObject(
        id="samovar",
        rect=Rect(60, 200, 92, 232),
        solid=False,
        interactable=False,
        texture_path="sprites/bahtiyar/down0.png",
        z=1,
    )
    return Scene(
        id="scene17",
        objects=[background, door_exit, bucket, ebi, samovar],
        player_pos=(230, 220),
        player_size=(70, 70),
        interact_distance=28.0,
        player_texture_path="sprites/bahtiyar/down0.png",
        scale_player_texture_to_rect=True,
        player_z=2,
    )


def scene18() -> Scene:
    """Final dialog with grandmother and samovar."""
    background = StaticObject(
        id="bg",
        rect=Rect(0, 0, 496, 279),
        solid=False,
        interactable=False,
        texture_path="sprites/backgrounds/home.png",
        z=0,
        scale_texture_to_rect=True,
    )
    samovar = StaticObject(
        id="samovar",
        rect=Rect(60, 200, 92, 232),
        solid=False,
        interactable=False,
        texture_path="sprites/bahtiyar/down0.png",
        z=1,
    )
    ebi_big = NPC(
        id="ebi_big_final2",
        name="Әби",
        rect=Rect(38, 190, 90, 280),
        solid=False,
        interactable=True,
        dialog_lines=["Рәхмәт! Хәзер чәй эчәбез"],
        repeatable=False,
        persist_progress=True,
        texture_path="sprites/objects/grandma.png",
        z=1,
        next_scene_factory=scene17,
    )
    scene = Scene(
        id="scene18",
        objects=[background, samovar, ebi_big],
        player_pos=(-100, -100),
        player_size=(80, 80),
        player_texture_path="sprites/bahtiyar/down0.png",
        player_z=1,
    )
    scene.start_dialog_with(ebi_big)
    return scene


def scene1_house() -> Scene:
    return make_house_scene("scene1_house", scene1)


def scene3_house() -> Scene:
    return make_house_scene("scene3_house", scene3, True, scene4)


def scene5_house() -> Scene:
    return make_house_scene("scene5_house", scene5)


def scene7_house() -> Scene:
    return make_house_scene("scene7_house", scene7, True, scene8)


scenes = {
    "scene1": scene1(),
    "scene2": scene2(),
    "scene3": scene3(),
    "scene4": scene4(),
    "scene5": scene5(),
    "scene6": scene6(),
    "scene7": scene7(),
    "scene8": scene8(),
    "scene9": scene9(),
    "scene10": scene10(),
    "scene11": scene11(),
    "scene12": scene12(),
    "scene13": scene13(),
    "scene14": scene14(),
    "scene15": scene15(),
    "scene16": scene16(),
    "scene17": scene17(),
    "scene18": scene18(),
    "scene1_house": scene1_house(),
    "scene3_house": scene3_house(),
    "scene5_house": scene5_house(),
    "scene7_house": scene7_house(),
}

