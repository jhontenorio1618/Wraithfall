import pygame, sys, os
import game_window as WIN
import entity_classes as ENTITY
from battle_menu import Battle
import pygame.event as EVENTS


pygame.init()
SCREEN = pygame.display.set_mode(WIN.window_size())
pygame.display.set_caption("debug: player actions")
clock = pygame.time.Clock()

# Sprite Groups
game_sprites = pygame.sprite.Group()
mob_sprites = pygame.sprite.Group()
item_sprites = pygame.sprite.Group()
sword_sprite = pygame.sprite.Group()
sprite_groups = {"Game": game_sprites, "Mob": mob_sprites, "Item": item_sprites, "Sword": sword_sprite}


def spawn_entity(new_entity, entity_type, spawn_xy=(None, None)):
    # TODO figure out how to insert hyperparameters unique for an energy without being overabundant
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
    dummy_wraith = spawn_entity(ENTITY.Mob(), "Mob")
    dummy_wraith.set_speed(0, 0)

# Sword Entity
sword = spawn_entity(ENTITY.Sword(), "Sword", spawn_xy=(WIN.WIN_WIDTH/2, WIN.WIN_HEIGHT/2 - 75))

# Item Entities
for i in range(5):
    healing_item = spawn_entity(ENTITY.Item(item_id=0), "Item")

# TODO implement
bounding_box_test_sprites = pygame.sprite.Group()
box = ENTITY.BoundingBox()
game_sprites.add(box)
bounding_box_test_sprites.add(box)

# Game Loop
looping = True
combat_invul = False
while looping:
    clock.tick(WIN.FPS)
    # Input Events
    for event in EVENTS.get():
        if event.type == pygame.KEYDOWN:
            # Escape Key
            if event.key == pygame.K_ESCAPE:
                WIN.game_exit()
            # G key
            if event.key == pygame.K_g:
                # Access Sword Menu
                if player.access_sword() is not None:
                    access = Battle(player)
                    access.sword_menu()
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
        # check click on window exit button
        if event.type == pygame.QUIT:
            WIN.game_exit()
    # Update game sprites
    game_sprites.update()

    player_box_collide = pygame.sprite.spritecollide(player, bounding_box_test_sprites, False)
    if player_box_collide:
        player.warp(WIN.WIN_WIDTH, WIN.WIN_HEIGHT)

    # Player and Mob collision
    player_mob_collide = pygame.sprite.spritecollide(player, mob_sprites, False)
    if not combat_invul and player_mob_collide:
        combat = Battle(player, player_mob_collide)
        remaining_mob = combat.combat_screen()
        if remaining_mob:
            # Run away was chosen
            # TODO make this invulnerability for a few seconds. changing position could lead to bugs
            # player.warp(player.rect.x - 10, player.rect.y - 10)
            combat_invul = True
            start_invul_time = pygame.time.get_ticks()
        else:
            # Defeated mob, so remove mob from map
            pygame.sprite.spritecollide(player, mob_sprites, True)
        # Recover HP at the end of combat
        # player.set_stats({"HP": player.get_stats()["HP Max"]})

    if combat_invul:
        curr_time = pygame.time.get_ticks()
        if curr_time - start_invul_time >= 5000:
            combat_invul = False

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

    SCREEN.fill("#000000")
    game_sprites.draw(SCREEN)
    # update the display window...
    pygame.display.update()