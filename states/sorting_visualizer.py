import pygame, os
import math
import random, math
import copy

from pygame.rect import Rect
from pygame.time import delay


import config.config as config

from states.state import State
from states.sorts.BubbleSort import BubbleSort
from states.sorts.SelectionSort import SelectionSort


class SortingVisualizer(State):
    """
    main sorting state
    used as interface for the sorting classes
    """
    def __init__(self, visualizer_manager):
        super().__init__(visualizer_manager)
        self.visualizer_manager = visualizer_manager
        self.visualizer_manager.display_reset = True  # change to true when need to refresh the entire display instead of the bar area
        self.bars_array = []
        self.bars_color = []
        self.array_bottom = config.SCREEN_HEIGHT
        self.array_min_height = round(self.array_bottom / 1.2)  # bars min and max possible height
        self.array_max_height = round(self.array_bottom / 2.2)
        self.array_length = 10  # bars amount
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
        #self.current_sort = MergeSort(self, self.visualizer_manager, self.overlay)
        self.sorting_background = pygame.image.load(os.path.join(config.assets_dir, "graphics", "background.jpg")).convert()

    def update(self, delta_time, actions):
        """check and update changes and properties"""
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
                    self.delay_input = pygame.time.get_ticks() + 40
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
                    if isinstance(self.current_sort, MergeSort):
                        self.current_sort.merging = False
                        self.current_sort = MergeSort(self, self.visualizer_manager, self.overlay)
        self.overlay.update(actions)
        # check what sort selected and update
        if self.current_sort:
            self.current_sort.update()

    def render(self, display):
        """check if needed and render changes on screen"""
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

    def screen_update(self, display, height_diff):
        """called when the screen is resized"""
        self.overlay.screen_update(display, height_diff)
        display.blit(self.sorting_background, (0,0))
        if self.current_sort:
            self.current_sort.reset_loop()
        self.array_bottom = self.visualizer_manager.SCREEN_HEIGHT
        self.array_min_height = round(self.array_bottom / 1.2)
        self.array_max_height = round(self.array_bottom / 2.2)

    def generate_bars(self):
        """generate bars based on the options from main class"""
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

    def draw_bars(self, display, height_diff=0):
        """draw and generate bars based on screen size"""
        bars_area = self.visualizer_manager.SCREEN_WIDTH * 0.8  # bars will always be inside this area
        bars_width =  round((bars_area * 0.7) / self.array_length)
        bars_gap = math.ceil((bars_area * 0.3) / self.array_length - 1)
        start_pos = round((self.visualizer_manager.SCREEN_WIDTH - ((bars_gap * (self.array_length - 1)) + (bars_width * self.array_length)))/2)
        first_draw = False
        if not self.bars_array:  # check if already sorting, draw current array
            first_draw = True
        else:
            display.blit(self.sorting_background, (self.visualizer_manager.SCREEN_WIDTH *0, self.visualizer_manager.SCREEN_HEIGHT*0.4, self.visualizer_manager.SCREEN_WIDTH *1, self.visualizer_manager.SCREEN_HEIGHT*0.6))
        for i in range(len(self.numbers)):
            #self.bars_array.append(pygame.draw.line(display, self.bars_color[i], (start_pos,self.array_bottom), (start_pos,self.numbers[i]), bars_width))  # line
            if first_draw:
                self.bars_array.append(pygame.draw.rect(display, self.bars_color[i], (start_pos, self.numbers[i], bars_width, self.array_bottom - self.numbers[i])))  # rect
            else:
                pygame.draw.rect(display, self.bars_color[i], self.bars_array[i])
            start_pos += bars_gap + bars_width

    def remove_bar(self, display, bar):
        """
        remove a bar by blitting the background in the size of the bar(max height of the bar) on the bar
        """
        display.blit(self.sorting_background, (bar.x, bar.y), bar)

