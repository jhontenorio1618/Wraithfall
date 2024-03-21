import pygame
import pytmx
from pytmx.util_pygame import load_pygame


def load_map(filename):
    #to load the  tmx file
    tm = load_pygame (filename)
    return tm


def draw_map(screen, tiled_map):
   #draw the map to the Pygame screen
    for layer in tiled_map.visible_layers:
        if isinstance (layer, pytmx.TiledTileLayer):
            for x, y, gid, in layer:
                tile = tiled_map.get_tile_image_by_gid (gid)
                if tile:
                    screen.blit (tile, (x * tiled_map.tilewidth, y * tiled_map.tileheight))


def main():
    pygame.init ()
    screen = pygame.display.set_mode ((1200, 960))

    tm = load_map ('Map/GameMap.tmx')
    # tm = load_map ('WraithFall Map/TSXFiles/GameMapLevelOne.tmx')
    clock = pygame.time.Clock ()

    running = True
    while running:
        for event in pygame.event.get ():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                # Escape Key
                if event.key == pygame.K_ESCAPE:
                    running = False
        screen.fill ((0, 0, 0))
        # screen.fill ("purple")
        draw_map (screen, tm)

        pygame.display.flip ()
        clock.tick (60)

    pygame.quit ()


if __name__ == "__main__":
    main ()
