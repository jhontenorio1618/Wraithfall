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
    tm = load_pygame(filename)
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


def check_collision(player, tiled_map, layer_name):
    layer = tiled_map.get_layer_by_name(layer_name)
    if layer is None:
        return False

    collision_detected = False

    if isinstance(layer, pytmx.TiledObjectGroup):
        for obj in layer:

            padding_x = 90
            padding_y = 90

            if obj.name == "tree":
                obj_rect = pygame.Rect(obj.x + padding_x, obj.y + padding_y, 244 - 2 * padding_x, 301 - 2 * padding_y)
            elif obj.name == "car":
                obj_rect = pygame.Rect(obj.x + padding_x, obj.y + padding_y, 285 - 2 * padding_x, 191 - 2 * padding_y)
            elif obj.name == "wood":
                obj_rect = pygame.Rect(obj.x + padding_x, obj.y + padding_y, 194 - 2 * padding_x, 126 - 2 * padding_y)
            else:
                continue

            if player.rect.colliderect(obj_rect):
                print(f"Collision detected with: {obj.name}")
                collision_detected = True

    return collision_detected




def handle_collisions(player, tiled_map):
    if check_collision(player, tiled_map, "land_object"):
        player.speed_x = 0
        player.speed_y = 0
        print("Collision with an object in land_object layer!")
    if check_collision(player, tiled_map, "next_level_chopper"):
        print("Level change trigger!")

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

    handle_collisions(player, tiled_map)
    game_sprites.update()

    SCREEN.fill("#000000")
    draw_map(SCREEN, tiled_map)
    game_sprites.draw(SCREEN)
    pygame.display.update()

pygame.quit()
