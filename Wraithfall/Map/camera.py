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

        #box setup
        self.camera_borders = {'left': 200, 'right': 200, 'top': 100}
        l = self.camera_borders['left']
        t = self.camera_borders['top']
        w = self.display_surface.get_size()[0] - (self.camera_borders['left'] + self.camera_borders['right'])
        h = self.display_surface.get_size()[1] - (self.camera_borders['top'] + self.camera_borders['bottom'])

        self.camera_rect = pygame.Rect(l,t,w,h)


        self.ground_surf = pygame.image.load('insert file here').convert_alpha()
        self.ground_rect = self.ground_surf.get_rect(topleft = (0,0))

        self.zoom_scale = 1
        self.internal_surf_size = (2500, 2500)
        self.internal_surf = pygame.Surface(self.internal_surf_size, pygame.SRCLAPHA)
        self.internal_rect = self.internal_surf.get_rect(center = (self.half_w,self.half_h))
        self.internal_surface_size_vector = pygame.math.Vector2(self.internal_surf_size)
        self.internal_offset = pygame.math.Vector2()
        self.internal_offset.x = self.internal_surf_size[0] // 2 - self.half_w
        self.internal_offset.y = self.internal_surf_size[1] // 2 - self.half_h
    def center_target_camera(self, target):
        self.offset.x = target.rect.centerx - self.half_w
        self.offset.y = target.rect.centery - self.half_h

    def box_target_camera(self, target):

        if target.rect.left < self.camera_rect.left:
            self.camera_rect.left = target.rect.left
        if target.rect.right > self.camera_rect.right:
            self.camera_rect.right = target.rect.right
        if target.rect.top < self.camera_rect.top:
            self.camera_rect.top = target.rect.top
        if target.rect.bottom > self.camera_rect.bottom:
            self.camera_rect.bottom = target.rect.bottom


        self.offset.x = self.camera_rect.left - self.camera_border['left']
        self.offset.x = self.camera_rect.left - self.camera_border['top']
    def zoom_keyboard_control(self):
        keys = pygame.key.get_pressed()
        if keys [pygame.K_q]:
            self.zoom_scale += 0.1
        if keys [pygame.K_e]:
            self.zoom_scale -= 0.1

    def custom_draw(self,player):

        self.box_target_camera(player)

        self.internal_surf.fill('black')

         #ground
        ground_offset = self.ground_rect.topleft - self.offset
        self.internal_surf.blit(self.ground_surf,ground_offset)

        #active elements
        for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.internal_surf.blit(sprite.image,sprite.rect)
        scaled_surf = pygame.transform.scale(self.internal_surf, self.internal_surface_size_vector * self.zoom_scale)
        scaled_rect = scaled_surf.get_rect(center = (self.half_w,self.half_h))

        self.display_surface.blit(scaled_surf, scaled_rect)

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