import pygame, sys, os, game_window as WIN

pygame.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 500

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Sprite sheets")

sprite_sheet_image = pygame.image.load(os.path.join(WIN.DIR_SPRITES, "GPAportraits.PNG")).convert_alpha()

BG = (50, 50, 50)


def get_image(sheet, frame, width, height, scale):
    image = pygame.Surface((width, height), pygame.SRCALPHA).convert_alpha()
    image.blit(sheet, (0, 0), ((frame * width), 0, width, height))
    image = pygame.transform.scale(image, (width * scale, height * scale))

    return image


frame_0 = get_image(sprite_sheet_image, 0, 104, 111, 2)
frame_1 = get_image(sprite_sheet_image, 1, 104, 111, 2)
frame_2 = get_image(sprite_sheet_image, 2, 104, 111, 2)
frame_3 = get_image(sprite_sheet_image, 3, 104, 111, 2)
frame_4 = get_image(sprite_sheet_image, 4, 104, 111, 2)

run = True
while run:

    # update background
    screen.fill(BG)

    # show frame image
    screen.blit(frame_0, (0, 0))
    screen.blit(frame_1, (200, 0))
    screen.blit(frame_2, (400, 0))
    screen.blit(frame_3, (600, 0))
    screen.blit(frame_4, (800, 0))

    # event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()
