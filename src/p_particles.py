from distutils.log import debug
import random
from src.p_camera import Camera
from src.p_log import Log
from src.p_sprite import PhysicsObject, AnimatedEntity, StaticSprite
from src.p_entities import Transform
import pygame

class Particle(PhysicsObject, AnimatedEntity):
    def __init__(self, **kwargs):
        """
        Optional arguments\n
            TRANSFORM = Transform()\n

            POSITION = (0,0)\n
            VELOCITY = (0,0)\n
            ACCELERATION = (0,0)\n
            FIXED_FORCE = (0,0)\n
            MASS = 1\n

            RADIUS = 5\n     
            COLOR = (255,255,255)\n    

            [Instead of radius and color image can be used]\n
            IMAGE_USED = False
            BASE_IMAGE_PATH\n
            BASE_IMAGE_SUFFIX\n

            NUM_FRAMES = 1\n
            ANIMATION_SPEED = 1\n
        """
        AnimatedEntity.__init__(self,**kwargs)
        PhysicsObject.__init__(
            self,
            TRANSFORM = kwargs.get("TRANSFORM",
                Transform(
                    kwargs.get("POSITION",pygame.Vector2(0,0)),
                    kwargs.get("ROTATION",pygame.Vector2(0,0))
                )),
            EXPERIENCES_FORCE = True,
            POSITION = kwargs.get("POSITION",pygame.Vector2(0,0)),
            VELOCITY = kwargs.get("VELOCITY",pygame.Vector2(0,0)),
            ACCELERATION = kwargs.get("ACCELERATION",pygame.Vector2(0,0)),
            FIXED_FORCE = kwargs.get("FIXED_FORCE",pygame.Vector2(0,0))
        )

        self.__image_used = kwargs.get("IMAGE_USED", False)
        self.__radius = kwargs.get("RADIUS", 5)
        self.__color = kwargs.get("COLOR", self.DEFAULT_COLOR)

        #If an image is not used then remove it from the render group
        if not self.__image_used: StaticSprite.EntitySpriteGroup.remove(self)

    def draw_self(self, camera :Camera):
        #If an image is ued it will get draw in draw sprite call instead 
        if not self.__image_used:
            print(camera.convert_world_vec_to_screen_vec(self._transform._position))
            pygame.draw.circle(camera._screen, self.__color, camera.convert_world_vec_to_screen_vec(self._transform._position), self.__radius)
    
    def update(self, delta_time=1):
        PhysicsObject.update(self, delta_time)
        AnimatedEntity.update(self, delta_time)

# class TopDownParticle(Particle):
#     def __init__(self,**kwargs):
#         """
#         Optional arguments\n
#             POSITION = (0,0) \n
#             VELOCITY = (0,0) \n
#             ACCELERATION = (0,0)
#             FORCE = (0,0)

#             HEIGHT = 5

#             MASS = 1

#             RADIUS = 5                      *Unimplemented \n
#             COLOR = (255,255,255)           *Unimplemented \n
#         """
#         Particle.__init__(self, **kwargs)

#         self.__height = kwargs.get("HEIGHT", 8)
#         self.__floor_y = self.get_position().y + self.__height

#         self.MAX_BOUNCES = 5
#         self.__bounce_count = 0
#         self.__bounce_velocity = pygame.Vector2(0.01, -0.3)

#         self.__bounce_decay_constant = 0.75

#     def update_physics(self, delta_time = 1):
#         if not self._physics_enabled(): return

#         if self.get_position().y > self.__floor_y:
#             self.__bounce_count += 1

#             self.__bounce_velocity.x = self.__bounce_velocity.x * self.__bounce_decay_constant
#             self.__bounce_velocity.y = self.__bounce_velocity.y * self.__bounce_decay_constant
#             self.set_velocity(self.__bounce_velocity)

#             self.get_position().y = self.__floor_y

#         if self.__bounce_count >= self.MAX_BOUNCES:
#             self.get_position().y = self.__floor_y
#             self._disable_physics()
#             return
            
#         Particle.update_physics(self, delta_time)

class ParticleSystem:
    ParticleSystems : list ["ParticleSystem"] = []

    def __init__(self, **kwargs):
        """
        Optional arguments\n
            POSITION = (0,0) \n
            POSITION_UNCERTAINTY = 5

            MAX_COUNT =  15
            DECAY_CONST = None                 

            RADIUS = 5
            RADIUS_UNCERTAINTY = 3

            FIXED_FORCE = (0,10)             
            INITIAL_VELOCITY = (-0.1,0)                     


            COLOR  = (255,255,255)
        """
        self._transform = kwargs.get("TRANSFORM",
            Transform(
                kwargs.get("POSITION",pygame.Vector2(0,0)),
                kwargs.get("ROTATION",pygame.Vector2(0,0))
            ))

        self.__position_uncertainty = kwargs.get("POSITION_UNCERTAINTY", 5)

        self.__initial_count = kwargs.get("MAX_COUNT", 15)
        self.__decay_constant = kwargs.get("DECAY_CONST", None)
        self.__count = 0
        self.__time = 0

        self.__radius = kwargs.get("RADIUS", 5)
        self.__radius_uncertainty = kwargs.get("RADIUS_UNCERTAINTY", 3)
        
        self.__fixed_force = pygame.Vector2(kwargs.get("FIXED_FORCE", (0,0.01)))
        self.__initial_velocity = pygame.Vector2(kwargs.get("INITIAL_VELOCITY", (-0.03,0)))

        self.__color = kwargs.get("COLOR", (255,0,255))

        self.__particles : list[Particle] = []
        
        self.__generate_particles()
        ParticleSystem.ParticleSystems.append(self)

    def __generate_particles(self):
        for _ in range(self.__initial_count):
            self.__particles.append(
                Particle(
                    POSITION = (
                        self._transform._position.x + random.randint(-self.__position_uncertainty, self.__position_uncertainty),
                        self._transform._position.y + random.randint(-self.__position_uncertainty, self.__position_uncertainty)
                        ),
                    VELOCITY=self.__initial_velocity,
                    FIXED_FORCE = self.__fixed_force,
                    MASS = random.random()*2 + 2.5,
                    RADIUS = self.__radius + random.randint(-self.__radius_uncertainty, self.__radius_uncertainty),
                    COLOR = self.__color))
            self.__count += 1

    def __update_particles_physics(self, delta_time = 1):
        #Slowly removes particle according to decay constant
        for _ in range(len(self.__particles) - self.__count):
            self.__particles.pop()
        
        #Update physics for each particle
        for particle in self.__particles:
            PhysicsObject.update(particle, delta_time)

        #If there are no more particles left delete this particle system instance
        try:
            if len(self.__particles) < 1:
                ParticleSystem.ParticleSystems.remove(self)
        except ValueError:
            Log.log_error("The particle group you are trying to update has decayed, please update via ParticleSystem.ParticleSystems instead.")

    def update(self, camera : Camera, delta_time = 1):
        self.__time += 1

        #If there is not decay constant the count stays the same 
        if self.__decay_constant:
            #y = -mx + c where 
            #y : num_particles 
            #m : decay constant
            #c : initial count
            self.__count = max(int(((-self.__decay_constant)*self.__time) + self.__initial_count),0)

        self.__update_particles_physics(delta_time)

        for particle in self.__particles:
            AnimatedEntity.update(particle, delta_time)
            particle.draw_self(camera)
