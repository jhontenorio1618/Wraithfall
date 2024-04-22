import pygame, sys, os, game_window as WIN

pygame.init()

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 500
BG = (50, 50, 50)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Sprite sheets")

mc_sheet = pygame.image.load(os.path.join(WIN.DIR_SPRITES, "MCSPRITESHEET.PNG")).convert_alpha()
gpa_sheet = pygame.image.load(os.path.join(WIN.DIR_SPRITES, "GRANDPAspritesheet.png")).convert_alpha()
sword_sheet = pygame.image.load(os.path.join(WIN.DIR_SPRITES, "SWORDspritesheet.png")).convert_alpha()


def get_image(sheet, frame, width, height, scale):
    image = pygame.Surface((width, height), pygame.SRCALPHA).convert_alpha()
    image.blit(sheet, (0, 0), ((frame * width), 0, width, height))
    image = pygame.transform.scale(image, (width * scale, height * scale))

    return image


def collect_frames(sheet, total_frames, width, height, scale):
    frames = []
    for i in range(total_frames):
        frame = get_image(sheet, i, width, height, scale)
        frames.append(frame)
    return frames


# Main Character Frames
mc_sprites = collect_frames(mc_sheet, 12, 14, 17, 3)
gpa_sprites = collect_frames(gpa_sheet, 12, 14, 17, 3)
sword_sprites = collect_frames(sword_sheet, 16, 17, 20, 3)


def print_frames(frames, x, y):
    for i in range(len(frames)):
        screen.blit(frames[i], (x, y))
        x += 50
        if x > SCREEN_WIDTH:
            x = 0
            y += 50
    y += 50
    x = 0
    return x, y


run = True
# currently, set to print main character, grandpa, and sword sprites
sprites_to_print = [mc_sprites, gpa_sprites, sword_sprites]
while run:

    # update background
    screen.fill(BG)

    # show frame images
    x_ref, y_ref = 0, 0
    for sprites in sprites_to_print:
        x_ref, y_ref = print_frames(sprites, x_ref, y_ref)

    # event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()
