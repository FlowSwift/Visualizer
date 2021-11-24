
import pygame, os
import random, math


import config.config as config

from states.state import State

class SortingVisualizer(State):
    def __init__(self, visualizer_manager):
        super().__init__(visualizer_manager)
        self.visualizer_manager = visualizer_manager
        self.visualizer_manager.display_reset = True
        self.array_bottom = config.SCREEN_HEIGHT
        self.array_min_height = round(self.array_bottom / 1.2)
        self.array_max_height = round(self.array_bottom / 2.2)
        self.delay = 50
        self.array_length = 200
        self.array_modes = {"sort_mode" : "random", "duplicates" : True}  # sort modes: "random" "nearly_sorted"
        self.array_asc_order = True
        self.unsorted_amount = 1  # precentage
        self.reset_delay = 0
        self.target_time = 0
        self.sorting = False
        self.delay_input = pygame.time.get_ticks()
        self.overlay = Overlay(self, visualizer_manager)
        self.bubble_sort = BubbleSort(self, visualizer_manager, self.overlay)
        self.sorting_background = pygame.image.load(os.path.join(config.assets_dir, "graphics", "background.jpg")).convert()
        
    
    def update(self, delta_time, actions):
        if pygame.time.get_ticks() > self.delay_input:
            self.delay_input = pygame.time.get_ticks() + 30
            if actions["left_key"]:
                if self.delay > 0:
                    self.delay -= 1
                    self.overlay.render_bool = True
            if actions["right_key"]:
                if self.delay < 150:
                    self.delay += 1
                    self.overlay.render_bool = True
            if actions["down_key"]:
                if self.array_length > 10:
                    self.array_length -= 2
                    self.overlay.render_bool = True
            if actions["up_key"]:
                if self.array_length < 250:
                    self.array_length += 2
                    self.overlay.render_bool = True
            if actions["space"]:
                self.add_delay(200, self.reset_delay)
                self.bubble_sort.reset_loop()
        self.bubble_sort.update()
        

    def render(self, display):
        if not self.sorting:
            display.blit(self.sorting_background, (0,0))
            self.overlay.render_bool = True
        if self.overlay.render_bool:
            self.overlay.render_bool = False
            self.visualizer_manager.display_reset = True
            self.overlay.render(display)
        self.bubble_sort.render(display)

    def add_delay(self, delay=None, delay_type=None):
        if delay == None: delay = self.sorting_visualizer.delay
        if not delay_type: delay_type = self.target_time
        self.target_time = delay + pygame.time.get_ticks()

    def screen_update(self, display, height_diff):
        self.overlay.screen_update(display, height_diff)
        self.bubble_sort.screen_update(display, height_diff)


class Overlay:
    def __init__(self, sorting_visualizer, visualizer_manager):
        self.sorting_visualizer = sorting_visualizer
        self.visualizer_manager = visualizer_manager
        self.prev_text = None
        self.render_bool = True
        self.overlay_height = math.floor(self.visualizer_manager.SCREEN_HEIGHT * 0.20)
        self.box_height = math.floor(self.overlay_height * 0.4 )
        self.box_width = math.floor(self.visualizer_manager.SCREEN_WIDTH * 0.10)


    def update(self):
        pass

    def render(self, display):
        self.overlay_rect = pygame.draw.rect(display, config.overlay_color, (0, 0, self.visualizer_manager.SCREEN_WIDTH, self.overlay_height))
        self.render_text(display)
        
        #pygame.draw.rect(display, config.overlay_color, (0, 0, self.visualizer_manager.SCREEN_WIDTH, self.overlay_height))

    def render_text(self,display):
        #if self.prev_text:  # hide previous text(if not done by rendering the overlay under)
        #    display.blit(self.sorting_visualizer.sorting_background, (self.prev_text.x, self.prev_text.y), self.prev_text)
        start_stop_pos_x = math.floor(self.visualizer_manager.SCREEN_WIDTH * 0.08)
        start_stop_pos_y = math.floor(self.visualizer_manager.SCREEN_HEIGHT * 0.04)
        array_length_pos_x = start_stop_pos_x
        array_length_pos_y = math.floor(self.visualizer_manager.SCREEN_HEIGHT * 0.13)

        self.visualizer_manager.draw_text(display, (f"Speed: {self.sorting_visualizer.delay} :"), config.overlay_text_color, start_stop_pos_x, start_stop_pos_y, "font_sorting_overlay")
        self.visualizer_manager.draw_text(display, (f"Length: {self.sorting_visualizer.array_length} :"), config.overlay_text_color, array_length_pos_x, array_length_pos_y, "font_sorting_overlay")
        self.visualizer_manager.draw_text(display, "USE: <><><>", (69,69,69), self.visualizer_manager.SCREEN_WIDTH/2, self.visualizer_manager.SCREEN_HEIGHT/2 -200)

    def screen_update(self, display, height_diff):
        self.overlay_height = math.floor(self.visualizer_manager.SCREEN_HEIGHT * 0.20)
        self.box_height = math.floor(self.overlay_height * 0.4 )
        self.box_width = math.floor(self.visualizer_manager.SCREEN_WIDTH * 0.10)
        self.render(display)

    def render_overlay(self, display):
        pass

