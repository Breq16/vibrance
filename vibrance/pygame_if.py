import multiprocessing

import pygame

from . import Interface, pipe


class PyGameInput(pipe.PipeInput):
    def __init__(self):
        super().__init__()

        pygame_proc = multiprocessing.Process(target=self.runApp)
        pygame_proc.start()

    def setColor(self, color):
        self.out_pipe.send(color)

    def runApp(self):
        pygame.init()
        color = "000000"

        screen = pygame.display.set_mode((1000, 500))
        pygame.display.set_caption("Vibrance")
        clock = pygame.time.Clock()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    self.launch("keydown", event.key)

                elif event.type == pygame.KEYUP:
                    self.launch("keyup", event.key)

            if self.in_pipe.poll():
                color = self.in_pipe.recv()

            pygame.draw.rect(screen, pygame.Color("#"+color), (0, 0, 1000, 500))
            pygame.display.flip()
            clock.tick(30)

        pygame.quit()

class PyGameInterface(Interface):
    def __init__(self):
        super().__init__()

        self.keydownCallback = None
        self.keyupCallback = None

    def keydown(self, func):
        self.keydownCallback = func
        return func

    def keyup(self, func):
        self.keyupCallback = func
        return func

    def run(self, pygame_in, ctrl):
        for event, key in pygame_in:
            if event == "keydown":
                if self.keydownCallback:
                    self.keydownCallback(key, pygame_in)
            elif event == "keyup":
                if self.keyupCallback:
                    self.keyupCallback(key, pygame_in)
            self.update(ctrl)
