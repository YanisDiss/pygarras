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
clock = pygame.time.Clock()
pygame.key.set_repeat(50, 50)


player = (Entity(DEFINITIONS["arena_closer"], c.SPAWN_POINT[0], c.SPAWN_POINT[1]))
if player.color == COLORS["COL_GREY"]:
    player.color = COLORS["COL_BLUE"]

for i in range(150):
    pos = (random.uniform(0, c.ARENA_DIMENSIONS[0]), random.uniform(0, c.ARENA_DIMENSIONS[1]))
    rand = random.randrange(0, 4)
    
    global food
    if rand == 0:
        food = Entity(DEFINITIONS["egg"], pos[0], pos[1])
    if rand == 1:
        food = Entity(DEFINITIONS["square"], pos[0], pos[1])
    if rand == 2:
        food = Entity(DEFINITIONS["triangle"], pos[0], pos[1])
    if rand == 3:
        rand = random.randrange(0, 2)
        if rand == 0:
            food = Entity(DEFINITIONS["pentagon"], pos[0], pos[1])
        if rand == 1:
            rand = random.randrange(0, 2)
            if rand == 0:
                food = Entity(DEFINITIONS["beta_pentagon"], pos[0], pos[1])
            if rand == 1:
                food = Entity(DEFINITIONS["alpha_pentagon"], pos[0], pos[1])
    food.angle = random.uniform(0, math.tau)

while True:
    from inputs import manage_inputs, player_mouse_left, player_move_up, player_move_down, player_move_left, player_move_right
    time_now = pygame.time.get_ticks()
    window.fill(COLORS["COL_OUTER_BACKGROUND"])
    pygame.draw.rect(window, COLORS["COL_BACKGROUND"], pygame.Rect(-(c.CAMERA_X / c.CAMERA_FOV) + c.WINDOW_DIMENSIONS[0] / 2, -(c.CAMERA_Y / c.CAMERA_FOV) + c.WINDOW_DIMENSIONS[1] / 2, c.ARENA_DIMENSIONS[0] / c.CAMERA_FOV, c.ARENA_DIMENSIONS[1] / c.CAMERA_FOV))
    
    draw_grid(int(20 / c.CAMERA_FOV))
    time = pygame.time.Clock()
    delta = time.tick(c.FRAMES_PER_SECOND)
    
    c.CAMERA_FOV += (c.CAMERA_FOV_TARGET - c.CAMERA_FOV) / 10
    
    # do a physics step and draw all entities
    for entity in entities:
        if entity.render:
            draw_entity(entity)
        entity.step(delta)

    # draw entity info
    for entity in entities:
        if entity.render and entity.render_health:
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
    clock.tick(c.FRAMES_PER_SECOND)