import pygame, sys, os, game_window as WIN

pygame.init()

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 900
BG = (50, 50, 50)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Sprite sheets")

mc_sheet = pygame.image.load(os.path.join(WIN.DIR_SPRITES, "MCSPRITESHEET.PNG")).convert_alpha()
gpa_sheet = pygame.image.load(os.path.join(WIN.DIR_SPRITES, "GRANDPAspritesheet.png")).convert_alpha()
sword_sheet = pygame.image.load(os.path.join(WIN.DIR_SPRITES, "SWORDspritesheet.png")).convert_alpha()

# Sword Variations
firesword_sheet = pygame.image.load(os.path.join(WIN.DIR_SPRITES, "FIRESWORDSPRITESHEET.png")).convert_alpha()
darksword_sheet = pygame.image.load(os.path.join(WIN.DIR_SPRITES, "DARKSWORDSPRITESHEET.png")).convert_alpha()
icesword_sheet = pygame.image.load(os.path.join(WIN.DIR_SPRITES, "ICESWORDSPRITESHEET.png")).convert_alpha()

# Mobs
wraithsoul_sheet = pygame.image.load(os.path.join(WIN.DIR_SPRITES, "WRAITHSOULSPRITESHEET.png")).convert_alpha()
wraith1_sheet = pygame.image.load(os.path.join(WIN.DIR_SPRITES, "WRAITH1SPRITESHEET.png")).convert_alpha()
wraith2_sheet = pygame.image.load(os.path.join(WIN.DIR_SPRITES, "WRAITH2SPRITESHEET.png")).convert_alpha()
wraith3_sheet = pygame.image.load(os.path.join(WIN.DIR_SPRITES, "WRAITH3SPRITESHEET.png")).convert_alpha()
bosswraith_sheet = pygame.image.load(os.path.join(WIN.DIR_SPRITES, "BOSSWRAITHSPRITESHEET.png")).convert_alpha()
deer_sheet = pygame.image.load(os.path.join(WIN.DIR_SPRITES, "DEERSPRITESHEET.png")).convert_alpha()

# Battle Sprites
battlesword_sheet = pygame.image.load(os.path.join(WIN.DIR_SPRITES, "BATTLESWORDspritesheet.png")).convert_alpha()
firebattle_sheet = pygame.image.load(os.path.join(WIN.DIR_SPRITES, "FIREBATTLEspritesheet.png")).convert_alpha()
darkbattle_sheet = pygame.image.load(os.path.join(WIN.DIR_SPRITES, "DARKBATTLEspritesheet.png")).convert_alpha()
icebattle_sheet = pygame.image.load(os.path.join(WIN.DIR_SPRITES, "ICEBATTLEspritesheet.png")).convert_alpha()
attacksword_sheet = pygame.image.load(os.path.join(WIN.DIR_SPRITES, "ATTACKSWORDspritesheet.png")).convert_alpha()

# Items
bandage_sheet = pygame.image.load(os.path.join(WIN.DIR_SPRITES, "BANDAGEsprite.png")).convert_alpha()
dirtybandage_sheet = pygame.image.load(os.path.join(WIN.DIR_SPRITES, "DIRTYBANDAGEsprite.png")).convert_alpha()
fireessence_sheet = pygame.image.load(os.path.join(WIN.DIR_SPRITES, "FIREESSENCEsprite.png")).convert_alpha()
iceessence_sheet = pygame.image.load(os.path.join(WIN.DIR_SPRITES, "ICEESSENCEsprite.png")).convert_alpha()
darkessence_sheet = pygame.image.load(os.path.join(WIN.DIR_SPRITES, "DARKESSENCEsprite.png")).convert_alpha()
apple_sheet = pygame.image.load(os.path.join(WIN.DIR_SPRITES, "APPLEsprite.png")).convert_alpha()
deermeat_sheet = pygame.image.load(os.path.join(WIN.DIR_SPRITES, "DEERMEATsprite.png")).convert_alpha()

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
gpa_sprites = collect_frames(gpa_sheet, 12, 17, 17, 3)
sword_sprites = collect_frames(sword_sheet, 16, 17, 20, 3)

# Sword Variations
firesword_sprites = collect_frames(firesword_sheet, 16, 17, 20, 3)
darksword_sprites = collect_frames(darksword_sheet, 16, 17, 20, 3)
icesword_sprites = collect_frames(icesword_sheet, 16, 17, 20, 3)

# Mob Frames
wraithsoul_sprites = collect_frames(wraithsoul_sheet, 12, 17, 17, 3)
wraith1_sprites = collect_frames(wraith1_sheet, 24, 18, 20, 3)
wraith2_sprites = collect_frames(wraith2_sheet, 10, 17, 20, 3)
wraith3_sprites = collect_frames(wraith3_sheet, 8, 17, 20, 3)
bosswraith_sprites = collect_frames(bosswraith_sheet, 5, 59, 52, 2)
deer_sprites = collect_frames(deer_sheet, 6, 23, 20, 3)

# Item Frames
bandage_sprite = collect_frames(bandage_sheet, 1, 19, 12, 2)
dirtybandage_sprite = collect_frames(dirtybandage_sheet, 1, 18, 12, 2)
fireessence_sprite = collect_frames(fireessence_sheet, 1, 14, 17, 2)
iceessence_sprite = collect_frames(iceessence_sheet, 1, 14, 15, 2)
darkessence_sprite = collect_frames(darkessence_sheet, 1, 14, 17, 2)
apple_sprite = collect_frames(apple_sheet, 1, 18, 12, 2)
deermeat_sprite = collect_frames(deermeat_sheet, 1, 16, 17, 2)

# Battle Frames
battlesword_sprites = collect_frames(battlesword_sheet, 6, 850, 990, 1)
firebattle_sprites = collect_frames(firebattle_sheet, 6, 315, 333, 1)
darkbattle_sprites = collect_frames(darkbattle_sheet, 6, 315, 333, 1)
icebattle_sprites = collect_frames(icebattle_sheet, 6, 315, 333, 1)
attacksword_sprites = collect_frames(attacksword_sheet, 5, 1223, 1133, 1)




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


def display_sprites():
    run = True
    # currently, set to print main character, grandpa, and sword sprites
    sprites_to_print = [battlesword_sprites, attacksword_sprites]
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

# display_sprites()