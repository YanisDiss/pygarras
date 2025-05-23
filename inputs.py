import pygame
import config as c
import random
import sys
from globals import entities, window, clickables
from utils import get_world_mouse, is_targeted
from definitions import DEFINITIONS
from entity import Entity, Gun, player_entity_id
from colors import COLORS

player_mouse_left = 0
player_mouse_middle = 0
player_mouse_right = 0

player_move_up = 0
player_move_down = 0
player_move_left = 0
player_move_right = 0

def is_mouse_over_button(button = (None,None)):
    pos , dim = button
    mouse_x, mouse_y = pygame.mouse.get_pos()
    button_rect = pygame.Rect(pos[0], pos[1], dim[0], dim[1])
    return button_rect.collidepoint(mouse_x, mouse_y)

def is_button_clicked(button = (None,None)):
    pos , dim = button
    mouse_x, mouse_y = pygame.mouse.get_pos()
    button_rect = pygame.Rect(pos[0], pos[1], dim[0], dim[1])
    is_clicked = pygame.mouse.get_pressed()[0] == True and button_rect.collidepoint(mouse_x, mouse_y)
    return is_clicked

def update_movement_state(event, down):
    global player_move_up, player_move_down, player_move_left, player_move_right
    
    if event.key == pygame.K_a or event.key == pygame.K_LEFT:
        player_move_left = down
        
    if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
        player_move_right = down
        
    if event.key == pygame.K_w or event.key == pygame.K_UP:
        player_move_up = down
        
    if event.key == pygame.K_s or event.key == pygame.K_DOWN:
        player_move_down = down
        
def update_mouse_state(event, down):
    global player_mouse_left, player_mouse_middle, player_mouse_right
    
    if event.button == pygame.BUTTON_LEFT:
        player_mouse_left = down
    
    if event.button == pygame.BUTTON_MIDDLE:
        player_mouse_middle = down
    
    if event.button == pygame.BUTTON_RIGHT:
        player_mouse_right = down

def manage_inputs(event,input_type, down):
    if input_type == "key":
        update_movement_state(event,down)
        
        if event.key == pygame.K_k:
            for entity in entities[:]:
                if entity.alive and is_targeted(entity, get_world_mouse()):
                    entity.define(DEFINITIONS["octo_tank"])
                    
        if event.key == pygame.K_e:
            if c.CAMERA_FOV_TARGET < 10:
                c.CAMERA_FOV_TARGET += 0.1
                    
        if event.key == pygame.K_q:
            if c.CAMERA_FOV_TARGET > 0.3:
                c.CAMERA_FOV_TARGET -= 0.1
                    
        if event.key == pygame.K_f:
           foods = random.choice(["egg", "square", "triangle", "pentagon"])
           food = Entity(DEFINITIONS[foods], get_world_mouse()[0], get_world_mouse()[1])

        if event.key == pygame.K_h:
            for entity in entities[:]:
                if entity.alive and is_targeted(entity, get_world_mouse()):
                    entity.change_health(entity.max_health / 10)

        if event.key == pygame.K_m:
            for entity in entities[:]:
                if entity.alive and is_targeted(entity, get_world_mouse()):
                    entity.draw_on_minimap = not entity.draw_on_minimap
    
    if input_type == "mouse":
        update_mouse_state(event,down)
        
        if is_button_clicked(clickables["boosterButton"]):
            for entity in entities[:]:
                if entity.alive and entity.id == player_entity_id:
                    entity.define(DEFINITIONS["booster"])
                    #entity.color = COLORS["COL_BLUE"]
        if is_button_clicked(clickables["acButton"]):
            for entity in entities[:]:
                if entity.alive and entity.id == player_entity_id:
                    entity.define(DEFINITIONS["arena_closer"])

