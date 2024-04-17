import pygame
import game_window as WIN


class BoundingBox(pygame.sprite.Sprite):
    """ Bounding Boxes spawned in the game to allow for a particular effect to happen in specified location.
    For example: mob detection radius, area to apply particular effect, etc. """

    def __init__(self, bound_box_size=(100, 100), entity_anchor=None, location_coord=(WIN.WIN_WIDTH, WIN.WIN_HEIGHT)):
        # TODO figure out transparency
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(bound_box_size)
        trans_color = "#FF00FF"
        self.image.fill(trans_color)
        self.image.set_colorkey(trans_color)
        self.rect = self.image.get_rect()
        self.speed_x = 0
        self.speed_y = 0
        if entity_anchor is None:
            self.rect.centerx, self.rect.centery = location_coord
            # self.rect.y = location_coord[1]
        else:
            self.rect.centerx, self.rect.centery = entity_anchor.get_coord()
        self.entity_anchor = entity_anchor

    def update(self):
        """ If tied to an Entity, follow the Entity when it moves """
        if self.entity_anchor is None:
            self.speed_x = 0
            self.speed_y = 0
        else:
            # Stick to associated mob
            self.rect.centerx, self.rect.centery = self.entity_anchor.get_coord()

    def warp(self, x=None, y=None):
        """ Move bounding box to given coordinates. Used for spawning and moving position on map.
        Returns the new coordinates of the bounding box. """
        if x is None:
            self.rect.centerx = WIN.random.randrange(WIN.WIN_WIDTH - self.rect.width)
        else:
            self.rect.centerx = x
        if y is None:
            self.rect.centery = WIN.random.randrange(WIN.WIN_HEIGHT - self.rect.height)
        else:
            self.rect.centery = y
        return x, y

    def get_entity(self):
        """ Returns associated Entity, if one exists """
        return self.entity_anchor

    def set_entity(self, entity):
        entity.set_bb_anchor(self)
        self.entity_anchor = entity
        return self.entity_anchor


class Entity(pygame.sprite.Sprite):
    """ Superclass for Player, Mob, Item, and Sword classes. """

    def __init__(self, bound_box_size=(20, 20), image_fill="#FFFFFF"):
        """ bound_box_size = size of the sprite
        image_fill = color code for basic rectangle without sprite """
        pygame.sprite.Sprite.__init__(self)
        # Determining basic appearance of Sprite
        # TODO add way to insert sprites in the hyperparameters
        self.image = pygame.Surface(bound_box_size)
        self.image.fill(image_fill)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIN.WIN_WIDTH
        self.rect.centery = WIN.WIN_HEIGHT
        self.speed_x = 0
        self.speed_y = 0
        self.bb_anchor = None
        # RPG Stats
        self.HP_Max = 1
        self.HP = 1
        self.ATK = 1
        self.DEF = 1
        self.SPD = 0

    def update(self):
        """ Calculate movement of the Entity. """
        self.rect.centerx += self.speed_x
        self.rect.centery += self.speed_y

    def get_speed(self):
        """ Return the current speed of the Entity. """
        return self.speed_x, self.speed_y

    def set_speed(self, x, y):
        """ Specify the speed Entity moves. """
        self.speed_x = x
        self.speed_y = y

    def get_coord(self):
        """ Return the current coordinates of the Entity. """
        return self.rect.centerx, self.rect.centery

    def warp(self, x=None, y=None):
        """ Move Entity to given coordinates. Used for spawning and moving position on map.
        If no coordinates are given, then the Entity is spawned randomly on screen.
        Returns new coordinates of the Entity. """
        if x is None:
            self.rect.centerx = WIN.random.randrange(WIN.WIN_WIDTH - self.rect.width)
        else:
            self.rect.centerx = x
        if y is None:
            self.rect.centery = WIN.random.randrange(WIN.WIN_HEIGHT - self.rect.height)
        else:
            self.rect.centery = y
        return x, y

    def set_stats(self, stat_list):
        """ Where stat_list is a dictionary that has keys which represent the stats
        and values that signify what to change the stats into.
        Then, returns a dictionary of the Entity's stats. """
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
        """ Returns a dictionary of the Entity's stats. """
        return {"ATK": self.ATK, "HP Max": self.HP_Max, "HP": self.HP, "DEF": self.DEF, "SPD": self.SPD}

    def hp_update(self, val):
        """ Quickly modify HP. Used during combat. """
        # Quickly modify HP. Used for combat
        self.HP += val
        if self.HP > self.HP_Max:
            self.HP = self.HP_Max
        return self.HP

    def get_bb_anchor(self):
        return self.bb_anchor

    def set_bb_anchor(self, bb):
        self.bb_anchor = bb
        return self.bb_anchor


