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
sound = pygame.mixer.Sound(os.path.join(WIN.DIR_MUSIC, "pencilwriting.wav"))
# play sound and loop until text is finished
# sound.play(loops=-1)

#Text lines
text_lines = [
    textbox.TextBox("JOURNAL: \"June 18th, 2058: ", "MainCharacter", "Neutral"),
    textbox.TextBox("Dear Alice,", "MainCharacter", "Neutral"),
    textbox.TextBox("It's been six months, now, since the Rift appeared in the sky above the city.", "MainCharacter", "Sad"),
    textbox.TextBox("When Grandpa lets me go up on the roof of the cabin, I've got a perfect view of it", "MainCharacter", "Neutral"),
    textbox.TextBox("now, just past a few moutain peaks. It looks like the fabric of the sky is torn open.", "MainCharacter", "Neutral"),
    textbox.TextBox("The black smoke pours out constantly, covering the world in darkness.", "MainCharacter", "Neutral"),
    textbox.TextBox("They still don't know how to stop it; it's hidden the sun from everyone now.", "MainCharacter", "Sad"),
    textbox.TextBox("Just last week the UN declared a worldwide emergency, fearful of a new ice age.", "MainCharacter", "Neutral"),
    textbox.TextBox("It's supposed to be summer here, but it's still freezing.", "MainCharacter", "Sad"),
    textbox.TextBox("Grandpa thinks we'll never see the sun again...", "MainCharacter", "Sad"),
    textbox.TextBox("The wraiths are coming constantly from the Rift now, too.", "MainCharacter", "Neutral"),
    textbox.TextBox("Grandpa and I were attacked by one in the woods a few weeks ago; at this point,", "MainCharacter", "Neutral"),
    textbox.TextBox("it's barely safe to go out and hunt.", "MainCharacter", "Neutral"),
    textbox.TextBox("Two of them got our neighbor, Nellie, this week.", "MainCharacter", "Sad"),
    textbox.TextBox("I know it sounds stupid, but I've been researching the rift in my spare time.", "MainCharacter", "Neutral"),
    textbox.TextBox("I want to understand it. I want to figure out why it's here.", "MainCharacter", "Neutral"),
    textbox.TextBox("I'll be writing you to keep documenting my findings.", "MainCharacter", "Neutral"),
    textbox.TextBox("Who knows, maybe I'll actually figure something out.", "MainCharacter", "Excited"),
    textbox.TextBox("I know the city's destroyed now, but I hope you're alright.", "MainCharacter", "Happy"),
    textbox.TextBox("I'm not even sure if these letters ever get to you. If they do, write back, ok?", "MainCharacter", "Neutral"),
    textbox.TextBox("Eventually, I'll come find you.", "MainCharacter", "Happy"),
    textbox.TextBox("-   Oliver\"", "MainCharacter", "Neutral")
]

#initialize variables
current_line_index = 0
clock = pygame.time.Clock()

# Main loop
running = True

# Initializes the scene as a SceneManager object which manages the Textbox objects
scene1 = textbox.SceneManager(text_lines)
while running:
    SCREEN.fill("black")

    for event in pygame.event.get():
        # If user closes the window exit the loop
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            # If enter key is pressed move to the next line
            if event.key == pygame.K_RETURN:
                scene1.next_textbox()
                """
                current_line_index = (current_line_index + 1) % len(text_lines)
                current_text_line = text_lines[current_line_index]
                current_text_line.text_index = 0
                #Stop sound before playing again
                sound.stop()
                # Play sound when text is displayed
                sound.play()
                """

    scene1.draw_textboxes(SCREEN)
    """
    #draw text box
    current_text_line = text_lines[current_line_index]
    current_text_line.draw(SCREEN)
    
    # Update text index base on time
    current_text_line.update()

    # Stop sound once all text is displayed
    if current_text_line.text_index >= len(current_text_line.text):
        sound.stop()
    """

    # Update the display
    pygame.display.flip()
    clock.tick(WIN.get_fps())


pygame.quit()
sys.exit()