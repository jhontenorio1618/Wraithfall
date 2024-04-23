import pygame, sys, os
import game_window as WIN
import entity_classes as ENTITY
from battle_menu import Battle, item_menu, sword_menu
import pygame.event as EVENTS
import pytmx
from pytmx.util_pygame import load_pygame
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
                        scale_factor = 0.45  # size for objects
                        scaled_img = pygame.transform.scale(obj.image, (int(obj.width * scale_factor), int(obj.height * scale_factor)))
                        screen.blit(scaled_img, (obj.x, obj.y))

    def check_collisions(self, player):
        for layer_name in self.collision_layers:
            layer = self.tiled_map.get_layer_by_name(layer_name)
            if layer is None:
                continue

            if isinstance(layer, pytmx.TiledObjectGroup):
                for obj in layer:
                    padding_x, padding_y = 90, 90
                    width, height = {
                        "tree": (244, 301),
                        "car": (285, 191),
                        "wood": (194, 126)
                    }.get(obj.name, (0, 0))

                    if width == 0 and height == 0:
                        continue

                    obj_rect = pygame.Rect(obj.x + padding_x, obj.y + padding_y, width - 2 * padding_x, height - 2 * padding_y)
                    if player.rect.colliderect(obj_rect):
                        print(f"Collision detected with: {obj.name}")
                        return True
        return False
