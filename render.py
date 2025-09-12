import pygame
import sys
import json
import scenes
from data_helper import *

pygame.init()

info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h
FPS = 30

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("chehfgerg")
clock = pygame.time.Clock()

data = load_game()
current_scene = scenes.scenes[data["scene"]]
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
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
sys.exit()




