import pygame, sys, os, game_window as WIN
from button import Button
import entity_classes as ENTITY
from game_window import random, math, get_font, window_size, game_exit, scale_to_screen as stsc, DIR_SPRITES, DIR_IMAGES

from cutscenes import play_scene, get_scene
from textbox import TextBox, SceneManager
from view_spritesheets import collect_frames
from audio_mixer import load_mixer, play_mixer, pause_mixer, unpause_mixer, stop_mixer, unload_mixer

pygame.init()
SCREEN = pygame.display.set_mode(window_size())
pygame.display.set_caption("Battle")

def setup_button(coords, text, font_size=75, base_color="#FFFFFF", hovering_color="#A90505"):
    """ Uses parameters to create new button object.
        "display_button" is a boolean used for telling code to make button clickable or not.
            Can be ignored if unwanted."""
    NEW_BUTTON = Button(image=None, pos=stsc(coords),
                        text_input=text, font=get_font(stsc(font_size)),
                        base_color=base_color, hovering_color=hovering_color)
    display_button = False
    return NEW_BUTTON, display_button


def enable_button(button, PLAY_MOUSE_POSITION):
    """ Assures the button appears on screen and color changes when mouse touches it.
        Returns "True", which is intended to be used in combination with "display_button" in setup_button,
            but also assures that the button has been setup. """
    button.changeColor(PLAY_MOUSE_POSITION)
    button.update(SCREEN)
    display = True
    return display


def display_text(text, coords, font_size, font_color="White", align="left"):
    """ Displays given text at given coordinates with given size and color of font."""
    text_to_display = get_font(stsc(font_size)).render(text, True, font_color)
    if align == "center":
        text_rect = text_to_display.get_rect(center=stsc(coords))
    else:
        # Default to aligning left
        text_rect = text_to_display.get_rect(topleft=stsc(coords))
    SCREEN.blit(text_to_display, text_rect)


def draw_rect(coords, size, fill=False, border=True, fill_color="#313131", border_color="White", border_size=2):
    # Set the Rectangles
    if fill:
        body_rect = pygame.Rect(stsc(coords), stsc(size))
        pygame.draw.rect(SCREEN, fill_color, body_rect)
    if border:
        border_rect = pygame.Rect(stsc(coords), stsc(size))
        pygame.draw.rect(SCREEN, border_color, border_rect, stsc(border_size))

    """if border_size is None:
        pygame.draw.rect(SCREEN, fill_color, body_rect)
    else:
        pygame.draw.rect(SCREEN, fill_color, body_rect, stsc(border_size))"""


def item_display_overworld(player, game_sprite_group, gui_sprite_group):
    success = False
    if player.check_inventory():
        # Only display if the player has items in their inventory

        # White outline for box
        draw_rect(coords=(40, 525), size=(150, 150), fill=False, fill_color=(49, 49, 49, 128))
        # Used for transparent effect of box
        s = pygame.Surface((150, 150), pygame.SRCALPHA)
        s.fill((49, 49, 49, 128))  # "#313131" with transparency
        SCREEN.blit(s, (40, 525))

        # Indicates button player should press to use items
        display_text(text="[ F ]", coords=(115, 648), font_size=16, font_color="White", align="center")
        current_item = player.access_item()
        if len(player.inventory) > 1:
            # Display only if player has multiple items
            inv_position = player.inventory.index(current_item) + 1
            inv_text = str(inv_position) + "/" + str(len(player.inventory))
            # Print inventory position out of total in inventory
            display_text(text=inv_text, coords=(115, 537), font_size=12, font_color="White", align="center")
            # Show commands for navigating inventory
            display_text(text="<- Q", coords=(44, 532), font_size=16, font_color="White")
            display_text(text="E ->", coords=(154, 532), font_size=16, font_color="White")
        if current_item.found_player is not None:
            item_name = current_item.get_name()
            for item in gui_sprite_group:
                # Stops any sprite overlapping
                item.kill()
            # Print item name
            display_text(text=item_name, coords=(115, 626), font_size=16, font_color="White", align="center")
            # Assure current_item is in proper sprite groups
            if current_item not in gui_sprite_group:
                gui_sprite_group.add(current_item)
            if current_item not in game_sprite_group:
                game_sprite_group.add(current_item)
            # Display item appearance (coords are center of item)
            current_item.warp(x=stsc(115), y=stsc(590))
        else:
            # Stop Item from appearing in GUI by killing it
            if current_item in gui_sprite_group:
                current_item.kill()
        success = True
    else:
        for item in gui_sprite_group:
            item.kill()
    return success


