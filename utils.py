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

def make_color_lighter(color):
    return (min(color[0] + 65, 255), min(color[1] + 65, 255), min(color[2] + 65, 255))

def make_color_darker(color):
    return (color[0] // 2, color[1] // 2, color[2] // 2)