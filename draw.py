import pygame
import math
import random

from colors import COLORS
from globals import window
import config as c

from utils import make_color_lighter, make_color_darker

def draw_grid(cell_size):
    ... # genuienly cannot come up with a way to draw the grid correctly when the fov is different than 1

def draw_guns(entity):
    render_stroke_width = int(c.STROKE_WIDTH / c.CAMERA_FOV)
    entity_render_x = (entity.x - c.CAMERA_X + (c.WINDOW_DIMENSIONS[0] * c.CAMERA_FOV) / 2) / c.CAMERA_FOV
    entity_render_y = (entity.y - c.CAMERA_Y + (c.WINDOW_DIMENSIONS[1] * c.CAMERA_FOV) / 2) / c.CAMERA_FOV
    
    for gun in entity.guns:
        angle = entity.angle + gun.angle
        length = (gun.length * 2 * entity.size/20) / c.CAMERA_FOV
        width = (gun.width * entity.size/20) / c.CAMERA_FOV
        gun_render_x = (gun.x - gun.length_recoil) / c.CAMERA_FOV
        gun_render_y = gun.y / c.CAMERA_FOV
        
        lighter = make_color_lighter(gun.color)
        color = lighter if entity.injured == 1 and entity.injured_tick == 1 else gun.color
        darker = make_color_darker(gun.color)

        aspect = gun.aspect if gun.aspect > 1 else gun.aspect if 0<gun.aspect<=1 else 1
        aspect2 = abs(gun.aspect) if gun.aspect < -1 else abs(gun.aspect) if -1<gun.aspect<=0 else 1

        offset_x = gun_render_x * math.cos(angle) - gun_render_y * math.sin(angle) * entity.size/20
        offset_y = gun_render_x * math.sin(angle) + gun_render_y * math.cos(angle) * entity.size/20
        base_x = entity_render_x + offset_x * 2
        base_y = entity_render_y + offset_y * 2

        p1x = base_x + width * math.sin(angle) * aspect2
        p1y = base_y - width * math.cos(angle) * aspect2

        p2x = base_x - width * math.sin(angle) * aspect2
        p2y = base_y + width * math.cos(angle) * aspect2

        p3x = base_x + length * math.cos(angle) - width * math.sin(angle) * aspect
        p3y = base_y + length * math.sin(angle) + width * math.cos(angle) * aspect

        p4x = base_x + length * math.cos(angle) + width * math.sin(angle) * aspect
        p4y = base_y + length * math.sin(angle) - width * math.cos(angle) * aspect

        # Define the polygon for the gun barrel
        polygon = [(p1x, p1y), (p2x, p2y), (p3x, p3y), (p4x, p4y)]
        
        for p in polygon:
            pygame.draw.circle(window, darker, (int(p[0]), int(p[1])), render_stroke_width // 2)
            
        pygame.draw.polygon(window, darker, polygon, render_stroke_width)
        pygame.draw.polygon(window, color, polygon)

def draw_entity(entity):
    render_stroke_width = int(c.STROKE_WIDTH / c.CAMERA_FOV)
    render_x = (entity.x - c.CAMERA_X + (c.WINDOW_DIMENSIONS[0] * c.CAMERA_FOV) / 2) / c.CAMERA_FOV
    render_y = (entity.y - c.CAMERA_Y + (c.WINDOW_DIMENSIONS[1] * c.CAMERA_FOV) / 2) / c.CAMERA_FOV
    render_size = entity.size / c.CAMERA_FOV
    
    lighter = make_color_lighter(entity.color)
    color = lighter if entity.injured == 1 and entity.injured_tick == 1 else entity.color
    darker = make_color_darker(entity.color)

    if entity.guns != []: draw_guns(entity)
    if entity.shape == 0:
        pygame.draw.circle(window, darker, (render_x, render_y), render_size + render_stroke_width // 2)
        pygame.draw.circle(window, color, (render_x, render_y), render_size)
        
    elif entity.shape > 0:
        vertices = []
        for i in range(entity.shape):
            step = (math.tau / entity.shape) * i + entity.angle
            vertices.append((
                math.cos(step) * render_size + render_x,
                math.sin(step) * render_size + render_y
            ))
        
        for v in vertices:
            pygame.draw.circle(window, darker, (int(v[0]), int(v[1])), render_stroke_width // 2)
        
        pygame.draw.polygon(window, darker, vertices, render_stroke_width)
        pygame.draw.polygon(window, color, vertices)
            
    elif entity.shape < 0:
        shape = abs(entity.shape) * 2
        vertices = []
        for i in range(shape):
            which_size = render_size if i & 1 == 0 else render_size / 3
            step = (math.tau / shape) * i + entity.angle
            
            vertices.append((
                math.cos(step) * which_size + render_x,
                math.sin(step) * which_size + render_y
            ))
        
        for v in vertices:
            pygame.draw.circle(window, darker, (int(v[0]), int(v[1])), render_stroke_width // 2)

        pygame.draw.polygon(window, darker, vertices, render_stroke_width)
        pygame.draw.polygon(window, color, vertices)
    