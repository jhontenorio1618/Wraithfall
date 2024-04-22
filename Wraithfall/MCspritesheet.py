import pygame, sys, os, game_window as WIN

pygame.init()

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 500

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Sprite sheets")

sheet = pygame.image.load(os.path.join(WIN.DIR_SPRITES, "MCSPRITESHEET.PNG")).convert_alpha()

BG = (50, 50, 50)


def get_image(sheet, frame, width, height, scale):
    image = pygame.Surface((width, height), pygame.SRCALPHA).convert_alpha()
    image.blit(sheet, (0, 0), ((frame * width), 0, width, height))
    image = pygame.transform.scale(image, (width * scale, height * scale))

    return image


frame_0 = get_image(sheet, 0, 14, 17, 3)
frame_1 = get_image(sheet, 1, 14, 17, 3)
frame_2 = get_image(sheet, 2, 14, 17, 3)
frame_3 = get_image(sheet, 3, 14, 17, 3)
frame_4 = get_image(sheet, 4, 14, 17, 3)
frame_5 = get_image(sheet, 5, 14, 17, 3)
frame_6 = get_image(sheet, 6, 14, 17, 3)
frame_7 = get_image(sheet, 7, 14, 17, 3)
frame_8 = get_image(sheet, 8, 14, 17, 3)
frame_9 = get_image(sheet, 9, 14, 17, 3)
frame_10 = get_image(sheet, 10, 14, 17, 3)
frame_11 = get_image(sheet, 11, 14, 17, 3)

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
    # facing away
    screen.blit(frame_4, (0, 50))
    screen.blit(frame_5, (50, 50))
    screen.blit(frame_6, (100, 50))
    screen.blit(frame_7, (150, 50))
    # facing right
    screen.blit(frame_8, (0, 100))
    screen.blit(frame_9, (50, 100))
    screen.blit(frame_10, (100, 100))
    screen.blit(frame_11, (150, 100))

    # event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()
