
import pygame, os
import random, math


import config.config as config

from states.state import State

array_bottom = config.SCREEN_HEIGHT
array_min_height = array_bottom - 70
array_max_height = array_bottom - 270

class SortingVisualizer(State):
    sorting_background = pygame.image.load(os.path.join(config.assets_dir, "graphics", "background.jpg"))
    def __init__(self, visualiser):
        super().__init__(visualiser)
        self.delay = 50 
        self.array_length = 10
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
        self.initilize = False
        self.sorting = False
        self.next = False
        self.generate_bars()

    def add_delay(self, delay=None):
        if not delay: delay = self.sorting_visualizer.delay
        self.target_time = delay + pygame.time.get_ticks()

    def update(self):
        if self.bars_array and pygame.time.get_ticks() >= self.target_time:
            self.sorting = True
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
                        self.generate_bars()
                        self.i = 0
                    self.swapped = False
            else:
                self.sorting = False
                self.generate_bars()
                self.i = 0

    def generate_bars(self):
        if not self.bars_array or self.sorting == False:
            self.bars_array = []
            if self.sorting_visualizer.array_modes["duplicates"]:
                self.numbers = [random.randrange(self.array_max_hei) for i in range(self.sorting_visualizer.array_length)]
            else: 
                height_gap = round((array_min_height - array_max_height)/self.sorting_visualizer.array_length)
                self.numbers = []
                i = array_max_height
                for j in range(self.sorting_visualizer.array_length):
                    self.numbers.append(i)
                    i += height_gap
                random.shuffle(self.numbers)
            if self.sorting_visualizer.array_modes["sort_mode"] == "nearly_sorted":
                unsorted_amount = math.ceil(self.sorting_visualizer.unsorted_amount/100 * self.sorting_visualizer.array_length)
                self.numbers.sort(reverse=self.sorting_visualizer.array_asc_order)
                for i in range(unsorted_amount):
                    random_num1 = random.randrange(3,len(self.numbers)-3)
                    random_num2 = random.randrange(random_num1-3, random_num1+4)
                    self.numbers[random_num1], self.numbers[random_num2] = self.numbers[random_num2], self.numbers[random_num1]

    def draw_bars(self, display):
        self.bars_color = [config.bars_color for i in range(self.sorting_visualizer.array_length)]
        bars_area = self.visualizer.SCREEN_WIDTH * 0.8
        bars_width =  round((bars_area * 0.7) / self.sorting_visualizer.array_length)
        bars_gap = math.ceil((bars_area * 0.3) / self.sorting_visualizer.array_length - 1)
        start_pos = round((self.visualizer.SCREEN_WIDTH - ((bars_gap * (self.sorting_visualizer.array_length - 1)) + (bars_width * self.sorting_visualizer.array_length)))/2)
        for i in range(self.sorting_visualizer.array_length):
            #self.bars_array.append(pygame.draw.line(display, self.bars_color[i], (start_pos,array_bottom), (start_pos,self.numbers[i]), bars_width))  # line
            self.bars_array.append(pygame.draw.rect(display, self.bars_color[i], (start_pos, self.numbers[i], bars_width, array_bottom - self.numbers[i])))  # rect
            start_pos += bars_gap + bars_width

    def remove_bar(self, display, bar):
        display.blit(SortingVisualizer.sorting_background, (bar.x, bar.y), bar)

    def render(self, display):
        if self.sorting:
            # get images size of bars and increase to max height, use it to replace a bar with the background and "remove" it
            img_cover_bar1, img_cover_bar2 = self.bars_array[self.j].copy(), self.bars_array[self.j+1].copy()
            img_cover_bar1.height, img_cover_bar1.y = array_bottom-array_max_height+1, array_max_height
            img_cover_bar2.height, img_cover_bar2.y = array_bottom-array_max_height+1, array_max_height
            self.remove_bar(display, img_cover_bar1)
            self.remove_bar(display, img_cover_bar2)
            pygame.draw.rect(display, self.bars_color[self.j], self.bars_array[self.j])
            pygame.draw.rect(display, self.bars_color[self.j+1], self.bars_array[self.j+1])
        else:
            display.blit(SortingVisualizer.sorting_background, (0,0))
            self.draw_bars(display)

    def screen_update(self, display):
        display.blit(SortingVisualizer.sorting_background, (0,0))
        self.draw_bars(display)