def item_menu(player, bg="black"):
    in_menu = True
    selected_item = None
    while in_menu:
        PLAY_MOUSE_POSITION = pygame.mouse.get_pos()
        SCREEN.fill(bg)

        draw_rect(coords=(100, 50), size=(1080, 500))
        s = pygame.Surface((1080, 500), pygame.SRCALPHA)
        s.fill((49, 49, 49, 128))  # "#313131" with transparency
        SCREEN.blit(s, (100, 50))

        draw_rect(coords=(530, 575), size=(220, 100))
        s = pygame.Surface((220, 100), pygame.SRCALPHA)
        s.fill((49, 49, 49, 128))  # "#313131" with transparency
        SCREEN.blit(s, (530, 575))

        item_buttons = []
        item_pointer = 1
        x_axis = 370
        y_axis = 130
        for item in player.inventory:
            button_text = str(item_pointer) + ". " + item.get_name()
            # Button pressed for BASE sword form
            CURRENT_ITEM, item_displayed = setup_button(coords=(x_axis, y_axis), text=button_text, font_size=52)
            # item_displayed = False
            item_buttons.append([CURRENT_ITEM, item_displayed])
            y_axis += 75
            item_pointer += 1
            if item_pointer % 5 == 1:
                y_axis = 130
                x_axis += 520

        BACK_BUTTON, back_displayed = setup_button(coords=(645, 620), text="BACK", font_size=52)
        # back_displayed = False

        for i in range(len(item_buttons)):
            item_buttons[i][1] = enable_button(item_buttons[i][0], PLAY_MOUSE_POSITION)
        back_displayed = enable_button(BACK_BUTTON, PLAY_MOUSE_POSITION)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit()
            if event.type == pygame.KEYDOWN:
                # Escape Key
                if event.key == pygame.K_ESCAPE:
                    game_exit()
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

        draw_rect(coords=(100, 50), size=(1080, 500))
        s = pygame.Surface((1080, 500), pygame.SRCALPHA)
        s.fill((49, 49, 49, 128))  # "#313131" with transparency
        SCREEN.blit(s, (100, 50))

        draw_rect(coords=(530, 575), size=(220, 100))
        s = pygame.Surface((220, 100), pygame.SRCALPHA)
        s.fill((49, 49, 49, 128))  # "#313131" with transparency
        SCREEN.blit(s, (530, 575))

        # Button pressed for BASE sword form
        SWORD_BASE, base_displayed = setup_button(coords=(345, 180), text="BASE", font_size=80, hovering_color="#FFCC40")
        # Button pressed for FIRE sword form
        SWORD_FIRE, fire_displayed = setup_button(coords=(327, 420), text="FIRE", font_size=80,hovering_color="#FF0000")
        # Button pressed for ICE sword form
        SWORD_ICE, ice_displayed = setup_button(coords=(976, 180), text="ICE", font_size=80,hovering_color="#0000FF")
        # Button pressed for DARK sword form
        SWORD_DARK, dark_displayed = setup_button(coords=(926, 420), text="DARK", font_size=80,hovering_color="#FF00FF")
        # Button pressed to exit Sword menu without making a selection
        BACK_BUTTON, back_displayed = setup_button(coords=(645, 620), text="BACK", font_size=52)

        base_displayed = enable_button(SWORD_BASE, PLAY_MOUSE_POSITION)
        fire_displayed = enable_button(SWORD_FIRE, PLAY_MOUSE_POSITION)
        ice_displayed = enable_button(SWORD_ICE, PLAY_MOUSE_POSITION)
        dark_displayed = enable_button(SWORD_DARK, PLAY_MOUSE_POSITION)
        back_displayed = enable_button(BACK_BUTTON, PLAY_MOUSE_POSITION)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit()
            if event.type == pygame.KEYDOWN:
                # Escape Key
                if event.key == pygame.K_ESCAPE:
                    game_exit()
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
    def __init__(self, player=ENTITY.Player(), mob=ENTITY.Mob(), bg="black", scene=None):
        self.player = player
        self.mob = mob
        self.background_color = bg
        self.player_chosen_action = 0
        self.selected_item = None
        self.in_combat = True
        self.mob_living = True
        self.player_living = True
        self.status_effects = {"Normal": 0, "Burning": 1, "Frozen": 2}
        self.mob_effect = 0
        self.player_effect = 0
        if scene is not None:
            self.playing_cutscene = True
        else:
            self.playing_cutscene = False
        self.scene = scene

    def combat_screen(self):
        open_sword_menu = False
        open_item_menu = False
        current_exp, goal_exp = self.player.get_exp(for_next_lvl=True)
        exp_gained = 0
        player_decided = False
        enemy_decided = False
        loot_id = 1
        # Load music
        load_mixer("battlemusic.wav")
        play_mixer(-1)
        animation_sprite_group = pygame.sprite.Group()
        battle_anim = BattleAnimation()
        if self.player.access_sword() is not None:
            battle_anim.shift_form(self.player.access_sword().get_form())
        battle_anim.move()
        animation_sprite_group.add(battle_anim)

        # Load background image
        background_image = pygame.image.load(os.path.join(DIR_IMAGES, "BATTLEBG.png")).convert_alpha()
        scaled_background_image = pygame.transform.scale(background_image, (1280, 720))
        
        #Load mob image  # Load mob image
        mob_image = pygame.image.load(os.path.join(DIR_SPRITES, "WRAITHSINGLEFRAME.png")).convert_alpha()
        mob_image = pygame.transform.scale(mob_image, (200, 200))  # Adjust size as needed


        while self.in_combat:
            if open_sword_menu:
                # Pressed SWORD button
                sword_form = sword_menu(self.player)
                battle_anim.shift_form(sword_form)
                open_sword_menu = False
            if open_item_menu:
                # Pressed ITEM button
                self.selected_item = item_menu(self.player, bg=self.background_color)
                if self.selected_item:
                    self.player_chosen_action = 2
                    player_decided = True
                open_item_menu = False

            PLAY_MOUSE_POSITION = pygame.mouse.get_pos()

            # Blit background image
            SCREEN.blit(scaled_background_image, (0, 0))

            animation_sprite_group.draw(SCREEN)

            # Button pressed to attack the mob
            BATTLE_FIGHT, fight_displayed = setup_button(coords=(360, 533), text="FIGHT")
            # Button pressed to access item menu
            if self.player.check_inventory():
                item_base_color, item_hover_color = "#FFFFFF", "#A90505"
            else:
                item_base_color, item_hover_color = "#636363", "#636363"
            BATTLE_ITEM, item_displayed = setup_button(coords=(960, 533), text="ITEM",
                                                       base_color=item_base_color, hovering_color=item_hover_color)
            # Button pressed to escape combat
            BATTLE_RUN, run_displayed = setup_button(coords=(960, 633), text="RUN")
            # Button pressed to access sword menu
            if self.player.access_sword() is not None:
                sword_base_color, sword_hover_color = "#FFFFFF", "#A90505"
            else:
                sword_base_color, sword_hover_color = "#636363", "#636363"
            BATTLE_SWORD, sword_displayed = setup_button(coords=(360, 633), text="SWORD",
                                                         base_color=sword_base_color, hovering_color=sword_hover_color)
            # After combat is finished, button pressed to exit combat menu # 960, 583
            BATTLE_NEXT, next_displayed = setup_button(coords=(640, 540), text="NEXT")

            # Mob Data Box
            mob_border_status = {0: "White", 1: "Red", 2: "Blue"}
            draw_rect(coords=(75, 50), size=(500, 150), fill=False,
                      border_color=mob_border_status[self.mob_effect], border_size=2)
            s = pygame.Surface((500, 150), pygame.SRCALPHA)
            s.fill((49, 49, 49, 128))  # "#313131" with transparency
            SCREEN.blit(s, (75, 50))
            self.draw_status_bar(coords=(115, 135), size=(420, 30),
                                 curr_val=self.mob.get_stats()["HP"], max_val=self.mob.get_stats()["HP Max"])
            display_text(text=self.mob.get_name(), coords=(95, 63), font_size=40, font_color="White")

            #Blit mob image unnderneath mobs status bar
            SCREEN.blit(mob_image,(250,200))
            
            # Player Data Box
            player_stats = self.player.get_stats()
            draw_rect(coords=(705, 275), size=(500, 150), fill=False, border_size=2)
            s = pygame.Surface((500, 150), pygame.SRCALPHA)
            s.fill((49, 49, 49, 128))  # "#313131" with transparency
            SCREEN.blit(s, (705, 275))
            self.draw_status_bar(coords=(745, 360), size=(420, 30),
                                 curr_val=player_stats["HP"], max_val=player_stats["HP Max"])
            player_hp_text = str(player_stats["HP"]) + "/" + str(player_stats["HP Max"])
            display_text(text=player_hp_text, coords=(1160, 395), font_size=20, font_color="White")
            atk_display = "ATK: " + str(player_stats["ATK"])
            def_display = "DEF: " + str(player_stats["DEF"])
            spd_display = "SPD: " + str(player_stats["SPD"])
            player_stat_list = atk_display + "  " + def_display + "  " + spd_display
            display_text(text=player_stat_list, coords=(745, 330), font_size=20, font_color="White")

            display_text(text=self.player.get_name(), coords=(1060, 288), font_size=40, font_color="White")
            if self.player.access_sword() is not None:
                sword_form_key = {"BASE": "#FFCC40", "FIRE": "#FF0000", "ICE": "#0000FF", "DARK": "#FF00FF"}
                sword_color = sword_form_key[self.player.access_sword().get_form()]
                draw_rect(coords=(720, 288), size=(20, 20),
                          fill=True, fill_color=sword_color, border_size=1)

            if not self.playing_cutscene:
                # Command Box
                draw_rect(coords=(20, 480), size=(1240, 220), fill=False, border_size=2)
                s = pygame.Surface((1240, 220), pygame.SRCALPHA)
                s.fill((49, 49, 49, 128))  # "#313131" with transparency
                SCREEN.blit(s, (20, 480))
                if self.mob_living and self.player_living:
                    # Mob remains alive
                    # TODO Put visuals for mobs here
                    # The battle is ongoing. Show FIGHT, RUN, ITEM buttons
                    fight_displayed = enable_button(BATTLE_FIGHT, PLAY_MOUSE_POSITION)
                    item_displayed = enable_button(BATTLE_ITEM, PLAY_MOUSE_POSITION)
                    sword_displayed = enable_button(BATTLE_SWORD, PLAY_MOUSE_POSITION)
                    run_displayed = enable_button(BATTLE_RUN, PLAY_MOUSE_POSITION)
                else:
                    # Mob is dead
                    stop_mixer()
                    unload_mixer()
                    # Essence for Sword is dropped
                    possible_loot_ids = [1, 2, 3]
                    loot_id = random.choice(possible_loot_ids)
                    # Display exit button that appears as "NEXT"
                    next_displayed = enable_button(BATTLE_NEXT, PLAY_MOUSE_POSITION)
                    new_exp = current_exp + exp_gained
                    self.draw_status_bar(coords=(430, 610), size=(420, 30),
                                         curr_val=new_exp, max_val=goal_exp, type="EXP")
            else:
                self.playing_cutscene = play_scene(self.scene, self.playing_cutscene)

            # self.display_hp(entity=self.player, coords=(30, 30), font_size=30)
            # self.display_hp(entity=self.mob, coords=(640, 360), font_size=30)

            # Determine what happens for each event
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        # Escape Key
                        game_exit()
                    if next_displayed and event.key == pygame.K_SPACE:
                        # "NEXT" Button Shortcut
                        self.in_combat = False
                    if self.playing_cutscene and event.key == pygame.K_RETURN:
                        self.playing_cutscene = not self.scene.next_textbox()

                if not self.playing_cutscene and event.type == pygame.MOUSEBUTTONDOWN:
                    if fight_displayed and BATTLE_FIGHT.checkForInput(PLAY_MOUSE_POSITION):
                        # "FIGHT" Button: attack the mob
                        self.player_chosen_action = 1
                        player_decided = True
                    if item_displayed and BATTLE_ITEM.checkForInput(PLAY_MOUSE_POSITION) \
                            and self.player.check_inventory():
                        # "ITEM" Button: open item menu to select an item to use
                        open_item_menu = True
                    if sword_displayed and BATTLE_SWORD.checkForInput(PLAY_MOUSE_POSITION) \
                            and self.player.access_sword() is not None:
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
                        random_order = random.sample([self.player_turn, self.enemy_turn], 2)
                        first_turn = random_order[0]
                        second_turn = random_order[1]
                first_turn()
                # TODO check if participants are alive
                second_turn()
                # TODO check if participants are alive
                if self.player_living and not self.mob_living:
                    # Player gains EXP for killing Mob
                    exp_gained = self.mob.drop_exp()
                    self.player.gain_exp(exp_gained)

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


            animation_sprite_group.update()
            pygame.display.update()

        return self.mob_living, loot_id

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
                status_chance = random.randrange(100)
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
                    bonus_dmg = math.ceil(self.player.get_stats()["ATK"] * .3)
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
            # self.selected_item = None
        self.player_chosen_action = 0
        return 0

    def enemy_turn(self):
        # Enemy attacks
        status_chance = random.randrange(100)
        if not (self.mob_effect == 2 and status_chance >= 40):
            # 60% for Mob to be frozen and unable to move
            if self.mob_effect == 1:
                fire_dmg = math.ceil(self.mob.get_stats()["HP Max"] * 0.1)
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

    def draw_status_bar(self, coords, size, curr_val, max_val, type="HP"):
        # defaults for status bar dimension
        BAR_WIDTH, BAR_HEIGHT = stsc(size)
        x_coord, y_coord = stsc(coords)
        if curr_val < 0:
            curr_val = 0
        elif curr_val >= max_val:
            curr_val = max_val
        bar_fill = (curr_val / max_val) * BAR_WIDTH
        bar_rect = pygame.Rect(x_coord, y_coord, BAR_WIDTH, BAR_HEIGHT)
        fill_rect = pygame.Rect(x_coord, y_coord, bar_fill, BAR_HEIGHT)
        pygame.draw.rect(SCREEN, "Black", bar_rect)
        border_color = "White"
        if type == "HP":
            if bar_fill <= BAR_WIDTH/2:
                pygame.draw.rect(SCREEN, "Yellow", fill_rect)
            elif bar_fill <= BAR_WIDTH/5:
                pygame.draw.rect(SCREEN, "Red", fill_rect)
            else:
                pygame.draw.rect(SCREEN, "Green", fill_rect)
        elif type == "EXP":
            if curr_val >= max_val:
                border_color = "#FFCC40"
            pygame.draw.rect(SCREEN, "#80e4ff", fill_rect)
        pygame.draw.rect(SCREEN, border_color, bar_rect, 3)

    def display_hp(self, entity, coords, font_size):
        # TODO old code. likely can delete
        current_hp = entity.get_stats()["HP"]
        max_hp = entity.get_stats()["HP Max"]
        hp_text_color = "Green"
        if current_hp <= 0:
            hp_text_color = "Red"
        hp_text = str(current_hp) + "/" + str(max_hp)
        display_text(text=hp_text, font_size=font_size, font_color=hp_text_color, coords=coords)
        return current_hp



