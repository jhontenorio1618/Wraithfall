import pygame, sys, os, game_window as WIN
from button import Button
import pygame.event as EVENTS
import entity_classes as ENTITY

pygame.init()
SCREEN = pygame.display.set_mode(WIN.window_size())
pygame.display.set_caption("Battle")


class Battle:
    def __init__(self, player=ENTITY.Player(), mobs=ENTITY.Mob()):
        self.player = player
        self.mobs = mobs
        # TODO make "in_combat", "mobs_living", and "player_living" variables here instead of local

    def combat_screen(self):
        in_combat = True
        mobs_living = True
        player_living = True
        open_sword_menu = False
        open_item_menu = False
        enemy_turn = False
        exp_gained = 0
        while in_combat:
            if open_sword_menu:
                # Pressed SWORD button
                self.sword_menu()
                open_sword_menu = False
            if open_item_menu:
                # Pressed ITEM button
                used_item = self.item_menu()
                enemy_turn = used_item
                open_item_menu = False

            if enemy_turn:
                # Enemy attacks
                self.player.hp_update(self.enemy_turn())
                if self.player.get_stats()["HP"] <= 0:
                    # Player is dead
                    in_combat = False
                    player_living = False
                enemy_turn = False

            PLAY_MOUSE_POSITION = pygame.mouse.get_pos()
            SCREEN.fill("black")

            # Button pressed to "FIGHT"
            BATTLE_FIGHT = Button(image=None, pos=(320, 460),
                                  text_input="FIGHT", font=WIN.get_font(75), base_color="#FFFFFF", hovering_color="#A90505")
            fight_displayed = False
            # Button pressed to "RUN"
            BATTLE_RUN = Button(image=None, pos=(960, 460),
                                text_input="RUN", font=WIN.get_font(75), base_color="#FFFFFF", hovering_color="#A90505")
            run_displayed = False
            # Button pressed to exit combat menu after finishing the fight
            BATTLE_NEXT = Button(image=None, pos=(960, 460),
                                 text_input="NEXT", font=WIN.get_font(75), base_color="#FFFFFF", hovering_color="#A90505")
            next_displayed = False
            # Button pressed to access item menu
            BATTLE_ITEM = Button(image=None, pos=(320, 580),
                                  text_input="ITEM", font=WIN.get_font(75), base_color="#FFFFFF", hovering_color="#A90505")
            item_displayed = False
            # Button pressed to access sword menu
            BATTLE_SWORD = Button(image=None, pos=(960, 580),
                                 text_input="SWORD", font=WIN.get_font(75), base_color="#FFFFFF", hovering_color="#A90505")
            sword_displayed = False

            if mobs_living:
                # Mobs are displayed as living
                # TODO Put visuals for mobs here
                PLAY_TEXT = WIN.get_font(45).render("This is where the magic will happen.", True, "White")
                PLAY_RECT = PLAY_TEXT.get_rect(center=(640, 260))
                mob_hp_color = "Green"
                # The battle is ongoing. Show FIGHT, RUN, and ITEM buttons
                BATTLE_FIGHT.changeColor(PLAY_MOUSE_POSITION)
                BATTLE_FIGHT.update(SCREEN)
                fight_displayed = True
                BATTLE_RUN.changeColor(PLAY_MOUSE_POSITION)
                BATTLE_RUN.update(SCREEN)
                run_displayed = True
                BATTLE_ITEM.changeColor(PLAY_MOUSE_POSITION)
                BATTLE_ITEM.update(SCREEN)
                item_displayed = True
                if self.player.access_sword() is not None:
                    BATTLE_SWORD.changeColor(PLAY_MOUSE_POSITION)
                    BATTLE_SWORD.update(SCREEN)
                    sword_displayed = True
            else:
                # Mobs are displayed as dead, the battle has ended.
                PLAY_TEXT = WIN.get_font(45).render("The wraith is dead. :)", True, "Red")
                PLAY_RECT = PLAY_TEXT.get_rect(center=(640, 260))
                mob_hp_color = "Red"
                # Display exit button that appears as "NEXT"
                BATTLE_NEXT.changeColor(PLAY_MOUSE_POSITION)
                BATTLE_NEXT.update(SCREEN)
                next_displayed = True
            SCREEN.blit(PLAY_TEXT, PLAY_RECT)

            self.display_hp(mob_hp_color)

            # Determine what happens for each event
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    WIN.game_exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        # Escape Key
                        WIN.game_exit()
                    if next_displayed and event.key == pygame.K_SPACE:
                        # "NEXT" Button Shortcut
                        in_combat = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if fight_displayed and BATTLE_FIGHT.checkForInput(PLAY_MOUSE_POSITION):
                        # "FIGHT" Button: attack the mob
                        damage_inflicted = self.mobs.get_stats()["DEF"] - self.player.get_stats()["ATK"]
                        if damage_inflicted > 0:
                            damage_inflicted = 0
                        # Calculate Mob HP after damage
                        self.mobs.hp_update(damage_inflicted)
                        if self.mobs.get_stats()["HP"] <= 0:
                            # Mob is dead
                            mobs_living = False
                            # Player gains EXP from killing mob
                            self.player.gain_exp(self.mobs.drop_exp())
                        else:
                            # Enemy's turn to attack
                            enemy_turn = True
                    if run_displayed and BATTLE_RUN.checkForInput(PLAY_MOUSE_POSITION):
                        # "RUN" Button: flee from fight without killing the mobs
                        in_combat = self.run_state()
                    if next_displayed and BATTLE_NEXT.checkForInput(PLAY_MOUSE_POSITION):
                        # "NEXT" Button: click to leave combat after killing the mobs
                        in_combat = False
                    if sword_displayed and BATTLE_SWORD.checkForInput(PLAY_MOUSE_POSITION):
                        # "SWORD" Button: open sword menu to change form of sword
                        open_sword_menu = True
                    if item_displayed and BATTLE_ITEM.checkForInput(PLAY_MOUSE_POSITION):
                        # "ITEM" Button: open item menu to select an item to use
                        open_item_menu = True

            pygame.display.update()
        return mobs_living

    def fight_state(self):
        # Clicked FIGHT Button
        # TODO finish
        self.player_turn()
        self.enemy_turn()
        return 0

    def run_state(self):
        # Clicked RUN Button
        # TODO calculate RUN % chance
        success = True
        return success

    def sword_menu(self):
        in_menu = True
        while in_menu:
            PLAY_MOUSE_POSITION = pygame.mouse.get_pos()
            SCREEN.fill("black")

            # Button pressed for BASE sword form
            SWORD_BASE = Button(image=None, pos=(320, 220),
                                  text_input="BASE", font=WIN.get_font(75), base_color="#FFFFFF", hovering_color="#FFCC40")
            base_displayed = False
            # Button pressed for FIRE sword form
            SWORD_FIRE = Button(image=None, pos=(320, 340),
                                text_input="FIRE", font=WIN.get_font(75), base_color="#FFFFFF", hovering_color="#FF0000")
            fire_displayed = False
            # Button pressed for ICE sword form
            SWORD_ICE = Button(image=None, pos=(320, 460),
                                 text_input="ICE", font=WIN.get_font(75), base_color="#FFFFFF", hovering_color="#0000FF")
            ice_displayed = False
            # Button pressed for DARK sword form
            SWORD_DARK = Button(image=None, pos=(320, 580),
                                  text_input="DARK", font=WIN.get_font(75), base_color="#FFFFFF", hovering_color="#FF00FF")
            dark_displayed = False

            BACK_BUTTON = Button(image=None, pos=(150, 650),
                                 text_input="BACK", font=WIN.get_font(75), base_color="#FFFFFF", hovering_color="#FFCC40")
            back_displayed = False

            SWORD_BASE.changeColor(PLAY_MOUSE_POSITION)
            SWORD_BASE.update(SCREEN)
            base_displayed = True
            SWORD_FIRE.changeColor(PLAY_MOUSE_POSITION)
            SWORD_FIRE.update(SCREEN)
            fire_displayed = True
            SWORD_ICE.changeColor(PLAY_MOUSE_POSITION)
            SWORD_ICE.update(SCREEN)
            ice_displayed = True
            SWORD_DARK.changeColor(PLAY_MOUSE_POSITION)
            SWORD_DARK.update(SCREEN)
            dark_displayed = True

            BACK_BUTTON.changeColor(PLAY_MOUSE_POSITION)
            BACK_BUTTON.update(SCREEN)
            back_displayed = True

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    WIN.game_exit()
                if event.type == pygame.KEYDOWN:
                    # Escape Key
                    if event.key == pygame.K_ESCAPE:
                        WIN.game_exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if base_displayed and SWORD_BASE.checkForInput(PLAY_MOUSE_POSITION):
                        self.player.access_sword().shift_form("BASE")
                        in_menu = False
                        base_displayed, fire_displayed, ice_displayed, dark_displayed = False, False, False, False
                    if fire_displayed and SWORD_FIRE.checkForInput(PLAY_MOUSE_POSITION):
                        self.player.access_sword().shift_form("FIRE")
                        in_menu = False
                        base_displayed, fire_displayed, ice_displayed, dark_displayed = False, False, False, False
                    if ice_displayed and SWORD_ICE.checkForInput(PLAY_MOUSE_POSITION):
                        self.player.access_sword().shift_form("ICE")
                        in_menu = False
                        base_displayed, fire_displayed, ice_displayed, dark_displayed = False, False, False, False
                    if dark_displayed and SWORD_DARK.checkForInput(PLAY_MOUSE_POSITION):
                        self.player.access_sword().shift_form("DARK")
                        in_menu = False
                        base_displayed, fire_displayed, ice_displayed, dark_displayed = False, False, False, False
                    if back_displayed and BACK_BUTTON.checkForInput(PLAY_MOUSE_POSITION):
                        in_menu = False
            pygame.display.update()

    def item_menu(self):
        in_menu = True
        used_item = False
        while in_menu:
            PLAY_MOUSE_POSITION = pygame.mouse.get_pos()
            SCREEN.fill("black")

            item_buttons = []
            item_pointer = 0
            y_axis = 100
            for item in self.player.inventory:
                button_text = str(item_pointer) + ". " + item.get_name()
                # Button pressed for BASE sword form
                CURRENT_ITEM = Button(image=None, pos=(320, y_axis),
                                      text_input=button_text, font=WIN.get_font(75), base_color="#FFFFFF", hovering_color="#FFCC40")
                y_axis += 120
                item_displayed = False
                item_buttons.append([CURRENT_ITEM, item_displayed])
                item_pointer += 1

            BACK_BUTTON = Button(image=None, pos=(150, 650),
                                text_input="BACK", font=WIN.get_font(75), base_color="#FFFFFF", hovering_color="#FFCC40")
            back_displayed = False

            for i in range(len(item_buttons)):
                item_buttons[i][0].changeColor(PLAY_MOUSE_POSITION)
                item_buttons[i][0].update(SCREEN)
                item_buttons[i][1] = True
            BACK_BUTTON.changeColor(PLAY_MOUSE_POSITION)
            BACK_BUTTON.update(SCREEN)
            back_displayed = True

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    WIN.game_exit()
                if event.type == pygame.KEYDOWN:
                    # Escape Key
                    if event.key == pygame.K_ESCAPE:
                        WIN.game_exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for i in range(len(item_buttons)):
                        if item_buttons[i][1] and item_buttons[i][0].checkForInput(PLAY_MOUSE_POSITION):
                            selected_item = self.player.access_item(i)
                            selected_item.use_item()
                            used_item = True
                            in_menu = False
                    if back_displayed and BACK_BUTTON.checkForInput(PLAY_MOUSE_POSITION):
                        in_menu = False

            if not self.player.inventory:
                in_menu = False
            pygame.display.update()
        return used_item

    def player_turn(self):
        # TODO Put player attack in here probably? instead of in display code
        return 0

    def enemy_turn(self):
        damage_inflicted = self.player.get_stats()["DEF"] - self.mobs.get_stats()["ATK"]
        if damage_inflicted > 0:
            damage_inflicted = 0
        # self.player.hp_update(damage_inflicted)
        return damage_inflicted

    def display_hp(self, mob_hp_color):
        # Mob HP display
        mob_hp_text = WIN.get_font(30).render(str(self.mobs.get_stats()["HP"]) + "/" +
                                              str(self.mobs.get_stats()["HP Max"]), True, mob_hp_color)
        mob_hp_rect = mob_hp_text.get_rect(center=(640, 360))
        SCREEN.blit(mob_hp_text, mob_hp_rect)

        # Player HP display
        player_hp_text = WIN.get_font(30).render(str(self.player.get_stats()["HP"]) + "/" +
                                                 str(self.player.get_stats()["HP Max"]), True, "Green")
        player_hp_rect = mob_hp_text.get_rect(center=(30, 30))
        SCREEN.blit(player_hp_text, player_hp_rect)


