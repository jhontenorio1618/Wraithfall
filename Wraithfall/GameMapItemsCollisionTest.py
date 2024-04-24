import pygame, sys
from pytmx import load_pygame
from entity_classes import Player
import pygame.event as EVENTS
import game_window as WIN
import pygame, sys, os
from pytmx import load_pygame
from entity_classes import Player, Entity
import game_window as WIN
import entity_classes as ENTITY
from battle_menu import Battle, item_menu, sword_menu
import pygame.event as EVENTS
import pytmx

# Initialize pygame
pygame.init()

# Set screen dimensions
WIN_WIDTH = 1280
WIN_HEIGHT = 720
screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))


# Define the map class with collision checking
def check_collision(new_rect):
    return level_1_map.check_collisions(new_rect)

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
                        scale_factor = 1.0  # Default scaling
                        scaled_img = pygame.transform.scale(obj.image, (
                            int(obj.width * scale_factor), int(obj.height * scale_factor)))
                        screen.blit(scaled_img, (obj.x, obj.y))

    def check_collisions(self, player_rect):
        for layer_name in self.collision_layers:
            layer = self.tiled_map.get_layer_by_name(layer_name)
            if layer is None:
                continue

            for obj in layer:
                padding_x, padding_y = 0, 0
                obj_rect = pygame.Rect(obj.x + padding_x, obj.y + padding_y, obj.width - 2 * padding_x,
                                       obj.height - 2 * padding_y)

                if player_rect.colliderect(obj_rect):
                    return obj_rect  # Return the colliding object's rectangle
        return None

# Create player and map objects
player = Player(bound_box_size=(20, 10), image_fill="#FFFFFF")
level_1_map = Map('Game_map/game_map/Main_Map.tmx')  # Ensure path is correct

# Boundary check function
def keep_player_in_bounds(player):
    if player.rect.left < 0:
        player.rect.left = 0
    elif player.rect.right > WIN_WIDTH:
        player.rect.right = WIN_WIDTH

    if player.rect.top < 0:
        player.rect.top = 0
    elif player.rect.bottom > WIN_HEIGHT:
        player.rect.bottom = WIN_HEIGHT

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Clear the screen
    screen.fill((0, 0, 0))

    # Update player and check for collisions
    player.update(check_collision)  # Assuming `update()` updates player's position
    keep_player_in_bounds(player)  # Boundary check

    # Draw map and player
    level_1_map.draw(screen)
    screen.blit(player.image, player.rect)

    # Check for collisions with map objects
    collision_obj = level_1_map.check_collisions(player.rect)

    if collision_obj:
        # Draw a circle on the object with which the player collides
        circle_color = (255, 0, 0)  # Red color
        circle_center = (collision_obj.centerx, collision_obj.centery)  # Center of the object
        circle_radius = 30  # Radius of the circle

        pygame.draw.circle(screen, circle_color, circle_center, circle_radius)

    # Update the display
    pygame.display.flip()

pygame.quit()
