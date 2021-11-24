import time
import pygame
from pygame.time import get_ticks
import config.config as config
from states.state import State
from states.sorting_visualizer import SortingVisualizer



class MainMenu(State):
    def __init__(self, visualizer):
        super().__init__(visualizer)
        self.visualizer = visualizer
        self.delay_input = 0

    def update(self, delta_time, actions):
        if actions["space"]:
            if pygame.time.get_ticks() > self.delay_input:
                self.delay_input = pygame.time.get_ticks() + 100
                ev = pygame.event.Event(pygame.VIDEORESIZE, size=(config.SCREEN_WIDTH,config.SCREEN_HEIGHT))
                pygame.event.post(ev)
                sorting_visualizer_state = SortingVisualizer(self.visualizer)
                sorting_visualizer_state.enter_state()
        

    def render(self, display):
        display.fill((255,255,255))
        self.visualizer.draw_text(display, "Game States", (0,0,0), self.visualizer.SCREEN_WIDTH/2, self.visualizer.SCREEN_HEIGHT/2)

