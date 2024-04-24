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
    textbox.TextBox("...", "Sword", "Neutral"), #sword
    textbox.TextBox("'Hold on, this thing's... blinking at me!'", "MainCharacter", "Neutral"), #MC
    textbox.TextBox("'Yeah, and this THING can hear you, too, kid.'", "Sword", "Mad"), #Sword
    textbox.TextBox("'Y-You can hear my thoughts?!'", "MainCharacter", "Neutral"), #MC
    textbox.TextBox("'Sure can. Call it a magical soul bond, if that floats your boat.'", "Sword", "Happy"), #Sword
    textbox.TextBox("'We got psychologically linked when you picked me up.'", "Sword", "Neutral"), #Sword
    textbox.TextBox("'Great... this isn't weird at all.'", "MainCharacter", "Neutral"), #MC
    textbox.TextBox("'We don't have time for this - can you just kill that giant wraith for me?!'", "MainCharacter", "Neutral"), #MC
    textbox.TextBox("'Woah, too good for introductions are we?'", "Sword", "Mad"), #Sword
    textbox.TextBox("'I'm Acheron, and you are...?'", "Sword", "Happy"), #Sword
    textbox.TextBox("'Oliver - now hurry up and do something! I've gotta help my Grandpa!'", "MainCharacter", "Angry"), #MC
    textbox.TextBox("'Sheesh - pushy are we?'", "Sword", "Mad"), #Sword
    textbox.TextBox("'Fine, fine. But we've gotta work together to get this done, alright?'", "Sword", "Neutral") #Sword
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