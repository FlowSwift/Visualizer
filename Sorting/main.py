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

numbers = [random.randrange(300,600) for i in range(ARRAY_LENGTH)]
start_pos = 200 # starting position of the array
bars_gap = 8
delay = 500

bars_c = "red"
bars_compared_c = "blue"
bars_swapped_c = "green"

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
def draw_array(numbers, start_pos, bars_gap, current_left_main=0, check=False, swapped=False):
    global ARRAY_BOTTOM  # starting height of bars
    WINDOW.fill(BACKGROUND)  # background
    current_pos = start_pos - bars_gap  # bar position
    skip = False
    for current_left in range(len(numbers)): 
        current_pos += bars_gap  # shift to next bar
        if current_left == current_left_main:  # check if drawing the same bar the function was called for
            # if swapping values, make thee pair green
            if swapped:
                color = bars_swapped_c
            else:
                color = bars_compared_c
            pygame.draw.line(WINDOW, color, (current_pos,ARRAY_BOTTOM), (current_pos,numbers[current_left_main]), 3)
            pygame.draw.line(WINDOW, color, (current_pos+bars_gap,ARRAY_BOTTOM), (current_pos+bars_gap,numbers[current_left_main+1]), 3)

            skip = True #skip next pair to not overide color current right bar color
            continue
        elif skip == True:
            skip = False
            continue
        else: # make the rest of the bars red
            color = bars_c
            pygame.draw.line(WINDOW, color, (current_pos,ARRAY_BOTTOM), (current_pos,numbers[current_left]), 3)
    pygame.display.update()

def main():
    run = True
    while run:
        check_events()

        # bubble_sort
        for n in range(len(numbers)):
            swapped = False
            for i in range(len(numbers)-1-n):
                check_events()  # check for quitting
                draw_array(numbers, start_pos, bars_gap,i)  # draw the current array
                animate_delay(int(delay/3))  # wait
                if numbers[i+1] > numbers[i]:  # swap numbers if right bigger than left and animate
                    swapped = True
                    tmp = numbers[i]
                    numbers[i], numbers[i+1] = numbers[i+1], tmp
                    draw_array (numbers, start_pos, bars_gap, i, True, swapped)
                    pygame.display.update()
                    animate_delay(int(delay/1.5))
            if swapped == False:  # check if any swaps were done and if not, array is sorted
                break

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main() 