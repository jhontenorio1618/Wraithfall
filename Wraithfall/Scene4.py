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
    textbox.TextBox("...You held your own, Oliver. Good.", "Grandpa", "Happy"), #grandpa
    textbox.TextBox("'...What is this?'", "MainCharacter", "Neutral"), 
    textbox.TextBox("*Retrieves an item from the wraiths corpse*", "MainCharacter", "Neutral"), 
    textbox.TextBox("*Obtained WRAITH ESSENCE*", "MainCharacter", "Neutral"), 
    textbox.TextBox("'This could be useful to my research...'", "MainCharacter", "Neutral"), 
    textbox.TextBox("*Sigh*...That venison meat should be enough to keep us fed for the next week, at least.", "Grandpa", "Neutral"),
    textbox.TextBox("Let's go home, kid.", "Grandpa", "Happy"), 
    
]

#initialize variables
clock = pygame.time.Clock()

# Main loop
running = True

# Initializes the scene as a SceneManager object which manages the Textbox objects
scene3 = textbox.SceneManager(text_lines, "text_sound.wav")
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