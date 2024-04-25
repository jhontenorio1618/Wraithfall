import time

import pygame, sys
import abc  # For abstract base classes
from pytmx import load_pygame
from entity_classes import Player
import pygame.event as EVENTS
import pytmx

# Initialize Pygame
pygame.init ()

# Set screen dimensions
WIN_WIDTH = 1280
WIN_HEIGHT = 720
screen = pygame.display.set_mode ((WIN_WIDTH, WIN_HEIGHT))
# Set the current level, which determines which map is used
current_level = 3  # Change this variable to switch between levels

DEFAULT_START_POSITION = (70, 70)  # Adjust as needed

START_POSITION = (900,600)
BACK_POSITION = (1260,720)
is_collised = False
is_first_screen_map = True


# Abstract base class for maps
class AbstractMap (abc.ABC):
    def __init__(self, filename, collision_layers=None):
        self.tiled_map = load_pygame (filename)
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
class DynamicCollisionMap (AbstractMap):
    def __init__(self, filename, collision_layers=None):
        super ().__init__ (filename, collision_layers)

    def draw(self, screen):
        for layer in self.tiled_map.visible_layers:
            if isinstance (layer, pytmx.TiledTileLayer):
                tile_width = self.tiled_map.tilewidth
                tile_height = self.tiled_map.tileheight
                for x, y, gid in layer:
                    tile = self.tiled_map.get_tile_image_by_gid (gid)
                    if tile:
                        screen.blit (tile, (x * tile_width, y * tile_height))
            elif isinstance (layer, pytmx.TiledObjectGroup):
                for obj in layer:
                    if obj.image:
                        scale_factor = 1.0  # size for objects
                        scaled_img = pygame.transform.scale (obj.image, (
                            int (obj.width * scale_factor), int (obj.height * scale_factor)))
                        screen.blit (scaled_img, (obj.x, obj.y))

    def check_collisions(self, player_rect):
        for layer_name in self.collision_layers:
            layer = self.tiled_map.get_layer_by_name (layer_name)

            if layer is None:
                continue
            for obj in layer:
                if obj.name != "cave":
                    padding_x, padding_y = 0, 0
                    obj_rect = pygame.Rect (
                        obj.x + padding_x,
                        obj.y + padding_y,
                        obj.width - 0 * padding_x,
                        obj.height - 0 * padding_y
                    )
                else:
                    padding_x, padding_y = 0, 0
                    obj_rect = pygame.Rect (
                        obj.x + padding_x,
                        obj.y + padding_y,
                        obj.width - 0 * padding_x,
                        obj.height - 0 * padding_y
                    )
                if player_rect.colliderect (obj_rect):
                    print (obj.name)
                    if obj.name == "cave":
                        print ('you will be in the next level in 3 sec')
                        time.sleep (1)
                        running (2, True,False,False)
                    if obj.name == "cave_exit":
                        print ('you will be in the next level in 3 sec')
                        time.sleep (1)
                        running (1, True,False,True)
                    if obj.name == "gate":
                        print ('you will be in the next level in 3 sec')
                        time.sleep (1)
                        running (1, True,False,False )
                    if obj.name.lower () == "thorny_bush":  # Check if the object is a spike
                        player.hp_update (-0.01)  # Decrease health by 1 (or more based on your game design)
                        print (f"Player hit bush! New HP: {player.HP}")
                    if obj.name.lower () == "cave":  # Check for cave collision
                        return True, "cave"
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
player = Player (bound_box_size=(20, 10), image_fill="#FFFFFF")

player.rect.x, player.rect.y = DEFAULT_START_POSITION  # Set the start position

# Create different map objects with dynamic collision layers
level_1_map = DynamicCollisionMap (
    'Game_map/game_map/Main_Map.tmx',
    collision_layers=["land_object", "next_level_chopper"]
)

level_2_map = DynamicCollisionMap (
    "Map/wraithfall_cave1.tmx",
    collision_layers=["collision", 'Lava','cave_exit'],

)
level_3_map = DynamicCollisionMap (
    'Game_map/game_map/second_Map2.tmx',
    collision_layers=["second_land_objects","gate"]
)




# Select the map based on the current level
def select_map(level_number):
    if level_number == 1:
        return level_1_map
    elif level_number == 2:
        return level_2_map
    elif level_number == 3:
        return level_3_map
    else:
        raise ValueError ("Invalid level number")

def running(current_level, is_collised, is_first_screen_map, is_come_back):
    # Main game loop
    running = True
    if current_level  == 3 and is_first_screen_map == True:
        player.rect.x, player.rect.y = START_POSITION
    elif current_level  == 1 and is_come_back == True:
        print('come back level')
        player.rect.x, player.rect.y = BACK_POSITION
        player.update()
    if is_collised == True:
        # is_collised = False
        player.rect.x, player.rect.y = DEFAULT_START_POSITION  # Reset position to start

    while running:
        for event in pygame.event.get ():
            if event.type == pygame.QUIT:
                pygame.quit ()
                sys.exit ()

        screen.fill ((0, 0, 0))




        selected_map = select_map (current_level)

        # Update player and check for collisions
        player.update (lambda rect: selected_map.check_collisions (rect))  # Use lambda for map-based collision check

        keep_player_in_bounds (player)  # Boundary check

        # Draw map and player
        selected_map.draw (screen)
        screen.blit (player.image, player.rect)

        # Update the display
        pygame.display.flip ()


running (current_level, False,is_first_screen_map, False)
pygame.quit ()
