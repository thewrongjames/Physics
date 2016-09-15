from .vector import Vector

def get_line_collision(
        line_1_point_1,
        line_1_point_2,
        line_2_point_1,
        line_2_point_2
    ):
    x1, y1 = line_1_point_1.tuple
    x2, y2 = line_1_point_2.tuple
    x3, y3 = line_2_point_1.tuple
    x4, y4 = line_2_point_2.tuple
    if x2 - x1 == 0 and x4 - x3 == 0:
        raise ValueError("The lines do not collide.")
    if y2 - y1 == 0 and y4 - y3 == 0:
        raise ValueError("The lines do not collide.")
    if x2 - x1 == 0:
        m2 = (y4 - y3) / (x4 - x3)
        return Vector(x1, m2 * (x1 - x3) + y3)
    if x4 - x3 == 0:
        m1 = (y2 - y1) / (x2 - x1)
        return Vector(x3, m1 * (x3 - x1) + y1)
    m1 = (y2 - y1) / (x2 - x1)
    m2 = (y4 - y3) / (x4 - x3)
    if m1 == m2:
        raise ValueError("The lines do not collide.")
    x = ((x1 * m1) - (x3 * m2) - y1 + y3) / (m1 - m2)
    y = m1 * (x - x1) + y1
    return Vector(x, y)

def in_direction(test_point, start, direction):
    if direction.x != 0:
        return ((test_point.x - start.x) / direction.x >= 0)
    elif direction.y != 0:
        return ((test_point.y - start.y) / direction.y >= 0)
    else:
        raise Exception

def point_is_on_line(point, interval):
    x1, y1 = interval[0].tuple
    x2, y2 = interval[1].tuple
    if x2 == x1:
        return (point.x == x1)
    m = (y2 - y1) / (x2 - x1)
    y = m * (point.x - x1) + y1
    return (point.y == y)

def point_is_on_interval(point, interval):
    direction = interval[1] - interval[0]
    return (
        point_is_on_line(point, interval)
        and
        in_direction(point, interval[0], direction)
        and not in_direction(point, interval[1], direction)
    )

def point_is_on_this_side_of_interval(reference, point, interval):
    try:
        collision = get_line_collision(reference, point, *interval)
    except ValueError:
        return True
    distance_to_point = (point - reference).magnitude
    distance_to_collision = (collision - reference).magnitude
    direction = point - reference
    correct_direction = in_direction(collision, reference, direction)
    return (distance_to_point <= distance_to_collision) or not correct_direction

def displacement_of_collision_of_interval_and_line_to_point_from_reference_from_point(
            reference,
            point,
            interval
    ):
    #In this function the reference simply gives direction.
    #If you were to to draw a line through reference and point, and then find
    #where that collides with the line made by the interval, and then get the
    #displacement of that collision from point, that would be the output of
    #this function
    collision = get_line_collision(reference, point, *interval)
    return collision - point

def midpoint(point1, point2):
    return Vector((point2.x + point1.x) / 2, (point2.y + point1.y) / 2)

def vector_to_line(point, interval):
    #This returns the perpendicular vector from a point to a line.
    c = point
    m = interval[0]
    n = interval[1]
    v = n - m
    t = (v.x * c.x + v.y * c.y - v.x * m.x - v.y * m.y) / (v.x**2 + v.y**2)
    p = m + (v * t)
    return p - c
