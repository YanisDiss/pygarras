import pygame
import math
import random

from colors import COLORS
from globals import window
import config as c

def draw_grid(cell_size):
    grid_x = c.CAMERA_X / c.CAMERA_FOV % cell_size
    grid_y = c.CAMERA_Y / c.CAMERA_FOV % cell_size
    
    for x in range(0, c.WINDOW_DIMENSIONS[0] + 1, cell_size):
        pygame.draw.line(window, COLORS["COL_GRID"], (x - grid_x, 0), (x - grid_x, c.WINDOW_DIMENSIONS[1]), int(2 / c.CAMERA_FOV))
    for y in range(0, c.WINDOW_DIMENSIONS[1] + 1, cell_size):
        pygame.draw.line(window, COLORS["COL_GRID"], (0, y - grid_y), (c.WINDOW_DIMENSIONS[0], y - grid_y), int(2 / c.CAMERA_FOV))

def draw_guns(entity):
    render_x = (entity.x - c.CAMERA_X + (c.WINDOW_DIMENSIONS[0] * c.CAMERA_FOV) / 2) / c.CAMERA_FOV
    render_y = (entity.y - c.CAMERA_Y + (c.WINDOW_DIMENSIONS[1] * c.CAMERA_FOV) / 2) / c.CAMERA_FOV
    
    for gun in entity.guns:
        angle = entity.angle + gun.angle
        length = (gun.length * 2 * entity.size/20 - gun.length_recoil) / c.CAMERA_FOV
        width = (gun.width * entity.size/20) / c.CAMERA_FOV
        lighter = (min(gun.color[0] + 50, 255), min(gun.color[1] + 50, 255), min(gun.color[2] + 50, 255))
        color = lighter if entity.injured == 1 and entity.injured_tick == 1 else gun.color
        darker = (color[0] // 2, color[1] // 2, color[2] // 2)

        aspect = gun.aspect if gun.aspect > 1 else gun.aspect if 0<gun.aspect<=1 else 1
        aspect2 = abs(gun.aspect) if gun.aspect < -1 else abs(gun.aspect) if -1<gun.aspect<=0 else 1

        offset_x = gun.x * math.cos(angle) - gun.y * math.sin(angle) / c.CAMERA_FOV
        offset_y = gun.x * math.sin(angle) + gun.y * math.cos(angle) / c.CAMERA_FOV
        base_x = render_x + offset_x * 2
        base_y = render_y + offset_y * 2

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
            pygame.draw.circle(window, darker, (int(p[0]), int(p[1])), c.STROKE_WIDTH / c.CAMERA_FOV)
            pygame.draw.polygon(window, darker, polygon, int(c.STROKE_WIDTH*2 / c.CAMERA_FOV))
            pygame.draw.polygon(window, color, polygon)

def draw_entity(entity):
    render_x = (entity.x - c.CAMERA_X + (c.WINDOW_DIMENSIONS[0] * c.CAMERA_FOV) / 2) / c.CAMERA_FOV
    render_y = (entity.y - c.CAMERA_Y + (c.WINDOW_DIMENSIONS[1] * c.CAMERA_FOV) / 2) / c.CAMERA_FOV
    render_size = entity.size / c.CAMERA_FOV
    lighter = (min(entity.color[0] + 50, 255), min(entity.color[1] + 50, 255), min(entity.color[2] + 50, 255))
    color = lighter if entity.injured == 1 and entity.injured_tick == 1 else entity.color
    darker = (color[0] // 2, color[1] // 2, color[2] // 2)

    if entity.guns != []: draw_guns(entity)
    if entity.shape == 0:
        pygame.draw.circle(window, darker, (int(render_x), int(render_y)), int(render_size + c.STROKE_WIDTH / c.CAMERA_FOV))
        pygame.draw.circle(window, color, (int(render_x), int(render_y)), int(render_size))
        
    elif entity.shape > 0:
        stroke_vertices = []
        fill_vertices = []
        for i in range(entity.shape):
            step = (math.tau / entity.shape) * i + entity.angle
            fill_vertices.append((
                math.cos(step) * render_size + render_x,
                math.sin(step) * render_size + render_y
            ))
            stroke_vertices.append((
                math.cos(step) * (render_size + c.STROKE_WIDTH / c.CAMERA_FOV) + render_x,
                math.sin(step) * (render_size + c.STROKE_WIDTH / c.CAMERA_FOV) + render_y
            ))
        
        pygame.draw.polygon(window, darker, stroke_vertices)
        pygame.draw.polygon(window, color, fill_vertices)
            
    elif entity.shape < 0:
        shape = abs(entity.shape) * 2
        stroke_vertices = []
        fill_vertices = []
        for i in range(shape):
            which_size = render_size if i & 1 == 0 else render_size / 3
            step = (math.tau / shape) * i + entity.angle
            fill_vertices.append((
                math.cos(step) * which_size + render_x,
                math.sin(step) * which_size + render_y
            ))
            stroke_vertices.append((
                math.cos(step) * (which_size + c.STROKE_WIDTH / c.CAMERA_FOV) + render_x,
                math.sin(step) * (which_size + c.STROKE_WIDTH / c.CAMERA_FOV) + render_y
            ))
        

        pygame.draw.polygon(window, darker, stroke_vertices)
        pygame.draw.polygon(window, color, fill_vertices)
    