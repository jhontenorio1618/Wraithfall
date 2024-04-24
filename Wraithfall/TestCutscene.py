import pygame
import game_window as WIN
import os
import textbox
import sys
from game_window import get_font, scale_to_screen as stsc

from cutscenes import play_scene, get_scene

pygame.init()

# Set screen size using the dimensions in the window_size function in game_window
SCREEN = pygame.display.set_mode(WIN.window_size())
pygame.display.set_caption("Cutscenes")

# Load the sound file
pygame.mixer.init()

clock = pygame.time.Clock()

def test_scene(scene):
    run = True
    end_of_scene = False
    while run:
        SCREEN.fill("black")

        for event in pygame.event.get():
            # If user closes the window exit the loop
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                # If enter key is pressed move to the next line
                if event.key == pygame.K_RETURN:
                    end_of_scene = scene.next_textbox()

        scene.draw_textboxes(SCREEN)

        # Update the display
        pygame.display.flip()
        clock.tick(WIN.get_fps())
        if end_of_scene:
            run = False


test_scene(get_scene(1))
test_scene(get_scene(2))
test_scene(get_scene(3))
pygame.quit()
sys.exit()