import pygame
import game_window as WIN
import os
import view_portraits
import textbox
import sys

pygame.init()

#Set screen size using the dimensions in the window_size function in game_window
SCREEN = pygame.display.set_mode(WIN.window_size())
pygame.display.set_caption("Menu")

# Load the sound file
pygame.mixer.init()

#Text lines
text_lines = [
    textbox.TextBox("...Oliver, that isn't wise...", "Grandpa", "Mad"), #grandpa
    textbox.TextBox("Oliver!!", "Grandpa", "Mad"), #grandpa
]

#initialize variables
clock = pygame.time.Clock()

# Initializes the scene as a SceneManager object which manages the Textbox objects
scene3 = textbox.SceneManager(text_lines, "text_sound.wav")
def play_cutscene_6_4YES():
    # Main loop
    running = True
    while running:
        SCREEN.fill("black")

        for event in pygame.event.get():
            # If user closes the window exit the loop
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                # If enter key is pressed move to the next line
                if event.key == pygame.K_RETURN:
                    scene3.next_textbox()

        scene3.draw_textboxes(SCREEN)

        # Update the display
        pygame.display.flip()
        clock.tick(WIN.get_fps())
    pygame.quit()
    sys.exit()

# play_cutscene_6_4YES()

