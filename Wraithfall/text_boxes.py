import game_window as WIN
import os
import pygame
import sys
import view_portraits

pygame.init()

# Set screen size using the dimensions in the window_size function in game_window
SCREEN = pygame.display.set_mode(WIN.window_size())
pygame.display.set_caption("Menu")


def get_image(sheet, frame, width, height, scale):
    image = pygame.Surface((width, height), pygame.SRCALPHA).convert_alpha()
    image.blit(sheet, (0, 0), ((frame * width), 0, width, height))
    image = pygame.transform.scale(image, (width * scale, height * scale))
    return image


# Dictionary mapping character names to portrait frames
character_portraits = {
    "MainCharacter": {
        "Neutral": get_image(view_portraits.mc_sheet, 0, 104, 111, 2),
        "Happy": get_image(view_portraits.mc_sheet, 1, 104, 111, 2),
        "Excited": get_image(view_portraits.mc_sheet, 2, 104, 111, 2),
        "Sad": get_image(view_portraits.mc_sheet, 3, 104, 111, 2),
        "Angry": get_image(view_portraits.mc_sheet, 4, 104, 111, 2)
    }
}


# Function to get the correct frame for a character's emotion
def get_character_frame(character_name, emotion):
    return character_portraits[character_name][emotion]


# Load font
def get_font(size):
    return pygame.font.Font(os.path.join(WIN.DIR_FONTS, "grand9Kpixel.ttf"), size)


# Font size
font_size = 20
font = WIN.get_font(font_size)

# Display test text
""" [0]: Text to display
    [1]: Reference to character (from character_portraits)
    [2]: Reference to character's emotion """
text_lines = [
        ["Welcome to Wraithfall...", "MainCharacter", "Happy"],
        ["Press Enter...", "MainCharacter",  "Excited"],
        ["New line of text test...", "MainCharacter", "Neutral"]
    ]
# Index to keep track of the characters
current_line_index = 0
current_text_line = text_lines[current_line_index]
# index to keep track of the characters
text_index = 0
# Time delay between the display of each character (in seconds)
text_delay = 0.1

# Load the sound file
pygame.mixer.init()
sound = pygame.mixer.Sound(os.path.join(WIN.DIR_MUSIC, "text_sound.wav"))
# play sound and loop until text is finished
sound.play(loops=-1)

# Add a clock to control the frame rate
clock = pygame.time.Clock()


def draw_text_box(text, character, emote):
    # Define dimensions and position of the textbox
    text_box_width = WIN.WIN_WIDTH - 40
    text_box_height = font_size + 100
    text_box_rect = pygame.Rect((20, WIN.WIN_HEIGHT - text_box_height - 20), (text_box_width, text_box_height))

    pygame.draw.rect(SCREEN, "white", text_box_rect, 2)

    # Get the character name
    character_name = character  # "MainCharacter"
    emotion = emote
    # Get the emotion based on the current line of text
    """if "Welcome" in text_to_display:
        emotion = "Happy"
    elif "Press Enter" in text_to_display:
        emotion = "Excited"
    else:
        emotion = "Neutral"  # Default emotion"""

    # Get the character portrait for the current emotion
    portrait = get_character_frame(character_name, emotion)
    if portrait:
        portrait_rect = portrait.get_rect(topleft=(25, WIN.WIN_HEIGHT - text_box_height - 95))
        SCREEN.blit(portrait, portrait_rect)

    # Center the text within the text box
    text_surface = font.render(text[:text_index + 1], True, "white")
    text_rect = text_surface.get_rect(center=text_box_rect.center)

    # Blit the text surface onto the screen
    SCREEN.blit(text_surface, text_rect)


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
                text_index = 0
                current_line_index = (current_line_index + 1) % len(text_lines)
                current_text_line = text_lines[current_line_index]
                # Play sound when text is displayed
                sound.play()

    draw_text_box(current_text_line[0], current_text_line[1], current_text_line[2])  # Draw the outline of the text box

    # Delay the characters before displaying them
    if pygame.time.get_ticks() % (text_delay * 40) == 0 and text_index < len(current_text_line[0]):
        # Increment the index to display the next character
        text_index += 1

    # Stop sound once all text is displayed
    if text_index >= len(current_text_line[0]):
        sound.stop()

    # Update the display
    pygame.display.flip()
    clock.tick(WIN.get_fps())

pygame.quit()
sys.exit()