class Player(Entity):
    def __init__(self, bound_box_size=(30, 30), image_fill="#FFFFFF", player_stats=None):
        """ bound_box_size = size of the sprite
        image_fill = color code for basic rectangle without sprite
        player_stats = dictionary of RPG stats, where the keys are strings of the stats and values are ints """
        Entity.__init__(self, bound_box_size=bound_box_size, image_fill=image_fill)
        if player_stats is None:
            # Default Player Stats if none are given to initialize.
            player_stats = {"ATK": 2, "HP Max": 5, "HP": 5, "DEF": 1, "SPD": 0}
        self.found_sword = None
        self.inventory = []
        self.inventory_max = 3
        self.inventory_pointer = 0
        self.set_stats(player_stats)
        self.EXP = 0
        self.hunger = 100

    def update(self):
        """ Calculate the movement of the player. """
        self.speed_x = 0
        self.speed_y = 0
        key_state = pygame.key.get_pressed()
        # TODO make player diagonal movements smooth & consistent
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
        """ Returns Sword if the player has it. Otherwise, returns None. """
        return self.found_sword

    def pickup_sword(self, sword):
        """ Connects picked up sword to player. Run by Sword Entity's pickup() method. """
        self.found_sword = sword

    def access_item(self, pointer=None):
        """ Given inventory index (pointer),
        retrieve reference to the item in inventory as long as one exists. """
        if pointer is not None:
            self.inventory_pointer = 0
            self.scroll_inv(pointer)
        using_item = None
        if self.inventory and self.inventory[self.inventory_pointer]:
            using_item = self.inventory[self.inventory_pointer]
        return using_item

    def scroll_inv(self, move):
        """ Scroll through indexes of inventory.
        When move is positive, go "right." When move is negative, go "left." """
        self.inventory_pointer += move
        if self.inventory_pointer > len(self.inventory) - 1:
            self.inventory_pointer = 0
        if self.inventory_pointer < 0:
            self.inventory_pointer = len(self.inventory) - 1

    def pickup_item(self, item):
        """ Adds picked up item to inventory as long as inventory is not full. """
        can_pickup = False
        if len(self.inventory) < self.inventory_max:
            can_pickup = True
            self.inventory.append(item)
        return can_pickup

    def lose_item(self, item):
        """ Item was used, so remove it from player's inventory. """
        if item in self.inventory:
            self.inventory.remove(item)

    def get_stats(self):
        """ Returns a dictionary of stats. Includes changes done by equipping SWORD. """
        ATK_mod = 0
        if self.found_sword is not None:
            ATK_mod = self.found_sword.get_stats()["ATK"]
        return {"ATK": self.ATK + ATK_mod, "HP Max": self.HP_Max, "HP": self.HP, "DEF": self.DEF, "SPD": self.SPD}

    def gain_exp(self, exp):
        """ Adds to EXP total. Returns new EXP total. """
        self.EXP += exp
        # TODO level check
        return self.EXP

    def set_exp(self, exp):
        """ Changes EXP total. Returns new EXP total. """
        self.EXP = exp
        # TODO level check
        return self.EXP


class Mob(Entity):
    def __init__(self, bound_box_size=(20, 20), image_fill="#FF0000", mob_stats=None, exp=1):
        """ bound_box_size = size of the sprite
        image_fill = color code for basic rectangle without sprite
        mob_stats = dictionary of RPG stats, where the keys are strings of the stats and values are ints
        exp = the number of exp the mob entity gives player when killed """
        Entity.__init__(self, bound_box_size=bound_box_size, image_fill=image_fill)
        if mob_stats is None:
            mob_stats = {"ATK": 2, "HP Max": 5, "HP": 5, "DEF": 1, "SPD": 0}
        self.set_stats(mob_stats)
        self.exp_gain = exp
        self.target = None

    def update(self):
        """ Calculate movement of the Mob. """
        self.speed_x = 0
        self.speed_y = 0
        if self.target is not None:
            player_x, player_y = self.target.get_coord()
            mob_x, mob_y = self.get_coord()
            distance_x = player_x - mob_x
            distance_y = player_y - mob_y
            distance = (distance_x**2 + distance_y**2)**0.5
            if distance != 0:
                self.speed_x = 4 * distance_x/distance
                self.speed_y = 4 * distance_y/distance

        super(Mob, self).update()
        # TODO write unique walking behaviors

    def drop_exp(self):
        """ Returns the number of EXP the mob will give player are dying. Used in combat menu. """
        return self.exp_gain

    def set_target(self, player):
        self.target = player
        return self.target

    def get_target(self):
        return self.target