class MergeSort:
    def __init__(self, sorting_visualizer, visualizer_manager, overlay):
        self.sorting_visualizer = sorting_visualizer
        self.visualizer_manager = visualizer_manager
        self.sorting_visualizer.sorting = False  # set sorting to false before init
        self.merge_delay = 4  # multiplier
        self.merging = True  # used for breaking out
        self.merging_init = False  # used to skip merge function when on a recursive game loopa call and already merging
        self.k = 0  # the index of the current number in the main array, outside the recursive function

    def add_delay(self, delay_time):
        """
        Adds delay between animation and wait till delay time passed
        Game loop runs during that time.
        """
        self.sorting_visualizer.target_time = pygame.time.get_ticks() + delay_time
        while pygame.time.get_ticks() <= self.sorting_visualizer.target_time and self.merging:
            self.visualizer_manager.visualizer_loop(True)

    def merge(self, bars, index):
        """recursive visualization"""
        bars_len = len(bars)
        if bars_len > 1:
            half = bars_len//2
            left_arr = copy.deepcopy(bars)[:half]
            left_arr_len = len(left_arr)
            right_arr = copy.deepcopy(bars)[half:]
            right_arr_len = len(right_arr)
            self.merge(left_arr, index)
            self.merge(right_arr, index + half)
            self.k = index  # current index in bars_array
            i, j, k = 0, 0, 0
            if self.merging:
                for o in range(len(bars)):  # color bars before sorting
                    self.sorting_visualizer.bars_color[self.k + o] = config.bars_swapped_color
                    self.add_delay(self.sorting_visualizer.delay*self.merge_delay)
            while i < left_arr_len and j < right_arr_len and self.merging:
                if left_arr[i].y > right_arr[j].y:  # check if left is smaller than right
                    bars[k].height, bars[k].y = left_arr[i].height, left_arr[i].y
                    self.sorting_visualizer.bars_array[self.k].height, self.sorting_visualizer.bars_array[self.k].y = left_arr[i].height, left_arr[i].y  # swap the bars in the displayed array
                    self.sorting_visualizer.bars_color[self.k] = config.bars_compared_color
                    i += 1
                    self.add_delay(self.sorting_visualizer.delay*self.merge_delay)
                else:
                    bars[k].height, bars[k].y = right_arr[j].height, right_arr[j].y
                    self.sorting_visualizer.bars_array[self.k].height, self.sorting_visualizer.bars_array[self.k].y = right_arr[j].height, right_arr[j].y
                    self.sorting_visualizer.bars_color[self.k] = config.bars_compared_color
                    j += 1
                    self.add_delay(self.sorting_visualizer.delay*self.merge_delay)
                k += 1
                self.k += 1
            while i < left_arr_len and self.merging:
                bars[k].height, bars[k].y = left_arr[i].height, left_arr[i].y
                self.sorting_visualizer.bars_array[self.k].height, self.sorting_visualizer.bars_array[self.k].y = left_arr[i].height, left_arr[i].y
                self.sorting_visualizer.bars_color[self.k] = config.bars_compared_color
                i += 1
                k += 1
                self.k += 1
                self.add_delay(self.sorting_visualizer.delay*self.merge_delay)
            while j < right_arr_len and self.merging:
                bars[k].height, bars[k].y = right_arr[j].height, right_arr[j].y
                self.sorting_visualizer.bars_array[self.k].height, self.sorting_visualizer.bars_array[self.k].y = right_arr[j].height, right_arr[j].y
                self.sorting_visualizer.bars_color[self.k] = config.bars_compared_color
                j += 1
                k += 1
                self.k += 1
                self.add_delay(self.sorting_visualizer.delay*self.merge_delay)
            

    def update(self):
        """check and update changes and properties"""
        if not self.merging_init and self.sorting_visualizer.sorting:
            self.merging_init = True
            tmp_array = copy.deepcopy(self.sorting_visualizer.bars_array)
            self.merge(tmp_array, 0)
            self.reset_loop()

    def reset_loop(self):
        """Used to start a new sort loop, will generate a new array"""
        self.sorting_visualizer.sorting = False
        self.merging_init = False
        
        

    def render(self, display):
        """Draw and render the screen"""
        if self.sorting_visualizer.sorting:
            display.blit(self.sorting_visualizer.sorting_background, (self.visualizer_manager.SCREEN_WIDTH *0.1, self.visualizer_manager.SCREEN_HEIGHT*0.4))
            self.sorting_visualizer.draw_bars(display)
            #self.sorting_visualizer.draw_bars(display)  # redraw chart after inner loop iteration
        elif self.merging:  # if not sorting, draw bars and and start sorting
            self.sorting_visualizer.sorting = True
            self.sorting_visualizer.generate_bars()
            self.sorting_visualizer.draw_bars(display)