class BattleAnimation(pygame.sprite.Sprite):
    def __init__(self, id=0):
        """ id = 0 for Player animations.
            id = 1 for Mob animations. """
        pygame.sprite.Sprite.__init__(self)
        self.images = {'forward': [0, 1, 2, 3, 4, 5], 'backward': [0, 1, 2, 3, 4, 5]}
        self.current_frame = 0
        self.animation_speed = 0.13
        self.last_update = pygame.time.get_ticks()
        self.load_spritesheets("BATTLESWORDspritesheet.png")
        self.direction = 'forward'
        self.image = self.images['forward'][self.current_frame]
        self.rect = self.image.get_rect()

    def load_spritesheets(self, sprite_sheet):
        battlesword_sheet = pygame.image.load(os.path.join(DIR_SPRITES, sprite_sheet)).convert_alpha()
        frame_width = 110
        frame_height = 120
        scale = stsc(6)

        # Load all frames for each direction
        all_frames = collect_frames(battlesword_sheet, 6, frame_width, frame_height, scale)

        # Splits the frames into forward, backward, right, and left directions
        self.images['forward'] = all_frames[:5]
        #self.images['backward'] = all_frames[8:]
        #self.images['right'] = all_frames[:7]
        #self.images['left'] = [pygame.transform.flip(frame, True, False) for frame in self.images['right']]

    def update(self):
        now = pygame.time.get_ticks()
        animation_interval = 250  # Constant factor for animation speed
        if now - self.last_update > animation_interval:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.images[self.direction])
            self.image = self.images[self.direction][self.current_frame]

    def move(self, x=WIN.WIN_WIDTH/2+100, y=WIN.WIN_HEIGHT/2):

        """ Move bounding box to given coordinates. Used for spawning and moving position on map.
        Returns the new coordinates of the bounding box. """
        self.rect.centerx = x
        self.rect.centery = y
        return x, y

    def shift_form(self, form):
        """ Given a string of a specified form, changes the sword to that form.
        Used in combination of the SWORD menu. """
        # TODO should change aspects of the sword here. For now, it's only visual
        if form == "BASE":
            self.load_spritesheets("BATTLESWORDspritesheet.png")
            # self.image.fill("#FFCC40")
        if form == "FIRE":
            self.load_spritesheets("FIREBATTLEspritesheet.png")
            # self.image.fill("#FF0000")
        if form == "ICE":
            self.load_spritesheets("ICEBATTLEspritesheet.png")
            # self.image.fill("#0000FF")
        if form == "DARK":
            self.load_spritesheets("DARKBATTLEspritesheet.png")
            # self.image.fill("#FF00FF")
        return form





