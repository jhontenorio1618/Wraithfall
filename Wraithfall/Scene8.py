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
    textbox.TextBox("No... please, no!", "MainCharacter", "Neutral"), #MC
    textbox.TextBox("He's all I have left!", "MainCharacter", "Sad"), #MC
    textbox.TextBox("Ugh... Oliver", "Grandpa", "Dead1"), #Grandpa
    textbox.TextBox("Kid...save your bandages...this is it for me...", "Grandpa", "Dead2"), #Grandpa
    textbox.TextBox("I meant it when I said that I was proud of you...", "Grandpa", "Dead1"), #Grandpa
    textbox.TextBox("...This world is dark and cruel, but keep pushing...", "Grandpa", "Dead2"), #Grandpa
    textbox.TextBox("...for me, ok?", "Grandpa", "Dead1"), #Grandpa
    textbox.TextBox("And for your mom...", "Grandpa", "Dead2"), #Grandpa
    textbox.TextBox("I'll finally get to be with my little girl again...", "Grandpa", "Dead1"), #Grandpa
    textbox.TextBox("Please...", "MainCharacter", "Sad"), #MC
    textbox.TextBox("I'm sorry I can't be there for you...Oliver...", "Grandpa", "Dead2"), #Grandpa

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