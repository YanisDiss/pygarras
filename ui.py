import pygame
import math

import config as c
from colors import COLORS
from globals import window

# ui stuff
pygame.font.init()
ui_stroke_width = 3
ui_offset = 10
ui_minimap_size = 150
large_font = pygame.font.Font("assets/fonts/Ubuntu-Bold.ttf", 20)

def draw_hp_bar(entity):
    render_x = (entity.x - c.CAMERA_X + (c.WINDOW_DIMENSIONS[0] * c.CAMERA_FOV) / 2) / c.CAMERA_FOV
    render_y = (entity.y - c.CAMERA_Y + (c.WINDOW_DIMENSIONS[1] * c.CAMERA_FOV) / 2) / c.CAMERA_FOV
    
    
    render_entity_size = entity.size * (2 / c.CAMERA_FOV)
    render_offset_x = -(entity.size / c.CAMERA_FOV) + render_x
    render_offset_y = (entity.size + 10) / c.CAMERA_FOV + render_y
    
    render_bar_width = 3 / c.CAMERA_FOV
    render_outline_width = 3.5 / c.CAMERA_FOV
    
    if entity.alive and entity.health < entity.max_health:
        health_percentage = entity.health / entity.max_health
        entity.old_health_percentage += (health_percentage - entity.old_health_percentage) * 0.3
        
        pygame.draw.rect(window, COLORS["COL_BLACK"], (render_offset_x - render_outline_width / 2, render_offset_y - render_outline_width / 2, (render_entity_size + render_outline_width)          , render_bar_width + render_outline_width ), 0, 10)
        pygame.draw.rect(window, COLORS["COL_GREEN"], (render_offset_x                           , render_offset_y                           , (render_entity_size * (entity.old_health_percentage)), render_bar_width)                        , 0, 10)


def draw_minimap():
    transparent = pygame.Surface(c.WINDOW_DIMENSIONS, pygame.SRCALPHA)
    pygame.draw.rect(transparent, (*COLORS["COL_BACKGROUND"], 128), ((c.WINDOW_DIMENSIONS[0]-ui_minimap_size-ui_offset, c.WINDOW_DIMENSIONS[1]-ui_minimap_size-ui_offset),(ui_minimap_size, ui_minimap_size)))
    window.blit(transparent, (0, 0))
    pygame.draw.rect(window, COLORS["COL_BLACK"], ((c.WINDOW_DIMENSIONS[0]-ui_minimap_size-ui_offset, c.WINDOW_DIMENSIONS[1]-ui_minimap_size-ui_offset),(ui_minimap_size, ui_minimap_size)), ui_stroke_width)

    # text
    pygarras_text = large_font.render("pygarras.io", True, COLORS["COL_BLACK"])
    window.blit(pygarras_text, (c.WINDOW_DIMENSIONS[0]-ui_offset-108, c.WINDOW_DIMENSIONS[1]-ui_minimap_size-ui_offset - 30))


def draw_minimap_point(entity, color=None):
    point_radius = 2
    color = entity.color if color is None else color
    render_x = (c.WINDOW_DIMENSIONS[0] - ui_minimap_size - ui_offset) + (entity.x / c.ARENA_DIMENSIONS[0]) * ui_minimap_size
    render_y = (c.WINDOW_DIMENSIONS[1] - ui_minimap_size - ui_offset) + (entity.y / c.ARENA_DIMENSIONS[1]) * ui_minimap_size
    
    pygame.draw.circle(window, color, (int(render_x), int(render_y)), point_radius, 0)
