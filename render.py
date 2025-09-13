from functools import cmp_to_key

import pygame
import sys
import scenes
from scene import Scene
from data_helper import *

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

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.DOUBLEBUF)
pygame.display.set_caption("Чәчәк Quest")
clock = pygame.time.Clock()

data = load_game()
print(data)
current_scene: Scene = scenes.scenes[data["scene"]]

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
                
    screen.fill((0, 0, 0))
    scene_info = current_scene.get_draw_data()

    sorted_objects = scene_info["objects"]
    sorted_objects.append(scene_info["player"])
    sorted_objects.sort(key=cmp_to_key(cmp_objects))

    for obj in sorted_objects:
        rect = obj["rect"]
        x_l = rect.x1 * SCALE
        y_t = rect.y1 * SCALE
        width = (rect.x2 - rect.x1) * SCALE
        height = (rect.y2 - rect.y1) * SCALE

        sprite = pygame.image.load(obj["texture_path"]).convert_alpha()
        sprite = pygame.transform.scale(sprite, (width, height))
        rect = sprite.get_rect(topleft=(x_l, y_t))
        screen.blit(sprite, rect)

    if scene_info["ui"]["mode"] == "dialog":
        dialog_rect = pygame.Rect(0, HEIGHT - DIALOG_HEIGHT, WIDTH, DIALOG_HEIGHT)
        pygame.draw.rect(screen, DIALOG_COLOR, dialog_rect, border_radius=20)
        pygame.draw.rect(screen, BORDER_COLOR, dialog_rect, border_radius=20, width=BORDER_WIDTH)
        text_surface = DIALOG_FONT.render(scene_info["ui"]["text"], True, TEXT_COLOR)
        text_rect = text_surface.get_rect(center=dialog_rect.center)
        screen.blit(text_surface, text_rect)
    else:
        if scene_info["ui"]["mode"] == "hint":
            screen.blit(E_SPRITE, E_RECT)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            current_scene.move_forward()
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            current_scene.move_back()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            current_scene.move_left()
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            current_scene.move_right()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()




