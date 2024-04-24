import pygame
import sys
import os
import game_window as WIN
from button import Button
from Scene6_4IfYes import play_cutscene_6_4YES
from Scene6_4IfNo import play_cutscene_6_4NO

pygame.init()

#Set screen size using dimensions in the window_size function in game_window
SCREEN = pygame.display.set_mode(WIN.window_size())
pygame.display.set_caption("Wraithfall")

#Load font
def get_font(size, font_file="grand9kpixel.ttf"):
    return pygame.font.Font(os.path.join(WIN.DIR_FONTS, font_file), size)

def play_scene6_3CHOICE():
    run = True
    decision = None
    while run:
        #Get current mouse position
        CHOICE_MOUSE_POS = pygame.mouse.get_pos()
        
        #Create yes and no button
        YES_BUTTON = Button(image=None, pos=(540,500),
                            text_input="YES", font=get_font(75), base_color="#FFFFFF", hovering_color="#A90505")
        NO_BUTTON = Button(image=None, pos=(740,500),
                           text_input="NO", font=get_font(75), base_color="#FFFFFF", hovering_color="#A90505")

        #Update button colors and positions
        YES_BUTTON.changeColor(CHOICE_MOUSE_POS)
        YES_BUTTON.update(SCREEN)
        NO_BUTTON.changeColor(CHOICE_MOUSE_POS)
        NO_BUTTON.update(SCREEN)
        
        #Event loop
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if YES_BUTTON.checkForInput(CHOICE_MOUSE_POS):
                    #Execute IfYes Scene if yes is clicked
                    run = False
                    decision = play_cutscene_6_4YES
                    # os.system("python Scene6_4IfYes.py")
                if NO_BUTTON.checkForInput(CHOICE_MOUSE_POS):
                    run = False
                    decision = play_cutscene_6_4NO
                    # os.system("python Scene6_4IfNo.py")

        if decision is not None:
            decision()
        pygame.display.update()
    pygame.quit()
    sys.exit()

#play_scene6_3CHOICE()
