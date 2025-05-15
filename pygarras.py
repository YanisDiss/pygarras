import math
import pygame
import sys
import random

# Constants

# Colors
COL_BLACK = (0, 0, 0)
COL_GREY = (128, 128, 128)
COL_OUTER_BACKGROUND = (180, 180, 180)
COL_BACKGROUND = (200, 200, 200)
COL_GRID = (170, 170, 170)
COL_WHITE = (255, 255, 255)
COL_RED = (255, 48, 48)
COL_GREEN = (87, 255, 87)
COL_BLUE = (0, 180, 225)
COL_YELLOW = (255, 255, 0)
COL_PURPLE = (105, 43, 255)
COL_ORANGE = (255, 129, 27)
COL_PINK = (199, 38, 128)
COL_LAVENDER = (150, 94, 199)
COL_DARK_GREEN = (43, 186, 93)

# settings

window_dimensions = (1280, 720)  # in pixels
arena_dimensions = (2000, 2000) # also in pixels
frames_per_second = 60

# Parameters

initial_position = [arena_dimensions[0] / 2, arena_dimensions[1] / 2]
initial_orientation = 0
entities = []
stroke_width = 3

# Initialization

pygame.init()
window = pygame.display.set_mode(window_dimensions)
pygame.display.set_caption("pygarras")
horloge = pygame.time.Clock()
pygame.key.set_repeat(50, 50)

# defs
camera_x = arena_dimensions[0] / 2
camera_y = arena_dimensions[1] / 2
camera_fov = 1

player_entity_id = 0
entity_id = 0

def tick_entity_id():
    global entity_id
    entity_id += 1

def get_world_mouse():
    player_mouse = pygame.mouse.get_pos()
    
    x = (player_mouse[0] + camera_x - window_dimensions[0] / 2)
    y = (player_mouse[1] + camera_y - window_dimensions[1] / 2)
    
    return (x, y)

class Gun:
    def __init__(self, master, length, width, aspect, x, y, angle, col, can_shoot, auto_shoot, fire_rate, delay, recoil, bullet_speed):
        self.length = length
        self.width = width
        self.aspect = aspect
        self.x = x
        self.y = y
        self.angle = math.radians(angle)
        self.col = col
        
        self.can_shoot = can_shoot
        self.master = master
        self.fire_rate = fire_rate
        
        self.recoil = recoil
        self.bullet_speed = bullet_speed
        
        self.tick = self.fire_rate - (delay * fire_rate)
        self.length_recoil = 0
        
        self.auto_shoot = auto_shoot
    
    def animate(self):
        self.length_recoil *= 0.9
        if self.auto_shoot:
            self.shoot()
    
    def shoot(self):
        if self.can_shoot == 1:
            self.tick += 1
            
            if self.tick >= self.fire_rate:
                self.tick = 0
                self.length_recoil = self.length / 2 * self.master.size/40
                
                spawn_x = self.master.x + self.x + math.cos(self.master.angle + self.angle) * (self.length * 2 * self.master.size/20)
                spawn_y = self.master.y + self.y + math.sin(self.master.angle + self.angle) * (self.length * 2 * self.master.size/20)
                spawn_size = self.width * (self.master.size / 20)
                
                bullet = Entity("bullet", spawn_x, spawn_y, spawn_size, 0, self.master.col, 5, self.master.team)
                bullet.vx = math.cos(self.master.angle + self.angle) * self.bullet_speed
                bullet.vy = math.sin(self.master.angle + self.angle) * self.bullet_speed
                
                self.master.vx += math.cos(self.master.angle + self.angle + math.pi) * self.recoil
                self.master.vy += math.sin(self.master.angle + self.angle + math.pi) * self.recoil
                
                entities.append(bullet)
        

