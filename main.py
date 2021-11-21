import sys

import pygame
import Sorting.bubble as sorting

pygame.init()
WIDTH, HEIGHT = 1366, 768
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
BACKGROUND_SURF = pygame.image.load("graphics/background.jpg").convert()
BACKGROUND_IMG = BACKGROUND_SURF

pygame.display.set_caption("Visualizer!")
clock = pygame.time.Clock()
FPS = 60
clock.tick(FPS)

def check_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

def main_menu():
    WINDOW.blit(BACKGROUND_IMG, (0, 0))
    pygame.display.update()

def main():
    screen = "main_menu"
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    screen = "a"
        if screen == "main_menu":
            main_menu()
        else: 
            sorting.main()
            screen = "main_menu"

if __name__ == "__main__":
    main()