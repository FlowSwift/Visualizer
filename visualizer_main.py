from states.main_menu import MainMenu

import os, time

import pygame


class Visualizer():
    def __init__(self) -> None:
        pygame.init()
        self.CANVAS_W, self.CANVAS_H = 480, 270
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = 1920, 1080
        self.canvas = pygame.Surface((self.CANVAS_W, self.CANVAS_H))
        self.WINDOW = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.running, self.playing = True, True
        self.actions = {"space": False}
        self.dt, self.prev_time = 0, 0
        self.current_tick = 0
        self.state_stack = []
        self.load_assets()
        self.load_states()
    
    def visualizer_loop(self):
        while self.playing:
            self.get_dt()
            self.check_events()
            self.update()
            self.render()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.actions["space"] = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    self.actions["space"] = False
    
    def update(self):
        self.state_stack[-1].update(self.dt, self.actions)

    def render(self):
        self.state_stack[-1].render(self.canvas)
        self.WINDOW.blit(pygame.transform.scale(self.canvas, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT)), (0,0))
        pygame.display.flip()

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
    
    def load_assets(self):
        self.assets_dir = os.path.join("assets")
        self.graphics_dir = os.path.join(self.assets_dir, "graphics")
        self.fonts_dir = os.path.join(self.assets_dir, "fonts")
        self.font= pygame.font.Font(os.path.join(self.fonts_dir, "Game Of Squids.ttf"), 20)
        

    def load_states(self):
        self.main_menu_screen = MainMenu(self)
        self.state_stack.append(self.main_menu_screen)

    def reset_keys(self):
        for action in self.actions:
            self.actions[action] = False

if __name__ == "__main__":
    v = Visualizer()
    while v.running:
        v.visualizer_loop()