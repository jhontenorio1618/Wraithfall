import pygame, sys, os, game_window as WIN

pygame.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Portrait Sheets")

mc_sheet = pygame.image.load(os.path.join(WIN.DIR_SPRITES, "MCportraits.PNG")).convert_alpha()
gpa_sheet = pygame.image.load(os.path.join(WIN.DIR_SPRITES, "GPAportraits.PNG")).convert_alpha()
sword_sheet = pygame.image.load(os.path.join(WIN.DIR_SPRITES, "SWRDportraits.png")).convert_alpha()

BG = (50, 50, 50)


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

def get_portrait_frames():
    mc_sheet = pygame.image.load(os.path.join(WIN.DIR_SPRITES, "MCportraits.PNG")).convert_alpha()
    gpa_sheet = pygame.image.load(os.path.join(WIN.DIR_SPRITES, "GPAportraits.PNG")).convert_alpha()
    sword_sheet = pygame.image.load(os.path.join(WIN.DIR_SPRITES, "SWRDportraits.png")).convert_alpha()

    mc_portraits = collect_frames(mc_sheet, 5, 104, 111, 2)
    gpa_portraits = collect_frames(gpa_sheet, 5, 104, 111, 2)
    sword_portraits = collect_frames(sword_sheet, 3, 65, 111, 2)

    return {
        "MainCharacter": {
            "Neutral": mc_portraits[0],
            "Happy": mc_portraits[1],
            "Excited": mc_portraits[2],
            "Sad": mc_portraits[3],
            "Angry": mc_portraits[4]
        },
        "Grandpa": {
            "Neutral": gpa_portraits[0],
            "Happy": gpa_portraits[1],
            "Mad": gpa_portraits[2],
            "Dead1": gpa_portraits[3],
            "Dead2": gpa_portraits[4]
        },
        "Sword": {
            "Neutral": sword_portraits[0],
            "Happy": sword_portraits[1],
            "Mad": sword_portraits[2]
        }
    }


def print_frames(frames, x, y):
    for i in range(len(frames)):
        screen.blit(frames[i], (x, y))
        x += 200
        if x > SCREEN_WIDTH:
            x = 0
            y += 200
    y += 200
    x = 0
    return x, y


def display_portraits():
    run = True
    # currently, set to print main character, grandpa, and sword portraits
    portraits_to_print = [mc_portraits, gpa_portraits, sword_portraits]
    while run:

        # update background
        screen.fill(BG)

        # show frame image
        x_ref, y_ref = 0, 0
        for sprites in portraits_to_print:
            x_ref, y_ref = print_frames(sprites, x_ref, y_ref)

        # event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()

# display_portraits()