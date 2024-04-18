import pygame, sys, os, game_window as WIN
from button import Button
import entity_classes as ENTITY


pygame.init()
SCREEN = pygame.display.set_mode(WIN.window_size())
pygame.display.set_caption("Battle")


def item_menu(player):
    in_menu = True
    selected_item = None
    while in_menu:
        PLAY_MOUSE_POSITION = pygame.mouse.get_pos()
        SCREEN.fill("black")

        item_buttons = []
        item_pointer = 0
        y_axis = 100
        for item in player.inventory:
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
                        selected_item = player.access_item(i)
                        # selected_item.use_item()
                        in_menu = False
                if back_displayed and BACK_BUTTON.checkForInput(PLAY_MOUSE_POSITION):
                    in_menu = False

        if not player.inventory:
            in_menu = False
        pygame.display.update()
    return selected_item


def sword_menu(player):
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
                    player.access_sword().shift_form("BASE")
                    in_menu = False
                    base_displayed, fire_displayed, ice_displayed, dark_displayed = False, False, False, False
                if fire_displayed and SWORD_FIRE.checkForInput(PLAY_MOUSE_POSITION):
                    player.access_sword().shift_form("FIRE")
                    in_menu = False
                    base_displayed, fire_displayed, ice_displayed, dark_displayed = False, False, False, False
                if ice_displayed and SWORD_ICE.checkForInput(PLAY_MOUSE_POSITION):
                    player.access_sword().shift_form("ICE")
                    in_menu = False
                    base_displayed, fire_displayed, ice_displayed, dark_displayed = False, False, False, False
                if dark_displayed and SWORD_DARK.checkForInput(PLAY_MOUSE_POSITION):
                    player.access_sword().shift_form("DARK")
                    in_menu = False
                    base_displayed, fire_displayed, ice_displayed, dark_displayed = False, False, False, False
                if back_displayed and BACK_BUTTON.checkForInput(PLAY_MOUSE_POSITION):
                    in_menu = False
        pygame.display.update()
    return player.access_sword().get_form()


