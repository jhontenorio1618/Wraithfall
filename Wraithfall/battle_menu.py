import pygame, sys, os, game_window as WIN
from button import Button
import pygame.event as EVENTS
import entity_classes as ENTITY

pygame.init()
SCREEN = pygame.display.set_mode(WIN.window_size())
pygame.display.set_caption("Battle")


class Battle():
    def __init__(self, player=ENTITY.Player(), mobs=[ENTITY.Mob()]):
        self.player = player
        self.mobs = mobs

    def combat_screen(self):
        in_combat = True
        mobs_living = True
        while in_combat:
            PLAY_MOUSE_POSITION = pygame.mouse.get_pos()

            SCREEN.fill("black")

            # TODO Buttons seem to appear even when they shouldn't exist and can be pressed
            # Button pressed to "FIGHT"
            BATTLE_FIGHT = Button(image=None, pos=(320, 460),
                                  text_input="FIGHT", font=WIN.get_font(75), base_color="#FFFFFF", hovering_color="#A90505")
            # Button pressed to "RUN"
            BATTLE_RUN = Button(image=None, pos=(960, 460),
                                text_input="RUN", font=WIN.get_font(75), base_color="#FFFFFF", hovering_color="#A90505")
            # Button pressed to exit combat menu after finishing the fight
            BATTLE_NEXT = Button(image=None, pos=(960, 460),
                                 text_input="NEXT", font=WIN.get_font(75), base_color="#FFFFFF", hovering_color="#A90505")

            if mobs_living:
                # Mobs are displayed as living
                # TODO Put visuals for mobs here
                PLAY_TEXT = WIN.get_font(45).render("This is where the magic will happen.", True, "White")
                PLAY_RECT = PLAY_TEXT.get_rect(center=(640, 260))
                mob_hp_color = "Green"
                # The battle is ongoing. Show FIGHT and RUN buttons
                BATTLE_FIGHT.changeColor(PLAY_MOUSE_POSITION)
                BATTLE_FIGHT.update(SCREEN)
                BATTLE_RUN.changeColor(PLAY_MOUSE_POSITION)
                BATTLE_RUN.update(SCREEN)
            else:
                # Mobs are displayed as dead, the battle has ended.
                PLAY_TEXT = WIN.get_font(45).render("The wraith is dead. :)", True, "Red")
                PLAY_RECT = PLAY_TEXT.get_rect(center=(640, 260))
                mob_hp_color = "Red"
                # Display exit button that appears as "NEXT"
                BATTLE_NEXT.changeColor(PLAY_MOUSE_POSITION)
                BATTLE_NEXT.update(SCREEN)
            SCREEN.blit(PLAY_TEXT, PLAY_RECT)

            # Mob HP display
            mob_hp_text = WIN.get_font(30).render(str(self.mobs[0].get_stats()["HP"]) + "/" +
                                                  str(self.mobs[0].get_stats()["HP Max"]), True, mob_hp_color)
            mob_hp_rect = mob_hp_text.get_rect(center=(640, 360))
            SCREEN.blit(mob_hp_text, mob_hp_rect)

            # Determine what happens for each event
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    WIN.game_exit()
                if event.type == pygame.KEYDOWN:
                    # Escape Key
                    if event.key == pygame.K_ESCAPE:
                        WIN.game_exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if BATTLE_FIGHT.checkForInput(PLAY_MOUSE_POSITION):
                        damage_inflicted = self.mobs[0].get_stats()["DEF"] - self.player.get_stats()["ATK"]
                        if damage_inflicted > 0:
                            damage_inflicted = 0
                        # "FIGHT" Button
                        self.mobs[0].hp_update(damage_inflicted)
                        if self.mobs[0].get_stats()["HP"] <= 0:
                            mobs_living = False
                    if BATTLE_RUN.checkForInput(PLAY_MOUSE_POSITION):
                        # "RUN" Button: flee from fight without killing the mobs
                        # TODO for some reason need to click twice for it to process
                        in_combat = False
                    if BATTLE_NEXT and BATTLE_NEXT.checkForInput(PLAY_MOUSE_POSITION):
                        # TODO NEXT button can still technically be pressed even when it isn't blit'd
                        # "NEXT" Button: click to leave combat after killing the mobs
                        in_combat = False

            pygame.display.update()
        return mobs_living

