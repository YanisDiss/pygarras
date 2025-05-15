import math
import pygame
import sys
import random

# Constants

# Colors
COL_BLACK = (0, 0, 0)
COL_GREY = (128, 128, 128)
COL_BACKGROUND = (200, 200, 200)
COL_GRID = (180, 180, 180)
COL_WHITE = (255, 255, 255)
COL_RED = (255, 48, 48)
COL_GREEN = (87, 255, 87)
COL_BLUE = (0, 180, 225)
COL_YELLOW = (255, 255, 0)

# settings

window_dimensions = (2560, 1440)  # in pixels
frames_per_second = 120

# Parameters

initial_position = [960, 540]
initial_orientation = 0
entities = []
stroke_width = 3

# Initialization

pygame.init()
window = pygame.display.set_mode(window_dimensions)
pygame.display.set_caption("pygarras")
horloge = pygame.time.Clock()
pygame.key.set_repeat(500, 50) 

# defs

class Gun:
    def __init__(self, length,width,aspect,x,y,angle,col):
        self.length = length
        self.width = width
        self.aspect = aspect
        self.x = x
        self.y = y
        self.angle = math.radians(angle)
        self.col = col

class Entity:
    def __init__(self, x, y, size, shape, col, health, guns=[]):
        self.x = x
        self.y = y
        self.size = size
        self.shape = shape
        self.vx = 0.0
        self.vy = 0.0
        self.ax = 0.0
        self.ay = 0.0
        self.col = col
        self.health = health
        self.max_health = health
        self.old_health_percentage = 1.0
        self.alive = True
        self.angle = 0.0
        self.guns = []
    
    def kill(self):
        self.alive = False
        self.health = 0
        entities.remove(self)

    def damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.kill()

    def heal(self, amount):
        self.health = min(self.health + amount, self.max_health)

    def spin(self, angle):
        self.angle += angle
        if self.angle > 2 * math.pi:
            self.angle -= 2 * math.pi
        elif self.angle < -2 * math.pi:
            self.angle += 2 * math.pi

def is_targeted(entity, mouse_pos):
    difference = math.sqrt((entity.x - mouse_pos[0]) ** 2 + (entity.y - mouse_pos[1]) ** 2)
    return difference < entity.size

def move_player():
    if event.key == pygame.K_LEFT:
        player.vx -= .1
    if event.key == pygame.K_RIGHT:
        player.vx += .1
    if event.key == pygame.K_UP:
        player.vy -= .1
    if event.key == pygame.K_DOWN:
        player.vy += .1

def manage_inputs(input_type):
    if input_type == "key":
        move_player()
        if event.key == pygame.K_k:
            for entity in entities[:]:
                if entity.alive and is_targeted(entity,pygame.mouse.get_pos()):
                    entity.kill()
        if event.key == pygame.K_f:
            new_entity = Entity(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], 20, 0, COL_RED, 100)
            new_entity.guns.append(Gun(18, 8, 1, 0, 0, 0, COL_GREY))
            new_entity.guns.append(Gun(14, 8, 1, 0, -1, 140, COL_GREY))
            new_entity.guns.append(Gun(14, 8, 1, 0, 1, -140, COL_GREY))
            new_entity.guns.append(Gun(16, 8, 1, 0, 0, 150, COL_GREY))
            new_entity.guns.append(Gun(16, 8, 1, 0, 0, -150, COL_GREY))
            entities.append(new_entity)
        if event.key == pygame.K_q:
            for entity in entities[:]:
                if entity.alive and is_targeted(entity,pygame.mouse.get_pos()):
                    entity.damage(10)
        if event.key == pygame.K_h:
            for entity in entities[:]:
                if entity.alive and is_targeted(entity,pygame.mouse.get_pos()):
                    entity.heal(10)
        
    elif input_type == "mouse":
        ...

def draw_grid():
    for x in range(0, window_dimensions[0], 20):
        pygame.draw.line(window, COL_GRID, (x, 0), (x, window_dimensions[1]), 1)
    for y in range(0, window_dimensions[1], 20):
        pygame.draw.line(window, COL_GRID, (0, y), (window_dimensions[0], y), 1)

