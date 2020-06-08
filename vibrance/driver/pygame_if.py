import multiprocessing

import pygame

from . import pipe


class PyGameDriver(pipe.PipeDriver):
    def __init__(self, name=""):
        super().__init__(name, driver_type="pygame")

    def open(self):
        self.proc = multiprocessing.Process(target=self.runApp)
        self.proc.start()
        super().open()

    def close(self):
        super().close()
        self.proc.terminate()
        self.proc.join()
        self.proc.close()
        self.proc = None

    def runApp(self):
        pygame.init()
        color = "000000"

        screen = pygame.display.set_mode((50, 50))
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

    def getStatus(self):
        status = {}

        if self.enabled:
            status["health"] = "success"
            status["message"] = "PyGame Enabled"
        else:
            status["health"] = "inactive"
            status["message"] = "PyGame Disabled"

        return status
