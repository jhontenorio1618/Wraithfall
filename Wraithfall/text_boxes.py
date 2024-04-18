import pygame, sys, os, game_window as WIN

pygame.init()

# Set screen size using the dimensions in the window_size function in game_window
SCREEN = pygame.display.set_mode(WIN.window_size())
pygame.display.set_caption("Menu")

# Load font
def get_font(size):
    return pygame.font.Font(os.path.join(WIN.DIR_FONTS, "grand9Kpixel.ttf"), size)

# Font size
font_size = 20
font = get_font(font_size)

# Display test text
text_lines = [
    "Welcome to Wraithfall...",
    "Press Enter...",
    "New line of text test..."
]
# Index to keep track of the characters
current_line_index = 0
text_to_display = text_lines[current_line_index]
#index to keep track of the characters
text_index = 0
# Time delay between the display of each character (in seconds)
text_delay = 0.1

#Load the sound file
pygame.mixer.init()
sound = pygame.mixer.Sound(os.path.join(WIN.DIR_AUDIO, "text_sound.wav"))
#play sound and loop until text is finished
sound.play(loops=-1)

# Add a clock to control the frame rate
clock = pygame.time.Clock()

def draw_text_box():
    # Define dimensions and position of the textbox
    text_box_width = WIN.WIN_WIDTH - 40
    text_box_height = font_size + 100
    text_box_rect = pygame.Rect((20, WIN.WIN_HEIGHT - text_box_height - 20), (text_box_width, text_box_height))
    
    pygame.draw.rect(SCREEN, "white", text_box_rect, 2)

    # Center the text within the text box
    text_surface = font.render(text_to_display[:text_index + 1], True, "white")
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
            #If enter key is pressed move to the next line
            if event.key == pygame.K_RETURN:
                text_index = 0
                current_line_index = (current_line_index + 1) % len (text_lines)
                text_to_display = text_lines[current_line_index]
                #Play sound when text is displayed
                sound.play()

    draw_text_box()  # Draw the outline of the text box

    # Delay the characters before displaying them
    if pygame.time.get_ticks() % (text_delay * 40) == 0 and text_index < len(text_to_display):
        # Increment the index to display the next character
        text_index += 1
        
    #Stop sound once all text is displayed
    if text_index >= len (text_to_display):
        sound.stop()

    # Update the display
    pygame.display.flip()
    clock.tick(WIN.FPS)

pygame.quit()
sys.exit()
