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
    textbox.TextBox("Now that was good...", "Grandpa", "Happy"), #grandpa
    textbox.TextBox("Y'know...", "Grandpa", "Happy"), #grandpa
    textbox.TextBox("We might not have fast food anymore, but nothing tastes better than meat you caught yourself.", "Grandpa", "Happy"), #grandpa
    textbox.TextBox("...", "Grandpa", "Neutral"), #grandpa
    textbox.TextBox("Hey, I'm really proud of you, Oliver.", "Grandpa", "Happy"), #grandpa
    textbox.TextBox("I know things got hard after you lost your mom...", "Grandpa", "Neutral"), #grandpa
    textbox.TextBox("And I know they got harder with this whole \"otherworldly apocalypse\" thing going on.", "Grandpa", "Neutral"), #grandpa
    textbox.TextBox("You're really growning into your own out here.", "Grandpa", "Happy"), #grandpa
    textbox.TextBox("...", "Grandpa", "Neutral"), #grandpa
    textbox.TextBox("You know--", "Grandpa", "Happy"), #grandpa
    textbox.TextBox("What the-?!", "MainCharacter", "Neutral"), #Maincharacter
    textbox.TextBox("...Now, I've seen plenty of strange things these past few months, but that was new.", "Grandpa", "Neutral"), #grandpa
    textbox.TextBox("Whatever came out of that rift just now, it landed on our mountain.", "Grandpa", "Mad"), #grandpa
    textbox.TextBox("...", "Grandpa", "Neutral"), #grandpa
    textbox.TextBox("...What, you want to go see what it is?", "Grandpa", "Neutral"), #grandpa
    textbox.TextBox("Kid, I feel like I don't need to explain to you why that's too dangerous.", "Grandpa", "Mad"), #grandpa
    textbox.TextBox("*Sigh*...Alright, fine. I know you're curious about the rift. ", "Grandpa", "Neutral"), #grandpa
    textbox.TextBox("Whatever it is, we don't get close, got it?", "Grandpa", "Neutral"), #grandpa
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