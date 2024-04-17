import pygame, os, sys, math, random

""" Pygame Window Setup & Variables"""
# TODO contemplate reformatting all of this to be an class instead of separate vars and defs

# TODO verify dimensions
WIN_WIDTH = 1280
WIN_HEIGHT = 720
FPS = 30
# Directory
DIR_MAIN = os.path.dirname(__file__)
# relative path to assets dir
DIR_ASSETS = os.path.join(DIR_MAIN, "assets")
# relative path to image dir
DIR_IMAGES = os.path.join(DIR_ASSETS, "images")
# relative path to image dir
DIR_FONTS = os.path.join(DIR_ASSETS, "fonts")


def window_size():
    """ Returns tuple of window width x height """
    return WIN_WIDTH, WIN_HEIGHT


def game_exit():
    pygame.quit()
    sys.exit()


def get_font(size):
    """ Load font in specified size for the game.

    TODO: could change this to be able to take any specified font we have in assets? if we want more fonts """
    return pygame.font.Font(os.path.join(DIR_FONTS, "grand9Kpixel.ttf"), size)


def setup_window():
    # TODO maybe use this as a method to call for initialize pygame window?
    pygame.init()
    SCREEN = pygame.display.set_mode(window_size())
    pygame.display.set_caption("Menu")