class Battle:
    def __init__(self, player=ENTITY.Player(), mob=ENTITY.Mob()):
        self.player = player
        self.mob = mob
        self.player_chosen_action = 0
        self.selected_item = None
        self.in_combat = True
        self.mob_living = True
        self.player_living = True
        self.status_effects = {"Normal": 0, "Burning": 1, "Frozen": 2}
        self.mob_effect = 0
        self.player_effect = 0

    def combat_screen(self):
        open_sword_menu = False
        open_item_menu = False
        exp_gained = 0
        player_decided = False
        enemy_decided = False
        while self.in_combat:
            if open_sword_menu:
                # Pressed SWORD button
                sword_menu(self.player)
                open_sword_menu = False
            if open_item_menu:
                # Pressed ITEM button
                self.selected_item = item_menu(self.player)
                if self.selected_item:
                    self.player_chosen_action = 2
                    player_decided = True
                open_item_menu = False



            PLAY_MOUSE_POSITION = pygame.mouse.get_pos()
            SCREEN.fill("black")

            # Button pressed to "FIGHT"
            BATTLE_FIGHT = Button(image=None, pos=(320, 460),
                                  text_input="FIGHT", font=WIN.get_font(75), base_color="#FFFFFF", hovering_color="#A90505")
            fight_displayed = False
            # Button pressed to "RUN" # 960, 460
            BATTLE_RUN = Button(image=None, pos=(960, 580),
                                text_input="RUN", font=WIN.get_font(75), base_color="#FFFFFF", hovering_color="#A90505")
            run_displayed = False
            # Button pressed to exit combat menu after finishing the fight
            BATTLE_NEXT = Button(image=None, pos=(960, 460),
                                 text_input="NEXT", font=WIN.get_font(75), base_color="#FFFFFF", hovering_color="#A90505")
            next_displayed = False
            # Button pressed to access item menu # 320, 580
            BATTLE_ITEM = Button(image=None, pos=(960, 460),
                                  text_input="ITEM", font=WIN.get_font(75), base_color="#FFFFFF", hovering_color="#A90505")
            item_displayed = False
            # Button pressed to access sword menu # 960, 580
            BATTLE_SWORD = Button(image=None, pos=(320, 580),
                                 text_input="SWORD", font=WIN.get_font(75), base_color="#FFFFFF", hovering_color="#A90505")
            sword_displayed = False

            if self.mob_living:
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
                        self.in_combat = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if fight_displayed and BATTLE_FIGHT.checkForInput(PLAY_MOUSE_POSITION):
                        self.player_chosen_action = 1
                        player_decided = True
                    if item_displayed and BATTLE_ITEM.checkForInput(PLAY_MOUSE_POSITION):
                        # "ITEM" Button: open item menu to select an item to use
                        open_item_menu = True
                    if sword_displayed and BATTLE_SWORD.checkForInput(PLAY_MOUSE_POSITION):
                        # "SWORD" Button: open sword menu to change form of sword
                        self.player_chosen_action = 3
                        open_sword_menu = True
                    if run_displayed and BATTLE_RUN.checkForInput(PLAY_MOUSE_POSITION):
                        # "RUN" Button: flee from fight without killing the mobs
                        self.in_combat = self.run_state()
                    if next_displayed and BATTLE_NEXT.checkForInput(PLAY_MOUSE_POSITION):
                        # "NEXT" Button: click to leave combat after killing the mobs
                        self.in_combat = False

            if player_decided:
                # TODO Logic for enemy making move decision
                enemy_decided = True

            if player_decided and enemy_decided:
                player_speed = self.player.get_stats()["SPD"]
                mob_speed = self.mob.get_stats()["SPD"]
                if player_speed > mob_speed:
                    # Player is faster, so player goes first.
                    first_turn = self.player_turn
                    second_turn = self.enemy_turn
                elif player_speed < mob_speed:
                    # Mob is faster, so mob goes first.
                    first_turn = self.enemy_turn
                    second_turn = self.player_turn
                else:
                    # Speed is tied. Randomly decide who goes first this turn.
                    random_order = WIN.random.sample([self.player_turn, self.enemy_turn], 2)
                    first_turn = random_order[0]
                    second_turn = random_order[1]
                first_turn()
                # TODO check if participants are alive
                second_turn()
                # TODO check if participants are alive

                """ Process Decisions
                
                speed to determine who goes first? run these turns in methods maybe
                
                player accuracy check
                    self.mob.hp_update(CALCULATED DAMAGE DONE BY MOB)
                        check if mob should be alive. kill if not and do not run rest of code
                    if status effect should be inflicted, inflict it
                
                enemy accuracy check
                    if mob should be affected by status effect, affect it
                        check if mob should be alive. kill if not and do not run rest of code
                    self.player.hp_update(CALCULATED DAMAGE DONE BY MOB)"""

                player_decided = False
                enemy_decided = False

            pygame.display.update()
        return self.mob_living

    def run_state(self):
        # Clicked RUN Button
        # TODO calculate RUN % chance
        success = True
        return not success

    def player_turn(self):
        if self.player_chosen_action == 1:
            # "FIGHT" Button: attack the mob
            bonus_dmg = 0
            if self.player.access_sword() is not None:
                sword_form = self.player.access_sword().get_form()
                status_chance = WIN.random.randrange(100)
                if sword_form == "FIRE":
                    # Checks if Mob is already burning.
                    if self.mob_effect != 1:
                        print(status_chance)
                        if status_chance >= 0:
                            # 80% chance of working
                            self.mob_effect = 1
                            print("Mob is on fire.")
                if sword_form == "ICE":
                    # Checks if Mob is already frozen.
                    if self.mob_effect != 2:
                        print(status_chance)
                        if status_chance >= 25:
                            # 75% chance of working
                            self.mob_effect = 2
                            print("Mob is frozen.")
                if sword_form == "DARK":
                    bonus_dmg = WIN.math.ceil(self.player.get_stats()["ATK"] * .3)
                    print("Bonus Damage: " + str(bonus_dmg))
                    print("Mob has suffered more.")

            player_attack = self.player.get_stats()["ATK"] + bonus_dmg
            print("Total Attack: " + str(player_attack))
            damage_inflicted = self.mob.get_stats()["DEF"] - player_attack # self.player.get_stats()["ATK"] - bonus_dmg
            if damage_inflicted > 0:
                # If the damage inflicted was negative, the enemy's defense is too high.
                damage_inflicted = 0

            # Calculate Mob HP after damage
            self.mob.hp_update(damage_inflicted)
            if self.mob.get_stats()["HP"] <= 0:
                # Mob is dead
                self.mob_living = False
                # Player gains EXP from killing mob
                exp_gained = self.player.gain_exp(self.mob.drop_exp())
            else:
                # Enemy's turn to attack
                enemy_turn = True
        if self.player_chosen_action == 2:
            # TODO change so player items are always used first in combat
            self.selected_item.use_item()
            self.selected_item = None
        self.player_chosen_action = 0
        return 0

    def enemy_turn(self):
        # Enemy attacks
        status_chance = WIN.random.randrange(100)
        if not (self.mob_effect == 2 and status_chance >= 40):
            # 60% for Mob to be frozen and unable to move
            if self.mob_effect == 1:
                fire_dmg = WIN.math.ceil(self.mob.get_stats()["HP Max"] * 0.1)
                print("Burning Mob got burnt for " + str(fire_dmg))
                self.mob.hp_update(-fire_dmg)
            # Calculate Mob HP after damage

            if self.mob.get_stats()["HP"] <= 0:
                # Mob is dead
                self.mob_living = False
                # Player gains EXP from killing mob
                exp_gained = self.player.gain_exp(self.mob.drop_exp())
            else:
                damage_inflicted = self.player.get_stats()["DEF"] - self.mob.get_stats()["ATK"]
                if damage_inflicted > 0:
                    damage_inflicted = 0
                self.player.hp_update(damage_inflicted)
                if self.player.get_stats()["HP"] <= 0:
                    # Player is dead
                    self.in_combat = False
                    self.player_living = False
        else:
            print("Mob is FROZEN")
        return 0

    def display_hp(self, mob_hp_color):
        # Mob HP display
        mob_hp_text = WIN.get_font(30).render(str(self.mob.get_stats()["HP"]) + "/" +
                                              str(self.mob.get_stats()["HP Max"]), True, mob_hp_color)
        mob_hp_rect = mob_hp_text.get_rect(center=(640, 360))
        SCREEN.blit(mob_hp_text, mob_hp_rect)

        # Player HP display
        player_hp_text = WIN.get_font(30).render(str(self.player.get_stats()["HP"]) + "/" +
                                                 str(self.player.get_stats()["HP Max"]), True, "Green")
        player_hp_rect = mob_hp_text.get_rect(center=(30, 30))
        SCREEN.blit(player_hp_text, player_hp_rect)


