import math
import pygame
import sys
import random
import json

# file dependencies
from colors import COLORS
import config as c
from globals import entities, window
from ui import draw_hp_bar, draw_minimap, draw_minimap_point
from draw import draw_entity, draw_grid
from utils import get_world_mouse
from entity import Entity, Gun, player_entity_id
from definitions import DEFINITIONS

pygame.init()
pygame.display.set_caption("pygarras")
horloge = pygame.time.Clock()
pygame.key.set_repeat(50, 50)


player = (Entity(DEFINITIONS["booster"], c.SPAWN_POINT[0], c.SPAWN_POINT[1]))
player.color = COLORS["COL_BLUE"]

for i in range(150):
    Entity(DEFINITIONS[random.choice(["egg", "square", "triangle", "pentagon"])], random.randrange(0, c.ARENA_DIMENSIONS[0]), random.randrange(0, c.ARENA_DIMENSIONS[1]))

while True:
    from inputs import manage_inputs, player_mouse_left, player_move_up, player_move_down, player_move_left, player_move_right
    time_now = pygame.time.get_ticks()
    window.fill(COLORS["COL_OUTER_BACKGROUND"])
    pygame.draw.rect(window, COLORS["COL_BACKGROUND"], pygame.Rect(-c.CAMERA_X + c.WINDOW_DIMENSIONS[0] / 2, -c.CAMERA_Y + c.WINDOW_DIMENSIONS[1] / 2, c.ARENA_DIMENSIONS[0], c.ARENA_DIMENSIONS[1]))
    
    draw_grid(int(20 / c.CAMERA_FOV))
    time = pygame.time.Clock()
    delta = time.tick(c.FRAMES_PER_SECOND)
    
    # do a physics step and draw all entities
    for entity in entities:
        entity.step(delta)
        if entity.render and entity.is_visible:
            draw_entity(entity)

    # draw entity info
    for entity in entities:
        if entity.render and entity.render_health and entity.is_visible:
            draw_hp_bar(entity)

    #draw the actual ui
    draw_minimap()
    for entity in entities:
        if entity.render and entity.draw_on_minimap:
            if player_entity_id == entity.id:
                draw_minimap_point(entity, COLORS["COL_BLACK"])
            else: draw_minimap_point(entity)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            manage_inputs(event,"key", 1)
        
        elif event.type == pygame.KEYUP:
            manage_inputs(event,"key", 0)
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            manage_inputs(event,"mouse", 1)
            
        elif event.type == pygame.MOUSEBUTTONUP:
            manage_inputs(event,"mouse", 0)
    

    pygame.display.flip()
    horloge.tick(c.FRAMES_PER_SECOND)