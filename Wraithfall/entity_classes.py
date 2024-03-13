import pygame, random
import game_window as WIN


# TODO Make "class Entity(pygame.sprite.Sprite)" that the other entities extend [ex. class Player(Entity)] for stats
class Entity(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30, 30))
        self.image.fill("#FFFFFF")
        self.rect = self.image.get_rect()
        self.rect.x = WIN.WIN_WIDTH / 2
        self.rect.y = WIN.WIN_HEIGHT / 2
        self.speed_x = 0
        self.speed_y = 0
        self.HP_Max = 1
        self.HP = 1
        self.ATK = 1

    def set_stats(self, stat_list):
        if stat_list["ATK"]:
            self.ATK = stat_list["ATK"]
        if stat_list["HP Max"]:
            self.HP_Max = stat_list["HP Max"]
        if stat_list["HP"]:
            self.HP = stat_list["HP"]
        return self.get_stats()

    def get_stats(self):
        # TODO should be for all stats, for now returns HP
        return {"ATK": self.ATK, "HP Max": self.HP_Max, "HP": self.HP}

    def hp_update(self, val):
        self.HP += val
        return self.HP


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30, 30))
        self.image.fill("#FFFFFF")
        self.rect = self.image.get_rect()
        self.rect.x = WIN.WIN_WIDTH / 2
        self.rect.y = WIN.WIN_HEIGHT / 2
        self.speed_x = 0
        self.speed_y = 0
        # TODO Add more Stats... Idea: make this a dictionary?
        self.HP_Max = 5
        self.HP = 5
        self.ATK = 2

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

    def teleport(self, x, y):
        """ Move player to specified coordinates """
        self.rect.x = x
        self.rect.y = y

    def set_stats(self, stat_list):
        if stat_list["ATK"]:
            self.ATK = stat_list["ATK"]
        if stat_list["HP Max"]:
            self.HP_Max = stat_list["HP Max"]
        if stat_list["HP"]:
            self.HP = stat_list["HP"]
        return self.get_stats()

    def get_stats(self):
        # TODO should be for all stats, for now returns HP
        return {"ATK": self.ATK, "HP Max": self.HP_Max, "HP": self.HP}

    def hp_update(self, val):
        self.HP += val
        return self.HP


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
        self.speed_x = 0  # random.randrange(-3, 3)
        # random speed along the y-axis
        self.speed_y = 0  # random.randrange(1, 7)
        # TODO RPG Stats
        self.HP_Max = 5
        self.HP = 5
        self.ATK = 1

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

    def set_stats(self, stat_list):
        if stat_list["ATK"]:
            self.ATK = stat_list["ATK"]
        if stat_list["HP Max"]:
            self.HP_Max = stat_list["HP Max"]
        if stat_list["HP"]:
            self.HP = stat_list["HP"]
        return self.get_stats()

    def get_stats(self):
        # TODO should be for all stats, for now returns HP
        return {"ATK": self.ATK, "HP Max": self.HP_Max, "HP": self.HP}

    def hp_update(self, val):
        self.HP += val
        return self.HP

