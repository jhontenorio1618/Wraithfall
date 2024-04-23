import pygame, sys, os
import game_window as WIN
import entity_classes as ENTITY
from battle_menu import Battle, item_menu, sword_menu
import pygame.event as EVENTS
import pytmx
from pytmx.util_pygame import load_pygame


pygame.init()
SCREEN = pygame.display.set_mode(WIN.window_size())
pygame.display.set_caption("Wraithfall")
clock = pygame.time.Clock()

def load_map(filename):

    tm = load_pygame("Game_map/game_map/Main_Map.tmx")
    return tm

def draw_map(screen, tiled_map):

    for layer in tiled_map.visible_layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            for x, y, gid in layer:
                tile = tiled_map.get_tile_image_by_gid(gid)
                if tile:
                    screen.blit(tile, (x * tiled_map.tilewidth, y * tiled_map.tileheight))
        elif isinstance(layer, pytmx.TiledObjectGroup):
            for obj in layer:
                if obj.image:
                    scale_factor = 0.45  # size for objects
                    scaled_img = pygame.transform.scale(obj.image, (int(obj.width * scale_factor), int(obj.height * scale_factor)))
                    screen.blit(scaled_img, (obj.x, obj.y))
def spawn_entity(new_entity, entity_type, spawn_xy=(None, None)):

    sprite_groups[entity_type].add(new_entity)
    game_sprites.add(new_entity)
    new_entity.warp(x=spawn_xy[0], y=spawn_xy[1])
    return new_entity


tiled_map = load_map('Game_map/game_map/Main_Map.tmx')


game_sprites = pygame.sprite.Group()
mob_sprites = pygame.sprite.Group()
mob_vision_sprites = pygame.sprite.Group()
item_sprites = pygame.sprite.Group()
sword_sprite = pygame.sprite.Group()
sprite_groups = {
    "Game": game_sprites,
    "Mob": mob_sprites,
    "Mob Vision": mob_vision_sprites,
    "Item": item_sprites,
    "Sword": sword_sprite
}


player = ENTITY.Player()
player.warp(WIN.WIN_WIDTH/2, WIN.WIN_HEIGHT/2)
game_sprites.add(player)


looping = True
while looping:
    clock.tick(WIN.get_fps())

    for event in EVENTS.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                WIN.game_exit()
            # Player movement keys
            if event.key == pygame.K_LEFT:
                player.speed_x = -5
            elif event.key == pygame.K_RIGHT:
                player.speed_x = 5
            elif event.key == pygame.K_UP:
                player.speed_y = -5
            elif event.key == pygame.K_DOWN:
                player.speed_y = 5

        elif event.type == pygame.KEYUP:

            if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                player.speed_x = 0
            if event.key in [pygame.K_UP, pygame.K_DOWN]:
                player.speed_y = 0

        elif event.type == pygame.QUIT:
            WIN.game_exit()


    game_sprites.update()

    SCREEN.fill("#000000")
    draw_map(SCREEN, tiled_map)
    game_sprites.draw(SCREEN)
    pygame.display.update()

pygame.quit()
