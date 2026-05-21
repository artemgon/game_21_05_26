import pygame
import sys
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BLACK

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Battle Village")
    clock = pygame.time.Clock() 

    while True:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(BLACK)

        pygame.display.flip() 

    pygame.quit()
    sys.exit()

if __name__ == "__main__": 
    main()