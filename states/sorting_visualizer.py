
import pygame, os
import random, math

from pygame.draw import rect


import config.config as config

from states.state import State


  # main sorting state
class SortingVisualizer(State):
    def __init__(self, visualizer_manager):
        super().__init__(visualizer_manager)
        self.visualizer_manager = visualizer_manager
        self.visualizer_manager.display_reset = True  # change to true when need to refresh the entire display instead of the bar area
        self.bars_array = []
        self.bars_color = []
        self.array_bottom = config.SCREEN_HEIGHT
        self.array_min_height = round(self.array_bottom / 1.2)  # bars min and max possible height
        self.array_max_height = round(self.array_bottom / 2.2)
        self.array_length = 50  # bars amount
        self.array_modes = {"array_mode" : "random", "duplicates" : True}  # sort modes: "random" "nearly_sorted"
        self.array_asc_order = True  # IN PROGRESS
        self.unsorted_amount = 10  # How many swaps for a nearly sorted list
        self.reset_delay = 0  # delay for resetting array
        self.reset_delay_time = 0  # delay check
        self.delay = 50  # animation delay
        self.delay_input = 0  # delay check for key input
        self.sorting = False
        self.overlay = Overlay(self, visualizer_manager)
        self.bubble_sort = None #BubbleSort(self, self.visualizer_manager, self.overlay)
        self.sorting_background = pygame.image.load(os.path.join(config.assets_dir, "graphics", "background.jpg")).convert()
        
    # check and update changes
    def update(self, delta_time, actions):
        if not self.sorting:  # init if no sort going
            self.bubble_sort = BubbleSort(self, self.visualizer_manager, self.overlay)
        # check for key inputs if not on timeout.
        if pygame.time.get_ticks() > self.delay_input:
            if actions["left_key"]:
                if self.delay > 0:
                    self.delay -= 1
                    self.overlay.render_bool = True
                    self.delay_input = pygame.time.get_ticks() + 30
            if actions["right_key"]:
                if self.delay < 150:
                    self.delay += 1
                    self.overlay.render_bool = True
                    self.delay_input = pygame.time.get_ticks() + 30
            if actions["down_key"]:
                if self.array_length > 10:
                    self.array_length -= 2
                    self.overlay.render_bool = True
                    self.delay_input = pygame.time.get_ticks() + 30
            if actions["up_key"]:
                if self.array_length < 250:
                    self.array_length += 2
                    self.overlay.render_bool = True
                    self.delay_input = pygame.time.get_ticks() + 30
        if actions["space"]:  # different delay time
            if pygame.time.get_ticks() > self.reset_delay_time:
                self.reset_delay_time = pygame.time.get_ticks() + self.reset_delay
                if self.bubble_sort:
                    self.bubble_sort.reset_loop()
        self.overlay.update(actions)
        # check what sort selected and update
        if self.bubble_sort:
            self.bubble_sort.update()
        
    # check if needed and render changes on screen
    def render(self, display):
        if not self.sorting:
            display.blit(self.sorting_background, (0,0))
            self.overlay.render_bool = True
        # check if something requires a full render of the screen using render_bool and send signal to the visualizer_main state using display_reset
        if self.overlay.render_bool:
            self.overlay.render_bool = False
            self.visualizer_manager.display_reset = True
            self.overlay.render(display)
        # check what sort selected and render
        if self.bubble_sort:
            self.bubble_sort.render(display)

    # called when the screen is resized
    def screen_update(self, display, height_diff):
        self.overlay.screen_update(display, height_diff)
        if self.bubble_sort:
            self.bubble_sort.screen_update(display, height_diff)


