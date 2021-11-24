from pygame import display
from states.main_menu import MainMenu

import config.config as config

import os, time

import pygame

clock = pygame.time.Clock()
pygame.init()

class Visualizer():
    font = pygame.font.Font(os.path.join(config.fonts_dir, "Game Of Squids.ttf"), 20)
    def __init__(self) -> None:
        self.t = 0
        #self.CANVAS_W, self.CANVAS_H = config.SCREEN_WIDTH, config.SCREEN_HEIGHT
        #self.canvas = pygame.Surface((self.CANVAS_W, self.CANVAS_H))
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = config.SCREEN_WIDTH, config.SCREEN_HEIGHT
        self.WINDOW = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.running, self.playing = True, True
        self.actions = {"space": False, "left_key": False, "right_key": False}
        self.dt, self.prev_time = 0, 0
        self.display_reset = True
        self.resize_delay = 0
        self.current_tick = 0
        self.state_stack = []
        self.load_states()


    def visualizer_loop(self):
        while self.playing:
            #clock.tick(60)
            if self.resize_delay < pygame.time.get_ticks():
                self.get_dt()
                self.check_events()
                self.update()
                self.render()

    def add_delay(self, delay=None):
        self.resize_delay = delay + pygame.time.get_ticks()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.VIDEORESIZE:
                self.display_reset = True
                old_height = self.SCREEN_HEIGHT
                self.SCREEN_WIDTH, self.SCREEN_HEIGHT = event.size
                self.WINDOW = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame.RESIZABLE)
                self.state_stack[-1].bars.screen_update(self.WINDOW,((self.SCREEN_HEIGHT-old_height)/old_height)*100)
                pygame.display.flip()
                print(event.size)
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.actions["space"] = True
                if event.key == pygame.K_LEFT:
                    self.actions["left_key"] = True
                if event.key == pygame.K_RIGHT:
                    self.actions["right_key"] = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    self.actions["space"] = False
                if event.key == pygame.K_LEFT:
                    self.actions["left_key"] = False
                if event.key == pygame.K_RIGHT:
                    self.actions["right_key"] = False
    
    def update(self):
        self.state_stack[-1].update(self.dt, self.actions)

    def render(self):
        self.state_stack[-1].render(self.WINDOW)
        if self.display_reset:
            pygame.display.flip()
            self.display_reset = False
        pygame.display.update(self.SCREEN_WIDTH *0.1, self.SCREEN_HEIGHT*0.4, self.SCREEN_WIDTH *0.8, self.SCREEN_HEIGHT*0.6)

    def get_dt(self):
        now = time.time()
        self.dt = now - self.prev_time
        self.prev_time = now

    def draw_text(self, surface, text, color, x, y):
        text_surface = self.font.render(text, True, color)
        #text_surface.set_colorkey((0, 0, 0))
        text_rect = text_surface.get_rect()
        text_rect.center = (x,y)
        surface.blit(text_surface, text_rect)
        return text_rect

    def load_states(self):
        self.sorting_background = pygame.image.load(os.path.join(config.assets_dir, "graphics", "background.jpg")).convert()
        self.main_menu_screen = MainMenu(self)
        self.state_stack.append(self.main_menu_screen)

    def reset_keys(self):
        for action in self.actions:
            self.actions[action] = False

if __name__ == "__main__":
    v = Visualizer()
    while v.running:
        v.visualizer_loop()