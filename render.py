import pygame
import sys
import json
import scenes
from scene import Scene
from data_helper import *

pygame.init()

info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h
FPS = 30

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("chehfgerg")
clock = pygame.time.Clock()

dialog_font = pygame.font.SysFont("consolas", 40)

data = load_game()
print(data)
current_scene: Scene = scenes.scenes[data["scene"]]
current_scene_name = data["scene"]

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                save_game(current_scene_name)
                running = False
            if event.key == pygame.K_e:
                new_scene = current_scene.interact()
                if new_scene is not None:
                    current_scene = new_scene
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            current_scene.move_forward()
        if keys[pygame.K_s]:
            current_scene.move_back()
        if keys[pygame.K_a]:
            current_scene.move_left()
        if keys[pygame.K_d]:
            current_scene.move_right()


    screen.fill((0, 0, 0))
    scene_info = current_scene.get_draw_data()

    for object in scene_info["objects"]:
        rect = object["rect"]
        x1 = int(rect.x1 * 5)
        y1 = int(rect.y1 * 5)
        x2 = int(rect.x2 * 5)
        y2 = int(rect.y2 * 5)
        pygame.draw.rect(screen, (100, 200, 50), (x1, y1, x2 - x1, y2 - y1))

    player_rect = scene_info["player_rect"]
    player_x1 = int(player_rect.x1 * 5)
    player_y1 = int(player_rect.y1 * 5)
    player_x2 = int(player_rect.x2 * 5)
    player_y2 = int(player_rect.y2 * 5)
    pygame.draw.rect(screen, (255, 0, 0), (player_x1, player_y1, player_x2 - player_x1, player_y2 - player_y1))

    print(scene_info["ui"])
    if scene_info["ui"]["mode"] == "dialog":
        text_surface = dialog_font.render(scene_info["ui"]["text"], True, (255, 0, 0))
        DH = 200
        rect = pygame.Rect(0, HEIGHT - DH, WIDTH, DH)
        pygame.draw.rect(screen, (255, 255, 255), rect)
        text_rect = text_surface.get_rect(center=rect.center)
        screen.blit(text_surface, text_rect)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()




