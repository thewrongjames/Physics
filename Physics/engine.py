import pygame, time, sys,
from pygame.locals import *

class Engine:
    def __init__(self):
        self.events = None
        self.surface = None
        self.delta_time = 0

    def start(self, setup, update, width, height, caption = "Window"):
        #The setup and update functions are called at the begining,
        #and every frame, respectively.

        self.caption = str(caption)

        if not callable(setup) or not callable(update):
            raise Exception("setup and update must be callable.")

        try:
            self.width = int(width)
            self.height = int(height)
        except ValueError:
            raise ValueError("Cannot convert width and height to integers.")

        pygame.init()
        self.surface = pygame.display.set_mode((self.width, self.height))
        self.surface.fill(pygame.Color(255, 255, 255))

        setup()

        pygame.display.set_caption(self.caption)

        while True:
            start_time = time.time()
            self.events = pygame.event.get()

            update()

            for event in self.events:
                if event.type == KEYDOWN:.
                    if event.key == K_ESCAPE:
                        pygame.event.post(pygame.event.Event(QUIT))
                elif event.type == QUIT:
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
        self.delta_time = time.time() - start_time

def init():
    engine = Engine()
    return engine
