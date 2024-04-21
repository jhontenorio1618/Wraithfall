import pygame
import pytmx
from pytmx.util_pygame import load_pygame

def load_map(filename):
    # Load the TMX file
    tm = load_pygame(filename)
    return tm

def draw_map(screen, tiled_map):
    for layer in tiled_map.visible_layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            for x, y, gid in layer:
                tile = tiled_map.get_tile_image_by_gid(gid)
                if tile:
                    rect = pygame.Rect(x * tiled_map.tilewidth, y * tiled_map.tileheight, tiled_map.tilewidth, tiled_map.tileheight)
                    screen.blit(tile, (x * tiled_map.tilewidth, y * tiled_map.tileheight))
        elif isinstance(layer, pytmx.TiledObjectGroup):
            for obj in layer:
                if obj.image:
                    scaled_img = pygame.transform.scale(obj.image, (int(obj.width * 0.5), int(obj.height * 0.5)))  # Scale image
                    obj_rect = pygame.Rect(obj.x, obj.y, scaled_img.get_width(), scaled_img.get_height())
                    screen.blit(scaled_img, (obj.x, obj.y))

def main():
    pygame.init()
    screen = pygame.display.set_mode((1200, 960))
    tm = load_map('Game_map/game_map/Main_Map.tmx')  # Ensure this path is correct based on your directory structure
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False  # Handle ESC key to quit the game

        screen.fill((0, 0, 0))
        draw_map(screen, tm)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
