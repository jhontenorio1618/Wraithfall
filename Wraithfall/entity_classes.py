import pygame, random
import game_window as WIN


class BoundingBox(pygame.sprite.Sprite):
    def __init__(self, bound_box_size=(100, 100)):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(bound_box_size)
        self.image.fill("#000000")
        self.rect = self.image.get_rect()
        self.rect.x = WIN.WIN_WIDTH
        self.rect.y = WIN.WIN_HEIGHT


class Entity(pygame.sprite.Sprite):
    def __init__(self, bound_box_size=(20, 20), image_fill="#FFFFFF"):
        pygame.sprite.Sprite.__init__(self)
        # TODO keep in mind reinitializing these in subclasses
        self.image = pygame.Surface(bound_box_size)
        self.image.fill(image_fill)
        self.rect = self.image.get_rect()
        self.rect.x = WIN.WIN_WIDTH
        self.rect.y = WIN.WIN_HEIGHT
        self.speed_x = 0
        self.speed_y = 0
        # RPG Stats
        self.HP_Max = 1
        self.HP = 1
        self.ATK = 1
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

    def warp(self, x=None, y=None):
        # Move entity to given coordinates
        if x is None:
            self.rect.x = random.randrange(WIN.WIN_WIDTH - self.rect.width)
        else:
            self.rect.x = x
        if y is None:
            self.rect.y = random.randrange(WIN.WIN_HEIGHT - self.rect.height)
        else:
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
            self.DEF = stat_list["DEF"]
        if "SPD" in stat_list:
            self.SPD = stat_list["SPD"]
        return self.get_stats()

    def get_stats(self):
        # Return a dictionary of stats
        return {"ATK": self.ATK, "HP Max": self.HP_Max, "HP": self.HP, "DEF": self.DEF, "SPD": self.SPD}

    def hp_update(self, val):
        # Quickly modify HP. Used for combat
        self.HP += val
        if self.HP > self.HP_Max:
            self.HP = self.HP_Max
        return self.HP


class Player(Entity):
    def __init__(self, bound_box_size=(30, 30), image_fill="#FFFFFF", player_stats=None):
        Entity.__init__(self, bound_box_size=bound_box_size, image_fill=image_fill)
        if player_stats is None:
            player_stats = {"ATK": 2, "HP Max": 5, "HP": 5, "DEF": 1, "SPD": 0}
        self.found_sword = None
        self.inventory = []
        self.inventory_max = 3
        self.inventory_pointer = 0
        self.set_stats(player_stats)

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

    def access_item(self, pointer=None):
        if pointer is not None:
            self.inventory_pointer = 0
            self.scroll_inv(pointer)
        using_item = None
        if self.inventory and self.inventory[self.inventory_pointer]:
            using_item = self.inventory[self.inventory_pointer]
        return using_item

    def scroll_inv(self, move):
        self.inventory_pointer += move
        if self.inventory_pointer > len(self.inventory) - 1:
            self.inventory_pointer = 0
        if self.inventory_pointer < 0:
            self.inventory_pointer = len(self.inventory) - 1

    def pickup_item(self, item):
        can_pickup = False
        if len(self.inventory) < self.inventory_max:
            can_pickup = True
            self.inventory.append(item)
        return can_pickup

    def lose_item(self, item):
        if item in self.inventory:
            self.inventory.remove(item)

    def get_stats(self):
        ATK_mod = 0
        if self.found_sword is not None:
            ATK_mod = self.found_sword.get_stats()["ATK"]
        return {"ATK": self.ATK + ATK_mod, "HP Max": self.HP_Max, "HP": self.HP, "DEF": self.DEF, "SPD": self.SPD}


class Mob(Entity):
    def __init__(self, bound_box_size=(20, 20), image_fill="#FF0000", mob_stats=None):
        Entity.__init__(self, bound_box_size=bound_box_size, image_fill=image_fill)
        if mob_stats is None:
            mob_stats = {"ATK": 2, "HP Max": 5, "HP": 5, "DEF": 1, "SPD": 0}
        self.set_stats(mob_stats)

    def update(self):
        super(Mob, self).update()
        # TODO write unique walking behaviors


class PassiveMob(Entity):
    def __init__(self, bound_box_size=(20, 20), image_fill="#00FFFF", mob_stats=None):
        Entity.__init__(self, bound_box_size=bound_box_size, image_fill=image_fill)
        if mob_stats is None:
            mob_stats = {"ATK": 2, "HP Max": 5, "HP": 5, "DEF": 1, "SPD": 0}
        self.set_stats(mob_stats)

    def update(self):
        super(PassiveMob, self).update()
        # TODO write unique walking behaviors


class Sword(Entity):
    def __init__(self, bound_box_size=(15, 15), image_fill="#FFCC40", sword_attack=None):
        Entity.__init__(self, bound_box_size=bound_box_size, image_fill=image_fill)
        if sword_attack is None:
            sword_attack = {"ATK": 2}
        self.found_player = None
        self.form = "BASE"
        self.set_stats(sword_attack)

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

    """def get_stats(self):
        # Return a dictionary of stats
        # TODO should sword affect any stat besides ATK?
        return {"ATK": self.ATK}"""

    def shift_form(self, form):
        # Change the form of the sword
        # TODO should change aspects of the sword here. For now, it's only visual
        if form == "BASE":
            self.image.fill("#FFCC40")
        if form == "FIRE":
            self.image.fill("#FF0000")
        if form == "ICE":
            self.image.fill("#0000FF")
        if form == "DARK":
            self.image.fill("#FF00FF")


item_dict = {0: {"NAME": "Bandage", "TYPE": "HP", "VALUE": 5},
             1: {"NAME": "Fire Essence", "TYPE": "SWORD"},
             2: {"NAME": "Ice Essence", "TYPE": "SWORD"},
             3: {"NAME": "Dark Essence", "TYPE": "SWORD"}
             }


class Item(Entity):
    def __init__(self, bound_box_size=(15, 15), image_fill="#00FF00", item_id=0):
        Entity.__init__(self, bound_box_size=bound_box_size, image_fill=image_fill)
        self.found_player = None
        self.item_id = item_id
        self.name = item_dict[self.item_id]["NAME"]
        self.type = item_dict[self.item_id]["TYPE"]

    def pickup(self, player):
        picked_up = player.pickup_item(self)
        if picked_up:
            # Player has inventory for item
            self.found_player = player
        return picked_up

    def verify(self):
        # Returns Player entity is grabbed; otherwise, returns None
        return self.found_player

    def use_item(self):
        if self.type == "HP":
            self.found_player.hp_update(item_dict[self.item_id]["VALUE"])
        self.found_player.lose_item(self)

    def get_name(self):
        return self.name



