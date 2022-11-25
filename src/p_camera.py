from typing import Optional
import pygame, random

from src.p_entities import Entity, Transform

class Camera(Entity):
    """
    Call "draw_background" at the start of every frame,
    call update every frame,
    and "display_to_window" at the end of every frame
    """
    __WINDOW_CONTEXT_DEFINED = False

    WINDOW_SURFACE : pygame.Surface = None
    WINDOW_WIDTH : int = None
    WINDOW_HEIGHT : int = None

    @classmethod
    def set_window_context(cls, window_surface : pygame.Surface):
        cls.WINDOW_SURFACE = window_surface
        cls.WINDOW_WIDTH = cls.WINDOW_SURFACE.get_width()
        cls.WINDOW_HEIGHT = cls.WINDOW_SURFACE.get_height()

        cls.__WINDOW_CONTEXT_DEFINED = True

    def __init__(self, screen : pygame.Surface, position : pygame.Vector2 = (0,0)):
        #assert(Camera.__WINDOW_CONTEXT_DEFINED) would this not do the same thing?
        if not Camera.__WINDOW_CONTEXT_DEFINED: 
            raise Exception("Camera.__WINDOW_CONTEXT_DEFINED is undefined, call set_window_context with an appropriate pygame surface object")

        Entity.__init__(self)
        self._screen : pygame.Surface = screen
        self._transform._position : pygame.Vector2 = pygame.Vector2(position)

        self._SCREEN_WIDTH : int = self._screen.get_width()
        self._SCREEN_HEIGHT : int = self._screen.get_height()
        
        self._screen_to_window_scalar : pygame.Vector2 = pygame.Vector2(
            Camera.WINDOW_WIDTH/self._SCREEN_WIDTH,
            Camera.WINDOW_HEIGHT/self._SCREEN_WIDTH,
            )

        self._target : Optional[Entity] = None
        self._background_color = (0,0,0)
        
    def set_follow_target(self, target : Entity):
        self._target = target

    def draw_background(self):
        self._screen.fill(self._background_color)

    def update(self, delta_time = 1):
        if self._target:
            vec = self._target._transform._position.copy()

            vec.x -= self._SCREEN_WIDTH/2
            vec.y -= self._SCREEN_HEIGHT/2

            self._transform._position = vec

    def draw_to_window(self):
        pygame.draw.circle(Camera.WINDOW_SURFACE, (255,255,255),(100,100),100)

        pygame.transform.scale(self._screen, (Camera.WINDOW_WIDTH, Camera.WINDOW_HEIGHT), Camera.WINDOW_SURFACE)
        pygame.display.flip()

    def draw_to_surface(self, destination_surface :pygame.Surface, topleft : pygame.Vector2 = (0,0), size : pygame.Vector2 = None):
        if not size:
            size = (destination_surface.get_width(),destination_surface.get_height())

        scaled_surface = pygame.transform.scale(self._screen, size)
        destination_surface.blit(scaled_surface, topleft)

    #--- Less important functions ---#



    def screen_shake(self, mag_x = 1, mag_y = 1):
        self.__scroll.x = random.randint(-mag_x,mag_x)
        self.__scroll.y = random.randint(-mag_y,mag_y)



    #Primitive Coordinate Conversion functions

    def convert_world_vec_to_screen_vec(self, vec : pygame.Vector2) -> pygame.Vector2:
        vec = pygame.Vector2(vec)
        return vec - self._transform._position

    def convert_screen_vec_to_world_vec(self, vec : pygame.Vector2) -> pygame.Vector2:
        vec = pygame.Vector2(vec)
        return vec + self._transform._position

    def covert_screen_vec_to_window_vec(self, vec : pygame.Vector2) -> pygame.Vector2:
        vec = pygame.Vector2(vec)
        vec.x *= self._screen_to_window_scalar.x
        vec.y *= self._screen_to_window_scalar.y
        return vec

    def covert_window_vec_to_screen_vec(self, vec : pygame.Vector2) -> pygame.Vector2:
        vec = pygame.Vector2(vec)
        vec.x /= self._screen_to_window_scalar.x
        vec.y /= self._screen_to_window_scalar.y
        return vec



    #Derived Coordinate Conversion functions

    def convert_world_vec_to_window_vec(self, vec : pygame.Vector2) -> pygame.Vector2:
        return self.covert_screen_vec_to_window_vec(self.convert_world_vec_to_screen_vec(vec))

    def convert_window_vec_to_world_vec(self, vec : pygame.Vector2) -> pygame.Vector2:
        return self.convert_screen_vec_to_world_vec(self.covert_window_vec_to_screen_vec(vec))
        
    def get_blit_pos(self, vec: pygame.Vector2) -> pygame.Vector2:
        return self.convert_world_vec_to_screen_vec(vec)


    