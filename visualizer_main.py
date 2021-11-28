from pygame.constants import MOUSEBUTTONDOWN, MOUSEBUTTONUP
from states.main_menu import MainMenu
import sys

import config.config as config

import os, time, math

import pygame

clock = pygame.time.Clock()
pygame.init()

class Visualizer():
    "main visualizer state, manager of states"
    font_squid = pygame.font.Font(os.path.join(config.fonts_dir, "Game Of Squids.ttf"), 20)
    font_sorting_overlay_dir = os.path.join(config.fonts_dir, "Cotton Butter.ttf")
    def __init__(self) -> None:
        self.t = 0
        #self.CANVAS_W, self.CANVAS_H = config.SCREEN_WIDTH, config.SCREEN_HEIGHT
        #self.canvas = pygame.Surface((self.CANVAS_W, self.CANVAS_H))
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = config.SCREEN_WIDTH, config.SCREEN_HEIGHT
        self.WINDOW = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.running, self.playing = True, True
        self.actions = {"space": False, "left_key": False, "right_key": False, "up_key": False, "down_key": False, "left_mouse": False, "shift": False}  # key input checking.
        self.dt, self.prev_time = 0, 0  # delta time
        self.display_reset = True  # signal to render entire display on the next frame
        self.resize_delay = 0 
        self.state_stack = []
        self.load_assets()
        self.load_states()
        self.delay_input = 0

    def visualizer_loop(self, run_once=False):
        """main game loop"""
        while self.playing:
            #clock.tick(60)  # untick to not burn cpu
            if self.resize_delay < pygame.time.get_ticks():
                self.get_dt()
                self.check_events()
                self.update()
                self.render()
                if run_once:
                    return

    def check_events(self):
        """check events and set actions dicts with resaults to check from other states"""
        for event in pygame.event.get():
            if event.type == pygame.VIDEORESIZE:  # refresh, resize everything and render the entire screen on resize
                self.display_reset = True
                old_height = self.SCREEN_HEIGHT
                self.SCREEN_WIDTH, self.SCREEN_HEIGHT = event.size
                self.WINDOW = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame.RESIZABLE)
                self.state_stack[-1].screen_update(self.WINDOW,((self.SCREEN_HEIGHT-old_height)/old_height)*100)
                pygame.display.flip()
            if event.type == pygame.WINDOWEXPOSED:  # render entire screen when unminimize (pygame(SDL?) bug)
                self.display_reset = True
                pass
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if pygame.time.get_ticks() > self.delay_input:
                    self.delay_input = pygame.time.get_ticks() + 100
                    if event.key == pygame.K_SPACE:
                        self.actions["space"] = True
                    if event.key == pygame.K_LEFT:
                        self.actions["left_key"] = True
                    if event.key == pygame.K_RIGHT:
                        self.actions["right_key"] = True
                    if event.key == pygame.K_UP:
                        self.actions["up_key"] = True
                    if event.key == pygame.K_DOWN:
                        self.actions["down_key"] = True
                    if event.mod & pygame.KMOD_SHIFT:
                        self.actions["shift"] = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    self.actions["space"] = False
                if event.key == pygame.K_LEFT:
                    self.actions["left_key"] = False
                if event.key == pygame.K_RIGHT:
                    self.actions["right_key"] = False
                if event.key == pygame.K_UP:
                    self.actions["up_key"] = False
                if event.key == pygame.K_DOWN:
                    self.actions["down_key"] = False
                if event.mod & pygame.KMOD_SHIFT:
                        self.actions["shift"] = False
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.actions["left_mouse"] = True
            if event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    self.actions["left_mouse"] = False

    def update(self):
        """Update the top state of the stack"""
        self.state_stack[-1].update(self.dt, self.actions)

    def render(self):
        """render the entire screen or bar area"""
        self.state_stack[-1].render(self.WINDOW)
        if self.display_reset:  # check if entire display needs to be rendered due to changes
            pygame.display.flip()
            self.display_reset = False
        pygame.display.update(self.SCREEN_WIDTH *0, self.SCREEN_HEIGHT*0.4, self.SCREEN_WIDTH *1, self.SCREEN_HEIGHT*0.6)

    def get_dt(self):
        """get delta time"""
        now = time.time()
        self.dt = now - self.prev_time
        self.prev_time = now

    def draw_text(self, surface, text, color, x, y, font=None, scale=False):
        """helper function for displaying text"""
        if not font or font == "font_squid":
            font = Visualizer.font_squid
        elif font == "font_sorting_overlay":
            size = math.floor((self.SCREEN_WIDTH + self.SCREEN_HEIGHT) * 0.02)
            font = self.font_table[size]
        text_surface = font.render(text, True, color)
        #text_surface = pygame.transform.scale(text_surface,(self.SCREEN_WIDTH, math.floor(self.SCREEN_HEIGHT * 0.20)))
        #text_surface.set_colorkey((0, 0, 0))
        text_rect = text_surface.get_rect()
        text_rect.center = (x,y)
        surface.blit(text_surface, text_rect)
        return text_rect

    def load_assets(self):
        """load assests on startup"""
        ft = pygame.font.Font
        self.font_table = {}
        for i in range(0, 100):  # create different font size for responsiveness
            self.font_table[i] = ft(self.font_sorting_overlay_dir, i)

    def load_states(self):
        """Load and stack MainMenu state"""
        self.main_menu_screen = MainMenu(self)
        self.state_stack.append(self.main_menu_screen)

    def reset_keys(self):
        """reset_inputs"""
        for action in self.actions:
            self.actions[action] = False

if __name__ == "__main__":
    v = Visualizer()
    while v.running:
        v.visualizer_loop()