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
sound = pygame.mixer.Sound(os.path.join(WIN.DIR_MUSIC, "text_sound.wav"))
# play sound and loop until text is finished
sound.play(loops=-1)

#Text lines
text_lines = [
    textbox.TextBox("You know, I first taught your mom how to hunt in these mountains, too.", "MainCharacter", "Neutral"), #Grandpa
    textbox.TextBox("She'd be proud to see you out here today.", "MainCharacter", "Neutral"), #Grandpa
    textbox.TextBox("Here, this was hers. I've been using it as a good luck charm, but I want you to have it.", "MainCharacter", "Neutral"), #Grandpa
    textbox.TextBox("Handle it with care, okay?", "MainCharacter", "Neutral"), #Grandpa
    textbox.TextBox("Why don't you pick those up, Olive? They're a little bruised, but any food is good food...", "MainCharacter", "Neutral"), #Grandpa
    textbox.TextBox("That bit of wisdom's stuck with me since my army days.", "MainCharacter", "Neutral"), #Grandpa
    textbox.TextBox("...Quiet now", "MainCharacter", "Neutral"), #Grandpa
    textbox.TextBox("Those things... if only someone could figure out what they are, why they're here terrorizing us.", "MainCharacter", "Neutral"), #Grandpa
    textbox.TextBox("...Hold on.", "MainCharacter", "Neutral"), #Grandpa
    textbox.TextBox("There we go... you can tag the next one, alright, Oliver?", "MainCharacter", "Neutral"), #Grandpa
    textbox.TextBox("Now, go and fetch the carcass for me, please.", "MainCharacter", "Neutral"), #Grandpa
    textbox.TextBox("Oliver!!", "MainCharacter", "Neutral"), #Grandpa
]

#initialize variables
current_line_index = 0
clock = pygame.time.Clock()

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
                current_line_index = (current_line_index + 1) % len(text_lines)
                current_text_line = text_lines[current_line_index]
                current_text_line.text_index = 0
                #Stop the sound before it plays again.
                sound.stop()
                # Play sound when text is displayed
                sound.play()

    #draw text box
    current_text_line = text_lines[current_line_index]
    current_text_line.draw(SCREEN)
    
    # Update text index base on time
    current_text_line.update()

    # Stop sound once all text is displayed
    if current_text_line.text_index >= len(current_text_line.text):
        sound.stop()

    # Update the display
    pygame.display.flip()
    clock.tick(WIN.get_fps())

pygame.quit()
sys.exit()