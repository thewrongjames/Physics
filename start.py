import Physics
import random
import pygame

WIDTH = 800
HEIGHT = 600
G = 1000

scene = Physics.engine.init()

movers = []
num_movers = 10

def setup():
    global movers
    for i in range(num_movers):
        mass_size = random.randint(1, 10)
        movers.append(
            Physics.utilities.Mover(
                scene.surface,
                Physics.utilities.Circle(
                    Physics.utilities.Vector(
                        random.randint(
                            int(WIDTH*1/10),
                            int(WIDTH*9/10)
                        ),
                        random.randint(
                            int(HEIGHT*1/10),
                            int(HEIGHT*9/10)
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

def update():
    global movers

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
