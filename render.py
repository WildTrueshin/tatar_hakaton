from functools import cmp_to_key

import pygame
import sys
import scenes
from scene import Scene
from data_helper import *
from scenes import scene1

pygame.init()

info = pygame.display.Info()
WIDTH = info.current_w
HEIGHT = int(WIDTH / 16 * 9)
SCALE = HEIGHT / 279
FPS = 30
DIALOG_COLOR = (246, 235, 165)
TEXT_COLOR = (41, 43, 51)
DIALOG_HEIGHT = int(HEIGHT / 5)
DIALOG_FONT = pygame.font.SysFont("consolas", int(HEIGHT / 20))
BORDER_COLOR = (117, 56, 56)
BORDER_WIDTH = int(HEIGHT / 200)
E_SIZE = int(HEIGHT / 10)
E_PATH = "sprites/system/use_e.png"
E_SPRITE = pygame.image.load(E_PATH)
E_SPRITE = pygame.transform.scale(E_SPRITE, (E_SIZE, E_SIZE))
E_RECT = pygame.Rect(0, 0, E_SIZE, E_SIZE)


def draw_inventory(items):
    """Отрисовка окна инвентаря."""
    inv_rect = pygame.Rect(0, 0, WIDTH, HEIGHT)
    pygame.draw.rect(screen, DIALOG_COLOR, inv_rect)
    pygame.draw.rect(screen, BORDER_COLOR, inv_rect, width=BORDER_WIDTH)

    item_size = int(HEIGHT / 6)
    padding = int(item_size * 0.5)
    font_h = DIALOG_FONT.get_height()
    cols = max(1, (WIDTH - padding) // (item_size + padding))
    for i, item in enumerate(items):
        word = item["word"]
        path = item["texture_path"]
        sprite = pygame.image.load(path).convert_alpha()
        sprite = pygame.transform.scale(sprite, (item_size, item_size))
        col = i % cols
        row = i // cols
        x = padding + col * (item_size + padding)
        y = padding + row * (item_size + font_h + padding)
        screen.blit(sprite, (x, y))
        text_surface = DIALOG_FONT.render(word, True, TEXT_COLOR)
        text_rect = text_surface.get_rect(center=(x + item_size // 2, y + item_size + font_h // 2))
        screen.blit(text_surface, text_rect)


def draw_dialog(text, items):
    """Отрисовать диалог с картинками под словами из словаря."""
    dialog_rect = pygame.Rect(0, HEIGHT - DIALOG_HEIGHT, WIDTH, DIALOG_HEIGHT)
    pygame.draw.rect(screen, DIALOG_COLOR, dialog_rect, border_radius=20)
    pygame.draw.rect(screen, BORDER_COLOR, dialog_rect, border_radius=20, width=BORDER_WIDTH)

    words = text.split()
    space_w = DIALOG_FONT.size(" ")[0]
    surfaces = [DIALOG_FONT.render(w, True, TEXT_COLOR) for w in words]
    total_w = sum(s.get_width() for s in surfaces) + space_w * max(0, len(surfaces) - 1)
    x = (WIDTH - total_w) // 2
    y_text = dialog_rect.y + (DIALOG_HEIGHT - DIALOG_FONT.get_height()) // 2

    inventory_map = {item["word"].lower(): item["texture_path"] for item in items}
    for w, surf in zip(words, surfaces):
        screen.blit(surf, (x, y_text))
        clean = w.strip(".,!?;:\"'").lower()
        if clean in inventory_map:
            img = pygame.image.load(inventory_map[clean]).convert_alpha()
            img_size = DIALOG_FONT.get_height()
            img = pygame.transform.scale(img, (img_size, img_size))
            img_rect = img.get_rect(center=(x + surf.get_width() // 2, y_text + surf.get_height() + img_size // 2 + 5))
            screen.blit(img, img_rect)
        x += surf.get_width() + space_w


screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.DOUBLEBUF)
pygame.display.set_caption("Checheck game")
clock = pygame.time.Clock()

data = load_game()
print(data)
#if "scene" not in data.keys():
current_scene: Scene = scene1()
#else:
#    current_scene: Scene = scenes.scenes[data["scene"]]


def cmp_objects(obj1, obj2):
    if obj1["z"] < obj2["z"]:
        return -1
    if obj1["z"] > obj2["z"]:
        return 1
    if obj1["rect"].y2 < obj2["rect"].y2:
        return -1
    return 1


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                save_game(current_scene.get_name())
                running = False
            if event.key == pygame.K_e:
                res = current_scene.interact()
                if res:
                    current_scene = res
            if event.key == pygame.K_q:
                current_scene.toggle_inventory()

    # обновляем позицию игрока до отрисовки
    keys = pygame.key.get_pressed()
    if not current_scene.inventory_open and current_scene.text_window.mode != "dialog":
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            current_scene.move_forward()
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            current_scene.move_back()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            current_scene.move_left()
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            current_scene.move_right()

    scene_info = current_scene.get_draw_data()
    screen.fill((0, 0, 0))

    sorted_objects = scene_info["objects"] + [scene_info["player"]]
    sorted_objects.sort(key=cmp_to_key(cmp_objects))

    for obj in sorted_objects:
        rect = obj["rect"]
        x_l = int(rect.x1 * SCALE)
        y_t = int(rect.y1 * SCALE)
        width = int((rect.x2 - rect.x1) * SCALE)
        height = int((rect.y2 - rect.y1) * SCALE)
    
        if (obj["texture_path"] is not None):
            sprite = pygame.image.load(obj["texture_path"]).convert_alpha()
            sprite = pygame.transform.scale(sprite, (width, height))
            rect = sprite.get_rect(topleft=(x_l, y_t))
            screen.blit(sprite, rect)

    if scene_info["inventory"]["open"]:
        draw_inventory(scene_info["inventory"]["items"])
    elif scene_info["ui"]["mode"] == "dialog":
        draw_dialog(scene_info["ui"]["text"], scene_info["inventory"]["items"])
    else:
        if scene_info["ui"]["mode"] == "hint":
            screen.blit(E_SPRITE, E_RECT)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()




