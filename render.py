import pygame
import sys
import json
import scenes

pygame.init()

info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h
FPS = 30

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("chehfgerg")
clock = pygame.time.Clock()

with open("data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

current_scene = scenes.scenes[data["scene"]]

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
sys.exit()




