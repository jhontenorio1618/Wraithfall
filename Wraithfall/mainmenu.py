#Used this tutorial for help making the main menu https://www.youtube.com/watch?v=GMBqjxcKogA
import pygame, sys, os, game_window as WIN
from button import Button

pygame.init()

#Set screen size using the dimensions in the window_size function in game_window
SCREEN = pygame.display.set_mode(WIN.window_size())
pygame.display.set_caption("Menu")

#Load the menu title image
MENU_TITLE = pygame.image.load(os.path.join(WIN.DIR_IMAGES, "WRAITHFALL_TITLE.png")).convert_alpha()


#Load the background image
BG = pygame.image.load(os.path.join(WIN.DIR_IMAGES, "Main_Menu_Background.png")).convert()

#Set size for image
DEFAULT_MENU_BACKGROUND_IMAGE_SIZE=(1280,720)

#scale background image
BG = pygame.transform.scale(BG, DEFAULT_MENU_BACKGROUND_IMAGE_SIZE)

#Set a position
DEFAULT_BACKGROUND_IMAGE_POSITION = (640,360)


#load the font we want to use for the game
#will return the font in the desired size
def get_font(size, font_file="grand9Kpixel.ttf"):
    return pygame.font.Font(os.path.join(WIN.DIR_FONTS, font_file), size)

def play_music(music_file, n=-1):
    """ audio_file = name of the audio file you want to play.
        n = number of times audio should play. if -1, it will loop forever"""
    pygame.mixer.music.load(os.path.join(WIN.DIR_MUSIC, music_file))
    pygame.mixer.music.play(n)
    return music_file

#Load the music file
WIN.play_music("Main_Menu_Music.wav")
# pygame.mixer.music.load(os.path.join(WIN.DIR_AUDIO, "Main_Menu_Music.wav"))
# pygame.mixer.music.play(-1)

#If user clicks play, this is a place holder for now until game is ready
def play():
    #if game is not paused return false
    #paused = False #This will determine if game is paused in the future
    while True:

        from TestEntity import play_testentity

        # play_testentity()
        """
        #Retrieve current mouse position
        PLAY_MOUSE_POSITION = pygame.mouse.get_pos()
        
        SCREEN.fill("black")
        
        #Render text for play screen
        PLAY_TEXT = get_font(45).render("This is a place holder for the play screen", True, "White")
        PLAY_RECT = PLAY_TEXT.get_rect(center = (640, 260))
        SCREEN.blit(PLAY_TEXT, PLAY_RECT)
        
        #Create a button that will bring you back to the main menu
        PLAY_BACK = Button(image = None, pos=(640,460), # #A90505
                           text_input = "BACK", font = get_font(75), base_color="#FFFFFF", hovering_color="#A90505")
        PLAY_BACK.changeColor(PLAY_MOUSE_POSITION) #Change color of text when cursor hovers over
        PLAY_BACK.update(SCREEN) #updates the button
        
        #event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POSITION):
                    #break
                    #exit the play loop and go to main menu
                    main_menu()
                '''if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    paused = True
                    
            if paused:
                pause_menu()
                paused = False'''
            """
        pygame.display.update()
        
#ignore line 76-109 for now.
'''def text_objexts(text, font):
    textSurface = font.render(text, True("#FFFFF"))
    return textSurface, textSurface.get_rect()

def pause_menu():
    while paused: #Loop continnues as long as paused is True
        SCREEN.fill("black")
        
        #display paused text
        pausedText = pygame.font.Font("grand9KPixel.ttf", 115)
        TextSurf, TextRect = text_objects("PAUSED", pausedText)
        TextRect.center = ((SCREEN.get_width() / 2) (SCREEN.get_height / 2))
        SCREEN.blit(TextSurf, TextRect)
        
        #create buttons for paused menu
        RESUME_BUTTON = Button(image = None, pos = (SCREEN.get_width()//2, SCREEN.get_height//2-100),
                               text_input= "Resume", font = get_font(75), base_color = "#FFFFFF", hovering_color = "#A90505")
        QUIT_BUTTON = Button(image = None, pos = (SCREEN.get_width()//2, SCREEN.get_height()//2 +100),
                             text_input = "Quit", font = get_font(75), base_color = "#FFFFF", hovering_color = "#A90505")
        
        for button in [RESUME_BUTTON, QUIT_BUTTON]:
            button.changeColor(pygame.mouse.get_pos())
            button.update(SCREEN)
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if RESUME_BUTTON.checkForInput(pygame.mouse.get_pos()):
                    paused = False #Unpause when clicking resume
                if QUIT_BUTTON.checkForInput(pygame.mouse.get_pos()):
                    pygame.quit()
                    sys.exit()'''
      
def main_menu():
    while True:
        if not pygame.mixer.music.get_busy():
            # Assures main menu music is playing when on main menu
            play_music("Main_Menu_Music.wav")
        SCREEN.blit(BG,(0,0))
        
        #Get current mouse position
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        
        #Render text for main menu
        MENU_TEXT = get_font(150).render(" ", True, "#C2D7E7")
        MENU_RECT = MENU_TEXT.get_rect(center=(640,100))
        
        SCREEN.blit(MENU_TITLE, (0, 0))  # Blit the title image
        SCREEN.blit(MENU_TEXT, MENU_RECT)
        
        #Create play and quit buttons
        PLAY_BUTTON = Button (image=None, pos=(640,450),
                               text_input="PLAY", font = get_font(75), base_color="#FFFFFF", hovering_color="#A90505")
        QUIT_BUTTON = Button (image = None, pos=(640,540),
                               text_input="QUIT", font = get_font(75), base_color="#FFFFFF", hovering_color="#A90505")
        
        SCREEN.blit(MENU_TEXT, MENU_RECT)
        
        #Update button colors and positions
        for button in [PLAY_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        #event loop    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    WIN.stop_music()
                    play() #start the game when clicking play (text placeholder for now)
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit() #Close/quit the window when clicking the quit button.
                    
        pygame.display.update()
        

    
main_menu()