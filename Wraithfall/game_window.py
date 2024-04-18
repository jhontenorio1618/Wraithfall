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
# relative path to fonts dir
DIR_FONTS = os.path.join(DIR_ASSETS, "fonts")
# relative path to music dir
DIR_MUSIC = os.path.join(DIR_ASSETS, "music")
# relative path to sprite dir
DIR_SPRITE = os.path.join(DIR_ASSETS, "sprites")


def window_size():
    """ Returns tuple of window width x height """
    return WIN_WIDTH, WIN_HEIGHT


def get_fps():
    return FPS


def game_exit():
    pygame.quit()
    sys.exit()


def get_font(size, font_file="grand9Kpixel.ttf"):
    """ size = size of the letters
        font_file = name of the font in assets/fonts"""
    return pygame.font.Font(os.path.join(DIR_FONTS, font_file), size)


def play_music(music_file, loop=-1):
    """ music_file = name of the music file you want to play.
        loop = number of times audio should play. if -1, it will loop forever until stopped """
    if pygame.mixer.music.get_busy():
        stop_music()
    pygame.mixer.music.load(os.path.join(DIR_MUSIC, music_file))
    pygame.mixer.music.play(loop)
    return music_file


def stop_music(abrupt=True):
    if abrupt:
        pygame.mixer.music.stop()
    else:
        pygame.mixer.music.fadeout(250)


def play_sound(sound_file, loop=-1):
    """ sound_file = name of the sound file you want to play.
        loop = number of times audio should play. if -1, it will loop forever until stopped """
    #Load the sound file
    pygame.mixer.init()
    sound = pygame.mixer.Sound(os.path.join(DIR_MUSIC, sound_file))
    #play sound and loop until text is finished
    sound.play(loops=loop)
    return sound


def setup_window():
    # TODO maybe use this as a method to call for initialize pygame window?
    pygame.init()
    SCREEN = pygame.display.set_mode(window_size())
    pygame.display.set_caption("Menu")