class BubbleSort:
    def __init__(self, sorting_visualizer, visualizer_manager, overlay):
        self.sorting_visualizer = sorting_visualizer
        self.visualizer_manager = visualizer_manager
        self.overlay = overlay
        self.bars_array = []
        self.bars_color = []
        self.swapped = False
        self.before_swap = [0,0]
        self.current_action = "compare"
        self.action_stage = 0
        self.complex_visualize = False
        self.i = 0
        self.j = 0
        self.initilize = False
        self.next = False

    def update(self):
        if self.bars_array and pygame.time.get_ticks() >= self.sorting_visualizer.target_time:
            if self.next:
                self.current_action = None
                self.j+=1
                self.next = False
            if self.i < len(self.bars_array):
                if self.j < (len(self.bars_array) - 1 - self.i):
                    if self.current_action == "compare" or not self.current_action:
                        self.bars_color[self.j], self.bars_color[self.j+1] = config.bars_compared_color,config.bars_compared_color
                        self.sorting_visualizer.add_delay(self.sorting_visualizer.delay)
                        if self.bars_array[self.j].y < self.bars_array[self.j+1].y:  
                            self.current_action = "swap"
                        else:
                            self.current_action = "clear"
                    elif self.current_action == "swap":
                        self.swapped = True
                        if self.action_stage == 0:
                            self.bars_color[self.j], self.bars_color[self.j+1] = config.bars_swap_color, config.bars_swap_color
                            self.action_stage += 1
                            self.sorting_visualizer.add_delay(self.sorting_visualizer.delay*3)
                        elif self.action_stage == 1:
                            self.bars_color[self.j], self.bars_color[self.j+1] = config.bars_swapped_color, config.bars_swapped_color
                            self.before_swap[0], self.before_swap[1] = self.bars_array[self.j], self.bars_array[self.j+1]
                            self.bars_array[self.j].height, self.bars_array[self.j+1].height = self.bars_array[self.j+1].height, self.bars_array[self.j].height  # get start and ending position of self.bars_array
                            self.bars_array[self.j].y, self.bars_array[self.j+1].y = self.bars_array[self.j+1].y, self.bars_array[self.j].y
                            self.current_action = "clear"
                            self.action_stage = 0
                            self.sorting_visualizer.add_delay(self.sorting_visualizer.delay*3)
                    elif self.current_action == "clear":
                        self.bars_color[self.j], self.bars_color[self.j+1] = config.bars_color, config.bars_color
                        self.next = True
                else:
                    self.j = 0
                    self.i += 1
                    if not self.swapped:
                        self.reset_loop()
                    self.swapped = False
            else:
                self.reset_loop()

    def reset_loop(self):
        self.current_action = None
        self.sorting_visualizer.sorting = False
        self.generate_bars()
        self.i = 0
        self.j = 0

    def generate_bars(self):
        self.bars_array = []
        self.bars_color = [config.bars_color for i in range(self.sorting_visualizer.array_length)]
        if not self.bars_array or self.sorting_visualizer.sorting == False:
            if self.sorting_visualizer.array_modes["duplicates"]:
                self.numbers = [random.randrange(self.sorting_visualizer.array_max_height, self.sorting_visualizer.array_min_height) for i in range(self.sorting_visualizer.array_length)]
            else: 
                height_gap = round((self.sorting_visualizer.array_min_height - self.sorting_visualizer.array_max_height)/self.sorting_visualizer.array_length)
                self.numbers = []
                i = self.sorting_visualizer.array_max_height
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

    def draw_bars(self, display, height_diff=0):
        bars_area = self.visualizer_manager.SCREEN_WIDTH * 0.8
        bars_width =  round((bars_area * 0.7) / self.sorting_visualizer.array_length)
        bars_gap = math.ceil((bars_area * 0.3) / self.sorting_visualizer.array_length - 1)
        start_pos = round((self.visualizer_manager.SCREEN_WIDTH - ((bars_gap * (self.sorting_visualizer.array_length - 1)) + (bars_width * self.sorting_visualizer.array_length)))/2)
        self.generate_bars()
        for i in range(self.sorting_visualizer.array_length):
            #self.bars_array.append(pygame.draw.line(display, self.bars_color[i], (start_pos,self.sorting_visualizer.array_bottom), (start_pos,self.numbers[i]), bars_width))  # line
            self.bars_array.append(pygame.draw.rect(display, self.bars_color[i], (start_pos, self.numbers[i], bars_width, self.sorting_visualizer.array_bottom - self.numbers[i])))  # rect
            start_pos += bars_gap + bars_width


    def remove_bar(self, display, bar):
        display.blit(self.sorting_visualizer.sorting_background, (bar.x, bar.y), bar)

    def render(self, display):
        if self.sorting_visualizer.sorting:
            # get images size of bars and increase to max height, use it to replace a bar with the background and "remove" it
            img_cover_bar1, img_cover_bar2 = self.bars_array[self.j].copy(), self.bars_array[self.j+1].copy()
            img_cover_bar1.height, img_cover_bar1.y = self.sorting_visualizer.array_bottom-self.sorting_visualizer.array_max_height+1, self.sorting_visualizer.array_max_height
            img_cover_bar2.height, img_cover_bar2.y = self.sorting_visualizer.array_bottom-self.sorting_visualizer.array_max_height+1, self.sorting_visualizer.array_max_height
            self.remove_bar(display, img_cover_bar1)
            self.remove_bar(display, img_cover_bar2)
            pygame.draw.rect(display, self.bars_color[self.j], self.bars_array[self.j])
            pygame.draw.rect(display, self.bars_color[self.j+1], self.bars_array[self.j+1])
        else:
            self.sorting_visualizer.sorting = True
            
            self.draw_bars(display)

    def screen_update(self, display, height_diff):
        display.blit(self.sorting_visualizer.sorting_background, (0,0))
        self.overlay.render_text(display)
        self.reset_loop()
        self.sorting_visualizer.array_bottom = self.visualizer_manager.SCREEN_HEIGHT
        self.sorting_visualizer.array_min_height = round(self.sorting_visualizer.array_bottom / 1.2)
        self.sorting_visualizer.array_max_height = round(self.sorting_visualizer.array_bottom / 2.2)