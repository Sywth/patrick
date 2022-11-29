"""
You edit this file to make your game, this is the only file you edit
"""
from src.p_entities import Transform
from src.p_particles import ParticleSystem
from src.p_sprite import Player, MobileEntity

from patrick_namespace import *

#--- BASE EXAMPLE---#
player = Player(
    POSITION = (0,0),
    BASE_IMAGE_PATH="./resources/sprites/sprite_",
    BASE_IMAGE_SUFFIX=".png",
    NUM_FRAMES = 5,
    ANIMATION_SPEED = 0.009
    )


physics_entity = MobileEntity(    
    POSITION = (50,50),
    BASE_IMAGE_PATH="./resources/sprites/sprite_",
    BASE_IMAGE_SUFFIX=".png",
    NUM_FRAMES = 5,
    ANIMATION_SPEED = 0.02,
    TERM_COUNT = 4,
    EXPERIENCES_FORCE = True,
    MASS = 100,
    NAME = "My Physics Entity 001"
)


static_sprite = StaticSprite(
    IMAGE_PATH="./resources/misc/test_texture.png"
)
static_sprite._transform._position.x = 0
static_sprite._transform._position.y = 0


p_default_camera.set_follow_target(player)

player._speed = 0.1
Log.set_log_level(2)

particle_system = ParticleSystem(
    POSITION = player._transform._position,
    FIXED_FORCE = (0,0.000002),
    INITIAL_VELOCITY = (-0.05,0),
    COLOR = (140,150,243), 
    DECAY_CONST = 0.005,
    RADIUS_UNCERTAINTY = 12,
    POSITION_UNCERTAINTY = 25
)

def main_game_function() -> None:
    m_pos_in_world = p_default_camera.convert_window_vec_to_world_vec(pygame.mouse.get_pos())
    particle_system._transform._position = pygame.Vector2(m_pos_in_world)

    physics_entity._transform._position = pygame.Vector2(m_pos_in_world)
    particle_system._transform._position = pygame.Vector2(m_pos_in_world)
#--- END OF BASE EXAMPLE ---#

if __name__ == "__main__":
    #We can run the game by running main_script or game_loop this way
    import game_loop