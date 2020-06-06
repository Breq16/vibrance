import multiprocessing

import pygame

from . import pipe


class PyGameInput(pipe.PipeInput):
    def __init__(self):
        super().__init__("pygame")

        pygame_proc = multiprocessing.Process(target=self.runApp)
        pygame_proc.start()

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
                    self.launch("keydown", {"key": event.key})

                elif event.type == pygame.KEYUP:
                    self.launch("keyup", {"key": event.key})

            pygame.draw.rect(screen, pygame.Color("#"+color), (0, 0, 1000, 500))
            pygame.display.flip()
            clock.tick(30)

        pygame.quit()