class Entity:
    def __init__(self, type, x, y, size, shape, col, health, team):
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
        self.alive = 1
        self.angle = 0.0
        self.type = type
        self.guns = []
        self.id = entity_id
        self.food_angle = random.randrange(0, 62831) / 10000 # idk how to put floats in the random function cuz it yells at me so i just put ints and divide after
        
        self.can_collide = 1
        self.render_health = 1
        self.lifetime = -1
        
        if type == "bullet":
            self.can_collide = 0
            self.lifetime = 75
            self.render_health = 0
        
        self.team = team
        self.tick = 0
        
        self.render = 1
        self.die_animation_tick = 0
        self.is_visible = 0
        tick_entity_id()
    
    def step(self, delta_t):
        if self.alive:
            for gun in self.guns:
                gun.animate()

            self.vx += self.ax * delta_t
            self.vy += self.ay * delta_t

            if self.type == "food":
                self.angle -= math.hypot(self.vx, self.vy)
                self.vx += math.cos(self.food_angle) * 0.002
                self.vy += math.sin(self.food_angle) * 0.002

            if self.id == player_entity_id:
                player_mouse = get_world_mouse()
                self.angle = math.atan2(player_mouse[1] - self.y, player_mouse[0] - self.x)
                
                global camera_x
                global camera_y
                
                camera_x = self.x
                camera_y = self.y
                
                if player_move_up == 1:
                    self.vy -= 0.01
                if player_move_down == 1:
                    self.vy += 0.01
                if player_move_right == 1:
                    self.vx += 0.01
                if player_move_left == 1:
                    self.vx -= 0.01
                
                if player_mouse_left == 1:
                    for gun in self.guns:
                        gun.shoot()

            # Add collision detection and other logic here
            for other in entities:
                if self.id != other.id and other.alive:
                    dist = math.hypot(self.x - other.x, self.y - other.y)
                    
                    if dist <= self.size + other.size:
                        if self.can_collide and other.can_collide:
                            angle1 = math.atan2(self.y - other.y, self.x - other.x)
                            self.vx += math.cos(angle1) * 0.01
                            self.vy += math.sin(angle1) * 0.01
                            
                            angle2 = math.atan2(other.y - self.y, other.x - self.x)
                            other.vx += math.cos(angle2) * 0.01
                            other.vy += math.sin(angle2) * 0.01
                            
                        if self.team != other.team:
                            self.change_health(-0.2)
                            other.change_health(-0.2)
                        
            if self.type != "bullet":
                self.vx *= 0.95
                self.vy *= 0.95
            
            self.x += self.vx * delta_t
            self.y += self.vy * delta_t
            
            if self.x < self.size:
                self.x = self.size
                self.vx = 0
                
            if self.x > arena_dimensions[0] - self.size:
                self.x = arena_dimensions[0] - self.size
                self.vx = 0
                
            if self.y < self.size:
                self.y = self.size
                self.vy = 0
                
            if self.y > arena_dimensions[1] - self.size:
                self.y = arena_dimensions[1] - self.size
                self.vy = 0
            
            self.food_angle += 0.02
            self.tick += 1
            
            self.change_health(0.005) # heal overtime
            
            if self.tick == self.lifetime:
                self.kill()
            
        else:
            self.size -= self.size / 100 * delta_t
            
            if self.size <= 2:
                self.render = 0
                entities.remove(self)

        render_x = entity.x - camera_x + window_dimensions[0] / 2
        render_y = entity.y - camera_y + window_dimensions[1] / 2
        entity.is_visible = 1
        if (render_x < -entity.size or render_x > window_dimensions[0] + entity.size or render_y < -entity.size or render_y > window_dimensions[1] + entity.size):
            entity.is_visible = 0
        
    def change_health(self, amount):
        self.health += amount
        if self.health <= 0:
            self.kill()
        if (self.health >= self.max_health):
            self.health = self.max_health
    
    def kill(self):
        self.alive = False
        self.health = 0

def is_targeted(entity, mouse_pos):
    difference = math.sqrt((entity.x - mouse_pos[0]) ** 2 + (entity.y - mouse_pos[1]) ** 2)
    return difference < entity.size

def spawn_food(type, x, y):
    if type == "egg":
        food = Entity("food", x, y, 4, 0, COL_WHITE, 3, 100)
        entities.append(food)
    elif type == "square":
        food = Entity("food", x, y, 15, 4, COL_YELLOW, 5, 100)
        entities.append(food)
    elif type == "triangle":
        food = Entity("food", x, y, 17, 3, COL_ORANGE, 17, 100)
        entities.append(food)
    elif type == "pentagon":
        food = Entity("food", x, y, 20, 5, COL_PURPLE, 35, 100)
        entities.append(food)
    elif type == "hexagon":
        food = Entity("food", x, y, 40, 6, COL_PINK, 200, 100)
        entities.append(food)
    elif type == "heptagon":
        food = Entity("food", x, y, 46, 7, COL_DARK_GREEN, 300, 100)
        entities.append(food)
    elif type == "octagon":
        food = Entity("food", x, y, 55, 8, COL_LAVENDER, 500, 100)
        entities.append(food)
    

