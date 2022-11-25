from src.p_entities import Transform
from src.p_particles import ParticleSystem
from src.p_sprite import Player, MobileEntity
from patrick_namespace import *

#--- BASE TESTING START---#
player = Player(
    POSITION = (100,100),
    BASE_IMAGE_PATH="./resources/sprites/sprite_",
    BASE_IMAGE_SUFFIX=".png",
    NUM_FRAMES = 5,
    ANIMATION_SPEED = 0.009
    )

test_physics_entity = MobileEntity(    
    POSITION = (50,50),
    BASE_IMAGE_PATH="./resources/sprites/sprite_",
    BASE_IMAGE_SUFFIX=".png",
    NUM_FRAMES = 5,
    ANIMATION_SPEED = 0.02,
    TERM_COUNT = 4,
    EXPERIENCES_FORCE = True,
    MASS = 100)

p_default_camera.set_follow_target(player)

player._speed = 0.1
Log.set_log_level(2)

particle_system = ParticleSystem(
    POSITION = player._transform._position,
    FIXED_FORCE = (0,0.000002),
    INITIAL_VELOCITY = (-0.05,0),
    COLOR = (140,150,243), 
    DECAY_CONST = 0.05,
    RADIUS_UNCERTAINTY = 12,
    POSITION_UNCERTAINTY = 25
      )
#--- END OF BASE TESTING ---#

running = True
#main application loop
while running:
    p_frame_count += 1

    #refreshes the screen's background color to black 
    p_screen.fill((255,255,255))

    p_handle_events()
    p_update(p_delta_time)

    #TESTING --------------------
    m_pos_in_world = p_default_camera.convert_window_vec_to_world_vec(pygame.mouse.get_pos())
    particle_system._transform._position = pygame.Vector2(m_pos_in_world)
    for ps in ParticleSystem.ParticleSystems:
        ps.update(p_default_camera)
    #test_physics_entity._transform._position = pygame.Vector2(m_pos_in_world)
    #TESTING --------------------

    p_draw_frame(p_default_camera)
    p_draw_UI(p_default_camera)
    p_default_camera.draw_to_window()
    
    #pg_clock.tick tries to keep application running at '$FPS' frames per second,
    #this also returns in milliseconds the last it was called so we can also update delta time here
    p_delta_time = p_clock.tick()*p_TIME_SCALAR
pygame.quit() 