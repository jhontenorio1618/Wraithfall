import pygame, sys, os
import game_window as WIN
import entity_classes as ENTITY
import battle_menu as BATTLE
from battle_menu import Battle
import pygame.event as EVENTS


pygame.init()
SCREEN = pygame.display.set_mode(WIN.window_size())
pygame.display.set_caption("debug: player actions")
clock = pygame.time.Clock()

# Sprite Groups
game_sprites = pygame.sprite.Group()
mob_sprites = pygame.sprite.Group()

# Player Entity
player = ENTITY.Player()
game_sprites.add(player)

# Mob Entities
for i in range(5):
    dummy_wraith = ENTITY.Mob()
    dummy_wraith.set_speed(0, 0)
    game_sprites.add(dummy_wraith)
    mob_sprites.add(dummy_wraith)

# Game Loop
looping = True
while looping:
    clock.tick(WIN.FPS)
    # Input Events
    for event in EVENTS.get():
        if event.type == pygame.KEYDOWN:
            # Escape Key
            if event.key == pygame.K_ESCAPE:
                WIN.game_exit()

        # check click on window exit button
        if event.type == pygame.QUIT:
            WIN.game_exit()
    # 'updating' the game
    # update all game sprites
    game_sprites.update()

    player_mob_collide = pygame.sprite.spritecollide(player, mob_sprites, False)
    if player_mob_collide:
        combat = Battle(player, player_mob_collide)
        remaining_mob = combat.combat_screen()
        if remaining_mob:
            # Run away was chosen
            # TODO make this invulnerability for a few seconds. changing position could lead to bugs
            player.warp(player.rect.x - 10, player.rect.y - 10)
        else:
            # Defeated mob,sso remove mob from map
            # TODO there could be bugs with this- find way to remove mob regardless of collision
            pygame.sprite.spritecollide(player, mob_sprites, True)


    # draw
    # 'rendering' to the window
    SCREEN.fill("#000000")
    game_sprites.draw(SCREEN)
    # update the display window...
    pygame.display.update()