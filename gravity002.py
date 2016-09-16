import Physics
import random
import pygame

WIDTH = 800
HEIGHT = 600
G = 1000
NUM_MOVERS = 8
STARTING_VELOCITIES = True
CLEAR_SCREEN = True
MIN_MASS = 1
MAX_MASS = 20
CENTRE_MOMENTUM = True

scene = Physics.engine.init()

movers = []

def generate_movers_non_centred(number_of_movers):
    mover_list = []
    for i in range(number_of_movers):
        mass_size = random.randint(MIN_MASS, MAX_MASS)
        mover_list.append(
            Physics.utilities.Mover(
                scene.surface,
                Physics.utilities.Circle(
                    Physics.utilities.Vector(
                        random.randint(
                            int(WIDTH*2/10),
                            int(WIDTH*8/10)
                        ),
                        random.randint(
                            int(HEIGHT*2/10),
                            int(HEIGHT*8/10)
                        )
                    ),
                    mass_size,
                    pygame.Color(
                        random.randrange(256),
                        random.randrange(256),
                        random.randrange(256)
                    )
                ),
                mass_size
            )
        )
        if STARTING_VELOCITIES:
            movers[i].velocity = Physics.utilities.Vector(
                random.random() * 2 - 1,
                random.random() * 2 - 1
            ).get_at_magnitude(random.random() * 100)
    return mover_list

def generate_movers_centred(number_of_movers):
    movers_list = []
     

def setup():
    global movers
    if CENTRE_MOMENTUM:
        movers = generate_movers_non_centred()
    else:
        movers = generate_movers_centred()

def update():
    global movers

    if CLEAR_SCREEN:
        scene.surface.fill(pygame.Color(255, 255, 255))

    while None in movers:
        movers.remove(None)

    for a in range(len(movers)):
        for b in range(len(movers)):
            if a != b and movers[a] != None and movers[b] != None:
                displacement = movers[b].position - movers[a].position
                if movers[a].circle.collides_with_circle(movers[b].circle):
                    new_mass = movers[a].mass + movers[b].mass
                    ratio = movers[b].radius / (movers[a].radius + movers[b].radius)
                    new_position = movers[a].position + ratio * displacement
                    new_mover = Physics.utilities.Mover(
                        scene.surface,
                        Physics.utilities.Circle(
                            new_position,
                            movers[a].circle.radius + movers[b].circle.radius,
                            pygame.Color(
                                random.randrange(256),
                                random.randrange(256),
                                random.randrange(256)
                            )
                        ),
                        new_mass
                    )
                    new_momentum = (
                        movers[a].velocity * movers[a].mass
                        + movers[b].velocity * movers[b].mass
                    )
                    new_velocity = new_momentum / new_mass
                    new_mover.velocity = new_velocity
                    movers.append(new_mover)
                    movers[a] = None
                    movers[b] = None
                    continue
                distance = displacement.magnitude
                if distance < 5:
                    distance = 5
                if distance > 50:
                    distance = 50
                direction = displacement.unit_vector
                magnitude = (G * movers[a].mass * movers[b].mass) / distance**2
                gravity = direction * magnitude
                movers[a].apply_force(gravity)

        if movers[a] != None:
            movers[a].update(scene.delta_time)
            movers[a].display()

scene.start(setup, update, WIDTH, HEIGHT)
