import pygame, sys, os, game_window as WIN

pygame.init()

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 500

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Sprite sheets")

sprite_sheet_image = pygame.image.load(os.path.join(WIN.DIR_SPRITES, "SWORDspritesheet.png")).convert_alpha()

BG = (50, 50, 50)


def get_image(sheet, frame, width, height, scale):
    image = pygame.Surface((width, height), pygame.SRCALPHA).convert_alpha()
    image.blit(sheet, (0, 0), ((frame * width), 0, width, height))
    image = pygame.transform.scale(image, (width * scale, height * scale))

    return image


frame_0 = get_image(sprite_sheet_image, 0, 17, 20, 3)
frame_1 = get_image(sprite_sheet_image, 1, 17, 20, 3)
frame_2 = get_image(sprite_sheet_image, 2, 17, 20, 3)
frame_3 = get_image(sprite_sheet_image, 3, 17, 20, 3)
frame_4 = get_image(sprite_sheet_image, 4, 17, 20, 3)
frame_5 = get_image(sprite_sheet_image, 5, 17, 20, 3)
frame_6 = get_image(sprite_sheet_image, 6, 17, 20, 3)
frame_7 = get_image(sprite_sheet_image, 7, 17, 20, 3)

frame_8 = get_image(sprite_sheet_image, 8, 17, 20, 3)
frame_9 = get_image(sprite_sheet_image, 9, 17, 20, 3)
frame_10 = get_image(sprite_sheet_image, 10, 17, 20, 3)
frame_11 = get_image(sprite_sheet_image, 11, 17, 20, 3)
frame_12 = get_image(sprite_sheet_image, 12, 17, 20, 3)
frame_13 = get_image(sprite_sheet_image, 13, 17, 20, 3)
frame_14 = get_image(sprite_sheet_image, 14, 17, 20, 3)
frame_15 = get_image(sprite_sheet_image, 15, 17, 20, 3)
# frame_16 = get_image(sprite_sheet_image, 16, 17, 20, 3)

run = True
while run:

    # update background
    screen.fill(BG)

    # show frame image
    # facing forward
    screen.blit(frame_0, (0, 0))
    screen.blit(frame_1, (50, 0))
    screen.blit(frame_2, (100, 0))
    screen.blit(frame_3, (150, 0))
    screen.blit(frame_4, (200, 0))
    screen.blit(frame_5, (250, 0))
    screen.blit(frame_6, (300, 0))
    screen.blit(frame_7, (350, 0))
    # facing away
    screen.blit(frame_8, (0, 50))
    screen.blit(frame_9, (50, 50))
    screen.blit(frame_10, (100, 50))
    screen.blit(frame_11, (150, 50))
    screen.blit(frame_12, (200, 50))
    screen.blit(frame_13, (250, 50))
    screen.blit(frame_14, (300, 50))
    screen.blit(frame_15, (350, 50))
    # screen.blit(frame_16, (400, 50))

    # event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()
