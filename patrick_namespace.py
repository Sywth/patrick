import pygame
from typing import Optional
from src.p_entities import GameObject
from src.p_camera import Camera
from src.p_sprite import StaticSprite
from src.p_text_rendering import get_rendered_font
from src.p_log import Log
from os.path import exists

#---Window Initiation Start---#
p_SCREEN_WIDTH = 500    
p_SCREEN_HEIGHT = 250

p_SCREEN_SCALAR = 3
p_WINDOW_WIDTH = int(p_SCREEN_WIDTH * p_SCREEN_SCALAR)
p_WINDOW_HEIGHT = int(p_SCREEN_HEIGHT * p_SCREEN_SCALAR)

p_screen = pygame.Surface((p_SCREEN_WIDTH, p_SCREEN_HEIGHT))
p_window = pygame.display.set_mode((p_WINDOW_WIDTH,p_WINDOW_HEIGHT))

Camera.set_window_context(p_window)
p_default_camera = Camera(p_screen)
#---Window Initiation End---#

#--- Time variables/constants start---#
p_delta_time = 1
"""Time in ms between frames"""
p_FPS_CAP = 30 
"""maximum frames per second"""
p_TIME_SCALAR = 0.8
"""Can be used to scale p_delta_time"""
p_frame_count = 0
#--- Time variables/constants end---#

#--- pygame inits start---#
pygame.init()
pygame.display.set_caption("[Insert Title of Application]")
p_clock = pygame.time.Clock()
p_font = pygame.font.SysFont("Courier", 14)
#--- pygame inits end---#

#--- game loop base functions start ---#
p_running = True
def p_handle_events():
    global p_running
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            p_running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                p_running = False
#--- game loop base functions end ---#

#--- update functions ---#
def p_update(delta_time = 1):
    for game_object in GameObject.game_objects:
        game_object.update(delta_time)
        pass

    """
    for sprite in StaticSprite.EntitySpriteGroup:
        camera.screen.blit(entity.image, camera.get_blit_pos(entity.rect.topleft))
        StaticSprite.EntitySpriteGroup.draw(p_screen)
    """
    
def p_draw_frame(camera : Camera):
    StaticSprite.draw_all_sprites(camera)

def p_draw_UI(camera : Camera):
    #--- fps rendering ---#
    fps_str = str(round(p_clock.get_fps()))
    fps_text_surface = get_rendered_font(fps_str)

    camera._screen.blit(fps_text_surface, (0,0))
    #--- fps rendering ---#
