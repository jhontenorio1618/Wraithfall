import pygame, sys, os
from pytmx import load_pygame
from entity_classes import Player, Entity
import game_window as WIN
import entity_classes as ENTITY
from battle_menu import Battle, item_menu, sword_menu
import pygame.event as EVENTS
import pytmx


class Map:
    def __init__(self, filename):
        self.tiled_map = load_pygame(filename)
        self.collision_layers = ["land_object", "next_level_chopper"]

    def draw(self, screen):
        for layer in self.tiled_map.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = self.tiled_map.get_tile_image_by_gid(gid)
                    if tile:
                        screen.blit(tile, (x * self.tiled_map.tilewidth, y * self.tiled_map.tileheight))
            elif isinstance(layer, pytmx.TiledObjectGroup):
                for obj in layer:
                    if obj.image:
                        scale_factor = 1.0  # size for objects
                        scaled_img = pygame.transform.scale(obj.image, (
                            int(obj.width * scale_factor), int(obj.height * scale_factor)))
                        screen.blit(scaled_img, (obj.x, obj.y))

    def check_collisions(self, player_rect):
        """Checks for collisions between the player and objects in specified layers."""
        for layer_name in self.collision_layers:
            layer = self.tiled_map.get_layer_by_name(layer_name)
            if layer is None:
                continue

            for obj in layer:
                # Optional padding for fine-tuning collision accuracy
                padding_x, padding_y = 10, 10  # Adjust these values based on your game's needs
                obj_rect = pygame.Rect(obj.x + padding_x, obj.y + padding_y, obj.width - 2 * padding_x,
                                       obj.height - 2 * padding_y)

                if player_rect.colliderect(obj_rect):
                    print(f"Collision detected with: {obj.name}")
                    return True
        return False


class SecondMap(Map):
    def __init__(self, filename):
        super().__init__(filename)
        self.collision_layers = ["land_object", "second_land_objects"]

    def check_collisions(self, player_rect):
        """Checks for collisions between the player and objects in specified layers."""
        for layer_name in self.collision_layers:
            layer = self.tiled_map.get_layer_by_name(layer_name)
            if layer is None:
                continue

            for obj in layer:
                #
                padding_x, padding_y = 10, 10
                obj_rect = pygame.Rect(obj.x + padding_x, obj.y + padding_y, obj.width - 2 * padding_x,
                                       obj.height - 2 * padding_y)

                if player_rect.colliderect(obj_rect):
                    print(f"Collision detected with: {obj.name}")
                    return True
        return False


# level_1_map = Map('Game_map/game_map/Main_Map.tmx')
level_2_map = SecondMap('Game_map/game_map/second_map.tmx')


pygame.init()
screen = pygame.display.set_mode((1280, 720))

# Created and initialize player and level map objects
player = Player(bound_box_size=(30, 30),
                image_fill="#FFFFFF")
level_1_map = Map('Game_map/game_map/Main_Map.tmx')  # Ensure path and filename are correct


def check_collision(new_rect):

    return level_1_map.check_collisions(new_rect)


running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


    screen.fill((0, 0, 0))


    player.update(check_collision)


    level_1_map.draw(screen)
    screen.blit(player.image, player.rect)


    pygame.display.update()