class PassiveMob(Entity):
    def __init__(self, bound_box_size=(20, 20), image_fill="#00FFFF", mob_stats=None):
        Entity.__init__(self, bound_box_size=bound_box_size, image_fill=image_fill)
        if mob_stats is None:
            mob_stats = {"ATK": 2, "HP Max": 5, "HP": 5, "DEF": 1, "SPD": 0}
        self.set_stats(mob_stats)

    def update(self):
        """ Calculate movement of the Mob. """
        super(PassiveMob, self).update()
        # TODO write unique walking behaviors


class Sword(Entity):
    def __init__(self, bound_box_size=(15, 15), image_fill="#FFCC40", sword_attack=None):
        Entity.__init__(self, bound_box_size=bound_box_size, image_fill=image_fill)
        if sword_attack is None:
            sword_attack = {"ATK": 0}
        self.found_player = None
        self.form = "BASE"
        self.set_stats(sword_attack)
        self.EXP = 0

    def update(self):
        """ When in Player's possession, track and follow movement of the Player. Otherwise, do not move. """
        if self.found_player is None:
            self.speed_x = 0
            self.speed_y = 0
        else:
            # Hover beside player
            self.rect.centerx, self.rect.centery = self.found_player.get_coord()
            self.rect.centerx -= 25
            self.rect.centery -= 25
            # super(Sword, self).update()

    def pickup(self, player):
        """ Establishes reference to Player Entity, then starts to follow Player. """
        # Reference Player Entity
        self.found_player = player
        player.pickup_sword(self)
        # new_x, new_y = self.found_player.get_coord()
        self.update()

    def verify(self):
        """ Validates that the Sword is in possession of the Player by returning the Player.
         Otherwise, returns None. """
        return self.found_player

    """def get_stats(self):
        # Return a dictionary of stats
        # TODO should sword affect any stat besides ATK?
        return {"ATK": self.ATK}"""

    def shift_form(self, form):
        """ Given a string of a specified form, changes the sword to that form.
        Used in combination of the SWORD menu. """
        # TODO should change aspects of the sword here. For now, it's only visual
        if form == "BASE":
            self.form = "BASE"
            self.image.fill("#FFCC40")
        if form == "FIRE":
            self.form = "FIRE"
            self.image.fill("#FF0000")
        if form == "ICE":
            self.form = "ICE"
            self.image.fill("#0000FF")
        if form == "DARK":
            self.form = "DARK"
            self.image.fill("#FF00FF")
        return self.form

    def get_form(self):
        return self.form

    def gain_exp(self, exp):
        """ Adds to Sword's EXP total. Returns new EXP total. """
        self.EXP += exp
        # TODO level check
        return self.EXP

    def set_exp(self, exp):
        """ Changes Sword's EXP total. Returns new EXP total. """
        self.EXP = exp
        # TODO level check
        return self.EXP


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
        """ Checks if Player has room in inventory for item. If yes, set reference to Player. """
        picked_up = player.pickup_item(self)
        if picked_up:
            # Player has inventory for item
            self.found_player = player
        return picked_up

    def verify(self):
        """ Validates that the Item is in possession of the Player by returning the Player.
         Otherwise, returns None. """
        return self.found_player

    def use_item(self):
        """ Player selected to use Item from inventory. Determines what type of Item is being used, applies the Item,
        then removes the Item from the player's inventory (if it is finite). """
        if self.type == "HP":
            self.found_player.hp_update(item_dict[self.item_id]["VALUE"])
        self.found_player.lose_item(self)

    def get_name(self):
        """ Returns String name of the item. """
        return self.name



