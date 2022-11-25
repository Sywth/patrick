from enum import Enum
import pygame
from os.path import exists
from collections import defaultdict

from src.p_log import Log
from src.p_camera import Camera
from src.p_entities import Entity, Transform

class StaticSprite(Entity, pygame.sprite.Sprite):
    """
    Unanimated sprite in world space. Optional arguments are:\n
    \tIMAGE_PATH [Required]\n

    \tTRANSFORM = Transform()\n
    \tCOLOR = (255,0,255)\n
    """
    EntitySpriteGroup = pygame.sprite.Group()

    DEFAULT_COLOR = (255,0,255)
    DEFAULT_IMAGE_SIZE = (16,16)

    def __init__(self, **kwargs):
        Entity.__init__(self, transform=kwargs.get("TRANSFORM", Transform()))
        pygame.sprite.Sprite.__init__(self)

        def use_default_image():
            self.image = pygame.Surface(self.DEFAULT_IMAGE_SIZE)
            self.image.fill((kwargs.get('COLOR', self.DEFAULT_COLOR)))

        #If a image path is not provided create a rectangle with attributes provided (using COLOR)
        img_path = kwargs.get("IMAGE_PATH", None)
        if not img_path:
            Log.log_warning(f"image path '{img_path}' doesn't exist")
            use_default_image()

        #If a valid image path is given use that
        elif img_path and exists(img_path):
            self.image = pygame.image.load(img_path).convert_alpha()

        #If an invalid image path is given log an error and use default image
        else:
            Log.log_error(f"Cannot find image for sprite '{self.name}' with id '{id(self)}'")
            use_default_image() 

        #assign pygame.sprite.Sprite.rect object to a rect of the image
        self.rect = self.image.get_rect()
        #set the center to the position specified
        self.rect.center = (self._transform._position.x, self._transform._position.y)


        self._update_sprite_position()
        #Add self to sprites list
        StaticSprite.EntitySpriteGroup.add(self)

    @classmethod
    def draw_all_sprites(cls, camera : Camera):
        for sprite in cls.EntitySpriteGroup:
            camera._screen.blit(sprite.image, camera.get_blit_pos(sprite.rect.topleft))    

    def kill(self):
        pygame.sprite.Sprite.kill(self)

    def outline(self, camera : Camera, color = (255,255,255)):
        white_cut_out = pygame.mask.from_surface(self.image)
        white_cut_out = white_cut_out.to_surface(setcolor=color)
        white_cut_out.set_colorkey((0,0,0))

        topleft = pygame.Vector2(self.rect.topleft)
        topleft = camera.get_blit_pos(topleft) 

        camera._screen.blit(white_cut_out,(topleft.x , topleft.y-1))
        camera._screen.blit(white_cut_out,(topleft.x , topleft.y+1))
        camera._screen.blit(white_cut_out,(topleft.x-1, topleft.y))
        camera._screen.blit(white_cut_out,(topleft.x+1, topleft.y))

    def _update_sprite_position(self):
        self.rect.center = (self._transform._position.x, self._transform._position.y)

    def update(self, delta_time=1):
        self._update_sprite_position()
        Entity.update(self, delta_time)

class AnimatedEntity(StaticSprite):

    def __init__(self, **kwargs):
        """
        BASE_IMAGE_PATH [Required]\n
        BASE_IMAGE_SUFFIX [Required]\n

        NUM_FRAMES = 1\n
        TRANSFORM = Transform()\n
        ANIMATION_SPEED = 1\n
        """
        StaticSprite.__init__(self, **kwargs)

        num_frames = kwargs.get("NUM_FRAMES",None)
        if not num_frames:
            Log.log_warning(f"number of frames are not specified for '{self.name}', assumed to be 1 frame")
            num_frames = 1

        self.images : list[pygame.Surface] = [None for _ in range(num_frames)]
        self.current_image_index = 0.0

        self._transform =  kwargs.get("TRANSFORM",None)
        if not self._transform:
            Log.log_warning(f"unspecified TRANSFORM for sprite with name {self.name} and id {id(self)}. set to default")
            self._transform = Transform()
 
        base_image_suffix = kwargs.get("BASE_IMAGE_SUFFIX",None)
        base_image_path = kwargs.get("BASE_IMAGE_PATH",None)

        if not base_image_suffix:
            Log.log_warning(f"unspecified BASE_IMAGE_SUFFIX for sprite with name {self.name} and id {id(self)}. Assumed to be png")
            base_image_suffix = ".png"

        if not base_image_path:
            Log.log_error(f"unspecified BASE_IMAGE_PATH for sprite with name {self.name} and id {id(self)}")
            self.image = pygame.Surface(self.DEFAULT_IMAGE_SIZE)
            self.image.fill(self.DEFAULT_COLOR)
            base_image_path = ""
        
        for i in range(len(self.images)):
            path = base_image_path+str(i)+base_image_suffix
            if exists(path):
                self.images[i] = pygame.image.load(path).convert_alpha()
            else:
                Log.log_error(f"couldn't find sprite at path '{path}'")
                self.images[i] = pygame.Surface(self.DEFAULT_IMAGE_SIZE)
                self.images[i].fill(self.DEFAULT_COLOR)

        self.animation_speed = kwargs.get("ANIMATION_SPEED",None)
        if not self.animation_speed:
            Log.log_info(f"unspecified ANIMATION_SPEED for sprite with name {self.name} and id {id(self)}. Assumed to be speed of 1")
            self.animation_speed = 1.0

        self.image = self.images[int(self.current_image_index)]

    def update(self, delta_time = 1):
        self.current_image_index = (self.current_image_index + (self.animation_speed*delta_time)) % len(self.images)
        self.image = self.images[int(self.current_image_index)]
        StaticSprite.update(self, delta_time)


