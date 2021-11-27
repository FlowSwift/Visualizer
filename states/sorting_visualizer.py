import pygame, os
import math
import random, math


import config.config as config

from states.state import State
from states.sorts.BubbleSort import BubbleSort
from states.sorts.SelectionSort import SelectionSort

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
        self.target_time = 0 # animation delay check
        self.delay_input = 0  # delay check for key input
        self.sorting = False
        self.overlay = Overlay(self, visualizer_manager)
        self.bubble_sort = None #BubbleSort(self, self.visualizer_manager, self.overlay)
        self.selection_sort = None
        self.current_sort = BubbleSort(self, self.visualizer_manager, self.overlay)
        self.sorting_background = pygame.image.load(os.path.join(config.assets_dir, "graphics", "background.jpg")).convert()
        
    # check and update changes
    def update(self, delta_time, actions):
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
                if self.current_sort:
                    self.current_sort.reset_loop()
        self.overlay.update(actions)
        # check what sort selected and update
        if self.current_sort:
            self.current_sort.update()
        
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
        if self.current_sort:
            self.current_sort.render(display)

    # called when the screen is resized
    def screen_update(self, display, height_diff):
        self.overlay.screen_update(display, height_diff)
        display.blit(self.sorting_background, (0,0))
        if self.current_sort:
            self.current_sort.reset_loop()
        self.array_bottom = self.visualizer_manager.SCREEN_HEIGHT
        self.array_min_height = round(self.array_bottom / 1.2)
        self.array_max_height = round(self.array_bottom / 2.2)

