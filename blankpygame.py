import pygame
import sys
from pygame.locals import QUIT


def main():
    pygame.init()
    pygame.display.set_mode((400, 300))
    pygame.display.set_caption('Hello Pygame World!')
    while True:  # main game loop
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

if __name__ == '__main__':
    main()