class PhysicsObject:

    def __init__(self, **kwargs):
        """
        TRANSFORM = Transform(POSITION = (0,0), ROTATION = (0,0))\n

        EXPERIENCES_FORCE = False\n
        TERM_COUNT = 2\n

        FORCE = (0,0)\n
        FIXED_FORCE = (0,0)\n

        ACCELERATION = (0,0)\n
        VELOCITY = (0,0)\n
        """
        self._transform = kwargs.get("TRANSFORM", None)
        if not self._transform: 
            self._transform = Transform(
                kwargs.get("POSITION",pygame.Vector2(0,0)),
                kwargs.get("ROTATION",pygame.Vector2(0,0))
                )

        self.__experiences_force : bool = kwargs.get("EXPERIENCES_FORCE", True)
        self._mass : int = kwargs.get("MASS", 1)

        self.__term_count = kwargs.get("TERM_COUNT", 2)
        """Determines to what degree the position vector is calculated\n
            term 0 - stops at position (s = u)\n
            term 1 - stops at velocity (s = u + vt)\n
            term 2 - stops at acceleration (s = u + vt + at^2) and includes force (f= ma) if it EXPERIENCES_FORCE\n
            \n
            However if EXPERIENCES_FORCE flag is checked then TERM_COUNT will be 2
        """
        self.__force = pygame.Vector2(0,0)
        self.__fixed_force = pygame.Vector2(0,0)

        if self.__experiences_force:
            self.__term_count = 2
            self.__force = kwargs.get("FORCE", pygame.Vector2(0,0))
            """gets reset every frame, for a force that lasts until changed use FIXED_FORCE"""

            self.__fixed_force = kwargs.get("FIXED_FORCE", pygame.Vector2(0,0))
            """will not changed unless setter used and applied every frame"""

        self._velocity = kwargs.get("VELOCITY", pygame.Vector2(0,0))
        self._acceleration = kwargs.get("ACCELERATION", pygame.Vector2(0,0))

        self._physics_enabled :bool = True

    def enable_physics(self):
        self._physics_enabled = True

    def disable_physics(self):
        self._physics_enabled = False



    def apply_force(self, force : pygame.Vector2):
        """Applies a force to act on self for the current frame"""
        self.__force = pygame.Vector2(force)

    def get_current_force(self) -> pygame.Vector2:
        """Returns current force that will be applied on top of fixed force for this frame"""
        return self.__force.copy()
    
    def set_fixed_force(self, fixed_force : pygame.Vector2) :
        """Sets fixed_force to act on self indefinitely"""
        self.__fixed_force = pygame.Vector2(fixed_force)
        
    def get_fixed_force(self) -> pygame.Vector2:
        """Returns fixed_force acting on self"""
        return self.__fixed_force.copy()

    def get_net_force(self) -> pygame.Vector2:
        """Returns net force of fixed_force and force acting on self"""
        return self.__force + self.__fixed_force


    def __update_acceleration(self, delta_time = 1):
        """
        a = f/m
        """
        if self.__experiences_force and (self.__term_count >= 2):
            #TODO should it be += or = ???? considering now force is reset every round
            self._acceleration.x = ((self.__force.x + self.__fixed_force.x)/self._mass)*delta_time
            self._acceleration.y = ((self.__force.y + self.__fixed_force.y)/self._mass)*delta_time  

    def __update_velocity(self, delta_time = 1):
        """
        v = u + at
        """
        if self.__term_count >= 2:
            self._velocity.x += self._acceleration.x*delta_time
            self._velocity.y += self._acceleration.y*delta_time  

    def __update_position(self, delta_time = 1):
        """
        s = u + vt
        """
        if self.__term_count >= 1:
            self._transform._position.x += self._velocity.x*delta_time
            self._transform._position.y += self._velocity.y*delta_time 

    def update(self, delta_time = 1):
        if not self._physics_enabled: return
        self.__update_acceleration(delta_time)
        self.__update_velocity(delta_time)
        self.__update_position(delta_time)

        self.__force.x = 0
        self.__force.y = 0

