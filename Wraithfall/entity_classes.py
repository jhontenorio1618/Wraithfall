import pygame, random
import game_window as WIN

# TODO need stats
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30, 30))
        self.image.fill("#FFFFFF")
        self.rect = self.image.get_rect()
        self.rect.centerx = WIN.WIN_WIDTH / 2
        self.rect.centery = WIN.WIN_HEIGHT / 2
        self.speed_x = 0
        self.speed_y = 0

    def update(self):
        self.speed_x = 0
        self.speed_y = 0
        key_state = pygame.key.get_pressed()
        if key_state[pygame.K_LEFT]:
            self.speed_x = -5
        if key_state[pygame.K_RIGHT]:
            self.speed_x = 5
        if key_state[pygame.K_UP]:
            self.speed_y = -5
        if key_state[pygame.K_DOWN]:
            self.speed_y = 5
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        """if self.rect.right > winWidth:
            self.rect.right = winWidth
        if self.rect.left < 0:
            self.rect.left = 0"""


class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((20, 20))
        self.image.fill("#FF0000")
        # specify bounding rect for sprite
        self.rect = self.image.get_rect()
        # specify random start posn & speed
        self.rect.x = random.randrange(WIN.WIN_WIDTH - self.rect.width)
        self.rect.y = random.randrange(WIN.WIN_HEIGHT - self.rect.height)
        # random speed along the x-axis
        self.speed_x = random.randrange(-3, 3)
        # random speed along the y-axis
        self.speed_y = random.randrange(1, 7)

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        # check if extra sprite leaves the bottom of the game window - then randomise at the top...
        if self.rect.top > WIN.WIN_HEIGHT + 15 or self.rect.left < -15 or self.rect.right > WIN.WIN_WIDTH + 15:
            # specify random start posn & speed
            self.rect.x = random.randrange(WIN.WIN_WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -50)
            self.speed_x = random.randrange(-3, 3)
            self.speed_y = random.randrange(1, 7)

    def set_speed(self, x, y):
        self.speed_x = x
        self.speed_y = y

    def set_spawn(self, x, y):
        self.rect.centerx = x
        self.rect.centery = y