def draw_guns(entity):
    for gun in entity.guns:
        angle = entity.angle + gun.angle
        length = gun.length * 2 * entity.size/20
        width = gun.width * entity.size/20
        darker = (gun.col[0] // 2, gun.col[1] // 2, gun.col[2] // 2)

        aspect = gun.aspect if gun.aspect > 1 else gun.aspect if 0<gun.aspect<=1 else 1
        aspect2 = abs(gun.aspect) if gun.aspect < -1 else abs(gun.aspect) if -1<gun.aspect<=0 else 1

        offset_x = gun.x * math.cos(angle) - gun.y * math.sin(angle)
        offset_y = gun.x * math.sin(angle) + gun.y * math.cos(angle)
        base_x = entity.x + offset_x * 2
        base_y = entity.y + offset_y * 2

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
            pygame.draw.circle(window, darker, (int(p[0]), int(p[1])), stroke_width)
        pygame.draw.polygon(window,darker,polygon,stroke_width*2)
        pygame.draw.polygon(window,gun.col,polygon)


def move_entities(delta_t):
    for entity in entities:
        if entity.alive:
            entity.x += entity.vx * delta_t
            entity.y += entity.vy * delta_t

            entity.vx += entity.ax * delta_t
            entity.vy += entity.ay  * delta_t

            entity.vx *= 0.95
            entity.vy *= 0.95

            # Add collision detection and other logic here


def draw_entity(entity):

   

    if entity.guns != []: draw_guns(entity)
    darker = (entity.col[0] // 2, entity.col[1] // 2, entity.col[2] // 2)
    if entity.shape == 0:
        pygame.draw.circle(window, darker, (int(entity.x), int(entity.y)), entity.size + stroke_width)
        pygame.draw.circle(window, entity.col, (int(entity.x), int(entity.y)), entity.size)
    """elif entity.shape == "rectangle":
        pygame.draw.rect(window, entity.col, (int(entity.x), int(entity.y), entity.size, entity.size))
    elif entity.shape == "triangle":
        points = [
            (entity.x, entity.y),
            (entity.x + entity.size * math.cos(entity.angle), entity.y + entity.size * math.sin(entity.angle)),
            (entity.x - entity.size * math.cos(entity.angle), entity.y - entity.size * math.sin(entity.angle))
        ]
        pygame.draw.polygon(window, entity.col, points)"""
    

def draw_hp_bar(entity):
    outline_width = 5
    bar_width = 3
    if entity.alive  and entity.health < entity.max_health:
        health_percentage = entity.health / entity.max_health
        entity.old_health_percentage += (health_percentage - entity.old_health_percentage) * 0.3


        pygame.draw.rect(window, COL_BLACK, (entity.x - entity.size - outline_width/2, entity.y + entity.size + 10 - outline_width/2, entity.size * 2 + outline_width, bar_width + outline_width), 0, 10)
        pygame.draw.rect(window, COL_GREEN, (entity.x - entity.size, entity.y + entity.size + 10, entity.size * 2 * (entity.old_health_percentage), bar_width),0,10)


player = Entity(initial_position[0], initial_position[1], 20, 0, COL_BLUE, 100)
player.guns.append(Gun(32, 8, 1, 0, 0, 0, COL_GREY))
player.guns.append(Gun(5, 8, -1.4, 8, 0, 0, COL_GREY))
entities.append(player)

while True:
    time_now = pygame.time.get_ticks()
    window.fill(COL_BACKGROUND)
    draw_grid()
    time = pygame.time.Clock()
    delta = time.tick(frames_per_second)
    move_entities(delta)

    # draw the in-game elements
    for entity in entities:
        if entity.alive:
            draw_entity(entity)
            #entity.size += 0.1
            entity.spin(random.uniform(0,.8))
            #player.guns[0].aspect += 0.01
            player.angle = math.atan2(pygame.mouse.get_pos()[1] - player.y , pygame.mouse.get_pos()[0] - player.x)
            # Update entity position based on speed and angle

    # draw the in-game ui
    for entity in entities:
        draw_hp_bar(entity)

    #draw the actual ui
    ...

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            manage_inputs("key")
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            manage_inputs("mouse")
            

    pygame.display.flip()
    horloge.tick(frames_per_second)