
import pygame, os
import random, math


import config.config as config

from states.state import State


class SortingVisualizer(State):
    sorting_background = pygame.image.load(os.path.join(config.assets_dir, "graphics", "background.jpg"))
    def __init__(self, visualiser):
        super().__init__(visualiser)
        self.delay = 50 
        self.array_bottom = 479
        self.array_modes = {"sort_mode" : "random", "duplicates" : False}  # sort modes: "random" "nearly_sorted"
        self.array_asc_order = True
        self.unsorted_amount = 2  # precentage
        self.started = False
        self.prev_text = None
        self.bars = Bars(self, visualiser)
    
    def update(self, delta_time, actions):
        if actions["left_key"]:
            if self.delay > 0:
                self.delay -= 0.03
        if actions["right_key"]:
            if self.delay < 150:
                self.delay += 0.03
        if pygame.time.get_ticks() >= self.bars.target_time:
            self.bars.update()

    def render(self, display):
        if not self.started:
            display.blit(SortingVisualizer.sorting_background, (0,0))
            self.started = True
        if self.prev_text:
            display.blit(SortingVisualizer.sorting_background, (self.prev_text.x, self.prev_text.y), self.prev_text)
        self.prev_text = self.visualizer.draw_text(display, (f"Speed: {self.delay} :"), (69,69,69), self.visualizer.SCREEN_WIDTH/2, self.visualizer.SCREEN_HEIGHT/2 -100)
        self.visualizer.draw_text(display, "USE: <><><>", (69,69,69), self.visualizer.SCREEN_WIDTH/2, self.visualizer.SCREEN_HEIGHT/2 -200)
        self.bars.render(display)

class Bars:
    def __init__(self, sorting_visualizer, visualizer):
        self.sorting_visualizer = sorting_visualizer
        self.visualizer = visualizer
        self.array_length = 50
        self.bars_width =  round((self.visualizer.SCREEN_WIDTH * 0.8 * 0.7) / self.array_length)
        self.bars_gap = round((self.visualizer.SCREEN_WIDTH * 0.8 * 0.3) / self.array_length - 1)
        self.start_pos = visualizer.SCREEN_WIDTH/2 - (((self.bars_width * self.array_length) + (self.bars_gap * self.array_length - 1))/2)
        if self.array_length % 2 == 0: self.start_pos += (self.bars_gap + self.bars_width) / 2
        self.start_pos = round(self.start_pos)
        self.array_min_height = self.sorting_visualizer.array_bottom - 70
        self.array_max_height = self.sorting_visualizer.array_bottom - 270
        self.bars_array = []
        self.bars_color = []
        self.swapped = False
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
        if not delay: delay = self.sorting_visualizer.delay
        self.target_time = delay + pygame.time.get_ticks()

    def update(self):
        if self.bars_array:
            if self.next:
                self.current_action = "compare"
                self.j+=1
                self.next = False
            if self.i < len(self.bars_array):
                if self.j < (len(self.bars_array) - 1 - self.i):
                    if self.current_action == "compare":
                        self.bars_color[self.j], self.bars_color[self.j+1] = config.bars_compared_color,config.bars_compared_color
                        self.add_delay(self.sorting_visualizer.delay)
                        if self.bars_array[self.j].y < self.bars_array[self.j+1].y:  
                            self.current_action = "swap"
                        else:
                            self.current_action = "clear"
                    elif self.current_action == "swap":
                        self.swapped = True
                        if self.action_stage == 0:
                            self.bars_color[self.j], self.bars_color[self.j+1] = config.bars_swap_color, config.bars_swap_color
                            self.action_stage += 1
                            self.add_delay(self.sorting_visualizer.delay*3)
                        elif self.action_stage == 1:
                            self.bars_color[self.j], self.bars_color[self.j+1] = config.bars_swapped_color, config.bars_swapped_color
                            self.before_swap[0], self.before_swap[1] = self.bars_array[self.j], self.bars_array[self.j+1]
                            self.bars_array[self.j].height, self.bars_array[self.j+1].height = self.bars_array[self.j+1].height, self.bars_array[self.j].height  # get start and ending position of self.bars_array
                            self.bars_array[self.j].y, self.bars_array[self.j+1].y = self.bars_array[self.j+1].y, self.bars_array[self.j].y
                            self.current_action = "clear"
                            self.action_stage = 0
                            self.add_delay(self.sorting_visualizer.delay*3)
                    elif self.current_action == "clear":
                        self.bars_color[self.j], self.bars_color[self.j+1] = config.bars_color, config.bars_color
                        self.next = True
                else:
                    self.j = 0
                    self.i += 1
                    if not self.swapped:
                        self.sorting = False
                        self.i = 0
                    self.swapped = False
            else:
                self.sorting = False
                self.i = 0

    def draw_bars(self, display):
        current_pos = self.start_pos
        if not self.bars_array or self.sorting == False:
            self.sorting = True
            self.bars_array = []
            self.bars_color = [config.bars_color for i in range(self.array_length)]
            if self.sorting_visualizer.array_modes["duplicates"]:
                numbers = [random.randrange(self.array_max_height,self.array_min_height) for i in range(self.array_length)]
            else: 
                height_gap = round((self.array_min_height - self.array_max_height)/self.array_length)
                numbers = []
                i = self.array_max_height
                for j in range(self.array_length):
                    numbers.append(i)
                    i += height_gap
                random.shuffle(numbers)
            if self.sorting_visualizer.array_modes["sort_mode"] == "nearly_sorted":
                unsorted_amount = math.ceil(self.sorting_visualizer.unsorted_amount/100 * self.array_length)
                numbers.sort(reverse=self.sorting_visualizer.array_asc_order)
                for i in range(unsorted_amount):
                    random_num1 = random.randrange(3,len(numbers)-3)
                    random_num2 = random.randrange(random_num1-3, random_num1+4)
                    numbers[random_num1], numbers[random_num2] = numbers[random_num2], numbers[random_num1]
            for i in range(len(numbers)):
                #self.bars_array.append(pygame.draw.line(display, self.bars_color[i], (current_pos,self.sorting_visualizer.array_bottom), (current_pos,numbers[i]), self.bars_width))  # line
                self.bars_array.append(pygame.draw.rect(display, self.bars_color[i], (current_pos, numbers[i], self.bars_width, self.sorting_visualizer.array_bottom - numbers[i])))  # rect
                current_pos += self.bars_gap + self.bars_width

    def remove_bar(self, display, bar):
        display.blit(SortingVisualizer.sorting_background, (bar.x, bar.y), bar)

    def render(self, display):
        if self.sorting:
            # get images size of bars and increase to max height, use it to replace a bar with the background and "remove" it
            img_cover_bar1, img_cover_bar2 = self.bars_array[self.j].copy(), self.bars_array[self.j+1].copy()
            img_cover_bar1.height, img_cover_bar1.y = self.sorting_visualizer.array_bottom-self.array_max_height+1, self.array_max_height
            img_cover_bar2.height, img_cover_bar2.y = self.sorting_visualizer.array_bottom-self.array_max_height+1, self.array_max_height
            self.remove_bar(display, img_cover_bar1)
            self.remove_bar(display, img_cover_bar2)
            pygame.draw.rect(display, self.bars_color[self.j], self.bars_array[self.j])
            pygame.draw.rect(display, self.bars_color[self.j+1], self.bars_array[self.j+1])

        else:
            display.blit(SortingVisualizer.sorting_background, (0,0))
            self.draw_bars(display)
        


