import sys

import random
import pygame

 #  initilize pygame
pygame.init()
WIDTH, HEIGHT = 1366, 768
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Visualizer!")
clock = pygame.time.Clock()
FPS = 60
clock.tick(FPS)

BACKGROUND = "black"
ARRAY_BOTTOM = 700
ARRAY_LENGTH = 20
def check_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

 #  wait between animations
def animate_delay(delay=1000):
    target_time = pygame.time.get_ticks() + delay
    while pygame.time.get_ticks() < target_time:
        pass

 #  replace array with new array
def draw_array(numbers, start_pos, bars_gap):
    global ARRAY_BOTTOM  # starting height of bars
    WINDOW.fill(BACKGROUND)  # background
    current_pos = start_pos - bars_gap  # bar position
    for current_left in range(len(numbers)): 
        current_pos += bars_gap  # shift to next bar
        color = "red" 
        pygame.draw.line(WINDOW, color, (current_pos,ARRAY_BOTTOM), (current_pos,numbers[current_left]), 3)
    pygame.display.update()

def draw_pair(pair, left_pos, right_pos, color):
    pygame.draw.line(WINDOW, BACKGROUND, (left_pos, ARRAY_BOTTOM), (left_pos,0), 3)
    pygame.draw.line(WINDOW, BACKGROUND, (right_pos, ARRAY_BOTTOM), (right_pos,0), 3)
    pygame.draw.line(WINDOW, color, (left_pos, ARRAY_BOTTOM), (left_pos, pair[0]), 3)
    pygame.draw.line(WINDOW, color, (right_pos, ARRAY_BOTTOM), (right_pos, pair[1]), 3)
    pygame.display.update()
    

def main():
    numbers = [random.randrange(300,600) for i in range(ARRAY_LENGTH)]
    # numbers = [300, 350, 300, 300, 350, 300]
    start_pos = 200 # starting position of the array
    bars_gap = 8
    delay = 50
    run = True
    while run:
        check_events()

        # bubble_sort
        for n in range(len(numbers)):
            swapped = False
            for i in range(len(numbers)-1-n):
                check_events()  # check for quitting
                draw_array(numbers, start_pos, bars_gap)
                animate_delay(int(delay/2))
                left_pos, right_pos = start_pos + bars_gap*(i), start_pos + (bars_gap*(i)+bars_gap)
                draw_pair(numbers[i:i+2], left_pos, right_pos, "blue")
                animate_delay(int(delay))
                if numbers[i+1] > numbers[i]:
                    swapped = True
                    tmp = numbers[i]
                    numbers[i], numbers[i+1] = numbers[i+1], tmp
                    draw_pair(numbers[i:i+2], left_pos, right_pos, "green")
                    animate_delay(int(delay*2))
            if swapped == False:
                break

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()