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
    
    outline_width = 3.5
    bar_width = 3
    if entity.alive and entity.health < entity.max_health:
        health_percentage = entity.health / entity.max_health
        entity.old_health_percentage += (health_percentage - entity.old_health_percentage) * 0.3

        #start_x = render_x - entity.size - width/2
        #start_y = render_y + entity.size + 10 - width/2
        #end_x = render_x + entity.size * 2 + width
        #end_y = render_y + entity.size + 10 - width/2
        #pygame.draw.line(window, COL_BLACK, (start_x, start_y), (end_x, end_y), 6)
        #pygame.draw.line(window, COL_GREEN, (start_x, start_y), (end_x * (entity.old_health_percentage), end_y), 3)
        
        pygame.draw.rect(window, COLORS["COL_BLACK"], (render_x - entity.size - outline_width / 2, render_y + entity.size + 10 - outline_width / 2, (entity.size * 2 + outline_width), bar_width + outline_width ), 0, 10)
        pygame.draw.rect(window, COLORS["COL_GREEN"], (render_x - entity.size                    , render_y + entity.size + 10                    , (entity.size * 2 * (entity.old_health_percentage)), bar_width), 0, 10)


def draw_minimap():
    transparent = pygame.Surface(c.WINDOW_DIMENSIONS, pygame.SRCALPHA)
    pygame.draw.rect(transparent, (*COLORS["COL_BACKGROUND"], 128), ((c.WINDOW_DIMENSIONS[0]-ui_minimap_size-ui_offset, c.WINDOW_DIMENSIONS[1]-ui_minimap_size-ui_offset),(ui_minimap_size, ui_minimap_size)))
    window.blit(transparent, (0, 0))
    pygame.draw.rect(window, COLORS["COL_BLACK"], ((c.WINDOW_DIMENSIONS[0]-ui_minimap_size-ui_offset, c.WINDOW_DIMENSIONS[1]-ui_minimap_size-ui_offset),(ui_minimap_size, ui_minimap_size)), ui_stroke_width)

    # text
    text = large_font.render("pygarras.io", True, COLORS["COL_BLACK"])
    window.blit(text, (c.WINDOW_DIMENSIONS[0]-ui_minimap_size-ui_offset + 40, c.WINDOW_DIMENSIONS[1]-ui_minimap_size-ui_offset - 30))


def draw_minimap_point(entity, color=None):
    point_radius = 2
    color = entity.color if color is None else color
    render_x = (c.WINDOW_DIMENSIONS[0] - ui_minimap_size - ui_offset) + (entity.x / c.ARENA_DIMENSIONS[0]) * ui_minimap_size
    render_y = (c.WINDOW_DIMENSIONS[1] - ui_minimap_size - ui_offset) + (entity.y / c.ARENA_DIMENSIONS[1]) * ui_minimap_size
    
    pygame.draw.circle(window, color, (int(render_x), int(render_y)), point_radius, 0)
