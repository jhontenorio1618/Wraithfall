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
    textbox.TextBox("Up and at'em, eh, Oliver?", "Grandpa", "Happy"), #Grandpa
    textbox.TextBox("Finally - it's already past dawn!", "Grandpa", "Neutral"), #Grandpa
    textbox.TextBox("Not that anyone can tell anymore...", "Grandpa", "Neutral"), #Grandpa
    textbox.TextBox("The wraiths have been quiet since last night.", "Grandpa", "Neutral"), #Grandpa
    textbox.TextBox("They left another pile of drained deer carcasses by the treeline.", "Grandpa", "Mad"), #Grandpa
    textbox.TextBox("It's a shame, all that tainted meat...", "Grandpa", "Mad"), #Grandpa
    textbox.TextBox("...Listen, Oliver.", "Grandpa", "Neutral"), #Grandpa
    textbox.TextBox("While I've got no desire to let you anywhere near those abominations...", "Grandpa", "Neutral"), #Grandpa
    textbox.TextBox("...I'm getting old, and hunting is hard on my bones. ", "Grandpa", "Neutral"), #Grandpa
    textbox.TextBox("Come out with me right now - I can show you the ropes, yeah?", "Grandpa", "Happy"), #Grandpa
]

#initialize variables
clock = pygame.time.Clock()

# Main loop
running = True

# Initializes the scene as a SceneManager object which manages the Textbox objects
scene2 = textbox.SceneManager(text_lines, "text_sound.wav")
while running:
    SCREEN.fill("black")

    for event in pygame.event.get():
        # If user closes the window exit the loop
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            # If enter key is pressed move to the next line
            if event.key == pygame.K_RETURN:
                scene2.next_textbox()

    scene2.draw_textboxes(SCREEN)

    # Update the display
    pygame.display.flip()
    clock.tick(WIN.get_fps())


pygame.quit()
sys.exit()