
import math
import random
from definitions import DEFINITIONS
from colors import COLORS
import config as c
from globals import entities, window
from utils import get_world_mouse, is_targeted


player_entity_id = 0
entity_id = 0

def tick_entity_id():
    global entity_id
    entity_id += 1

class Gun:
    def __init__(self, master, length, width, aspect, x, y, angle, color, can_shoot, auto_shoot, fire_rate, delay, recoil, spread, shudder, bullet_speed, bullet_damage, entity):
        self.length = length
        self.width = width
        self.aspect = aspect
        self.x = x
        self.y = y
        self.angle = math.radians(angle)
        self.color = COLORS[color]
        
        self.can_shoot = can_shoot
        self.master = master
        self.fire_rate = fire_rate
        
        self.recoil = recoil
        self.spread = spread
        self.shudder = shudder
        
        self.bullet_speed = bullet_speed
        self.bullet_damage = bullet_damage
        
        self.tick = self.fire_rate - (delay * fire_rate)
        self.length_recoil = 0
        
        self.auto_shoot = auto_shoot
        
        self.entity = entity
    
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

                spawn_x = self.master.x + math.cos(self.master.angle + self.angle) * ((self.length + self.x) * 2 * self.master.size/20)
                spawn_y = self.master.y + math.sin(self.master.angle + self.angle) * ((self.length + self.x) * 2 * self.master.size/20)
                spawn_size = self.width * (self.master.size / 20)
                spawn_angle = self.master.angle + self.angle + random.uniform(-self.spread / 2, self.spread / 2)
                spawn_angle_inverted = spawn_angle + math.pi
                
                bullet = Entity(DEFINITIONS[self.entity], spawn_x, spawn_y)
                bullet.color = self.master.color
                bullet.team = self.master.team
                bullet.size = spawn_size
                bullet.angle = spawn_angle
                bullet.vx = math.cos(spawn_angle) * (self.bullet_speed + random.uniform(-self.shudder / 2, self.shudder / 2))
                bullet.vy = math.sin(spawn_angle) * (self.bullet_speed + random.uniform(-self.shudder / 2, self.shudder / 2))
                
                self.master.vx += math.cos(spawn_angle_inverted) * self.recoil
                self.master.vy += math.sin(spawn_angle_inverted) * self.recoil

class Entity:
    def __init__(self, definition, x, y):
       
        self.x = x
        self.y = y
        self.size = definition["size"]
        self.shape = definition["shape"]
        self.color = COLORS[definition["color"]]
        self.type = definition["type"]
        self.render_health = definition["render_health"]
        self.lifetime = definition["lifetime"]
        self.team = definition["team"]
        
        self.max_health = definition["body"]["health"]
        self.health = definition["body"]["health"]
        self.can_collide = definition["body"]["can_collide"]
        
        self.guns = []
        for gun in definition["guns"]:
            self.guns.append(Gun(
                self,
                gun["length"],
                gun["width"],
                gun["aspect"],
                gun["x"],
                gun["y"],
                gun["angle"],
                gun["color"],
                gun["properties"]["can_shoot"],
                gun["properties"]["auto_shoot"],
                gun["properties"]["fire_rate"],
                gun["properties"]["delay"],
                gun["properties"]["recoil"],
                gun["properties"]["spread"],
                gun["properties"]["shudder"],
                gun["properties"]["bullet_speed"],
                gun["properties"]["bullet_damage"],
                gun["properties"]["entity"]
            ))
        
        self.vx = 0.0
        self.vy = 0.0
        self.ax = 0.0
        self.ay = 0.0
        self.old_health_percentage = 1.0
        self.alive = 1
        self.angle = 0.0
        self.id = entity_id
        self.food_angle = random.uniform(0, math.tau)
        self.tick = 0
        self.render = 1
        self.die_animation_tick = 0
        self.is_visible = 0
        self.draw_on_minimap = False
        self.injured = 0
        self.injured_tick = 0
        
        tick_entity_id()
        entities.append(self)
    
    def step(self, delta_t):
        from inputs import manage_inputs, player_mouse_left, player_move_up, player_move_down, player_move_left, player_move_right
        if self.alive:
            for gun in self.guns:
                gun.animate()

            self.vx += self.ax * delta_t
            self.vy += self.ay * delta_t

            if self.type == "food":
                self.angle -= 0.02
                self.vx += math.cos(self.food_angle) * 0.0013
                self.vy += math.sin(self.food_angle) * 0.0013

            if self.id == player_entity_id:
                player_mouse = get_world_mouse()
                self.angle = math.atan2(player_mouse[1] - self.y, player_mouse[0] - self.x)
                
                c.CAMERA_X = self.x
                c.CAMERA_Y = self.y
                
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

                if self.type == "tank":
                    self.draw_on_minimap = True

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
            else: 
                self.vx *= 0.99
                self.vy *= 0.99
            
            self.x += self.vx * delta_t
            self.y += self.vy * delta_t
            
            if self.x < self.size:
                self.x = self.size
                self.vx = 0
                
            if self.x > c.ARENA_DIMENSIONS[0] - self.size:
                self.x = c.ARENA_DIMENSIONS[0] - self.size
                self.vx = 0
                
            if self.y < self.size:
                self.y = self.size
                self.vy = 0
                
            if self.y > c.ARENA_DIMENSIONS[1] - self.size:
                self.y = c.ARENA_DIMENSIONS[1] - self.size
                self.vy = 0
            
            self.food_angle += 0.01
            self.tick += 1
            
            self.change_health(0.005) # heal overtime
            
            if self.tick == self.lifetime:
                self.kill()
            
        else:
            self.size -= self.size / 100 * delta_t
            self.x += self.vx * delta_t
            self.y += self.vy * delta_t
            self.vx += self.ax * delta_t
            self.vy += self.ay * delta_t
            
            if self.size <= 2:
                self.render = 0
                entities.remove(self)

        if self.injured == 1:
            self.injured = 0
            self.injured_tick ^= 1 # toggle btween 0 and 1
        else:
            self.injured_tick = 0

        """render_x = entity.x - c.CAMERA_X + c.WINDOW_DIMENSIONS[0] / 2
        render_y = entity.y - c.CAMERA_Y + c.WINDOW_DIMENSIONS[1] / 2
        entity.is_visible = 1
        if (render_x < -entity.size or render_x > c.WINDOW_DIMENSIONS[0] + entity.size or render_y < -entity.size or render_y > c.WINDOW_DIMENSIONS[1] + entity.size):
            entity.is_visible = 0"""
        
        render_x = self.x - c.CAMERA_X + c.WINDOW_DIMENSIONS[0] / 2
        render_y = self.y - c.CAMERA_Y + c.WINDOW_DIMENSIONS[1] / 2
        self.is_visible = 1
        if (render_x < -self.size or render_x > c.WINDOW_DIMENSIONS[0] + self.size or render_y < -self.size or render_y > c.WINDOW_DIMENSIONS[1] + self.size):
            self.is_visible = 0
        
    def change_health(self, amount):
        self.health += amount
        if self.health <= 0:
            self.kill()
        if (self.health >= self.max_health):
            self.health = self.max_health
        if amount < 0:
            self.injured = 1
    def kill(self):
        self.alive = False
        self.health = 0
