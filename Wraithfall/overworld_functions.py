import pygame, sys, os
import game_window as WIN
import entity_classes as ENTITY
from battle_menu import Battle, item_menu, sword_menu, item_display_overworld
import pygame.event as EVENTS

from cutscenes import play_scene, get_scene
from textbox import TextBox, SceneManager

pygame.init()
SCREEN = pygame.display.set_mode(WIN.window_size())
pygame.display.set_caption("Code for Overworld")
clock = pygame.time.Clock()


# Sprite Groups
def setup_sprite_groups():
    game_sprites = pygame.sprite.Group()
    mob_sprites = pygame.sprite.Group()
    mob_vision_sprites = pygame.sprite.Group()
    npc_spites = pygame.sprite.Group()
    item_sprites = pygame.sprite.Group()
    sword_sprite = pygame.sprite.Group()
    gui_sprites = pygame.sprite.Group()
    sprite_groups = {"Game": game_sprites, "Mob": mob_sprites, "Mob Vision": mob_vision_sprites,
                     "Item": item_sprites, "Sword": sword_sprite, "GUI": gui_sprites,
                     "NPC": npc_spites}
    return sprite_groups


sprite_groups = setup_sprite_groups()

def get_sprite_groups():
    return sprite_groups


def spawn_entity(new_entity, entity_type, spawn_xy=(None, None), override_mob_vision=False):
    sprite_groups[entity_type].add(new_entity)
    sprite_groups["Game"].add(new_entity)
    if not override_mob_vision and entity_type == "Mob":
        dummy_box = spawn_entity(ENTITY.BoundingBox(bound_box_size=(225, 225)), "Mob Vision")
        dummy_box.set_entity(new_entity)
    new_entity.warp(x=spawn_xy[0], y=spawn_xy[1])
    return new_entity


def spawn_player(spawn_xy=(WIN.WIN_WIDTH/2, WIN.WIN_HEIGHT/2)):
    player = ENTITY.Player()
    sprite_groups["Game"].add(player)
    player.warp(x=spawn_xy[0], y=spawn_xy[1])
    return player


def check_player_death(player, is_dead=False):
    player_hp = player.get_stats()["HP"]
    death = False
    if player_hp <= 0 or is_dead:
        death = True
        # TODO remove debug code
        print("Player has died. How sad!")
        base_exp = player.get_exp(base_exp_of_lvl=True)
        print("Reverted EXP: " + str(player.set_exp(base_exp)))
        player.warp(x=WIN.WIN_WIDTH/2, y=WIN.WIN_HEIGHT/2)
    return death


def entity_collision(player, sprite_groups, combat_invul=False, invul_time=0, combat_cutscene=None):
    # Player and Mob collision
    player_mob_collide = pygame.sprite.spritecollide(player, sprite_groups["Mob"], False)
    if not combat_invul and player_mob_collide:
        if combat_cutscene.check_if_finished():
            battle_scene = None
        else:
            battle_scene = combat_cutscene
        combat = Battle(player, player_mob_collide[0], scene=battle_scene)
        remaining_mob = combat.combat_screen()
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