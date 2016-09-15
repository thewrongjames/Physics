import pygame
from .vector import Vector
from .shape import Rectangle
from .mover import Mover

class Liquid:
    def __init__(
            self,
            surface,
            rectangle,
            dragCoefficient = 0,
            colour = pygame.Color(0, 0, 0)
    ):
        if not isinstance(surface, pygame.Surface):
            raise TypeError("surface must be a pygame.Surface object.")
        if not isinstance(rectangle, Rectangle):
            raise TypeError("rect must be a Rectangle.")
        if not isinstance(dragCoefficient, (int, float)):
            raise TypeError("dragCoefficient must be a float or integer.")
        if not isinstance(colour, pygame.Color):
            raise TypeError("colour must be a pygame.color object.")
        self.surface = surface
        self.rectangle = rectangle
        self.dragCoefficient = dragCoefficient
        self.colour = colour

    def getDrag(self, mover):
        if not isinstance(mover, Mover):
            raise TypeError("mover must be a Mover.")
        drag = (
            self.dragCoefficient
            * mover.velocity.magnitude()**2
            * -(mover.velocity).unit_vector
        )
        return drag

    def display(self):
        pygame.draw.rect(
            self.surface,
            self.colour,
            pygame.Rect(
                self.rectangle.position.x,
                self.rectangle.position.y,
                self.rectangle.width,
                self.rectangle.height
            )
        )
