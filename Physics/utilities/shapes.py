from .vector import Vector
import pygame

def is_valid_interval(interval):
    if not isinstance(interval, (tuple, list)):
        return False
    if len(interval) != 2:
        return False
    if (
            not isinstance(interval[0], Vector)
            or not isinstance(interval[1], Vector)
    ):
        return False
    return True

class Shape:
    def __init__(self, position):
        if not isinstance(position, Vector):
            raise TypeError("position must be a Vector.")
        self.position = position

class Circle(Shape):
    def __init__(self, position, radius, colour = pygame.Color(0, 0, 0)):
        if not isinstance(position, Vector):
            raise TypeError("position must be a Vector.")
        if not isinstance(colour, pygame.Color):
            raise TypeError("colour must be of type pygame.Color.")
        self.position = position
        self.radius = radius
        self.colour = colour

    def collides_with_interval(self, interval):
        if not is_valid_interval(interval):
            raise ValueError("interval is not a valid interval.")
        #Really bad names are used to make the t= line not look disgusting.
        #c is the centre of the circle.
        #r is the radius of the circle.
        #m and n are ends of the interval.
        #v is the direction of n from m.
        #t is the distance along the interval mn (from m), that the closest
        #point will be.
        #p is that point.
        #The closest point may also be one of the ends, so, it check that too.
        #If t isn't just magic. Look here:
        #http://twopointoh.weebly.com/sdd-t2/well-now-im-back-from-outer-space
        c = self.position
        r = self.radius
        m = interval[0]
        n = interval[1]
        v = n - m
        t = (v.x * c.x + v.y * c.y - v.x * m.x - v.y * m.y) / (v.x**2 + v.y**2)
        p = m + (v * t)
        if t <= 0:
            return ((c - m).magnitude <= r)
        elif t < 1:
            return ((c - p).magnitude <= r)
        else:
            return ((c - n).magnitude <= r)

    def collides_with_circle(self, circle):
        if not isinstance(circle, Circle):
            raise TypeError("circle must be a Circle.")
        distance_between = (self.position - circle.position).magnitude
        if distance_between <= self.radius + circle.radius:
            return True
        return False

    #def collides_with_point(self, point):

    #def collides_with_rectangle(self, point):

    def display(self, surface):
        pygame.draw.circle(
            surface,
            self.colour,
            (int(self.position.x), int(self.position.y)),
            self.radius
        )

class Rectangle(Shape):
    def __init__(self, position, width, height, colour = pygame.Color(0, 0, 0)):
        #Position is the top left corner.
        if not isinstance(position, Vector):
            raise TypeError("position must be a Vector.")
        if (
                not isinstance(width, (int, float))
                and not isinstance(height, (int, float))
            ):
            raise TypeError("width and height must be numbers.")
        if width <= 0 or height <= 0:
            raise ValueError("width and height must be greater than 0")
        if not isinstance(colour, pygame.Color):
            raise TypeError("colour must be of type pygame.Color.")
        self.position = position
        self.width = width
        self.height = height
        self.colour = colour

    def collides_with_point(self, point):
        if not isinstance(point, Vector):
            raise TypeError("point must be a Vector.")
        if (
                point.x > self.x
                and point.x < self.x + self.width
                and point.y > self.y
                and point.y < self.y + self.height
            ):
            return True
        else:
            return False

    #def collides_with_circle(self, circle):

    #def collides_with_interval(self, interval):

    #def collides_with_rectangle(self, rectangle):

    def display(self, surface):
        pygame.draw.rect(
            surface,
            self.colour,
            pygame.Rect(
                int(self.position.x),
                int(self.position.y),
                int(self.width),
                int(self.height)
            )
        )
