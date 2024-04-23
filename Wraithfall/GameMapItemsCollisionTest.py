import pygame
import pygame.event as EVENTS
import pytmx
from pytmx.util_pygame import load_pygame
import game_window as WIN
import entity_classes as ENTITY
from battle_menu import Battle, item_menu, sword_menu

# Initialize Pygame
pygame.init ()
SCREEN = pygame.display.set_mode (WIN.window_size ())
pygame.display.set_caption ("Wraithfall")
clock = pygame.time.Clock ()


# Load the game map
def load_map(filename):
    return load_pygame (filename)


# Draw the game map
def draw_map(screen, tiled_map):
    for layer in tiled_map.visible_layers:
        if isinstance (layer, pytmx.TiledTileLayer):
            for x, y, gid in layer:
                tile = tiled_map.get_tile_image_by_gid (gid)
                if tile:
                    screen.blit (tile, (x * tiled_map.tilewidth, y * tiled_map.tileheight))
        elif isinstance (layer, pytmx.TiledObjectGroup):
            for obj in layer:
                if obj.image:
                    scale_factor = 0.45
                    scaled_img = pygame.transform.scale (obj.image, (
                    int (obj.width * scale_factor), int (obj.height * scale_factor)))
                    screen.blit (scaled_img, (obj.x, obj.y))


# Function to check collision with a specified layer
def check_collision(player, layer):
    if not isinstance (layer, pytmx.TiledObjectGroup):
        return None  # Return None if the layer is not a TiledObjectGroup

    collision_obj = None  # Initialize to store the object causing the collision
    for obj in layer:
        padding_x = 125
        padding_y = 125
        obj_rect = pygame.Rect (
            obj.x + padding_x,
            obj.y + padding_y,
            obj.width - 2 * padding_x,
            obj.height - 2 * padding_y
        )
        if player.rect.colliderect (obj_rect):
            collision_obj = obj  # Store the object causing the collision
            break  # No need to check further once a collision is detected

    return collision_obj  # Return the object that caused the collision


# Function to handle collisions and block entity movement
def handle_collisions(player, tiled_map):
    # Check collision with land_object layer
    land_object_layer = tiled_map.get_layer_by_name ("land_object")
    collision_obj = check_collision (player, land_object_layer)
    if collision_obj:
        # Determine the direction of collision and adjust player's position accordingly
        padding_x = 45
        padding_y = 45
        obj_rect = pygame.Rect (
            collision_obj.x + padding_x,
            collision_obj.y + padding_y,
            collision_obj.width - 2 * padding_x,
            collision_obj.height - 2 * padding_y
        )
        if player.speed_x > 0:  # Moving right
            player.rect.right = obj_rect.left  # Block on the left
        elif player.speed_x < 0:  # Moving left
            player.rect.left = obj_rect.right  # Block on the right
        if player.speed_y > 0:  # Moving down
            player.rect.bottom = obj_rect.top  # Block from above
        elif player.speed_y < 0:  # Moving up
            player.rect.top = obj_rect.bottom  # Block from below

        # Reset the speed after collision
        player.speed_x = 1
        player.speed_y = 1

        print ("Collision with an object in land_object layer!")

    # Check collision with next_level_chopper layer
    chopper_layer = tiled_map.get_layer_by_name ("next_level_chopper")
    if chopper_layer and check_collision (player, chopper_layer):
        print ("Level change trigger!")


tiled_map = load_map ("Game_map/game_map/Main_Map.tmx")

game_sprites = pygame.sprite.Group ()
mob_sprites = pygame.sprite.Group ()
mob_vision_sprites = pygame.sprite.Group ()
item_sprites = pygame.sprite.Group ()
sword_sprite = pygame.sprite.Group ()
sprite_groups = {
    "Game": game_sprites,
    "Mob": mob_sprites,
    "Mob Vision": mob_vision_sprites,
    "Item": item_sprites,
    "Sword": sword_sprite
}

# Initialize the player sprite
player = ENTITY.Player ()
player.warp (WIN.WIN_WIDTH / 2, WIN.WIN_HEIGHT / 2)
game_sprites.add (player)

# Main game loop
looping = True
while looping:
    clock.tick (WIN.get_fps ())

    # Handle events
    for event in EVENTS.get ():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                WIN.game_exit ()
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
            WIN.game_exit ()

    # Handle collisions to prevent walking through tiles
    handle_collisions (player, tiled_map)

    # Update and draw sprites
    game_sprites.update ()
    SCREEN.fill ("#000000")
    draw_map (SCREEN, tiled_map)
    game_sprites.draw (SCREEN)
    pygame.display.update ()

pygame.quit ()
