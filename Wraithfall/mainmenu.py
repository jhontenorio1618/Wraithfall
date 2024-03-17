#Used this tutorial for help making the main menu https://www.youtube.com/watch?v=GMBqjxcKogA
import pygame, sys, os, game_window as WIN
from button import Button

pygame.init()

SCREEN = pygame.display.set_mode(WIN.window_size())
pygame.display.set_caption("Menu")

MENU_TITLE = pygame.image.load(os.path.join(WIN.DIR_IMAGES, "WRAITHFALL_TITLE.png")).convert_alpha()


#Background
BG = pygame.image.load(os.path.join(WIN.DIR_IMAGES, "menu_screen.jpeg")).convert()

#Set size for image
DEFAULT_MENU_BACKGROUND_IMAGE_SIZE=(1280,720)

#scale image
BG = pygame.transform.scale(BG, DEFAULT_MENU_BACKGROUND_IMAGE_SIZE)

#Set a position
DEFAULT_BACKGROUND_IMAGE_POSITION = (640,360)


#load the font we want to use for the game
#will return the font in the desired size
def get_font(size):
    return pygame.font.Font(os.path.join(WIN.DIR_FONTS, "grand9Kpixel.ttf"), size)

#If user clicks play, this is a place holder for now until game is ready
def play():
    while True:
        PLAY_MOUSE_POSITION = pygame.mouse.get_pos()
        
        SCREEN.fill("black")
        
        PLAY_TEXT = get_font(45).render("This is a place holder for the play screen", True, "White")
        PLAY_RECT = PLAY_TEXT.get_rect(center = (640, 260))
        SCREEN.blit(PLAY_TEXT, PLAY_RECT)
        
        PLAY_BACK = Button(image = None, pos=(640,460), # #A90505
                           text_input = "BACK", font = get_font(75), base_color="#FFFFFF", hovering_color="#A90505")
        PLAY_BACK.changeColor(PLAY_MOUSE_POSITION)
        PLAY_BACK.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POSITION):
                    main_menu()
            
        pygame.display.update()
        
def main_menu():
    while True:
        SCREEN.blit(BG,(0,0))
        
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        
        MENU_TEXT = get_font(150).render("WRAITHFALL", True, "#C2D7E7")
        MENU_RECT = MENU_TEXT.get_rect(center=(640,100))
        
        SCREEN.blit(MENU_TITLE, (0, 0))  # Blit the title image
        SCREEN.blit(MENU_TEXT, MENU_RECT)
        
        
        PLAY_BUTTON = Button (image=None, pos=(640,400),
                               text_input="PLAY", font = get_font(75), base_color="#FFFFFF", hovering_color="#A90505")
        QUIT_BUTTON = Button (image = None, pos=(640,500),
                               text_input="QUIT", font = get_font(75), base_color="#FFFFFF", hovering_color="#A90505")
        
        SCREEN.blit(MENU_TEXT, MENU_RECT)
        
        for button in [PLAY_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()
                    
        pygame.display.update()
    
main_menu()