class MobileEntity(AnimatedEntity, PhysicsObject):
    def __init__(self, **kwargs):
        AnimatedEntity.__init__(self, **kwargs)
        PhysicsObject.__init__(
            self,
            MASS = kwargs.get("MASS", 1),
            EXPERIENCES_FORCE = kwargs.get("EXPERIENCES_FORCE", False),
            TRANSFORM = kwargs.get(
                "TRANSFORM", Transform(
                    kwargs.get("POSITION",pygame.Vector2(0,0)),
                    kwargs.get("ROTATION",pygame.Vector2(0,0)),
                    )),
            TERM_COUNT = 1) 

        self._direction = pygame.Vector2(0,0)
        self._speed = kwargs.get("SPEED", 1.5)

    def update(self, delta_time = 1):
        PhysicsObject.update(self, delta_time)
        AnimatedEntity.update(self, delta_time)

class Player(MobileEntity):
    class ACTION_GROUPS():
        class ACTIONS():
            MOVE_NORTH = 1
            MOVE_EAST = 2
            MOVE_SOUTH = 3
            MOVE_WEST = 4

            ATTACK_BLOCK = 5
            ATTACK_ATTACK = 6
        MOVE = 1
        ATTACK = 2

    def __init__(self, **kwargs):
        MobileEntity.__init__(self, **kwargs)
        self.current_actions : dict[Player.ACTION_GROUPS,list[Player.ACTION_GROUPS.ACTIONS]] = defaultdict(list)

    def update_player_controller(self):
        Log.log_warning("warning this is deprecated functions, player controller should be handled outside the player class ")

        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.current_actions[Player.ACTION_GROUPS.MOVE].append(Player.ACTION_GROUPS.ACTIONS.MOVE_NORTH)
        if keys[pygame.K_d]:
            self.current_actions[Player.ACTION_GROUPS.MOVE].append(Player.ACTION_GROUPS.ACTIONS.MOVE_EAST)
        if keys[pygame.K_s]:
            self.current_actions[Player.ACTION_GROUPS.MOVE].append(Player.ACTION_GROUPS.ACTIONS.MOVE_SOUTH)
        if keys[pygame.K_a]:
            self.current_actions[Player.ACTION_GROUPS.MOVE].append(Player.ACTION_GROUPS.ACTIONS.MOVE_WEST)

    def handle_actions(self):

        def handle_movement(action):
            direction_vec = pygame.Vector2(0,0)
            if action == Player.ACTION_GROUPS.ACTIONS.MOVE_NORTH:
                self._direction.y -= 1
            if action == Player.ACTION_GROUPS.ACTIONS.MOVE_EAST:
                self._direction.x += 1
            if action == Player.ACTION_GROUPS.ACTIONS.MOVE_SOUTH:
                self._direction.y += 1
            if action == Player.ACTION_GROUPS.ACTIONS.MOVE_WEST:
                self._direction.x -= 1

            self._rotation_bearing = direction_vec.angle_to(pygame.Vector2(1,0))

        def handle_attack(action):
            pass
            #dummy function to show how this will change in future

        for action_group in self.current_actions:
            for action in self.current_actions[action_group]:
                if action_group == Player.ACTION_GROUPS.MOVE:
                    handle_movement(action)
                if action_group == Player.ACTION_GROUPS.ATTACK:
                    handle_attack(action)

    def reset_actions(self):
        self.current_actions.clear()
        self._direction.x = 0
        self._direction.y = 0

    def update(self, delta_time=1):
        self.update_player_controller()
        self.handle_actions()

        self._velocity = pygame.Vector2(0,0)
        if not (self._direction.length_squared() == 0): 
            self._velocity = self._direction.normalize() * self._speed

        MobileEntity.update(self, delta_time)
        self.reset_actions()