class Overlay:
    def __init__(self, sorting_visualizer, visualizer_manager):
        self.sorting_visualizer = sorting_visualizer
        self.visualizer_manager = visualizer_manager
        self.render_bool = True # check if overlay was changed
        self.overlay_height = math.floor(self.visualizer_manager.SCREEN_HEIGHT * 0.20)
        self.array_modes = ["random", "nearly_sorted"]  # used to set selection colors
        self.array_modes_colors = {"random":config.overlay_text_selected, "nearly_sorted":config.overlay_text_unselected}  # current colors of the modes selection
        self.array_mode_selected = 0  # 0 for random, 1 for nearly_sorted
        self.duplicates_modes = ["true", "false"]  # used to set selection colors
        self.duplicates_modes_colors = {"true":config.overlay_text_selected, "false":config.overlay_text_unselected}  # current colors of the modes selection
        self.duplicates_mode_selected = 0  # 0 for True, 1 for False
        self.sort_modes = ["bubble", "selection", "merge"]  # used to set selection colors
        self.sort_modes_colors = {"bubble":config.overlay_text_selected, "selection":config.overlay_text_unselected, "merge":config.overlay_text_unselected}  # current colors of the modes selection
        self.sort_mode_selected = 0  # 0 for Bubble, 1 for Selection, 2 for Merge
        self.extra_delay_color = "blue"
        self.merge_current = False


    def update(self, actions):
        """Check for overlay changes and update in the main sorting state"""
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
                        self.sorting_visualizer.current_sort.merging = False
                        self.sorting_visualizer.current_sort = BubbleSort(self.sorting_visualizer, self.visualizer_manager, self)
                        self.sorting_visualizer.delay_input = pygame.time.get_ticks() + after_click_delay
                    if self.sort_mode_selection2.collidepoint(mouse_pos):
                        self.sort_mode_selected = 1
                        self.render_bool = True
                        sort_mode_button_change = True
                        self.sorting_visualizer.current_sort.merging = False
                        self.sorting_visualizer.current_sort = SelectionSort(self.sorting_visualizer, self.visualizer_manager, self)
                        self.sorting_visualizer.delay_input = pygame.time.get_ticks() + after_click_delay
                    if self.sort_mode_selection3.collidepoint(mouse_pos):
                        self.sort_mode_selected = 2
                        self.render_bool = True
                        sort_mode_button_change = True
                        if not isinstance(self.sorting_visualizer.current_sort, MergeSort):
                            self.sorting_visualizer.current_sort = MergeSort(self.sorting_visualizer, self.visualizer_manager, self)
                        self.sorting_visualizer.delay_input = pygame.time.get_ticks() + after_click_delay
                    if self.extra_delay_selection.collidepoint(mouse_pos):
                        if isinstance(self.sorting_visualizer.current_sort, SelectionSort):
                            if self.sorting_visualizer.current_sort.new_lowest_delay_check == True:
                                self.sorting_visualizer.current_sort.new_lowest_delay_check = False
                                self.extra_delay_color = "blue"
                            else:
                                self.sorting_visualizer.current_sort.new_lowest_delay_check = True
                                self.extra_delay_color = "red"
                        self.render_bool = True
                        self.sorting_visualizer.delay_input = pygame.time.get_ticks() + after_click_delay
                except:
                    print("No buttons yet!")
            self.mode_color_change(array_mode_button_change, self.array_modes, self.array_mode_selected, self.array_modes_colors)
            self.mode_color_change(array_duplicates_button_change, self.duplicates_modes, self.duplicates_mode_selected, self.duplicates_modes_colors)
            self.mode_color_change(sort_mode_button_change, self.sort_modes, self.sort_mode_selected, self.sort_modes_colors)

    def mode_color_change(self, button_change, modes, selected, colors):
        """
        check for button color change
        button_change -- a checker if the button was clicked at all
        modes -- a dict of the different available options
        selected -- currently selected option
        colors -- dict the modes as keywords and their colors as value
        """
        if button_change:
            for i in range(len(modes)):
                if i == selected:
                    colors[modes[i]] = config.overlay_text_selected
                else:
                    colors[modes[i]] = config.overlay_text_unselected

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
        sort_mode_selection3_x = math.floor(self.visualizer_manager.SCREEN_WIDTH * 0.90)
        sort_mode_selection3_y = math.floor(self.visualizer_manager.SCREEN_HEIGHT * 0.05)
        extra_delay_x = math.floor(self.visualizer_manager.SCREEN_WIDTH * 0.08)
        extra_delay_y = math.floor(self.visualizer_manager.SCREEN_HEIGHT * 0.25)

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
        self.sort_mode_selection3 = self.visualizer_manager.draw_text(display, (f"Merge Sort"), self.sort_modes_colors["merge"], sort_mode_selection3_x, sort_mode_selection3_y, "font_sorting_overlay")
        self.extra_delay_selection = self.visualizer_manager.draw_text(display, (f"Extra Animations"), self.extra_delay_color, extra_delay_x, extra_delay_y, "font_sorting_overlay")

    def screen_update(self, display, height_diff):
        """called when the screen is resized"""
        self.overlay_height = math.floor(self.visualizer_manager.SCREEN_HEIGHT * 0.20)
        self.render(display)
