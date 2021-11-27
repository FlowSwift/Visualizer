import pygame
import config.config as config

class SelectionSort:
    def __init__(self, sorting_visualizer, visualizer_manager, overlay):
        self.sorting_visualizer = sorting_visualizer
        self.visualizer_manager = visualizer_manager
        self.sorting_visualizer.sorting = False  # set sorting to false before init
        self.current_action = None
        self.next = False 
        self.i = 0  # selection main loop index
        self.j = 0  # selection inner loop index
        self.smallest_num_index = 0
        self.last_smallest_num_index = 0  # used for render
        self.swapped = False
        self.new_lowest_delay = self.sorting_visualizer.delay * 8
        self.new_lowest_target_time = 0
        self.new_lowest_delay_check = False

    def update(self):
        if self.sorting_visualizer.sorting and pygame.time.get_ticks() >= self.sorting_visualizer.target_time and (pygame.time.get_ticks() >= self.new_lowest_target_time or not self.new_lowest_delay_check):  # check animation delay
            if self.next:  # move to next iteration (used after render executed the last loop animation) 
                self.current_action = "compare"
                self.j += 1
                self.next = False
            if self.i < len(self.sorting_visualizer.bars_array):  # artificial loop 
                if self.j < (len(self.sorting_visualizer.bars_array)):  # j always start equal to i every main loop
                    if self.current_action == "compare" or not self.current_action:
                        if self.sorting_visualizer.bars_array[self.j].y > self.sorting_visualizer.bars_array[self.smallest_num_index].y:
                            if self.smallest_num_index != self.i:  # recolor the previous lowest number in the current loop
                                self.sorting_visualizer.bars_color[self.smallest_num_index] = config.bars_color
                            self.sorting_visualizer.bars_color[self.j] = config.bars_lowest_num_color  # set the smallest bar so far color
                            self.last_smallest_num_index = self.smallest_num_index  # save the last smallest bar to repaint to original color in render
                            self.smallest_num_index = self.j
                            self.new_lowest_target_time = pygame.time.get_ticks() + (self.new_lowest_delay)
                        else:
                            self.sorting_visualizer.bars_color[self.j] = config.bars_compared_color  # show comparison if no new smallest num
                            self.sorting_visualizer.target_time = pygame.time.get_ticks() + (self.sorting_visualizer.delay)  # animation delay
                        self.current_action = "clear"
                    elif self.current_action == "clear":  # after comparison animation, clear but dont show (no delay)
                        if self.j != self.smallest_num_index: self.sorting_visualizer.bars_color[self.j] = config.bars_color
                        self.next = True  # move to next iteration after render
                    if self.j == self.i:  # color the sorted bars
                            self.sorting_visualizer.bars_color[self.i] = config.bars_compared_color
                else:
                    self.swapped = True  # used in render
                    self.sorting_visualizer.bars_color[self.smallest_num_index] = config.bars_swapped_color  # color the new swapped bar (the unsorted bar)
                    self.sorting_visualizer.bars_color[self.i] = config.bars_swap_color  # color the previous bars 
                    # swap bars
                    self.sorting_visualizer.bars_array[self.smallest_num_index].height, self.sorting_visualizer.bars_array[self.i].height = self.sorting_visualizer.bars_array[self.i].height, self.sorting_visualizer.bars_array[self.smallest_num_index].height  # get start and ending position of self.sorting_visualizer.bars_array
                    self.sorting_visualizer.bars_array[self.smallest_num_index].y, self.sorting_visualizer.bars_array[self.i].y = self.sorting_visualizer.bars_array[self.i].y, self.sorting_visualizer.bars_array[self.smallest_num_index].y
                    self.i += 1
                    self.j = self.i
                    self.smallest_num_index = self.i
            else:
                self.reset_loop()

    def reset_loop(self):
        self.smallest_num_index = 0
        self.current_action = None
        self.sorting_visualizer.sorting = False
        self.i = 0
        self.j = 0

    def render(self, display):
        if self.sorting_visualizer.sorting:
            if self.swapped:
                self.sorting_visualizer.draw_bars(display)  # redraw chart after inner loop iteration
            else:
                pygame.draw.rect(display, self.sorting_visualizer.bars_color[self.j], self.sorting_visualizer.bars_array[self.j])
                pygame.draw.rect(display, self.sorting_visualizer.bars_color[self.smallest_num_index], self.sorting_visualizer.bars_array[self.smallest_num_index])
                pygame.draw.rect(display, self.sorting_visualizer.bars_color[self.last_smallest_num_index], self.sorting_visualizer.bars_array[self.last_smallest_num_index])
        else:  # if not sorting, draw bars and and start sorting
            self.sorting_visualizer.sorting = True
            self.sorting_visualizer.generate_bars()
            self.sorting_visualizer.draw_bars(display)
