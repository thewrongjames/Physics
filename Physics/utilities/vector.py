import math

def _sign(number):
    if number == 0:
        return 0
    return number / abs(number)

class Vector:
    def __init__(self, x=0, y=0):
        if not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
            raise TypeError("x any y must be floats or integers.")

        self.x = x
        self.y = y

    def __add__(self, adding_vector):
        if not isinstance(adding_vector, Vector):
            return NotImplemented
        return Vector(self.x+adding_vector.x, self.y+adding_vector.y)

    def __sub__(self, subing_vector):
        if not isinstance(subing_vector, Vector):
            return NotImplemented
        return Vector(self.x-subing_vector.x, self.y-subing_vector.y)

    def __mul__(self, multiplier):
        if not isinstance(multiplier, (int, float)):
            return NotImplemented
        return Vector(self.x * multiplier, self.y * multiplier)

    def __rmul__(self, multiplier):
        return self.__mul__(multiplier)

    def __truediv__(self, divisor):
        if not isinstance(divisor, (int, float)):
            return NotImplemented
        return Vector(self.x / divisor, self.y / divisor)

    @property
    def magnitude(self):
        return (self.x**2 + self.y**2)**0.5

    def normalise(self):
        divisor = self.magnitude
        if divisor != 0:
            self.x /= divisor
            self.y /= divisor

    def copy(self):
        return Vector(self.x, self.y)

    @property
    def inverted(self):
        vector = self.copy()
        vector *= -1
        return vector

    @property
    def inverted_x(self):
        vector = self.copy()
        vector.x = vector.x * -1
        return vector

    @property
    def inverted_y(self):
        vector = self.copy()
        vector.y = vector.y * -1
        return vector

    @property
    def unit_vector(self):
        vector = self.copy()
        vector.normalise()
        return vector

    @property
    def x_component(self):
        return Vector(self.x, 0)

    @property
    def y_component(self):
        return Vector(0, self.y)

    @property
    def tuple(self):
        return (self.x, self.y)

    def get_polar_from_reference(self, reference_point):
        #This will return this vector expressed as a distance and angle from
        #reference_point (also a vector vector).
        #Note, if the y axis will be inverted, then, so will the quadrants.
        #(i.e. 0 - PI/2 in the bottom right (0 still being the positive x axis
        #though)).
        if not isinstance(reference_point, Vector):
            raise TypeError("reference_point must be a vector.")
        y_difference = self.y - reference_point.y
        x_difference = self.x - reference_point.x
        if y_difference == 0:
            if x_difference >= 0:
                theta = 0
            else:
                theta = math.pi
        elif x_difference == 0:
            if y_difference > 0:
                theta = math.pi / 2
            elif y_difference < 0:
                theta = 3/2 * math.pi
        else:
            gradient = y_difference / x_difference
            if _sign(x_difference) == -1:
                theta = math.atan(gradient) + math.pi
            else:
                theta = math.atan(gradient)
        r = (self - reference_point).magnitude
        return (r, theta)

    @staticmethod
    def point_at_polar_from_reference(polar, reference_point):
        #This will return a vector created from a polar which is relative to
        #reference_point (also a vector).
        #Returns an absolute locative vector.
        if not isinstance(reference_point, Vector):
            raise TypeError("reference_point must be a Vector.")
        if not isinstance(polar, tuple):
            raise TypeError("polar must be a tuple.")
        if len(polar) != 2:
            raise ValueError("polar must contain two values.")
        r = polar[0]
        theta = polar[1]
        x = r * math.cos(theta) + reference_point.x
        y = r * math.sin(theta) + reference_point.y
        return Vector(x, y)

    def set_magnitude(self, magnitude):
        self.normalise()
        self *= magnitude

    def get_at_magnitude(self, magnitude):
        vector = self.unit_vector
        vector *= magnitude
        return vector

    def __eq__(self, other):
        if not isinstance(other, Vector):
            raise TypeError("other must be a vector")
        return (self.x == other.x and self.y == other.y)

    def __repr__(self):
        return "Vector ({}, {})".format(self.x, self.y)
