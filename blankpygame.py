import pygame
from pygame.locals import QUIT, KEYUP, K_ESCAPE


def main():
    pygame.init()
    pygame.display.set_mode((400, 300))
    pygame.display.set_caption('Hello Pygame World!')
    while True:  # main game loop
        for event in pygame.event.get():
            if (event.type == QUIT or
                    (event.type == KEYUP and event.key == K_ESCAPE)):
                pygame.quit()
                return

if __name__ == '__main__':
    main()
