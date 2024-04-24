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
    textbox.TextBox("Up and at'em, eh, Oliver?", "MainCharacter", "Neutral"), #Grandpa
    textbox.TextBox("Finally - it's already past dawn!", "MainCharacter", "Neutral"), #Grandpa
    textbox.TextBox("Not that anyone can tell anymore...", "MainCharacter", "Sad"), #Grandpa
    textbox.TextBox("The wraiths have been quiet since last night.", "MainCharacter", "Neutral"), #Grandpa
    textbox.TextBox("They left another pile of drained deer carcasses by the treeline.", "MainCharacter", "Neutral"), #Grandpa
    textbox.TextBox("It's a shame, all that tainted meat...", "MainCharacter", "Neutral"), #Grandpa
    textbox.TextBox("...Listen, Oliver.", "MainCharacter", "Sad"), #Grandpa
    textbox.TextBox("While I've got no desire to let you anywhere near those abominations...", "MainCharacter", "Neutral"), #Grandpa
    textbox.TextBox("...I'm getting old, and hunting is hard on my bones. ", "MainCharacter", "Sad"), #Grandpa
    textbox.TextBox("Come out with me right now - I can show you the ropes, yeah?", "MainCharacter", "Sad"), #Grandpa
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
    if current_line_index >= len(current_text_line.text):
        sound.stop()

    # Update the display
    pygame.display.flip()
    clock.tick(WIN.get_fps())

pygame.quit()
sys.exit()