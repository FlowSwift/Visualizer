
import pygame, os
import random

import config.config as config

from states.state import State


class SortingVisualizer(State):
    sorting_background = pygame.image.load(os.path.join(config.assets_dir, "graphics", "background.jpg"))
    def __init__(self, visualiser):
        super().__init__(visualiser)
        self.bars = Bars(visualiser)
        self.started = False
    
    def update(self, delta_time, actions):
        if pygame.time.get_ticks() >= self.bars.target_time:
            self.bars.update()

    def render(self, display):
        if not self.started:
            display.blit(SortingVisualizer.sorting_background, (0,0))
            self.started = True
        self.bars.render(display)

class Bars:
    def __init__(self, visualizer):
        self.start_pos = 20 # left starting position of the array
        self.bars_gap = 8
        self.bars_width =  3
        self.delay = 1 
        self.array_length = 30
        self.array_bottom = 270
        self.array_height = 50
        self.bars_array = []
        self.bars_color = []
        self.before_swap = [0,0]
        self.current_action = "compare"
        self.action_stage = 0
        self.complex_visualize = False
        self.target_time = 0
        self.i = 0
        self.j = 0
        self.sorting = False
        self.next = False

    def add_delay(self, delay=None):
        if not delay: delay = self.delay
        self.target_time = delay + pygame.time.get_ticks()

    def update(self):
        if self.bars_array:
            if self.next:
                self.current_action = "compare"
                self.j+=1
                self.next = False
            if self.i < len(self.bars_array):
                if self.j < (len(self.bars_array) - self.i - 1):
                    if self.current_action == "compare":
                        self.bars_color[self.j], self.bars_color[self.j+1] = config.bars_compared_color,config.bars_compared_color
                        self.add_delay(self.delay/1.5)
                        if self.bars_array[self.j].y < self.bars_array[self.j+1].y:  
                            self.current_action = "swap"
                        else:
                            self.current_action = "clear"
                    elif self.current_action == "swap":
                        if self.action_stage == 0:
                            self.bars_color[self.j], self.bars_color[self.j+1] = "green", "green"
                            self.action_stage += 1
                            self.add_delay(self.delay)
                        elif self.action_stage == 1:
                            self.before_swap[0], self.before_swap[1] = self.bars_array[self.j], self.bars_array[self.j+1]
                            self.bars_array[self.j].height, self.bars_array[self.j+1].height = self.bars_array[self.j+1].height, self.bars_array[self.j].height  # get start and ending position of self.bars_array
                            self.bars_array[self.j].y, self.bars_array[self.j+1].y = self.bars_array[self.j+1].y, self.bars_array[self.j].y
                            self.current_action = "clear"
                            self.action_stage = 0
                            self.add_delay(self.delay)
                    elif self.current_action == "clear":
                        self.bars_color[self.j], self.bars_color[self.j+1] = config.bars_color, config.bars_color
                        self.next = True
                else:
                    self.j = 0
                    self.i += 1
            else:
                self.i = 0
                self.sorting = False

    def draw_bars(self, display):
        current_pos = self.start_pos
        if not self.bars_array or self.sorting == False:
            self.sorting = True
            self.bars_array = []
            self.bars_color = [config.bars_color for i in range(self.array_length)]
            numbers = [random.randrange(self.array_height,150) for i in range(self.array_length)]
            for i in range(len(numbers)):
                self.bars_array.append(pygame.draw.line(display, self.bars_color[i], (current_pos,self.array_bottom), (current_pos,numbers[i]), self.bars_width))
                current_pos += self.bars_gap

    def remove_bar(self, display, bar):
        display.blit(SortingVisualizer.sorting_background, (bar.x, bar.y), bar)

    def render(self, display):
        if self.sorting:
            # get images size of bars and increase to max height, use it to replace a bar with the background and "remove" it
            img_cover_bar1, img_cover_bar2 = self.bars_array[self.j].copy(), self.bars_array[self.j+1].copy()
            img_cover_bar1.height, img_cover_bar1.y = self.array_bottom-self.array_height+1, self.array_height
            img_cover_bar2.height, img_cover_bar2.y = self.array_bottom-self.array_height+1, self.array_height

            self.remove_bar(display, img_cover_bar1)
            self.remove_bar(display, img_cover_bar2)
            pygame.draw.rect(display, self.bars_color[self.j], self.bars_array[self.j])
            pygame.draw.rect(display, self.bars_color[self.j+1], self.bars_array[self.j+1])

        else:
            display.blit(SortingVisualizer.sorting_background, (0,0))
            self.draw_bars(display)
        


