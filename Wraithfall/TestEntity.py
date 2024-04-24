import pygame, sys, os
import game_window as WIN
import entity_classes as ENTITY
from battle_menu import Battle, item_menu, sword_menu, item_display_overworld
import pygame.event as EVENTS

from overworld_functions import check_player_death, entity_collision

from cutscenes import play_scene, get_scene
from textbox import TextBox, SceneManager

pygame.init()
SCREEN = pygame.display.set_mode(WIN.window_size())
pygame.display.set_caption("debug: player actions")
clock = pygame.time.Clock()

# Sprite Groups
game_sprites = pygame.sprite.Group()
mob_sprites = pygame.sprite.Group()
mob_vision_sprites = pygame.sprite.Group()
item_sprites = pygame.sprite.Group()
sword_sprite = pygame.sprite.Group()
gui_sprites = pygame.sprite.Group()
sprite_groups = {"Game": game_sprites, "Mob": mob_sprites, "Mob Vision": mob_vision_sprites,
                 "Item": item_sprites, "Sword": sword_sprite, "GUI": gui_sprites}


def spawn_entity(new_entity, entity_type, spawn_xy=(None, None)):
    sprite_groups[entity_type].add(new_entity)
    game_sprites.add(new_entity)
    new_entity.warp(x=spawn_xy[0], y=spawn_xy[1])
    return new_entity


# Player Entity
player = ENTITY.Player()
player.warp(WIN.WIN_WIDTH/2, WIN.WIN_HEIGHT/2)
game_sprites.add(player)

# Mob Entities
for i in range(5):
    dummy_box = spawn_entity(ENTITY.BoundingBox(bound_box_size=(225, 225)), "Mob Vision")
    dummy_wraith = spawn_entity(ENTITY.Mob(), "Mob")
    dummy_box.set_entity(dummy_wraith)
    dummy_wraith.set_speed(0, 0)

# Sword Entity
sword = spawn_entity(ENTITY.Sword(), "Sword", spawn_xy=(WIN.WIN_WIDTH/2, WIN.WIN_HEIGHT/2 - 75))

# Item Entities
for i in range(5):
    healing_item = spawn_entity(ENTITY.Item(item_id=0), "Item")


test_entity_text_lines = [
    TextBox("Let's practice safety training, Oliver. Press [ENTER] to start.", "Grandpa", "Happy"),
]
combat_menu_text_lines = [
    TextBox("Careful, Oliver.", "Grandpa", "Neutral"),
]
test_entity_scene = SceneManager(test_entity_text_lines, "text_sound.wav")
combat_menu_scene = SceneManager(combat_menu_text_lines, "text_sound.wav")

# Game Loop
looping = True
combat_invul = False
invul_time = 0
playing_cutscene = True
first_battle = True
while looping:
    clock.tick(WIN.get_fps())
    # Input Events
    for event in EVENTS.get():
        if event.type == pygame.KEYDOWN:
            # Escape Key
            if event.key == pygame.K_ESCAPE:
                WIN.game_exit()
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
                    playing_cutscene = not test_entity_scene.next_textbox()

        # check click on window exit button
        if event.type == pygame.QUIT:
            WIN.game_exit()
    # Update game sprites
    if not playing_cutscene:
        game_sprites.update()

        combat_invul, invul_time = entity_collision(player, sprite_groups, combat_invul=combat_invul, invul_time=invul_time,
                                                    combat_cutscene=combat_menu_scene)

        """
        # Player and Mob collision
        player_mob_collide = pygame.sprite.spritecollide(player, mob_sprites, False)
        if not combat_invul and player_mob_collide:
            if first_battle:
                battle_scene = combat_menu_scene
                first_battle = False
            else:
                battle_scene = None
            combat = Battle(player, player_mob_collide[0], scene=battle_scene)
            remaining_mob = combat.combat_screen()
            if remaining_mob:
                # Run away was chosen
                combat_invul = True
                start_invul_time = pygame.time.get_ticks()
            else:
                # Defeated mob, so remove mob from map
                player_mob_collide[0].get_bb_anchor().kill()
                player_mob_collide[0].kill()
                combat_invul = True
                start_invul_time = pygame.time.get_ticks()
                # pygame.sprite.spritecollide(player, mob_sprites, True)
                # mob_sprites[0]

        if combat_invul:
            curr_time = pygame.time.get_ticks()
            if curr_time - start_invul_time >= 5000:
                combat_invul = False

        # Mob stops following Player if outside of detection bounding box
        for mob in mob_sprites:
            mob.set_target(None)

        # Checks if Player is in Mob's detection bounding box
        mob_detection_box = pygame.sprite.spritecollide(player, mob_vision_sprites, False)
        if mob_detection_box and not combat_invul:
            for mob in mob_detection_box:
                found_mob = mob.get_entity()
                if found_mob:
                    found_mob.set_target(player)

        # Player and Sword collision
        player_sword_collide = pygame.sprite.spritecollide(player, sword_sprite, False)
        if player_sword_collide:
            sword_ref = player_sword_collide[0]
            if sword_ref.verify() is None:
                # Player picks up the sword
                sword_ref.pickup(player)

        # Player and Item collision
        player_item_collide = pygame.sprite.spritecollide(player, item_sprites, False)
        if player_item_collide:
            item_ref = player_item_collide[0]
            if item_ref.verify() is None:
                # Player picks up item
                if item_ref.pickup(player):
                    remove_item = pygame.sprite.spritecollide(player, item_sprites, True)
        """

    check_player_death(player)

    SCREEN.fill("#000000")
    game_sprites.draw(SCREEN)
    # TODO GUI code here
    item_display_overworld(player, game_sprites, gui_sprites, SCREEN)
    gui_sprites.draw(SCREEN)

    playing_cutscene = play_scene(test_entity_scene, playing_cutscene)
    # print(playing_cutscene)
    # update the display window...
    pygame.display.update()

