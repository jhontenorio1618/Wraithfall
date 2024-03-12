import pygame, sys, os, game_window as WIN
from button import Button
import pygame.event as EVENTS

pygame.init()

SCREEN = pygame.display.set_mode(WIN.window_size())
pygame.display.set_caption("Battle")


def battle_menu():
    # TODO need way to remember player + the mob they are fighting
    while True:
        PLAY_MOUSE_POSITION = pygame.mouse.get_pos()

        SCREEN.fill("black")

        PLAY_TEXT = WIN.get_font(45).render("This is where the magic will happen.", True, "White")
        PLAY_RECT = PLAY_TEXT.get_rect(center = (640, 260))
        SCREEN.blit(PLAY_TEXT, PLAY_RECT)

        BATTLE_FIGHT = Button(image=None, pos=(320, 460),
                              text_input="FIGHT", font=WIN.get_font(75), base_color="#FFFFFF", hovering_color="#A90505")
        BATTLE_RUN = Button(image=None, pos=(960, 460),
                            text_input="RUN", font=WIN.get_font(75), base_color="#FFFFFF", hovering_color="#A90505")
        BATTLE_FIGHT.changeColor(PLAY_MOUSE_POSITION)
        BATTLE_FIGHT.update(SCREEN)
        BATTLE_RUN.changeColor(PLAY_MOUSE_POSITION)
        BATTLE_RUN.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                WIN.game_exit()
            if event.type == pygame.KEYDOWN:
                # Escape Key
                if event.key == pygame.K_ESCAPE:
                    WIN.game_exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if BATTLE_FIGHT.checkForInput(PLAY_MOUSE_POSITION):
                    # TODO Attack
                    x = 1
                if BATTLE_RUN.checkForInput(PLAY_MOUSE_POSITION):
                    # TODO "Run" from fight. should return to original position
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
