from math import gamma
from pygame import Vector2
from abc import ABC, abstractmethod

from src.p_log import Log

class GameObject(ABC):
    COUNT : int = 0
    game_objects : list["GameObject"] = []

    def __init__(self, **kwargs):
        #Abstract variable name meant to be overridden
        self.name = kwargs.get("NAME", "Unnamed")
        
        self.__id : int= GameObject.COUNT 
        GameObject.COUNT += 1
        GameObject.game_objects.append(self)

    def get_id(self) -> int:
        return self.__id

    def update(self, delta_time = 1):
        Log.log_info(f"Game object with '{self.name}' and id '{self.__id}' was updated")

class Transform:
    def __init__(self, position : Vector2 = (0,0), rotation : Vector2 = (0,0)):
        self._position : Vector2 = Vector2(position)
        self._rotation : Vector2 = Vector2(rotation)

class Entity(GameObject):

    def __init__(self, transform : Transform = Transform()):
        GameObject.__init__(self)
        self._transform = transform
    
    def update(self, delta_time = 1):
        GameObject.update(self,delta_time)