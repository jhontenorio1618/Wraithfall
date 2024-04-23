import pygame
import game_window as WIN
import os
import view_portraits
import textbox

pygame.init()

# Set screen size using the dimensions in the window_size function in game_window
SCREEN = pygame.display.set_mode(WIN.window_size())
pygame.display.set_caption("Menu")

# Load the sound file
pygame.mixer.init()
sound = pygame.mixer.Sound(os.path.join(WIN.DIR_MUSIC, "text_sound.wav"))
# play sound and loop until text is finished
sound.play(loops=-1)

# Text lines
text_lines = [
    textbox.TextBox("Welcome to Wraitfall...", "MainCharacter", "Happy"),
    textbox.TextBox("Press Enter...", "MainCharacter", "Excited")
]

# Initialize variables
current_line_index = 0
text_index = 0
text_delay = 0.1
clock = pygame.time.Clock()
running = True

# Main loop
while running:
    SCREEN.fill("black")

    for event in pygame.event.get():
        # If user closes the window exit the loop
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            # If enter key is pressed move to the next line
            if event.key == pygame.K_RETURN:
                text_index = 0
                current_line_index = (current_line_index + 1) % len(text_lines)
                current_text_line = text_lines[current_line_index]
                # Play sound when text is displayed
                sound.play()

    # Draw text box
    current_text_line = text_lines[current_line_index]
    current_text_line.draw(SCREEN)

    # Delay the characters before displaying them
    if pygame.time.get_ticks() % (text_delay * 40) == 0 and text_index < len(current_text_line.text):
        # Increment the index to display the next character
        text_index += 1

    # Stop sound once all text is displayed
    if text_index >= len(current_text_line.text):
        sound.stop()

    # Update the display
    pygame.display.flip()
    clock.tick(WIN.get_fps())

pygame.quit()
sys.exit()
