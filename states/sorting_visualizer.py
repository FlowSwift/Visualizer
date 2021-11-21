
import pygame, os
import random

from pygame import display

from states.state import State

class SortingVisualizer(State):
    def __init__(self, visualiser):
        super().__init__(visualiser)
        self.bars = Bars(visualiser)
        self.started = False
        self.background = pygame.image.load(os.path.join(self.visualizer.assets_dir, "graphics", "background.jpg"))
        
        
    
    def update(self, delta_time, actions):
        if pygame.time.get_ticks() >= self.bars.target_time:
            self.bars.update()

    def render(self, display):
        if not self.started:
            display.blit(self.background, (0,0))
        self.bars.render(display)

class Bars:
    def __init__(self, visualizer):
        self.start_pos = 20 # left starting position of the array
        self.bars_gap = 8
        self.bars_width =  3
        self.delay = 10
        self.array_length = 30
        self.array_bottom = 270
        self.bars_array = []
        self.bars_color = []
        self.current_action = "compare"
        self.action_stage = 0
        self.bars_c = "red"
        self.bars_compared_c = "blue"
        self.bars_swapped_c = "green"
        self.complex_visualize = False
        self.target_time = 0
        self.i = 0
        self.j = 0

    def add_delay(self, delay=None):
        if not delay: delay = self.delay
        self.target_time = delay + pygame.time.get_ticks()

    def make_bars_array(self, display, numbers):
        current_pos = self.start_pos
        color = self.bars_c
        for num in numbers:
            self.bars_array.append(pygame.draw.line(display, color, (current_pos,400), (current_pos,200), self.bars_width))
            current_pos += self.bars_gap

    def draw_bars(self, display):
        current_pos = self.start_pos
        if not self.bars_array:
            self.bars_color = ["red" for i in range(self.array_length)]
            numbers = [random.randrange(20,70) for i in range(self.array_length)]
            for i in range(len(numbers)):
                self.bars_array.append(pygame.draw.line(display, self.bars_color[i], (current_pos,self.array_bottom), (current_pos,numbers[i]), self.bars_width))
                current_pos += self.bars_gap
        else:
            for i in range(len(self.bars_array)):
                pygame.draw.rect(display, self.bars_color[i], self.bars_array[i])

    def update(self):
        if self.bars_array:
            if self.i < len(self.bars_array):
                if self.j < (len(self.bars_array) - self.i - 1):
                    if self.current_action == "compare":
                        self.bars_color[self.j], self.bars_color[self.j+1] = self.bars_compared_c, self.bars_compared_c
                        self.add_delay(self.delay/2)
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
                            self.bars_array[self.j].height, self.bars_array[self.j+1].height = self.bars_array[self.j+1].height, self.bars_array[self.j].height  # get start and ending position of self.bars_array
                            self.bars_array[self.j].y, self.bars_array[self.j+1].y = self.bars_array[self.j+1].y, self.bars_array[self.j].y
                            self.current_action = "clear"
                            self.action_stage = 0
                            self.add_delay(self.delay)
                    elif self.current_action == "clear":
                        self.bars_color[self.j], self.bars_color[self.j+1] = self.bars_c, self.bars_c
                        self.current_action = "compare"
                        self.j+=1
                else:
                    self.j = 0
                    self.i += 1
    
    def render(self, display):
        self.draw_bars(display)


