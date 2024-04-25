import pygame, sys, os
from game_window import random, math, get_font, window_size, WIN_WIDTH, WIN_HEIGHT, game_exit, \
    scale_to_screen as stsc, DIR_MUSIC
import entity_classes as ENTITY
from battle_menu import Battle, item_menu, sword_menu, item_display_overworld as item_display
import pygame.event as EVENTS
from audio_mixer import load_mixer, play_mixer, pause_mixer, unpause_mixer, stop_mixer

from cutscenes import play_scene, get_scene
from textbox import TextBox, SceneManager

pygame.init()
SCREEN = pygame.display.set_mode(window_size())
pygame.display.set_caption("Overworld Code")
clock = pygame.time.Clock()
# pygame.mixer.music.load(os.path.join(DIR_MUSIC, "backgroundmusic1.wav"))
# pygame.mixer.music.play(-1) #makes music continue to loop

""" Functions below are intended to be inserted BEFORE the Game Loop. """

# Sprite Groups
def setup_sprite_groups():
    """ Put before game loop and before trying to spawn any entities with spawn_entity (or spawn_player) """
    game_sprites = pygame.sprite.Group()  # All sprites
    mob_sprites = pygame.sprite.Group()  # Mob sprites
    mob_vision_sprites = pygame.sprite.Group()  # BoundingBoxes for mob vision
    npc_spites = pygame.sprite.Group()  # NPC sprites
    item_sprites = pygame.sprite.Group()  # Item sprites
    sword_sprite = pygame.sprite.Group()  # Sword sprite
    gui_sprites = pygame.sprite.Group()  # GUI sprites (items to be observed not touched)
    all_sprite_groups = {"Game": game_sprites, "Mob": mob_sprites, "Mob Vision": mob_vision_sprites,
                     "Item": item_sprites, "Sword": sword_sprite, "GUI": gui_sprites,
                     "NPC": npc_spites}
    return all_sprite_groups


sprite_groups = setup_sprite_groups()

def get_sprite_groups():
    """ Put into game loop to avoid issues with sprite_groups not updating. """
    return sprite_groups


def spawn_entity(new_entity, entity_type, spawn_xy=(None, None), override_mob_vision=False):
    """ Goes before the game loop. Assign to player="""
    sprite_groups[entity_type].add(new_entity)
    sprite_groups["Game"].add(new_entity)
    if not override_mob_vision and entity_type == "Mob":
        dummy_box = spawn_entity(ENTITY.BoundingBox(bound_box_size=(225, 225)), "Mob Vision")
        dummy_box.set_entity(new_entity)
    new_entity.warp(x=spawn_xy[0], y=spawn_xy[1])
    return new_entity


def spawn_player(spawn_xy=(WIN_WIDTH/2, WIN_HEIGHT/2)):
    """ Goes before the game loop. Assign to player="""
    player = ENTITY.Player()
    sprite_groups["Game"].add(player)
    player.warp(x=spawn_xy[0], y=spawn_xy[1])
    return player


""" Functions below are intended to be inserted INSIDE the Game Loop. """


def input_events(player, events, playing_cutscene=False, cutscene=None):
    # TODO don't use this will probably be deleted
    for event in events:
        if event.type == pygame.KEYDOWN:
            # Escape Key
            if event.key == pygame.K_ESCAPE:
                game_exit()
            if not playing_cutscene:
                # Overworld Controls

                # G key
                if event.key == pygame.K_g:
                    # Access Sword Menu
                    if player.access_sword() is not None:
                        sword_menu(player)
                # Q key
                if event.key == pygame.K_q:
                    player.scroll_inv(-1)
                    if player.inventory:
                        # TODO printing to terminal is temp, only for debugging purposes
                        print(str(player.inventory_pointer) + ": " + str(player.inventory[player.inventory_pointer].get_name()))
                # E key
                if event.key == pygame.K_e:
                    player.scroll_inv(1)
                    if player.inventory:
                        # TODO printing to terminal is temp, only for debugging purposes
                        print(str(player.inventory_pointer) + ": " + str(player.inventory[player.inventory_pointer].get_name()))
                # F key
                if event.key == pygame.K_f:
                    selected_item = player.access_item()
                    if selected_item is not None:
                        selected_item.use_item()
            else:
                # Cutscene Controls

                # Enter key
                if event.key == pygame.K_RETURN:
                    playing_cutscene = not cutscene.next_textbox()
        # check click on window exit button
        if event.type == pygame.QUIT:
            game_exit()


