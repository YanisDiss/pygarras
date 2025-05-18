import pygame
import config as c
import math

def get_world_mouse():
    player_mouse = pygame.mouse.get_pos()
    
    x = (player_mouse[0] + c.CAMERA_X - c.WINDOW_DIMENSIONS[0] / 2)
    y = (player_mouse[1] + c.CAMERA_Y - c.WINDOW_DIMENSIONS[1] / 2)
    
    return (x, y)

def is_targeted(entity, mouse_pos):
    difference = math.hypot((entity.x - mouse_pos[0]), (entity.y - mouse_pos[1]))
    return difference < entity.size 