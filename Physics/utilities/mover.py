import pygame
from .vector import Vector
from .shapes import Circle

class Mover():
    def __init__(
            self,
            surface,
            circle = Circle(Vector(0, 0), 10, pygame.Color(0, 0, 0)),
            mass = 1.0,
    ):
        if not isinstance(surface, pygame.Surface):
            raise TypeError("surface must be of type pygame.Surface.")
        if not isinstance(circle, Circle):
            raise TypeError("circle must be a Circle.")
        if not isinstance(mass, (float, int)):
            raise TypeError("mass must be either a float or an int.")

        self.surface = surface
        self.circle = circle
        self.mass = mass
        self.velocity = Vector(0, 0)
        self.acceleration = Vector(0, 0)

    @property
    def position(self):
        return self.circle.position

    @position.setter
    def position(self, value):
        if not isinstance(value, Vector):
            raise TypeError("position can only be set to a Vector.")
        self.circle.position = value

    @property
    def radius(self):
        return self.circle.radius

    @radius.setter
    def radius(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("radius must be a float or an int.")
        self.circle.radius = value

    def update(self, delta_time):
        self.velocity += self.acceleration * delta_time
        self.position += self.velocity * delta_time
        self.acceleration *= 0

    def apply_force(self, force):
        if not isinstance(force, Vector):
            raise TypeError("force must be a Vector.")
        if self.mass != 0:
            self.acceleration += (force / self.mass)
        else:
            raise ValueError("Force may only be applied to movers with mass.")

    def display(self):
        self.circle.display(self.surface)
