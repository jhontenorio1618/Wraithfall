import pygame
import game_window as WIN
import os
import view_portraits
import textbox
import sys
from game_window import get_font, scale_to_screen as stsc
from Scene6_3YESORNO import play_scene6_3CHOICE

pygame.init()

#Set screen size using the dimensions in the window_size function in game_window
SCREEN = pygame.display.set_mode(WIN.window_size())
pygame.display.set_caption("Menu")

# Load the sound file
pygame.mixer.init()

#Text lines
text_lines = [
    textbox.TextBox("...We shouldn't touch it. Let's go, Oliver.", "Grandpa", "Mad"), #grandpa
    textbox.TextBox("It would be best to call it a night.", "Grandpa", "Neutral"), #grandpa
    textbox.TextBox("Do you pick up the SWORD?", "MainCharacter", "Neutral"), #Maincharacter
    # textbox.TextBox("YES           NO", "MainCharacter", "Neutral"), #Maincharacter place holder for user choice.
]

#initialize variables
clock = pygame.time.Clock()



# Initializes the scene as a SceneManager object which manages the Textbox objects
scene3 = textbox.SceneManager(text_lines, "text_sound.wav")

def play_scene_6():
    # Main loop
    running = True
    end_of_scene = False
    while running:
        SCREEN.fill("black")

        for event in pygame.event.get():
            # If user closes the window exit the loop
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                # If enter key is pressed move to the next line
                if event.key == pygame.K_RETURN:
                    end_of_scene = scene3.next_textbox()

        scene3.draw_textboxes(SCREEN)

        # Update the display
        pygame.display.flip()
        clock.tick(WIN.get_fps())
        if end_of_scene:
            running = False
            play_scene6_3CHOICE()
    pygame.quit()
    sys.exit()

play_scene_6()