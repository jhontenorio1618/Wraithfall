import pygame, sys, os, game_window as WIN
from button import Button
import entity_classes as ENTITY


pygame.init()
SCREEN = pygame.display.set_mode(WIN.window_size())
pygame.display.set_caption("Battle")


def setup_button(coords, text, font_size=75, base_color="#FFFFFF", hovering_color="#A90505"):
    NEW_BUTTON = Button(image=None, pos=coords,
                        text_input=text, font=WIN.get_font(font_size),
                        base_color=base_color, hovering_color=hovering_color)
    return NEW_BUTTON


def enable_button(button, PLAY_MOUSE_POSITION):
    button.changeColor(PLAY_MOUSE_POSITION)
    button.update(SCREEN)
    display = True
    return display


def display_text(text, coords, font_size, font_color):
    text_to_display = WIN.get_font(font_size).render(text, True, font_color)
    text_rect = text_to_display.get_rect(center=coords)
    SCREEN.blit(text_to_display, text_rect)


def item_menu(player):
    in_menu = True
    selected_item = None
    while in_menu:
        PLAY_MOUSE_POSITION = pygame.mouse.get_pos()
        SCREEN.fill("black")

        item_buttons = []
        item_pointer = 1
        y_axis = 100
        for item in player.inventory:
            button_text = str(item_pointer) + ". " + item.get_name()
            # Button pressed for BASE sword form
            CURRENT_ITEM = setup_button(coords=(320, y_axis), text=button_text)
            item_displayed = False
            item_buttons.append([CURRENT_ITEM, item_displayed])
            y_axis += 120
            item_pointer += 1
        BACK_BUTTON = setup_button(coords=(150, 650), text="BACK")
        back_displayed = False

        for i in range(len(item_buttons)):
            item_buttons[i][1] = enable_button(item_buttons[i][0], PLAY_MOUSE_POSITION)
        back_displayed = enable_button(BACK_BUTTON, PLAY_MOUSE_POSITION)

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
        SWORD_BASE = setup_button(coords=(320, 220), text="BASE", hovering_color="#FFCC40")
        base_displayed = False
        # Button pressed for FIRE sword form
        SWORD_FIRE = setup_button(coords=(320, 340), text="FIRE", hovering_color="#FF0000")
        fire_displayed = False
        # Button pressed for ICE sword form
        SWORD_ICE = setup_button(coords=(320, 460), text="ICE", hovering_color="#0000FF")
        ice_displayed = False
        # Button pressed for DARK sword form
        SWORD_DARK = setup_button(coords=(320, 580), text="DARK", hovering_color="#FF00FF")
        dark_displayed = False
        BACK_BUTTON = setup_button(coords=(150, 650), text="BACK")
        back_displayed = False

        base_displayed = enable_button(SWORD_BASE, PLAY_MOUSE_POSITION)
        fire_displayed = enable_button(SWORD_FIRE, PLAY_MOUSE_POSITION)
        ice_displayed = enable_button(SWORD_ICE, PLAY_MOUSE_POSITION)
        dark_displayed = enable_button(SWORD_DARK, PLAY_MOUSE_POSITION)
        back_displayed = enable_button(BACK_BUTTON, PLAY_MOUSE_POSITION)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                WIN.game_exit()
            if event.type == pygame.KEYDOWN:
                # Escape Key
                if event.key == pygame.K_ESCAPE:
                    WIN.game_exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if base_displayed and SWORD_BASE.checkForInput(PLAY_MOUSE_POSITION):
                    # Base Sword form selected
                    player.access_sword().shift_form("BASE")
                    in_menu = False
                    base_displayed, fire_displayed, ice_displayed, dark_displayed = False, False, False, False
                if fire_displayed and SWORD_FIRE.checkForInput(PLAY_MOUSE_POSITION):
                    # Fire Sword form selected
                    player.access_sword().shift_form("FIRE")
                    in_menu = False
                    base_displayed, fire_displayed, ice_displayed, dark_displayed = False, False, False, False
                if ice_displayed and SWORD_ICE.checkForInput(PLAY_MOUSE_POSITION):
                    # Ice Sword form selected
                    player.access_sword().shift_form("ICE")
                    in_menu = False
                    base_displayed, fire_displayed, ice_displayed, dark_displayed = False, False, False, False
                if dark_displayed and SWORD_DARK.checkForInput(PLAY_MOUSE_POSITION):
                    # Dark Sword form selected
                    player.access_sword().shift_form("DARK")
                    in_menu = False
                    base_displayed, fire_displayed, ice_displayed, dark_displayed = False, False, False, False
                if back_displayed and BACK_BUTTON.checkForInput(PLAY_MOUSE_POSITION):
                    # Back button selected
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

            # Button pressed to attack the mob
            BATTLE_FIGHT = setup_button(coords=(320, 460), text="FIGHT")
            fight_displayed = False
            # Button pressed to access item menu
            BATTLE_ITEM = setup_button(coords=(960, 460), text="ITEM")
            item_displayed = False
            # Button pressed to escape combat
            BATTLE_RUN = setup_button(coords=(960, 580), text="RUN")
            run_displayed = False
            # Button pressed to access sword menu
            BATTLE_SWORD = setup_button(coords=(320, 580), text="SWORD")
            sword_displayed = False
            # After combat is finished, button pressed to exit combat menu
            BATTLE_NEXT = setup_button(coords=(960, 460), text="NEXT")
            next_displayed = False

            if self.mob_living:
                # Mob remains alive
                # TODO Put visuals for mobs here
                display_text(text="This is where the magic will happen.",
                             coords=(640, 260), font_size=45, font_color="White")
                # The battle is ongoing. Show FIGHT, RUN, and ITEM buttons
                fight_displayed = enable_button(BATTLE_FIGHT, PLAY_MOUSE_POSITION)
                run_displayed = enable_button(BATTLE_RUN, PLAY_MOUSE_POSITION)
                item_displayed = enable_button(BATTLE_ITEM, PLAY_MOUSE_POSITION)
                if self.player.access_sword() is not None:
                    # Player has SWORD, so show SWORD button
                    sword_displayed = enable_button(BATTLE_SWORD, PLAY_MOUSE_POSITION)
            else:
                # Mob is dead
                display_text(text="The wraith is dead. :)",
                             coords=(640, 260), font_size=45, font_color="Red", )
                # Display exit button that appears as "NEXT"
                next_displayed = enable_button(BATTLE_NEXT, PLAY_MOUSE_POSITION)

            self.display_hp(entity=self.player, coords=(30, 30))
            self.display_hp(entity=self.mob, coords=(640, 360))

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
                        # "FIGHT" Button: attack the mob
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
                # Calculate the outcomes of the Player and Enemy attacks
                if self.player_chosen_action == 2:
                    # Player ALWAYS goes first if using item
                    first_turn = self.player_turn
                    second_turn = self.enemy_turn
                else:
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
                if self.player_living and not self.mob_living:
                    # Player gains EXP for killing Mob
                    exp_gained = self.player.gain_exp(self.mob.drop_exp())

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
            else:
                # Enemy's turn to attack
                enemy_turn = True
        elif self.player_chosen_action == 2:
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

    def display_hp(self, entity, coords):
        current_hp = entity.get_stats()["HP"]
        max_hp = entity.get_stats()["HP Max"]
        hp_text_color = "Green"
        if current_hp <= 0:
            hp_text_color = "Red"
        hp_text = str(current_hp) + "/" + str(max_hp)
        display_text(text=hp_text, font_size=30, font_color=hp_text_color, coords=coords)
        return current_hp