# generate bars based on the options from main class
    def generate_bars(self):
        self.bars_array = []
        self.bars_color = [config.bars_color for i in range(self.array_length)]  # add the default color for all the bars
        if not self.bars_array or self.sorting == False:
            if self.array_modes["duplicates"]:  # creates a random array with duplicates
                self.numbers = [random.randrange(self.array_max_height, self.array_min_height) for i in range(self.array_length)]
            else:  # creates a non duplicates array based on the min and max array height. bigger gaps for smaller arrrays
                height_gap = round((self.array_min_height - self.array_max_height)/self.array_length)
                self.numbers = []
                i = self.array_max_height
                for j in range(self.array_length):
                    self.numbers.append(i)
                    i += height_gap
                random.shuffle(self.numbers)
            # check if nearly_sorted mode is on, sort the list then "mess" it depending on unsorted_amount from main class
            if self.array_modes["array_mode"] == "nearly_sorted":
                unsorted_amount = math.ceil(self.unsorted_amount/100 * self.array_length)
                self.numbers.sort(reverse=self.array_asc_order)
                for i in range(unsorted_amount):
                    random_num1 = random.randrange(3,len(self.numbers)-3)
                    random_num2 = random.randrange(random_num1-3, random_num1+4)
                    self.numbers[random_num1], self.numbers[random_num2] = self.numbers[random_num2], self.numbers[random_num1]

    # draw and generate bars based on screen size
    def draw_bars(self, display, height_diff=0):
        bars_area = self.visualizer_manager.SCREEN_WIDTH * 0.8  # bars will always be inside this area
        bars_width =  round((bars_area * 0.7) / self.array_length)
        bars_gap = math.ceil((bars_area * 0.3) / self.array_length - 1)
        start_pos = round((self.visualizer_manager.SCREEN_WIDTH - ((bars_gap * (self.array_length - 1)) + (bars_width * self.array_length)))/2)
        first_draw = False
        if not self.bars_array:
            first_draw = True
        else:
            display.blit(self.sorting_background, (self.visualizer_manager.SCREEN_WIDTH *0.1, self.visualizer_manager.SCREEN_HEIGHT*0.4, self.visualizer_manager.SCREEN_WIDTH *0.8, self.visualizer_manager.SCREEN_HEIGHT*0.6))
        for i in range(len(self.numbers)):
            #self.bars_array.append(pygame.draw.line(display, self.bars_color[i], (start_pos,self.array_bottom), (start_pos,self.numbers[i]), bars_width))  # line
            if first_draw:
                self.bars_array.append(pygame.draw.rect(display, self.bars_color[i], (start_pos, self.numbers[i], bars_width, self.array_bottom - self.numbers[i])))  # rect
            else:
                pygame.draw.rect(display, self.bars_color[i], self.bars_array[i])
            start_pos += bars_gap + bars_width

    # remove a bar by blitting the background in the size of the bar(max height of the bar) on the bar
    def remove_bar(self, display, bar):
        display.blit(self.sorting_background, (bar.x, bar.y), bar)

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
        self.sort_modes = ["bubble", "selection"]  # used to set selection colors
        self.sort_modes_colors = {"bubble":config.overlay_text_selected, "selection":config.overlay_text_color}  # current colors of the modes selection
        self.sort_mode_selected = 0  # 0 for Bubble, 1 for Selection


    def update(self, actions):
        after_click_delay = 500  # clicking timeout
        mouse_hold_delay = 200
        array_mode_button_change = False
        array_duplicates_button_change = False
        sort_mode_button_change = False
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
                    if self.sort_mode_selection1.collidepoint(mouse_pos):
                        self.sort_mode_selected = 0
                        self.render_bool = True
                        sort_mode_button_change = True
                        self.sorting_visualizer.current_sort = BubbleSort(self.sorting_visualizer, self.visualizer_manager, self)
                        self.sorting_visualizer.delay_input = pygame.time.get_ticks() + after_click_delay
                    if self.sort_mode_selection2.collidepoint(mouse_pos):
                        self.sort_mode_selected = 1
                        self.render_bool = True
                        sort_mode_button_change = True
                        self.sorting_visualizer.current_sort = SelectionSort(self.sorting_visualizer, self.visualizer_manager, self)
                        self.sorting_visualizer.delay_input = pygame.time.get_ticks() + after_click_delay
                except:
                    print("No buttons yet!")
            self.mode_color_change(array_mode_button_change, self.array_modes, self.array_mode_selected, self.array_modes_colors)
            self.mode_color_change(array_duplicates_button_change, self.duplicates_modes, self.duplicates_mode_selected, self.duplicates_modes_colors)
            self.mode_color_change(sort_mode_button_change, self.sort_modes, self.sort_mode_selected, self.sort_modes_colors)


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
        sort_mode_selection1_x = math.floor(self.visualizer_manager.SCREEN_WIDTH * 0.75)
        sort_mode_selection1_y = math.floor(self.visualizer_manager.SCREEN_HEIGHT * 0.05)
        sort_mode_selection2_x = math.floor(self.visualizer_manager.SCREEN_WIDTH * 0.75)
        sort_mode_selection2_y = math.floor(self.visualizer_manager.SCREEN_HEIGHT * 0.13)

        self.visualizer_manager.draw_text(display, (f"Speed: {self.sorting_visualizer.delay} < >"), config.overlay_text_color, start_stop_pos_x, start_stop_pos_y, "font_sorting_overlay")
        self.visualizer_manager.draw_text(display, (f"Length: {self.sorting_visualizer.array_length} /\ \/"), config.overlay_text_color, array_length_pos_x, array_length_pos_y, "font_sorting_overlay")
        self.visualizer_manager.draw_text(display, (f"Array Modes:"), config.overlay_text_color, array_mode_pos_x, array_mode_pos_y, "font_sorting_overlay")
        self.array_mode_selection1 = self.visualizer_manager.draw_text(display, (f"Random"), self.array_modes_colors["random"], array_mode_selection1_x, array_mode_selection1_y, "font_sorting_overlay")
        self.array_mode_selection2 = self.visualizer_manager.draw_text(display, (f"Nearly sorted: {self.sorting_visualizer.unsorted_amount}"), self.array_modes_colors["nearly_sorted"], array_mode_selection2_x, array_mode_selection2_y, "font_sorting_overlay")
        self.array_mode_selection_minus = self.visualizer_manager.draw_text(display, (f"-"), config.overlay_text_color, array_mode_selection_minus_x, array_mode_selection_control_y, "font_sorting_overlay")
        self.array_mode_selection_plus = self.visualizer_manager.draw_text(display, (f"+"), config.overlay_text_color, array_mode_selection_plus_x, array_mode_selection_control_y, "font_sorting_overlay")
        self.visualizer_manager.draw_text(display, (f"Duplicates:"), config.overlay_text_color, array_duplicates_pos_x, array_duplicates_pos_y, "font_sorting_overlay")
        self.array_duplicates_selection1 = self.visualizer_manager.draw_text(display, (f"True"), self.duplicates_modes_colors["true"], array_duplicates_selection1_x, array_duplicates_selection1_y, "font_sorting_overlay")
        self.array_duplicates_selection2 = self.visualizer_manager.draw_text(display, (f"False"), self.duplicates_modes_colors["false"], array_duplicates_selection2_x, array_duplicates_selection2_y, "font_sorting_overlay")
        self.sort_mode_selection1 = self.visualizer_manager.draw_text(display, (f"Bubble Sort"), self.sort_modes_colors["bubble"], sort_mode_selection1_x, sort_mode_selection1_y, "font_sorting_overlay")
        self.sort_mode_selection2 = self.visualizer_manager.draw_text(display, (f"Selection Sort"), self.sort_modes_colors["selection"], sort_mode_selection2_x, sort_mode_selection2_y, "font_sorting_overlay")

    # called when the screen is resized
    def screen_update(self, display, height_diff):
        self.overlay_height = math.floor(self.visualizer_manager.SCREEN_HEIGHT * 0.20)
        self.render(display)