player_mouse_left = 0
player_mouse_middle = 0
player_mouse_right = 0

player_move_up = 0
player_move_down = 0
player_move_left = 0
player_move_right = 0

def update_movement_state(down):
    global player_move_up
    global player_move_down
    global player_move_right
    global player_move_left
    
    if event.key == pygame.K_a or event.key == pygame.K_LEFT:
        player_move_left = down
        
    if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
        player_move_right = down
        
    if event.key == pygame.K_w or event.key == pygame.K_UP:
        player_move_up = down
        
    if event.key == pygame.K_s or event.key == pygame.K_DOWN:
        player_move_down = down
        
def update_mouse_state(down):
    global player_mouse_left
    global player_mouse_middle
    global player_mouse_right
    
    if event.button == pygame.BUTTON_LEFT:
        player_mouse_left = down
    
    if event.button == pygame.BUTTON_MIDDLE:
        player_mouse_middle = down
    
    if event.button == pygame.BUTTON_RIGHT:
        player_mouse_right = down

def manage_inputs(input_type, down):
    if input_type == "key":
        update_movement_state(down)
        
        if event.key == pygame.K_k:
            for entity in entities[:]:
                if entity.alive and is_targeted(entity, get_world_mouse()):
                    entity.kill()
                    
        if event.key == pygame.K_e:
            for entity in entities[:]:
                if entity.alive and is_targeted(entity, get_world_mouse()):
                    entity.size += 5
                    
        if event.key == pygame.K_q:
            for entity in entities[:]:
                if entity.alive and is_targeted(entity, get_world_mouse()):
                    entity.size -= 5
                    
        if event.key == pygame.K_j:
            for entity in entities[:]:
                if entity.alive and entity.guns == [] and is_targeted(entity, get_world_mouse()):
                    for i in range(abs(entity.shape)) :
                        entity.guns.append(Gun(entity, 12, 8, 1, 0, 0, (360 / abs(entity.shape)) * i - (360 / abs(entity.shape)) / 2, COL_GREY, 1, 1, 50, i * (1 / abs(entity.shape)), 0.04, 0.35))
    
    if input_type == "mouse":
        update_mouse_state(down)
        

def draw_grid(cell_size):
    grid_x = camera_x / camera_fov % cell_size
    grid_y = camera_y / camera_fov % cell_size
    
    for x in range(0, window_dimensions[0] + 1, cell_size):
        pygame.draw.line(window, COL_GRID, (x - grid_x, 0), (x - grid_x, window_dimensions[1]), int(2 / camera_fov))
    for y in range(0, window_dimensions[1] + 1, cell_size):
        pygame.draw.line(window, COL_GRID, (0, y - grid_y), (window_dimensions[0], y - grid_y), int(2 / camera_fov))

def draw_guns(entity):
    render_x = (entity.x - camera_x + (window_dimensions[0] * camera_fov) / 2) / camera_fov
    render_y = (entity.y - camera_y + (window_dimensions[1] * camera_fov) / 2) / camera_fov
    
    for gun in entity.guns:
        angle = entity.angle + gun.angle
        length = (gun.length * 2 * entity.size/20 - gun.length_recoil) / camera_fov
        width = (gun.width * entity.size/20) / camera_fov
        darker = (gun.col[0] // 2, gun.col[1] // 2, gun.col[2] // 2)

        aspect = gun.aspect if gun.aspect > 1 else gun.aspect if 0<gun.aspect<=1 else 1
        aspect2 = abs(gun.aspect) if gun.aspect < -1 else abs(gun.aspect) if -1<gun.aspect<=0 else 1

        offset_x = gun.x * math.cos(angle) - gun.y * math.sin(angle) / camera_fov
        offset_y = gun.x * math.sin(angle) + gun.y * math.cos(angle) / camera_fov
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
            pygame.draw.circle(window, darker, (int(p[0]), int(p[1])), stroke_width / camera_fov)
            pygame.draw.polygon(window, darker, polygon, int(stroke_width*2 / camera_fov))
            pygame.draw.polygon(window, gun.col, polygon)


def draw_entity(entity):
    render_x = (entity.x - camera_x + (window_dimensions[0] * camera_fov) / 2) / camera_fov
    render_y = (entity.y - camera_y + (window_dimensions[1] * camera_fov) / 2) / camera_fov
    render_size = entity.size / camera_fov

    if entity.guns != []: draw_guns(entity)
    darker = (entity.col[0] // 2, entity.col[1] // 2, entity.col[2] // 2)
    
    if entity.shape == 0:
        pygame.draw.circle(window, darker, (int(render_x), int(render_y)), int(render_size + stroke_width / camera_fov))
        pygame.draw.circle(window, entity.col, (int(render_x), int(render_y)), int(render_size))
        
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
                math.cos(step) * (render_size + stroke_width / camera_fov) + render_x,
                math.sin(step) * (render_size + stroke_width / camera_fov) + render_y
            ))
        
        pygame.draw.polygon(window, darker, stroke_vertices)
        pygame.draw.polygon(window, entity.col, fill_vertices)
            
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
                math.cos(step) * (which_size + stroke_width / camera_fov) + render_x,
                math.sin(step) * (which_size + stroke_width / camera_fov) + render_y
            ))
        

        pygame.draw.polygon(window, darker, stroke_vertices)
        pygame.draw.polygon(window, entity.col, fill_vertices)
    

