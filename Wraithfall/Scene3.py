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
    textbox.TextBox("You know, I first taught your mom how to hunt in these mountains, too.", "Grandpa", "Happy"), #Grandpa
    textbox.TextBox("She'd be proud to see you out here today.", "Grandpa", "Happy"), #Grandpa
    textbox.TextBox("Here, this was hers. I've been using it as a good luck charm, but I want you to have it.", "Grandpa", "Happy"), #Grandpa
    textbox.TextBox("*Retrieves Grandpa's Gift*", "MainCharacter", "Neutral"), #Main Character
    textbox.TextBox("'...a gun?'", "MainCharacter", "Neutral"), #Main Character
    textbox.TextBox("*Obtained GUN*", "MainCharacter", "Neutral"), #Main Character
    textbox.TextBox("Handle it with care, okay?", "Grandpa", "Neutral"), #Grandpa
    textbox.TextBox("Why don't you pick those up, Oliver? They're a little bruised, but any food is good food...", "Grandpa", "Neutral"), #Grandpa
    textbox.TextBox("That bit of wisdom's stuck with me since my army days.", "Grandpa", "Neutral"), #Grandpa
    textbox.TextBox("...Quiet now", "Grandpa", "Neutral"), #Grandpa
    textbox.TextBox("Those things... if only someone could figure out what they are, why they're here terrorizing us.", "Grandpa", "Mad"), #Grandpa
    textbox.TextBox("...Hold on.", "Grandpa", "Neutral"), #Grandpa
    textbox.TextBox("There we go... you can tag the next one, alright, Oliver?", "Grandpa", "Neutral"), #Grandpa
    textbox.TextBox("Now, go and fetch the carcass for me, please.", "Grandpa", "Neutral"), #Grandpa
    textbox.TextBox("Oliver!!", "Grandpa", "Neutral"), #Grandpa
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