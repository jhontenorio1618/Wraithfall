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

    def get_speed(self):
        return self.speed_x, self.speed_y

    def set_speed(self, x, y):
        # Specify the speed entity moves
        self.speed_x = x
        self.speed_y = y

    def get_coord(self):
        return self.rect.x, self.rect.y

    def warp(self, x, y):
        # Move entity to given coordinates
        self.rect.x = x
        self.rect.y = y

    def set_stats(self, stat_list):
        # Given a dictionary of stats, where keys are the stats and values are the new stat value
        if "ATK" in stat_list:
            self.ATK = stat_list["ATK"]
        if "HP Max" in stat_list:
            self.HP_Max = stat_list["HP Max"]
        if "HP" in stat_list:
            self.HP = stat_list["HP"]
        if "DEF" in stat_list:
            self.HP = stat_list["DEF"]
        if "SPD" in stat_list:
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
        self.found_sword = None

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

    def access_sword(self):
        # Returns Sword, or None if Sword not found
        return self.found_sword

    def pickup_sword(self, sword):
        self.found_sword = sword

    def get_stats(self):
        ATK_mod = 0
        if self.found_sword is not None:
            ATK_mod = self.found_sword.get_stats()["ATK"]
        return {"ATK": self.ATK + ATK_mod, "HP Max": self.HP_Max, "HP": self.HP, "DEF": self.DEF, "SPD": self.SPD}


class Mob(Entity):
    def __init__(self):
        Entity.__init__(self)
        self.image.fill("#FF0000")
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIN.WIN_WIDTH - self.rect.width)
        self.rect.y = random.randrange(WIN.WIN_HEIGHT - self.rect.height)

    def update(self):
        super(Mob, self).update()
        # TODO write unique walking behaviors


class Sword(Entity):
    def __init__(self):
        Entity.__init__(self)
        self.image = pygame.Surface((15, 15))
        self.image.fill("#FFCC40")
        self.rect = self.image.get_rect()
        self.rect.x = WIN.WIN_WIDTH / 2
        self.rect.y = WIN.WIN_HEIGHT / 2 - 75
        self.ATK = 2
        self.found_player = None
        self.form = "BASE"

    def update(self):
        if self.found_player is None:
            self.speed_x = 0
            self.speed_y = 0
        else:
            # Hover beside player
            self.rect.x, self.rect.y = self.found_player.get_coord()
            self.rect.x -= 25
            self.rect.y -= 25
            # super(Sword, self).update()

    def pickup(self, player):
        # Reference Player Entity
        self.found_player = player
        player.pickup_sword(self)
        # new_x, new_y = self.found_player.get_coord()
        self.update()

    def verify(self):
        # Returns Player entity is grabbed; otherwise, returns None
        return self.found_player

    def get_stats(self):
        # Return a dictionary of stats
        # TODO should sword affect any stat besides ATK?
        return {"ATK": self.ATK}

    def shift_form(self, form):
        # Change the form of the sword
        # TODO should change aspects of the sword here. For now, it's only visual
        if form is "BASE":
            self.image.fill("#FFCC40")
        if form is "FIRE":
            self.image.fill("#FF0000")
        if form is "ICE":
            self.image.fill("#0000FF")
        if form is "DARK":
            self.image.fill("#FF00FF")
