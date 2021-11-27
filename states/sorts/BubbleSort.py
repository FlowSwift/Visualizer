import pygame
import config.config as config

class BubbleSort:
    def __init__(self, sorting_visualizer, visualizer_manager, overlay):
        self.sorting_visualizer = sorting_visualizer
        self.visualizer_manager = visualizer_manager
        self.sorting_visualizer.sorting = False
        self.swapped = False
        self.current_action = None
        self.action_stage = 0
        self.i = 0  # bubble main loop
        self.j = 0  # bubble inner loop
        self.next = False  # move to next iteration

    #  bubble has 3 stages for the animation. 1st. comparing color. 2nd. unsorted(< or >) color. 3rd. after swap color
    def update(self):
        if self.sorting_visualizer.sorting and pygame.time.get_ticks() >= self.sorting_visualizer.target_time:  # check animation delay
            if self.next:  # move to next iteration
                self.current_action = None
                self.j+=1
                self.next = False
            # "artificial" bubble loop
            if self.i < len(self.sorting_visualizer.bars_array):
                if self.j < (len(self.sorting_visualizer.bars_array) - 1 - self.i):
                    # check if comparing and change the bar pair color to compre color. if next number < or > then depending on sort, set to swap action, otherwise set to clear
                    if self.current_action == "compare" or not self.current_action:
                        self.sorting_visualizer.bars_color[self.j], self.sorting_visualizer.bars_color[self.j+1] = config.bars_compared_color,config.bars_compared_color
                        self.sorting_visualizer.target_time = pygame.time.get_ticks() + (self.sorting_visualizer.delay)
                        if self.sorting_visualizer.bars_array[self.j].y < self.sorting_visualizer.bars_array[self.j+1].y:  
                            self.current_action = "swap"
                        else:
                            self.current_action = "clear"
                    # if actions is swap, set new color for the pair before swapping for stage 0 
                    elif self.current_action == "swap":
                        self.swapped = True
                        if self.action_stage == 0:
                            self.sorting_visualizer.bars_color[self.j], self.sorting_visualizer.bars_color[self.j+1] = config.bars_swap_color, config.bars_swap_color
                            self.action_stage += 1
                            self.sorting_visualizer.target_time = pygame.time.get_ticks() + (self.sorting_visualizer.delay*3)
                        elif self.action_stage == 1:  # if stage 1, change to after swap color and save old bars for removing in render()
                            self.sorting_visualizer.bars_color[self.j], self.sorting_visualizer.bars_color[self.j+1] = config.bars_swapped_color, config.bars_swapped_color
                            self.sorting_visualizer.bars_array[self.j].height, self.sorting_visualizer.bars_array[self.j+1].height = self.sorting_visualizer.bars_array[self.j+1].height, self.sorting_visualizer.bars_array[self.j].height  # get start and ending position of self.sorting_visualizer.bars_array
                            self.sorting_visualizer.bars_array[self.j].y, self.sorting_visualizer.bars_array[self.j+1].y = self.sorting_visualizer.bars_array[self.j+1].y, self.sorting_visualizer.bars_array[self.j].y
                            self.current_action = "clear"
                            self.action_stage = 0
                            self.sorting_visualizer.target_time = pygame.time.get_ticks() + (self.sorting_visualizer.delay*3)
                    elif self.current_action == "clear":  # restore bar colors to original color
                        self.sorting_visualizer.bars_color[self.j], self.sorting_visualizer.bars_color[self.j+1] = config.bars_color, config.bars_color
                        self.next = True
                else:  # once over array length for the inner loop, "add" iteration. also check if there was a swap, if no swap happened, list is sorted
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

    def render(self, display):
        if self.sorting_visualizer.sorting:
            # get images size of bars and increase to max height, use it to replace a bar with the background and "remove" it
            img_cover_bar1, img_cover_bar2 = self.sorting_visualizer.bars_array[self.j].copy(), self.sorting_visualizer.bars_array[self.j+1].copy()
            img_cover_bar1.height, img_cover_bar1.y = self.sorting_visualizer.array_bottom-self.sorting_visualizer.array_max_height+1, self.sorting_visualizer.array_max_height
            img_cover_bar2.height, img_cover_bar2.y = self.sorting_visualizer.array_bottom-self.sorting_visualizer.array_max_height+1, self.sorting_visualizer.array_max_height
            self.sorting_visualizer.remove_bar(display, img_cover_bar1)
            self.sorting_visualizer.remove_bar(display, img_cover_bar2)
            pygame.draw.rect(display, self.sorting_visualizer.bars_color[self.j], self.sorting_visualizer.bars_array[self.j])
            pygame.draw.rect(display, self.sorting_visualizer.bars_color[self.j+1], self.sorting_visualizer.bars_array[self.j+1])
        else:  # if not sorting, draw bars and and start sorting
            self.sorting_visualizer.generate_bars()
            self.sorting_visualizer.draw_bars(display)
            self.sorting_visualizer.sorting = True

    # called when the screen is resized
    def screen_update(self, display, height_diff):
        display.blit(self.sorting_visualizer.sorting_background, (0,0))
        self.reset_loop()
        self.sorting_visualizer.array_bottom = self.visualizer_manager.SCREEN_HEIGHT
        self.sorting_visualizer.array_min_height = round(self.sorting_visualizer.array_bottom / 1.2)
        self.sorting_visualizer.array_max_height = round(self.sorting_visualizer.array_bottom / 2.2)