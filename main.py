"""This is the demo scene shown in the gif in the readme, use it as a reference on how to use the framework"""
import random
from src.p_entities import Transform
from src.p_particles import ParticleSystem
from src.p_sprite import Player, MobileEntity
from patrick_namespace import *

from perlin_noise import PerlinNoise

RECORD = False
RECORDING_PATH = "recordings/recording001"
RECORD_EVERY_N_FRAMES = 15

def lerp(a: float,b: float,t: float) -> float:
    return a + (b-a)*t

def random_vec_2(scalar : float = 1.0) -> pygame.Vector2:
    return pygame.Vector2(random.random() - 0.5, random.random() - 0.5)  * scalar

perlin_noise_sampler = PerlinNoise(seed=42)
def perlin_noise(t: float) -> float:
    return perlin_noise_sampler([t])

ARBITRARY_OFFSET_1 = 231512
ARBITRARY_OFFSET_2 = 231512

def perlin_noise_vec2(t : float) -> pygame.Vector2:
    return pygame.Vector2(perlin_noise(t), perlin_noise(t+ARBITRARY_OFFSET_1))

#--- BASE TESTING START---#
player = Player(
    POSITION = (100,100),
    BASE_IMAGE_PATH="./resources/sprites/sprite_",
    BASE_IMAGE_SUFFIX=".png",
    NUM_FRAMES = 5,
    ANIMATION_SPEED = 0.009
    )

entity_count = 12
entities = [MobileEntity(    
    POSITION = (50,50),
    BASE_IMAGE_PATH="./resources/sprites/sprite_",
    BASE_IMAGE_SUFFIX=".png",
    NUM_FRAMES = 5,
    ANIMATION_SPEED = 0.02,
    TERM_COUNT = 4,
    EXPERIENCES_FORCE = True,
    MASS = 100,) for _ in range(entity_count)]

p_default_camera.set_follow_target(player)

player._speed = 0.1
Log.set_log_level(2)
#--- END OF BASE TESTING ---#

running = True
#main application loop
while running:
    p_frame_count += 1

    #refreshes the screen's background color to black 
    p_screen.fill((215, 241, 254))

    p_handle_events()
    p_update(p_delta_time)

    #TESTING --------------------
    m_pos_in_world = p_default_camera.convert_window_vec_to_world_vec(pygame.mouse.get_pos())

    for i,entity in enumerate(entities):
        entity._transform._position = lerp(entity._transform._position, player._transform._position, p_delta_time * 0.001)
        entity._transform._position += perlin_noise_vec2((i*ARBITRARY_OFFSET_2)+(p_frame_count/100)) * 5

    if (p_frame_count % 6 == 0) : ParticleSystem(
            POSITION = random.choice(entities)._transform._position,
            FIXED_FORCE = (0,0.000002),
            INITIAL_VELOCITY = (-0.05,-0.015),
            COLOR = (138,3,3), 
            DECAY_CONST = 0.02,
            RADIUS_UNCERTAINTY = 3,
            POSITION_UNCERTAINTY = 4,
            MAX_COUNT = 8,
        )

    for particle_system in ParticleSystem.ParticleSystems:
        particle_system.update(p_default_camera)
    
    #TESTING --------------------

    p_draw_frame(p_default_camera)
    p_draw_UI(p_default_camera)
    p_default_camera.draw_to_window()
    
    #pg_clock.tick tries to keep application running at '$FPS' frames per second,
    #this also returns in milliseconds the last it was called so we can also update delta time here
    p_delta_time = p_clock.tick()*p_TIME_SCALAR
    
    # For recording, this how the gif in the readme was created 
    if p_frame_count % RECORD_EVERY_N_FRAMES == 0:
        pygame.image.save(p_window, f"{RECORDING_PATH}/screenshot{p_frame_count}.jpeg")

pygame.quit() 