def item_display_overworld(player, game_sprite_group, gui_sprite_group):
    """ Goes into the game loop. Calls the function from battle_menu. """
    success = item_display(player, game_sprite_group, gui_sprite_group, SCREEN)
    return success


def check_player_death(player, is_dead=False):
    """ Goes into the game loop. """
    player_hp = player.get_stats()["HP"]
    death = False
    if player_hp <= 0 or is_dead:
        death = True
        # TODO remove debug code
        print("Player has died. How sad!")
        base_exp = player.get_exp(base_exp_of_lvl=True)
        print("Reverted EXP: " + str(player.set_exp(base_exp)))
        player.warp(x=WIN_WIDTH/2, y=WIN_HEIGHT/2)
    return death

music_pause = False

def entity_collision(player, sprite_groups, combat_invul=False, invul_time=0, combat_cutscene=None):
    """ Goes into the game loop. """
    # Player and Mob collision
    player_mob_collide = pygame.sprite.spritecollide(player, sprite_groups["Mob"], False)
    if not combat_invul and player_mob_collide:
        if combat_cutscene.check_if_finished():
            battle_scene = None
        else:
            battle_scene = combat_cutscene
        stop_mixer()
        combat = Battle(player, player_mob_collide[0], scene=battle_scene)
        remaining_mob = combat.combat_screen()
        load_mixer("backgroundmusic1.wav")
        play_mixer()
        if remaining_mob:
            # Run away was chosen
            combat_invul = True
            invul_time = pygame.time.get_ticks()
        else:
            # Defeated mob, so remove mob from map
            player_mob_collide[0].get_bb_anchor().kill()
            player_mob_collide[0].kill()
            combat_invul = True
            invul_time = pygame.time.get_ticks()
            # pygame.sprite.spritecollide(player, mob_sprites, True)
            # mob_sprites[0]
        # Recover HP at the end of combat
        # player.set_stats({"HP": player.get_stats()["HP Max"]})
        
        #pause music when entering battle
        # pygame.mixer.music.pause()
        music_paused = True

    if combat_invul:
        curr_time = pygame.time.get_ticks()
        if curr_time - invul_time >= 5000:
            combat_invul = False

    # Mob stops following Player if outside of detection bounding box
    for mob in sprite_groups["Mob"]:
        mob.set_target(None)

    # Checks if Player is in Mob's detection bounding box
    mob_detection_box = pygame.sprite.spritecollide(player, sprite_groups["Mob Vision"], False)
    if mob_detection_box and not combat_invul:
        for mob in mob_detection_box:
            found_mob = mob.get_entity()
            if found_mob:
                found_mob.set_target(player)

    # Player and Sword collision
    player_sword_collide = pygame.sprite.spritecollide(player, sprite_groups["Sword"], False)
    if player_sword_collide:
        sword_ref = player_sword_collide[0]
        if sword_ref.verify() is None:
            # Player picks up the sword
            sword_ref.pickup(player)

    # Player and Item collision
    player_item_collide = pygame.sprite.spritecollide(player, sprite_groups["Item"], False)
    if player_item_collide:
        item_ref = player_item_collide[0]
        if item_ref.verify() is None:
            # Player picks up item
            if item_ref.pickup(player):
                remove_item = pygame.sprite.spritecollide(player, sprite_groups["Item"], True)
    return combat_invul, invul_time