def draw_hp_bar(entity):
    render_x = (entity.x - camera_x + (window_dimensions[0] * camera_fov) / 2) / camera_fov
    render_y = (entity.y - camera_y + (window_dimensions[1] * camera_fov) / 2) / camera_fov
    
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
        
        pygame.draw.rect(window, COL_BLACK, (render_x - entity.size - outline_width / 2, render_y + entity.size + 10 - outline_width / 2, (entity.size * 2 + outline_width), bar_width + outline_width ), 0, 10)
        pygame.draw.rect(window, COL_GREEN, (render_x - entity.size                    , render_y + entity.size + 10                    , (entity.size * 2 * (entity.old_health_percentage)), bar_width), 0, 10)

"""
player = Entity(initial_position[0], initial_position[1], 20, 0, COL_BLUE, 100, "tank")
player.guns.append(Gun(player, 32, 8, 1, 0, 0, 0, COL_GREY, 1))
player.guns.append(Gun(player, 5, 8, -1.4, 8, 0, 0, COL_GREY, 0))
player_entity_id = player.id
entities.append(player)
"""

player = Entity("tank", initial_position[0], initial_position[1], 20, 0, COL_BLUE, 75, 0)
player.guns.append(Gun(player, 18, 8, 1, 0, 0, 0, COL_GREY, 1, 0, 20, 0, 0.01, 0.35))
player.guns.append(Gun(player, 14, 8, 1, 0, -1, 140, COL_GREY, 1, 0, 20, 0, 0.04, 0.35))
player.guns.append(Gun(player, 14, 8, 1, 0, 1, -140, COL_GREY, 1, 0, 20, 0, 0.04, 0.335))
player.guns.append(Gun(player, 16, 8, 1, 0, 0, 150, COL_GREY, 1, 0, 20, 0.5, 0.04, 0.35))
player.guns.append(Gun(player, 16, 8, 1, 0, 0, -150, COL_GREY, 1, 0, 20, 0.5, 0.04, 0.35))
entities.append(player)

for i in range(75):
    spawn_food(random.choice(["egg", "square", "triangle", "pentagon", "hexagon", "heptagon", "octagon"]), random.randrange(0, arena_dimensions[0]), random.randrange(0, arena_dimensions[1]))

while True:
    
    time_now = pygame.time.get_ticks()
    window.fill(COL_OUTER_BACKGROUND)
    
    pygame.draw.rect(window, COL_BACKGROUND, pygame.Rect(-camera_x + window_dimensions[0] / 2, -camera_y + window_dimensions[1] / 2, arena_dimensions[0], arena_dimensions[1]))
    
    draw_grid(int(20 / camera_fov))
    time = pygame.time.Clock()
    delta = time.tick(frames_per_second)
    
    # do a physics step for all entities
    for entity in entities:
        entity.step(delta)

    # draw the in-game elements
    for entity in entities:
        if entity.render and entity.is_visible:
            draw_entity(entity)

    # draw the in-game ui
    for entity in entities:
        if entity.render and entity.render_health and entity.is_visible:
            draw_hp_bar(entity)

    #draw the actual ui
    ...

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            manage_inputs("key", 1)
        
        elif event.type == pygame.KEYUP:
            manage_inputs("key", 0)
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            manage_inputs("mouse", 1)
            
        elif event.type == pygame.MOUSEBUTTONUP:
            manage_inputs("mouse", 0)
    

    pygame.display.flip()
    horloge.tick(frames_per_second)