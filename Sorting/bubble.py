import sys

import random
import pygame
from pygame import draw
from pygame import display
from pygame import color
from pygame.time import delay

 #  initilize pygame
pygame.init()
WIDTH, HEIGHT = 1366, 768
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
BACKGROUND_SURF = pygame.image.load("graphics/background.jpg").convert()
BACKGROUND_IMG = BACKGROUND_SURF

pygame.display.set_caption("Visualizer!")
clock = pygame.time.Clock()
FPS = 60
clock.tick(FPS)

BACKGROUND = "black"
ARRAY_BOTTOM = 700
ARRAY_LENGTH = 20
NUMBERS = [random.randrange(300,600) for i in range(ARRAY_LENGTH)]

start_pos = 200 # left starting position of the array
bars_gap = 8
bars_width =  3
DELAY = 150
bars_c = "red"
bars_compared_c = "blue"
bars_swapped_c = "green"
complex_visualize = False



def check_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

def animate_delay(delay=1000):
    target_time = pygame.time.get_ticks() + delay
    while pygame.time.get_ticks() < target_time:
        pass

def draw_array(numbers, start_pos, bars_gap, width = 3):
    current_pos = start_pos
    bars = []  # list of all the bars rectangles
    for num in numbers:
        color = bars_c
        bars.append(pygame.draw.line(WINDOW, color, (current_pos,ARRAY_BOTTOM), (current_pos,num), width))
        current_pos += bars_gap
    pygame.display.update()
    return bars

def color_rect(bar, color):
    pygame.draw.rect(WINDOW, color, bar)
    pygame.display.update()

def draw_pair(bars, color=bars_compared_c):
    color_rect(bars[0], color)
    color_rect(bars[1], color)

  # remove a rectangle and replace it with a portion of the original image
def remove_rect(bar):
    WINDOW.blit(BACKGROUND_IMG, (bar.x, bar.y), (bar))

  # remove 2 bars and swap them
def swap_bars(bars, delay=DELAY):
    remove_rect(bars[0])
    remove_rect(bars[1])
    bars[0].height, bars[1].height = bars[1].height, bars[0].height  # get start and ending position of bars
    bars[0].y, bars[1].y = bars[1].y, bars[0].y
    draw_pair(bars[0:2], color=bars_swapped_c)
    animate_delay(delay)

  # step by step swap
def swap_bars_complex(bars, delay=DELAY):
    draw_pair(bars[0:2], color="pink")
    pygame.display.update()
    animate_delay(DELAY)
    remove_rect(bars[0])
    pygame.draw.rect(WINDOW, "pink", (bars[1].left-bars_gap, bars[1].top, bars[1].width, bars[1].height))
    pygame.display.update()
    animate_delay(DELAY)
    remove_rect(bars[1])
    pygame.draw.rect(WINDOW, "pink", (bars[0].left+bars_gap, bars[0].top, bars[0].width, bars[0].height))
    pygame.display.update()
    animate_delay(DELAY)
    bars[0].height, bars[1].height = bars[1].height, bars[0].height  # get start and ending position of bars
    bars[0].y, bars[1].y = bars[1].y, bars[0].y
    draw_pair(bars[0:2], color=bars_swapped_c)
    animate_delay(DELAY*2)

def main():
    WINDOW.blit(BACKGROUND_IMG, (0, 0))  # background
    bars = []
    while True:
        check_events()
        # bubble_sort
        for n in range(len(NUMBERS)):
            swapped = False
            for i in range(len(NUMBERS)-1-n):  # on every main loop iteration, do one less inner loop iteration (n)
                check_events()  # check for input
                if not bars:
                    bars = draw_array(NUMBERS, start_pos, bars_gap, bars_width)  # draw and get a list of all the bars rectangles
                    pygame.display.update()
                draw_pair(bars[i:i+2])  # color the comparing bars
                animate_delay(int(DELAY/1.5))
                if bars[i].y < bars[i+1].y:
                    swapped = True
                    if complex_visualize:
                        swap_bars_complex(bars[i:i+2], delay=int(DELAY))  # show step by step
                    else:
                        swap_bars(bars[i:i+2], delay=int(DELAY))  # remove original then color new swapped bars
                draw_pair(bars[i:i+2], color=bars_c)  # recolor pair to orignal bar color
            if swapped == False:
                break

if __name__ == "__main__":
    main()