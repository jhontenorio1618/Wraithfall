import pygame, sys, os, game_window as WIN

pygame.init()

#Set screen size using the dimensions in the window_size function in game_window
SCREEN = pygame.display.set_mode(WIN.window_size())
pygame.display.set_caption("Menu")

#load font
def get_font(size):
    return pygame.font.Font(os.path.join(WIN.DIR_FONTS, "grand9Kpixel.ttf"), size)

#font size

font_size = 20
font = get_font(font_size)

#Display test text
text_to_display = "Welcome to Wraithfall..."
#Index to keep track of the characters
text_index = 0
#Time delay between the display of each character (in seconds)
text_delay = 0.1

#add a clock to control the frame rate
clock = pygame.time.Clock()

def draw_text_box(text):
    text_surface = font.render(text, True, "white")
    text_rect = text_surface.get_rect()
    #place at the bottom left of the screen
    text_rect.bottomleft = (0, WIN.WIN_HEIGHT)
    #blit the text surface onto the screen
    SCREEN.blit(text_surface, text_rect)
    
    #Main loop
running = True
while running:
    SCREEN.fill("black")
        
    for event in pygame.event.get():
        #uf yser closes the window exit the loop
        if event.type == pygame.QUIT:
            running = False
                
    #Display one character at a time
    if text_index < len(text_to_display):
        #Get the substring up to the current index
        text = text_to_display[:text_index + 1]
        #Draw the text box with current substring
        draw_text_box(text)
        #Delay the characters before displaying them
        if pygame.time.get_ticks() % (text_delay * 80) == 0:
            #Incremenet the index to display the next character
            text_index += 1
    
    #Update the display           
    pygame.display.flip()
    clock.tick(WIN.FPS)
        
pygame.quit()
sys.exit()
                
        
    