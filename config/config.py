import os
import pygame

  # 0screen resolution
SCREEN_WIDTH, SCREEN_HEIGHT = 848, 480

  # bar_settings
bars_color = "red"
bars_compared_color = "blue"
bars_swapped_color = "green"

  # ASSETS DIR
assets_dir = os.path.join("assets")
graphics_dir = os.path.join(assets_dir, "graphics")
fonts_dir = os.path.join(assets_dir, "fonts")

  # fonts
font = ""

  # images
sorting_background = ""

def load_assets():
    global font
    global sorting_background
    sorting_background = pygame.image.load(os.path.join(assets_dir, "graphics", "background.jpg")).convert()
    font = pygame.font.Font(os.path.join(fonts_dir, "Game Of Squids.ttf"), 20)