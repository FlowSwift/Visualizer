import pygame
import copy
import config.config as config


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
