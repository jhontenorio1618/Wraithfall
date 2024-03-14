import pygame, random
import game_window as WIN


class Entity(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # TODO keep in mind reinitializing these in subclasses
        self.image = pygame.Surface((20, 20))
        self.image.fill("#FFFFFF")
        self.rect = self.image.get_rect()
        self.rect.x = WIN.WIN_WIDTH / 2
        self.rect.y = WIN.WIN_HEIGHT / 2
        self.speed_x = 0
        self.speed_y = 0
        # RPG Stats
        self.HP_Max = 5
        self.HP = 5
        self.ATK = 2
        self.DEF = 1
        self.SPD = 0

    def update(self):
        # Entities move depending on their speed
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

    def set_speed(self, x, y):
        # Specify the speed entity moves
        self.speed_x = x
        self.speed_y = y

    def warp(self, x, y):
        # Move entity to given coordinates
        self.rect.x = x
        self.rect.y = y

    def set_stats(self, stat_list):
        # Given a dictionary of stats, where keys are the stats and values are the new stat value
        if stat_list["ATK"]:
            self.ATK = stat_list["ATK"]
        if stat_list["HP Max"]:
            self.HP_Max = stat_list["HP Max"]
        if stat_list["HP"]:
            self.HP = stat_list["HP"]
        if stat_list["DEF"]:
            self.HP = stat_list["DEF"]
        if stat_list["SPD"]:
            self.HP = stat_list["SPD"]
        return self.get_stats()

    def get_stats(self):
        # Return a dictionary of stats
        return {"ATK": self.ATK, "HP Max": self.HP_Max, "HP": self.HP, "DEF": self.DEF, "SPD": self.SPD}

    def hp_update(self, val):
        # Quickly modify HP. Used for combat
        self.HP += val
        return self.HP


class Player(Entity):
    def __init__(self):
        Entity.__init__(self)
        self.image = pygame.Surface((30, 30))
        self.image.fill("#FFFFFF")
        self.rect = self.image.get_rect()
        self.rect.x = WIN.WIN_WIDTH / 2
        self.rect.y = WIN.WIN_HEIGHT / 2

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
        super(Player, self).update()


class Mob(Entity):
    def __init__(self):
        Entity.__init__(self)
        self.image.fill("#FF0000")
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIN.WIN_WIDTH - self.rect.width)
        self.rect.y = random.randrange(WIN.WIN_HEIGHT - self.rect.height)

    def update(self):
        super(Mob, self).update()
        # check if extra sprite leaves the bottom of the game window - then randomise at the top...
        if self.rect.top > WIN.WIN_HEIGHT + 15 or self.rect.left < -15 or self.rect.right > WIN.WIN_WIDTH + 15:
            # specify random start posn & speed
            self.rect.x = random.randrange(WIN.WIN_WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -50)
            self.speed_x = random.randrange(-3, 3)
            self.speed_y = random.randrange(1, 7)



# TODO OLDER VERSIONS IN CASE SUPERCLASS MESSED UP. DELETE WHEN CONFIDENT
class OldPlayer(pygame.sprite.Sprite):
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


class OldMob(pygame.sprite.Sprite):
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