class Overlay:
    def __init__(self, sorting_visualizer, visualizer_manager):
        self.sorting_visualizer = sorting_visualizer
        self.visualizer_manager = visualizer_manager
        self.render_bool = True # check if overlay was changed
        self.overlay_height = math.floor(self.visualizer_manager.SCREEN_HEIGHT * 0.20)
        self.array_modes = ["random", "nearly_sorted"]  # used to set selection colors
        self.array_modes_colors = {"random":config.overlay_text_selected, "nearly_sorted":config.overlay_text_color}  # current colors of the modes selection
        self.array_mode_selected = 0  # 0 for random, 1 for nearly_sorted
        self.duplicates_modes = ["true", "false"]  # used to set selection colors
        self.duplicates_modes_colors = {"true":config.overlay_text_selected, "false":config.overlay_text_color}  # current colors of the modes selection
        self.duplicates_mode_selected = 0  # 0 for True, 1 for False


    def update(self, actions):
        after_click_delay = 500  # clicking timeout
        mouse_hold_delay = 200
        array_mode_button_change = False
        array_duplicates_button_change = False
        # check mouse inputs and add delay
        if pygame.time.get_ticks() > self.sorting_visualizer.delay_input:
            mouse_pos = pygame.mouse.get_pos()
            if actions["left_mouse"]:
                
                try:
                    if self.array_mode_selection1.collidepoint(mouse_pos):
                        self.array_mode_selected = 0
                        self.render_bool = True
                        array_mode_button_change = True
                        self.sorting_visualizer.array_modes["array_mode"] = "random"  # change the mode in sorting_visualizer instance
                        self.sorting_visualizer.delay_input = pygame.time.get_ticks() + after_click_delay
                    if self.array_mode_selection2.collidepoint(mouse_pos):
                        self.array_mode_selected = 1
                        self.render_bool = True
                        array_mode_button_change = True
                        self.sorting_visualizer.array_modes["array_mode"] = "nearly_sorted"  # change the mode in sorting_visualizer instance
                        self.sorting_visualizer.delay_input = pygame.time.get_ticks() + after_click_delay
                    if self.array_mode_selection_minus.collidepoint(mouse_pos):
                        if self.sorting_visualizer.unsorted_amount > 0:
                            self.sorting_visualizer.unsorted_amount -= 2
                        self.render_bool = True
                        self.sorting_visualizer.delay_input = pygame.time.get_ticks() + mouse_hold_delay
                    if self.array_mode_selection_plus.collidepoint(mouse_pos):
                        if self.sorting_visualizer.unsorted_amount < 30:
                            self.sorting_visualizer.unsorted_amount += 2
                        self.render_bool = True
                        self.sorting_visualizer.delay_input = pygame.time.get_ticks() + mouse_hold_delay
                    if self.array_duplicates_selection1.collidepoint(mouse_pos):
                        self.duplicates_mode_selected = 0
                        self.render_bool = True
                        array_duplicates_button_change = True
                        self.sorting_visualizer.array_modes["duplicates"] = True
                        self.sorting_visualizer.delay_input = pygame.time.get_ticks() + after_click_delay
                    if self.array_duplicates_selection2.collidepoint(mouse_pos):
                        self.duplicates_mode_selected = 1
                        self.render_bool = True
                        array_duplicates_button_change = True
                        self.sorting_visualizer.array_modes["duplicates"] = False
                        self.sorting_visualizer.delay_input = pygame.time.get_ticks() + after_click_delay
                except:
                    print("No buttons yet!")
            self.mode_color_change(array_mode_button_change, self.array_modes, self.array_mode_selected, self.array_modes_colors)
            self.mode_color_change(array_duplicates_button_change, self.duplicates_modes, self.duplicates_mode_selected, self.duplicates_modes_colors)

    #  change button color
    def mode_color_change(self, button_change, modes, selected, colors):
        if button_change:
            for i in range(len(modes)):
                if i == selected:
                    colors[modes[i]] = config.overlay_text_selected
                else:
                    colors[modes[i]] = config.overlay_text_color




    def render(self, display):
        self.overlay_rect = pygame.draw.rect(display, config.overlay_color, (0, 0, self.visualizer_manager.SCREEN_WIDTH, self.overlay_height))  # draw overlay background
        self.render_text(display)  # render overlay text
        #pygame.draw.rect(display, config.overlay_color, (0, 0, self.visualizer_manager.SCREEN_WIDTH, self.overlay_height))

    def render_text(self,display):
        #if self.prev_text:  # hide previous text(if not done by rendering the overlay under)
        #    display.blit(self.sorting_visualizer.sorting_background, (self.prev_text.x, self.prev_text.y), self.prev_text)
        start_stop_pos_x = math.floor(self.visualizer_manager.SCREEN_WIDTH * 0.08)
        start_stop_pos_y = math.floor(self.visualizer_manager.SCREEN_HEIGHT * 0.04)
        array_length_pos_x = start_stop_pos_x + 10
        array_length_pos_y = math.floor(self.visualizer_manager.SCREEN_HEIGHT * 0.13)
        array_mode_pos_x = math.floor(self.visualizer_manager.SCREEN_WIDTH * 0.25)
        array_mode_pos_y = math.floor(self.visualizer_manager.SCREEN_HEIGHT * 0.09)
        array_mode_selection1_x = math.floor(self.visualizer_manager.SCREEN_WIDTH * 0.38)
        array_mode_selection1_y = math.floor(self.visualizer_manager.SCREEN_HEIGHT * 0.05)
        array_mode_selection2_x = math.floor(self.visualizer_manager.SCREEN_WIDTH * 0.39)
        array_mode_selection2_y = math.floor(self.visualizer_manager.SCREEN_HEIGHT * 0.13)
        array_mode_selection_minus_x = math.floor(self.visualizer_manager.SCREEN_WIDTH * 0.37)
        array_mode_selection_plus_x = math.floor(self.visualizer_manager.SCREEN_WIDTH * 0.41)
        array_mode_selection_control_y = math.floor(self.visualizer_manager.SCREEN_HEIGHT * 0.17)
        array_duplicates_pos_x = math.floor(self.visualizer_manager.SCREEN_WIDTH * 0.53)
        array_duplicates_pos_y = math.floor(self.visualizer_manager.SCREEN_HEIGHT * 0.09)
        array_duplicates_selection1_x = math.floor(self.visualizer_manager.SCREEN_WIDTH * 0.625)
        array_duplicates_selection1_y = math.floor(self.visualizer_manager.SCREEN_HEIGHT * 0.05)
        array_duplicates_selection2_x = math.floor(self.visualizer_manager.SCREEN_WIDTH * 0.63)
        array_duplicates_selection2_y = math.floor(self.visualizer_manager.SCREEN_HEIGHT * 0.14)


        self.visualizer_manager.draw_text(display, (f"Speed: {self.sorting_visualizer.delay} < >"), config.overlay_text_color, start_stop_pos_x, start_stop_pos_y, "font_sorting_overlay")
        self.visualizer_manager.draw_text(display, (f"Length: {self.sorting_visualizer.array_length} /\ \/"), config.overlay_text_color, array_length_pos_x, array_length_pos_y, "font_sorting_overlay")
        self.visualizer_manager.draw_text(display, (f"Sort Modes:"), config.overlay_text_color, array_mode_pos_x, array_mode_pos_y, "font_sorting_overlay")
        self.array_mode_selection1 = self.visualizer_manager.draw_text(display, (f"Random"), self.array_modes_colors["random"], array_mode_selection1_x, array_mode_selection1_y, "font_sorting_overlay")
        self.array_mode_selection2 = self.visualizer_manager.draw_text(display, (f"Nearly sorted: {self.sorting_visualizer.unsorted_amount}"), self.array_modes_colors["nearly_sorted"], array_mode_selection2_x, array_mode_selection2_y, "font_sorting_overlay")
        self.array_mode_selection_minus = self.visualizer_manager.draw_text(display, (f"-"), config.overlay_text_color, array_mode_selection_minus_x, array_mode_selection_control_y, "font_sorting_overlay")
        self.array_mode_selection_plus = self.visualizer_manager.draw_text(display, (f"+"), config.overlay_text_color, array_mode_selection_plus_x, array_mode_selection_control_y, "font_sorting_overlay")
        self.visualizer_manager.draw_text(display, (f"Duplicates:"), config.overlay_text_color, array_duplicates_pos_x, array_duplicates_pos_y, "font_sorting_overlay")
        self.array_duplicates_selection1 = self.visualizer_manager.draw_text(display, (f"True"), self.duplicates_modes_colors["true"], array_duplicates_selection1_x, array_duplicates_selection1_y, "font_sorting_overlay")
        self.array_duplicates_selection2 = self.visualizer_manager.draw_text(display, (f"False"), self.duplicates_modes_colors["false"], array_duplicates_selection2_x, array_duplicates_selection2_y, "font_sorting_overlay")

    # called when the screen is resized
    def screen_update(self, display, height_diff):
        self.overlay_height = math.floor(self.visualizer_manager.SCREEN_HEIGHT * 0.20)
        self.render(display)


