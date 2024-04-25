import pygame, sys, os
from game_window import random, math, get_font, window_size, WIN_WIDTH, WIN_HEIGHT, game_exit, \
    scale_to_screen as stsc, DIR_MUSIC

pygame.init()
SCREEN = pygame.display.set_mode(window_size())
pygame.display.set_caption("Overworld Code")


def load_mixer(audio_file):
    pygame.mixer.music.load(os.path.join(DIR_MUSIC, audio_file))
    return True

def unload_mixer():
    pygame.mixer.music.unload()

def play_mixer(loops=-1):
    pygame.mixer.music.play(loops)

def pause_mixer():
    pygame.mixer.music.pause()

def unpause_mixer():
    pygame.mixer.music.unpause()

def stop_mixer():
    pygame.mixer.music.stop()

