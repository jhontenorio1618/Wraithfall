import pygame, sys
from random import randint
from pytmx.util_pygame import load_pygame


class Object(pygame.sprite.Sprite):
    def __init__(self,pos,group):
        super().__init__(group)
        self.image = pygame.image.load('insert map file').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)

class Player(pygame.sprite.Sprite):
    def __init__(self,pos,group):
        super().__init__(group)
        self.image = pygame.image.load('player object').convert_alpha()
        self.rect = self.image.get_rect(center = pos)
        self.direction = pygame.math.Vector2()
        self.speed = 5
        def input(self):
            key = pygame.key.get_pressed()

            if key[pygame.K_UP]:
                self.direction.y = -1
            elif key[pygame.K.K_DOWN]:
                self.direction.y = 1
            else:
                self.direction.y = 0

            if key[pygame.K_RIGHT]:
                self.direction.x = 1
            elif key[pygame.K_LEFT]:
                self.direction.x = -1
            else:
                self.direction.x = 0


        def update(self):
            self.input()
            self.rect.center += self.direction * self.speed
class CameraGroup(pygame.sprite.Group):
    def __int__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        #camera offset
        self.offset = pygame.math.Vector2(0,720)
        self.half_w = self.display_surface.get_size()[0] // 2
        self.half_h = self.display_surface.get_size()[1] // 2


        self.ground_surf = pygame.image.load('insert file here').convert_alpha()
        self.ground_rect = self.ground_surf.get_rect(topleft = (0,0))
    def center_target_camera(self, target):
        self.offset.x = target.rect.centerx - self.half_w
        self.offset.y = target.rect.centery - self.half_h
    def custom_draw(self,player):

        self.center_target_camera(player)

         #ground
        ground_offset = self.ground_rect.topleft - self.offset
        self.display_surface.blit(self.ground_surf,ground_offset)

        #active elements
        for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image,sprite.rect)

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()

camera_group = CameraGroup()
player = Player((640,360)),camera_group)

for i in range(20):
    random_x = randint(0,1000)
    random_y = randint(0,1000)
    Objects((random_x,random_y), camera_group)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            screen.fill('cabin room map.tmx')

            camera_group.update()
            camera_group.custom_draw(player)

            pygame.display.update()
            clock.tick(60)