class BubbleSort:
    def __init__(self, sorting_visualizer, visualizer_manager, overlay):
        self.sorting_visualizer = sorting_visualizer
        self.visualizer_manager = visualizer_manager
        self.overlay = overlay
        self.swapped = False
        self.before_swap = [0,0]
        self.current_action = "compare"
        self.action_stage = 0
        self.complex_visualize = False
        self.target_time = 0  # delay check for animation
        self.i = 0
        self.j = 0
        self.initilize = False
        self.next = False

    def update(self):
        if self.sorting_visualizer.bars_array and pygame.time.get_ticks() >= self.target_time:
            if self.next:
                self.current_action = None
                self.j+=1
                self.next = False
            if self.i < len(self.sorting_visualizer.bars_array):
                if self.j < (len(self.sorting_visualizer.bars_array) - 1 - self.i):
                    if self.current_action == "compare" or not self.current_action:
                        self.sorting_visualizer.bars_color[self.j], self.sorting_visualizer.bars_color[self.j+1] = config.bars_compared_color,config.bars_compared_color
                        self.target_time = pygame.time.get_ticks() + (self.sorting_visualizer.delay)
                        if self.sorting_visualizer.bars_array[self.j].y < self.sorting_visualizer.bars_array[self.j+1].y:  
                            self.current_action = "swap"
                        else:
                            self.current_action = "clear"
                    elif self.current_action == "swap":
                        self.swapped = True
                        if self.action_stage == 0:
                            self.sorting_visualizer.bars_color[self.j], self.sorting_visualizer.bars_color[self.j+1] = config.bars_swap_color, config.bars_swap_color
                            self.action_stage += 1
                            self.target_time = pygame.time.get_ticks() + (self.sorting_visualizer.delay*3)
                        elif self.action_stage == 1:
                            self.sorting_visualizer.bars_color[self.j], self.sorting_visualizer.bars_color[self.j+1] = config.bars_swapped_color, config.bars_swapped_color
                            self.before_swap[0], self.before_swap[1] = self.sorting_visualizer.bars_array[self.j], self.sorting_visualizer.bars_array[self.j+1]
                            self.sorting_visualizer.bars_array[self.j].height, self.sorting_visualizer.bars_array[self.j+1].height = self.sorting_visualizer.bars_array[self.j+1].height, self.sorting_visualizer.bars_array[self.j].height  # get start and ending position of self.sorting_visualizer.bars_array
                            self.sorting_visualizer.bars_array[self.j].y, self.sorting_visualizer.bars_array[self.j+1].y = self.sorting_visualizer.bars_array[self.j+1].y, self.sorting_visualizer.bars_array[self.j].y
                            self.current_action = "clear"
                            self.action_stage = 0
                            self.target_time = pygame.time.get_ticks() + (self.sorting_visualizer.delay*3)
                    elif self.current_action == "clear":
                        self.sorting_visualizer.bars_color[self.j], self.sorting_visualizer.bars_color[self.j+1] = config.bars_color, config.bars_color
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
        self.i = 0
        self.j = 0

    def generate_bars(self):
        self.sorting_visualizer.bars_array = []
        self.sorting_visualizer.bars_color = [config.bars_color for i in range(self.sorting_visualizer.array_length)]
        if not self.sorting_visualizer.bars_array or self.sorting_visualizer.sorting == False:
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
            if self.sorting_visualizer.array_modes["array_mode"] == "nearly_sorted":
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
            #self.sorting_visualizer.bars_array.append(pygame.draw.line(display, self.sorting_visualizer.bars_color[i], (start_pos,self.sorting_visualizer.array_bottom), (start_pos,self.numbers[i]), bars_width))  # line
            self.sorting_visualizer.bars_array.append(pygame.draw.rect(display, self.sorting_visualizer.bars_color[i], (start_pos, self.numbers[i], bars_width, self.sorting_visualizer.array_bottom - self.numbers[i])))  # rect
            start_pos += bars_gap + bars_width


    def remove_bar(self, display, bar):
        display.blit(self.sorting_visualizer.sorting_background, (bar.x, bar.y), bar)

    def render(self, display):
        if self.sorting_visualizer.sorting:
            # get images size of bars and increase to max height, use it to replace a bar with the background and "remove" it
            img_cover_bar1, img_cover_bar2 = self.sorting_visualizer.bars_array[self.j].copy(), self.sorting_visualizer.bars_array[self.j+1].copy()
            img_cover_bar1.height, img_cover_bar1.y = self.sorting_visualizer.array_bottom-self.sorting_visualizer.array_max_height+1, self.sorting_visualizer.array_max_height
            img_cover_bar2.height, img_cover_bar2.y = self.sorting_visualizer.array_bottom-self.sorting_visualizer.array_max_height+1, self.sorting_visualizer.array_max_height
            self.remove_bar(display, img_cover_bar1)
            self.remove_bar(display, img_cover_bar2)
            pygame.draw.rect(display, self.sorting_visualizer.bars_color[self.j], self.sorting_visualizer.bars_array[self.j])
            pygame.draw.rect(display, self.sorting_visualizer.bars_color[self.j+1], self.sorting_visualizer.bars_array[self.j+1])
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