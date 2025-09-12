import pygame
import sys
import json
import scenes
from scene import Scene
from data_helper import *

pygame.init()

info = pygame.display.Info()
HEIGHT = info.current_h
WIDTH = int(HEIGHT * 16 / 9)
SCALE = HEIGHT / 300
FPS = 30
DIALOG_COLOR = (246, 235, 165)
TEXT_COLOR = (41, 43, 51)
DIALOG_HEIGHT = int(HEIGHT / 5)
DIALOG_FONT = pygame.font.SysFont("consolas", int(HEIGHT / 40))
BORDER_COLOR = (117, 117, 56)
BORDER_WIDTH = int(HEIGHT / 320)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Checheck game")
clock = pygame.time.Clock()

data = load_game()
print(data)
current_scene: Scene = scenes.scenes[data["scene"]]

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
                current_scene = current_scene.interact()
    screen.fill((0, 0, 0))
    scene_info = current_scene.get_draw_data()

    sorted_objects = scene_info["objects"]
    sorted_objects.append(scene_info["player"])
    sorted_objects.sort(key=lambda obj: obj["z"])

    for object in sorted_objects:
        rect = object["rect"]
        x_l = rect.x1 * SCALE
        y_t = rect.y1 * SCALE
        width = (rect.x2 - rect.x1) * SCALE
        height = (rect.y2 - rect.y1) * SCALE

        sprite = pygame.image.load(object["texture_path"]).convert_alpha()
        sprite = pygame.transform.scale(sprite, (width, height))
        rect = sprite.get_rect(topleft=(x_l, y_t))
        screen.blit(sprite, rect)

    if scene_info["ui"]["mode"] == "hint":
        pass
    if scene_info["ui"]["mode"] == "dialog":
        dialog_rect = pygame.Rect(0, HEIGHT - DIALOG_HEIGHT, WIDTH, DIALOG_HEIGHT)
        pygame.draw.rect(screen, DIALOG_COLOR, dialog_rect, border_radius=20)
        pygame.draw.rect(screen, BORDER_COLOR, dialog_rect, border_radius=20, width=BORDER_WIDTH)
        text_surface = DIALOG_FONT.render(scene_info["ui"]["text"], True, TEXT_COLOR)
        text_rect = text_surface.get_rect(center=dialog_rect.center)
        screen.blit(text_surface, text_rect)
    else:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            current_scene.move_forward()
        if keys[pygame.K_s]:
            current_scene.move_back()
        if keys[pygame.K_a]:
            current_scene.move_left()
        if keys[pygame.K_d]:
            current_scene.move_right()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()




