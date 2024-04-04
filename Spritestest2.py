import pygame

pygame.init()

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Sprite sheets")

sprite_sheet_image = pygame.image.load("MCSPRITESFINAL.PNG").convert_alpha()

BG = (50, 50, 50)

def get_image(sheet, frame, width, height, scale):
    image = pygame.Surface((width, height), pygame.SRCALPHA).convert_alpha()
    image.blit(sheet, (0, 0), ((frame * width), 0, width, height))
    image = pygame.transform.scale(image, (width * scale, height * scale))

    return image


frame_0 = get_image(sprite_sheet_image, 0, 14, 17, 3)
frame_1 = get_image(sprite_sheet_image, 1, 14, 17, 3)
frame_2 = get_image(sprite_sheet_image, 2, 14, 17, 3)
frame_3 = get_image(sprite_sheet_image, 3, 14, 17, 3)



run = True
while run:

    # update background
    screen.fill(BG)

    #show frame image
    screen.blit(frame_0, (0, 0))
    screen.blit(frame_1, (50, 0))
    screen.blit(frame_2, (100, 0))
    screen.blit(frame_3, (150, 0))



    # event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()
