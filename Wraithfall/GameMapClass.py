import pygame, sys
import abc  # For abstract base classes
from pytmx import load_pygame
from entity_classes import Player
import pygame.event as EVENTS
import pytmx

# Initialize Pygame
pygame.init()

# Set screen dimensions
WIN_WIDTH = 1280
WIN_HEIGHT = 720
screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))


# Abstract base class for maps
class AbstractMap(abc.ABC):
    def __init__(self, filename, collision_layers=None):
        self.tiled_map = load_pygame(filename)
        if collision_layers:
            self.collision_layers = collision_layers
        else:
            self.collision_layers = []  # Default empty collision layers

    @abc.abstractmethod
    def draw(self, screen):
        pass

    @abc.abstractmethod
    def check_collisions(self, player_rect):
        pass


# Concrete map class with dynamic collision layers
class DynamicCollisionMap(AbstractMap):
    def __init__(self, filename, collision_layers=None):
        super().__init__(filename, collision_layers)

    def draw(self, screen):
        for layer in self.tiled_map.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                tile_width = self.tiled_map.tilewidth
                tile_height = self.tiled_map.tileheight
                for x, y, gid in layer:
                    tile = self.tiled_map.get_tile_image_by_gid(gid)
                    if tile:
                        screen.blit(tile, (x * tile_width, y * tile_height))
            elif isinstance(layer, pytmx.TiledObjectGroup):
                for obj in layer:
                    if obj.image:
                        scale_factor = 1.0  # size for objects
                        scaled_img = pygame.transform.scale (obj.image, (
                            int (obj.width * scale_factor), int (obj.height * scale_factor)))
                        screen.blit (scaled_img, (obj.x, obj.y))

    def check_collisions(self, player_rect):
        for layer_name in self.collision_layers:
            layer = self.tiled_map.get_layer_by_name(layer_name)
            if layer is None:
                continue
            for obj in layer:
                padding_x, padding_y = 0, 0
                obj_rect = pygame.Rect(
                    obj.x + padding_x,
                    obj.y + padding_y,
                    obj.width - 2 * padding_x,
                    obj.height - 2 * padding_y
                )

                if player_rect.colliderect(obj_rect):
                    return obj_rect  # Return the colliding object's rectangle
        return None


# Boundary check function to keep the player within bounds
def keep_player_in_bounds(player):
    if player.rect.left < 0:
        player.rect.left = 0
    elif player.rect.right > WIN_WIDTH:
        player.rect.right = WIN_WIDTH

    if player.rect.top < 0:
        player.rect.top = 0
    elif player.rect.bottom > WIN_HEIGHT:
        player.rect.bottom = WIN_HEIGHT


# Create the player
player = Player(bound_box_size=(20, 10), image_fill="#FFFFFF")

# Create different map objects with dynamic collision layers
level_1_map = DynamicCollisionMap(
    'Game_map/game_map/Main_Map.tmx',
    collision_layers=["land_object", "next_level_chopper"]
)

level_2_map = DynamicCollisionMap(
    'Game_map/game_map/second_Map.tmx',
    collision_layers=["s_ground_objects"]
)

# Set the current level, which determines which map is used
current_level = 2  # Change this variable to switch between levels

# Select the map based on the current level
def select_map(level_number):
    if level_number == 1:
        return level_1_map
    elif level_number == 2:
        return level_2_map
    else:
        raise ValueError("Invalid level number")

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Clear the screen
    screen.fill((0, 0, 0))

    # Select the appropriate map based on the current level
    selected_map = select_map(current_level)

    # Update player and check for collisions
    player.update(lambda rect: selected_map.check_collisions(rect))  # Use lambda for map-based collision check
    keep_player_in_bounds(player)  # Boundary check

    # Draw map and player
    selected_map.draw(screen)
    screen.blit(player.image, player.rect)

    # Check for collisions with map objects
    collision_obj = selected_map.check_collisions(player.rect)

    if collision_obj:
        # Draw a circle to indicate collision
        circle_color = (255, 0, 0)  # Red color
        circle_center = (collision_obj.centerx, circle_radius)  # Center of the object
        circle_radius = 30

        pygame.draw.circle(screen, circle_color, circle_center, circle_radius)

    # Update the display
    pygame.display.flip()

pygame.quit()
