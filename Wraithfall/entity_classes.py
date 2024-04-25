import pygame
from game_window import random, WIN_WIDTH, DIR_SPRITES, WIN_HEIGHT, scale_to_screen as stsc
import os
from view_spritesheets import collect_frames


def get_universal_scale():
    return stsc(3)


class BoundingBox(pygame.sprite.Sprite):
    """ Bounding Boxes spawned in the game to allow for a particular effect to happen in specified location.
    For example: mob detection radius, area to apply particular effect, etc. """

    def __init__(self, bound_box_size=(100, 100), fill_color="#FF00FF", entity_anchor=None, location_coord=(WIN_WIDTH, WIN_HEIGHT)):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(stsc(bound_box_size))
        trans_color = "#FF00FF"
        self.image.fill(fill_color)
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
            self.rect.centerx = random.randrange(WIN_WIDTH - self.rect.width)
        else:
            self.rect.centerx = x
        if y is None:
            self.rect.centery = random.randrange(WIN_HEIGHT - self.rect.height)
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
        self.image = pygame.Surface(stsc(bound_box_size))
        self.image.fill(image_fill)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIN_WIDTH
        self.rect.centery = WIN_HEIGHT
        self.speed_x = 0
        self.speed_y = 0
        self.bb_anchor = None
        self.name = ""
        # RPG Stats
        self.HP_Max = 1
        self.HP = 1
        self.ATK = 1
        self.DEF = 1
        self.SPD = 0

    def update(self):
        """ Calculate movement of the Entity. """
        self.rect.centerx += stsc(self.speed_x)
        self.rect.centery += stsc(self.speed_y)

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
            self.rect.centerx = random.randrange(WIN_WIDTH - self.rect.width)
        else:
            self.rect.centerx = x
        if y is None:
            self.rect.centery = random.randrange(WIN_HEIGHT - self.rect.height)
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

    def get_name(self):
        return self.name

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


""" Keys: Current Level of Player
    Values: Stored in a dictionary
        BASE EXP: Minimum total EXP needed for current level (same as previous NEXT LVL, or 0 if level 1)
        GOAL EXP: Total EXP needed to reach next level
        STATS: Dictionary of stats for player's corresponding level """
level_dict = {1: {"BASE EXP": 0, "GOAL EXP": 5, "STATS": {"ATK": 2, "HP Max": 10, "HP": 10, "DEF": 1, "SPD": 0}},
              2: {"BASE EXP": 5, "GOAL EXP": 15, "STATS": {"ATK": 3, "HP Max": 15, "HP": 15, "DEF": 2, "SPD": 0}},
              3: {"BASE EXP": 15, "GOAL EXP": 30, "STATS": {"ATK": 5, "HP Max": 20, "HP": 20, "DEF": 3, "SPD": 0}},
              4: {"BASE EXP": 30, "GOAL EXP": 50, "STATS": {"ATK": 6, "HP Max": 25, "HP": 25, "DEF": 4, "SPD": 0}},
              5: {"BASE EXP": 50, "GOAL EXP": 9999999999, "STATS": {"ATK": 8, "HP Max": 30, "HP": 30, "DEF": 5, "SPD": 0}},}


class Player(Entity):
    def __init__(self, bound_box_size=(30, 30), image_fill="#FFFFFF", player_stats=None):
        super().__init__()  # Initialize the base class (Entity)
        self.images = {'forward': [0, 1, 2, 3], 'backward': [4, 5, 6, 7], 'right': [8, 9, 10, 11], 'left': [8, 9, 10, 11]}
        self.current_frame = 0
        self.animation_speed = 0.1
        self.last_update = pygame.time.get_ticks()
        self.load_spritesheets(sprite_sheet="MCSPRITESHEET.png", dimensions=(14, 17, 2))
        self.image = self.images['forward'][self.current_frame]
        self.rect = self.image.get_rect()
        self.direction = 'forward'
        if player_stats is None:
            # Default Player Stats if none are given to initialize.
            player_stats = {"ATK": 2, "HP Max": 10, "HP": 10, "DEF": 1, "SPD": 0}
        self.name = "Oliver"
        self.found_sword = None
        self.inventory = []
        self.inventory_max = 10
        self.inventory_pointer = 0
        self.set_stats(player_stats)
        self.LVL = 1
        self.EXP = 0
        self.hunger = 100

    def load_spritesheets(self, sprite_sheet, dimensions):
        mc_sheet = pygame.image.load(os.path.join(DIR_SPRITES, "MCSPRITESHEET.png")).convert_alpha()
        frame_width = 14
        frame_height = 17
        scale = get_universal_scale()
        # Load all frames for each direction
        all_frames = collect_frames(mc_sheet, 12, frame_width, frame_height, scale)

        # Splits the frames into forward, backward, right, and left directions
        self.images['forward'] = all_frames[:3]
        self.images['backward'] = all_frames[4:7]
        self.images['right'] = all_frames[8:11]
        self.images['left'] = [pygame.transform.flip(frame, True, False) for frame in self.images['right']]

    def animate_walking(self):
        self.update()

    def update(self, collision_check_function=None):
        """ Update the player's position and animation. """
        now = pygame.time.get_ticks()
        if now - self.last_update > self.animation_speed * 1000:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.images[self.direction])
            self.image = self.images[self.direction][self.current_frame]

        key_state = pygame.key.get_pressed()
        self.speed_x = 0
        self.speed_y = 0
        # Diagonal movement
        if key_state[pygame.K_LEFT] and key_state[pygame.K_UP]:
            self.speed_x = -5
            self.speed_y = -5
            self.direction = 'left'
        elif key_state[pygame.K_RIGHT] and key_state[pygame.K_UP]:
            self.speed_x = 5
            self.speed_y = -5
            self.direction = 'right'
        elif key_state[pygame.K_LEFT] and key_state[pygame.K_DOWN]:
            self.speed_x = -5
            self.speed_y = 5
            self.direction = 'left'
        elif key_state[pygame.K_RIGHT] and key_state[pygame.K_DOWN]:
            self.speed_x = 5
            self.speed_y = 5
            self.direction = 'right'
        # Regular movement
        if key_state[pygame.K_LEFT]:
            self.speed_x = -5
            self.direction = 'left'
        elif key_state[pygame.K_RIGHT]:
            self.speed_x = 5
            self.direction = 'right'
        elif key_state[pygame.K_UP]:
            self.speed_y = -5
            self.direction = 'backward'
        elif key_state[pygame.K_DOWN]:
            self.speed_y = 5
            self.direction = 'forward'
        new_position = self.rect.move(self.speed_x, self.speed_y)

        if collision_check_function is not None and collision_check_function(new_position):
            # Testing collision
            print("Collision detected, movement blocked.")

            self.speed_x = 0
            self.speed_y = 0
        else:
            # Update position if no collision
            self.rect = new_position

        if not any([key_state[pygame.K_LEFT], key_state[pygame.K_RIGHT], key_state[pygame.K_UP],
                    key_state[pygame.K_DOWN]]):
            self.current_frame = 0
            self.image = self.images[self.direction][self.current_frame]
        # super(Player, self).update()
        # self.rect.x += self.speed_x
        # self.rect.y += self.speed_y

    def access_sword(self):
        """ Returns Sword if the player has it. Otherwise, returns None. """
        return self.found_sword

    def pickup_sword(self, sword):
        """ Connects picked up sword to player. Run by Sword Entity's pickup() method. """
        self.found_sword = sword

    def access_item(self, pointer=None):
        """ Given inventory index (pointer),
        retrieve reference to the item in inventory as long as one exists. """
        # print("inventory pointer check 0: " + str(self.inventory_pointer))
        if pointer is not None:
            self.inventory_pointer = 0
            self.scroll_inv(pointer)
            # print("inventory pointer check 1: " + str(self.inventory_pointer))
        using_item = None
        if self.inventory_pointer > len(self.inventory) - 1:
            self.inventory_pointer = 0
        if self.inventory_pointer < 0:
            self.inventory_pointer = len(self.inventory) - 1
        # print("inventory pointer check 2: " + str(self.inventory_pointer))
        if self.inventory and self.inventory[self.inventory_pointer]:
            using_item = self.inventory[self.inventory_pointer]
        return using_item

    def check_inventory(self):
        has_items = False
        if self.inventory:
            has_items = True
        return has_items

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

    def get_exp(self, for_next_lvl=False, base_exp_of_lvl=False):
        base_exp = level_dict[self.LVL]["BASE EXP"]
        goal_exp = level_dict[self.LVL]["GOAL EXP"]
        if for_next_lvl:
            needed_exp = goal_exp - base_exp
            current_exp = self.EXP - base_exp
            return current_exp, needed_exp
        elif base_exp_of_lvl:
            return base_exp
        else:
            return self.EXP

    def gain_exp(self, exp):
        """ Adds to EXP total. Returns new EXP total. """
        self.EXP += exp
        # Level Up
        while self.EXP >= level_dict[self.LVL]["GOAL EXP"]:
            self.LVL += 1
            self.set_stats(level_dict[self.LVL]["STATS"])
        # TODO Remove Debug
        print("Level: " + str(self.LVL) +
              "\nEXP Total: " + str(self.EXP) + "/" + str(level_dict[self.LVL]["GOAL EXP"]))
        return self.EXP

    def set_exp(self, exp):
        """ Changes EXP total. Returns new EXP total. """
        # Adjust Level to new  EXP total
        if self.EXP > exp:
            while self.EXP < level_dict[self.LVL]["BASE EXP"]:
                self.LVL -= 1
        elif self.EXP < exp:
            while self.EXP >= level_dict[self.LVL]["GOAL EXP"]:
                self.LVL += 1
        self.set_stats(level_dict[self.LVL]["STATS"])
        self.EXP = exp
        return self.EXP


""" Keys: Unique ID of Mob to call it
    Values: Stored in a dictionary
        NAME: In-game name of the Mob (can repeat for higher-leveled versions of the same type of Mob)
        STATS: Dictionary of stats {ATK, HP Max, HP, DEF, SPD} to set as Mob's stats
        EXP: Number of EXP given to player for killing mob
        SPRITE: Reference to sprite sheet for the mob """
mob_dict = {0: {"NAME": "Wraith", "STATS": {"ATK": 2, "HP Max": 3, "HP": 3, "DEF": 1, "SPD": 0},
                "EXP": 2, "SPRITE": "WRAITH1SPRITESHEET.png"},
            1: {"NAME": "[Boss Wraith]", "STATS": {"ATK": 2, "HP Max": 10, "HP": 10, "DEF": 10, "SPD": 0},
                "EXP": 50, "SPRITE": "BOSSWRAITHSPRITESHEET.png"},
            2: {"NAME": "Wraithsoul", "STATS": {"ATK": 2, "HP Max": 3, "HP": 3, "DEF": 1, "SPD": 0},
                "EXP": 2, "SPRITE": "WRAITHSOULSPRITESHEET.PNG"},
            3: {"NAME": "[Med Wraith 2]", "STATS": {"ATK": 2, "HP Max": 3, "HP": 3, "DEF": 1, "SPD": 0},
                "EXP": 2, "SPRITE": "WRAITH3SPRITESHEET.png"},
            4: {"NAME": "[Hard Wraith]", "STATS": {"ATK": 2, "HP Max": 3, "HP": 3, "DEF": 1, "SPD": 0},
                "EXP": 2, "SPRITE": "WRAITH2SPRITESHEET.png"}}

mob_sprite_data = {"WRAITH1SPRITESHEET.png":
                    {'f': [0, 7], 'b': [8, 15], 'r': [16,23], 'dimensions': [18, 20], 'total': 24},
                   "WRAITHSOULSPRITESHEET.PNG":
                       {'f': [0, 3], 'b': [4, 7], 'r': [8, 11],
                          'dimensions': [17, 17], 'total': 12},
                   "WRAITH3SPRITESHEET.png":
                         {'f': [0, 3], 'b': [4, 7],
                          # 'r': [4, 7], 'l': [0, 3],
                          'dimensions': [17, 20], 'total': 8},
                   "WRAITH2SPRITESHEET.png":
                         {'f': [0, 4], 'b': [5, 9],
                          # 'r': [5, 9], 'l': [0, 4],
                          'dimensions': [17, 20], 'total': 10},
                   "BOSSWRAITHSPRITESHEET.png":
                       {'f': [0, 5], 'b': [0, 5],
                        # 'r': [5, 9], 'l': [0, 4],
                        'dimensions': [59, 52], 'total': 5},
                   }


class Mob(Entity):
    def __init__(self, bound_box_size=(20, 20), image_fill="#FF0000", mob_id=0):
        """ bound_box_size = size of the sprite
        image_fill = color code for basic rectangle without sprite
        mob_stats = dictionary of RPG stats, where the keys are strings of the stats and values are ints
        exp = the number of exp the mob entity gives player when killed """
        # Entity.__init__(self, bound_box_size=bound_box_size, image_fill=image_fill)
        super().__init__()  # Initialize the base class (Entity)
        if mob_id not in mob_dict:
            mob_id = 0
        self.mob_id = mob_id
        self.sprite_sheet = mob_dict[self.mob_id]["SPRITE"]
        self.images = mob_sprite_data[self.sprite_sheet]
        sprite_data = mob_sprite_data[self.sprite_sheet]
        self.current_frame = 0
        self.animation_speed = 0.1
        self.last_update = pygame.time.get_ticks()
        self.load_spritesheets(sprite_sheet=self.sprite_sheet, dimensions=sprite_data["dimensions"], sprite_data=sprite_data)
        self.direction = 'forward'
        self.image = self.images['forward'][self.current_frame]
        self.rect = self.image.get_rect()
        self.mob_val = mob_dict[mob_id]
        self.name = self.mob_val["NAME"]
        self.set_stats(self.mob_val["STATS"])
        self.exp_gain = self.mob_val["EXP"]
        self.target = None
        
    def load_spritesheets(self, sprite_sheet, dimensions, sprite_data):
        wraith_sheet = pygame.image.load(os.path.join(DIR_SPRITES, sprite_sheet)).convert_alpha()
        frame_width = dimensions[0]
        frame_height = dimensions[1]
        scale = get_universal_scale()
        #Load all frames for each direction
        all_frames = collect_frames(wraith_sheet, sprite_data["total"], frame_width, frame_height, scale)
        # Splits the frames into forward, backward, right, and left directions
        f = sprite_data["f"]
        self.images['forward'] = all_frames[f[0]:f[1]]
        b = sprite_data["b"]
        self.images['backward'] = all_frames[b[0]:b[1]]
        if "r" in sprite_data:
            r = sprite_data["r"]
            self.images['right'] = all_frames[r[0]:r[1]]
        else:
            self.images['right'] = all_frames[b[0]:b[1]]
        if "l" in sprite_data:
            l = sprite_data["l"]
            self.images['left'] = all_frames[l[0]:l[1]]
        elif "r" in sprite_data:
            self.images['left'] = [pygame.transform.flip(frame, True, False) for frame in self.images['right']]
        else:
            self.images['left'] = all_frames[f[0]:f[1]]
        
    def update(self, collision_check_function=None):
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
        self.update_sprite(self.speed_x, self.speed_y)
        super(Mob, self).update()
        # TODO write unique walking behaviors

    def update_sprite(self, speed_x, speed_y):
        """ Update the player's position and animation. """
        now = pygame.time.get_ticks()
        animation_interval = 100  # Constant factor for animation speed
        if now - self.last_update > animation_interval:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.images[self.direction])
            self.image = self.images[self.direction][self.current_frame]

        # Diagonal movement
        move_sensitivity = 2
        if speed_y <= -move_sensitivity:
            # self.speed_x = -5
            # self.speed_y = -5
            self.direction = 'backward'
        elif speed_y >= move_sensitivity:
            # self.speed_x = 5
            # self.speed_y = -5
            self.direction = 'forward'
        elif speed_x <= -move_sensitivity: # and speed_y > 1:
            # self.speed_x = -5
            # self.speed_y = 5
            self.direction = 'left'
        elif speed_x >= move_sensitivity: # and speed_y > 1:
            # self.speed_x = 5
            # self.speed_y = 5
            self.direction = 'right'

        if speed_x == 0 and speed_y == 0:
            self.current_frame = 0
            self.image = self.images[self.direction][self.current_frame]

    def drop_exp(self):
        """ Returns the number of EXP the mob will give player are dying. Used in combat menu. """
        return self.exp_gain

    def set_target(self, player):
        self.target = player
        return self.target

    def get_target(self):
        return self.target


npc_dict = {0: {"NAME": "Grandpa", "SPRITE": "GRANDPAspritesheet.png",
                "dimensions": (17, 17, get_universal_scale()), "total": 12},
            1: {"NAME": "Deer", "SPRITE": "DEERSPRITEsheet.png",
                "dimensions": (23, 20, get_universal_scale()), "total": 6}}


class NPC(Entity):
    def __init__(self, bound_box_size=(20, 20), image_fill="#00FFFF", npc_id=0):
        # Entity.__init__(self, bound_box_size=bound_box_size, image_fill=image_fill)
        super().__init__()  # Initialize the base class (Entity)
        if npc_id not in npc_dict:
            npc_id = 0
        self.npc_id = npc_id
        self.images = {'forward': [0, 1, 2, 3], 'backward': [4, 5, 6, 7], 'right': [8, 9, 10, 11], 'left': [8, 9, 10, 11]}
        self.current_frame = 0
        self.animation_speed = 0.1
        self.last_update = pygame.time.get_ticks()
        self.sprite_sheet = npc_dict[self.npc_id]["SPRITE"]
        self.load_spritesheets(sprite_sheet=self.sprite_sheet, dimensions=npc_dict[self.npc_id]["dimensions"],
                               sprite_total=npc_dict[self.npc_id]["total"])
        self.image = self.images['forward'][self.current_frame]
        self.rect = self.image.get_rect()
        self.direction = 'forward'

        npc_stats = {"ATK": 2, "HP Max": 5, "HP": 5, "DEF": 1, "SPD": 0}
        self.set_stats(npc_stats)

    def update(self):
        """ Calculate movement of the Mob. """
        if self.npc_id == 1:
            now = pygame.time.get_ticks()
            if now - self.last_update > self.animation_speed * 5000:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.images[self.direction])
                self.image = self.images[self.direction][self.current_frame]

        super(NPC, self).update()
        # TODO write unique walking behaviors

    def load_spritesheets(self, sprite_sheet, dimensions, sprite_total):
        sheet = pygame.image.load(os.path.join(DIR_SPRITES, sprite_sheet)).convert_alpha()
        frame_width = dimensions[0]
        frame_height = dimensions[1]
        scale = dimensions[2]
        # Load all frames for each direction
        all_frames = collect_frames(sheet, sprite_total, frame_width, frame_height, scale)

        # Splits the frames into forward, backward, right, and left directions
        self.images['forward'] = all_frames[:3]
        self.images['backward'] = all_frames[4:7]
        self.images['right'] = all_frames[8:11]
        self.images['left'] = [pygame.transform.flip(frame, True, False) for frame in self.images['right']]


class Sword(Entity):
    def __init__(self, bound_box_size=(15, 15), image_fill="#FFCC40", sword_attack=None):
        # Entity.__init__(self, bound_box_size=bound_box_size, image_fill=image_fill)
        super().__init__()  # Initialize the base class (Entity)
        if sword_attack is None:
            sword_attack = {"ATK": 0}
        self.found_player = None
        self.form = "BASE"
        self.set_stats(sword_attack)
        self.EXP = 0
        self.images = {'forward': [0, 1, 2, 3, 4, 5, 6, 7], 'backward': [8, 9, 10, 11, 12, 13, 14, 15]}
        self.current_frame = 0
        self.animation_speed = 0.13
        self.last_update = pygame.time.get_ticks()
        self.load_spritesheets("SWORDspritesheet.png")
        self.direction = 'forward'
        self.image = self.images['forward'][self.current_frame]
        self.rect = self.image.get_rect()

    def load_spritesheets(self, sprite_sheet):
        sword_sheet = pygame.image.load(os.path.join(DIR_SPRITES, sprite_sheet)).convert_alpha()
        frame_width = 17
        frame_height = 17
        scale = get_universal_scale()

        # Load all frames for each direction
        all_frames = collect_frames(sword_sheet, 16, frame_width, frame_height, scale)

        # Splits the frames into forward, backward, right, and left directions
        self.images['forward'] = all_frames[:7]
        self.images['backward'] = all_frames[8:]
        self.images['right'] = all_frames[:7]
        self.images['left'] = [pygame.transform.flip(frame, True, False) for frame in self.images['right']]

    def update(self):
        """ When in Player's possession, track and follow movement of the Player. Otherwise, do not move. """
        now = pygame.time.get_ticks()
        animation_interval = 100  # Constant factor for animation speed
        if now - self.last_update > animation_interval:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.images[self.direction])
            self.image = self.images[self.direction][self.current_frame]

        if self.found_player is not None:
            # Get the player's key presses to determine the sword's direction
            player_key_state = pygame.key.get_pressed()
            if player_key_state[pygame.K_LEFT] and player_key_state[pygame.K_UP]:
                self.direction = 'backward'
            elif player_key_state[pygame.K_RIGHT] and player_key_state[pygame.K_UP]:
                self.direction = 'backward'
            elif player_key_state[pygame.K_LEFT] and player_key_state[pygame.K_DOWN]:
                self.direction = 'forward'
            elif player_key_state[pygame.K_RIGHT] and player_key_state[pygame.K_DOWN]:
                self.direction = 'forward'
            elif player_key_state[pygame.K_LEFT]:
                self.direction = 'left'
            elif player_key_state[pygame.K_RIGHT]:
                self.direction = 'right'
            elif player_key_state[pygame.K_UP]:
                self.direction = 'backward'
            elif player_key_state[pygame.K_DOWN]:
                self.direction = 'forward'

            # Calculate the offset based on the player's direction
            offset = (-30, -30)
            if self.direction == 'left':
                offset = (15, -30)
            elif self.direction == 'backward':
                offset = (-25, 40)
            elif self.direction == 'right' or self.direction == 'forward':
                offset = (-25, -30)

            # Interpolate the sword's position towards the target position
            speed = 0.11
            self.rect.centerx += int((self.found_player.rect.centerx + offset[0] - self.rect.centerx) * speed)
            self.rect.centery += int((self.found_player.rect.centery + offset[1] - self.rect.centery) * speed)

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
            self.load_spritesheets("SWORDspritesheet.png")
            # self.image.fill("#FFCC40")
        if form == "FIRE":
            self.form = "FIRE"
            self.load_spritesheets("FIRESWORDspritesheet.png")
            # self.image.fill("#FF0000")
        if form == "ICE":
            self.form = "ICE"
            self.load_spritesheets("ICESWORDspritesheet.png")
            # self.image.fill("#0000FF")
        if form == "DARK":
            self.form = "DARK"
            self.load_spritesheets("DARKSWORDspritesheet.png")
            # self.image.fill("#FF00FF")
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


""" Keys: Unique ID of Item to call it
    Values: Stored in a dictionary
        NAME: In-game name of the Item
        TYPE: Distinguishes what type of STAT the item affects. If SWORD, means it is an item for the Sword
        VALUE: The numeric effect the item has on the relevant stat disclosed in TYPE (does not appear for "SWORD" type)
        SPRITE: Reference to sprite sheet for the item """
item_dict = {0: {"NAME": "Bandage", "TYPE": "HP", "VALUE": 20, "SPRITE": "BANDAGEsprite.png"},
             1: {"NAME": "Fire Essence", "TYPE": "SWORD", "SPRITE": "FIREESSENCEsprite.png"},
             2: {"NAME": "Ice Essence", "TYPE": "SWORD", "SPRITE": "ICEESSENCEsprite.png"},
             3: {"NAME": "Dark Essence", "TYPE": "SWORD", "SPRITE": "DARKESSENCEsprite.png"},
             4: {"NAME": "Dirty Bandage", "TYPE": "HP", "VALUE": 5, "SPRITE": "DIRTYBANDAGEsprite.png"},
             5: {"NAME": "Apple", "TYPE": "HP", "VALUE": 10, "SPRITE": "APPLEsprite.png"}, # TODO apple sprite
             6: {"NAME": "Deer Meat", "TYPE": "HP", "VALUE": 30, "SPRITE": "DEERMEATsprite.png"} # TODO deer sprite
             }

item_sprite_data = {"BANDAGEsprite.png":
                       {'dimensions': [19, 12], 'total': 1},
                    "DIRTYBANDAGEsprite.png":
                        {'dimensions': [18, 12], 'total': 1},
                   "FIREESSENCEsprite.png":
                       {'dimensions': [14, 17], 'total': 1},
                   "ICEESSENCEsprite.png":
                        {'dimensions': [14, 15], 'total': 1},
                   "DARKESSENCEsprite.png":
                        {'dimensions': [14, 17], 'total': 1},
                    "APPLEsprite.png":
                        {'dimensions': [18, 12], 'total': 1}, # TODO apple sprite dimensions
                    "DEERMEATsprite.png":
                        {'dimensions': [16, 17], 'total': 1}, # TODO deer meat sprite dimensions
                   }

class Item(Entity):
    def __init__(self, bound_box_size=(15, 15), image_fill="#00FF00", item_id=0):
        #Entity.__init__(self, bound_box_size=bound_box_size, image_fill=image_fill)
        super().__init__()
        self.found_player = None
        if item_id not in item_dict:
            item_id = 0
        self.item_id = item_id
        self.sprite_sheet = item_dict[self.item_id]["SPRITE"]
        self.images = {'forward': [0]}
        sprite_data = item_sprite_data[self.sprite_sheet]
        self.current_frame = 0
        self.load_spritesheets(sprite_sheet=self.sprite_sheet, dimensions=sprite_data["dimensions"], sprite_data=sprite_data)
        self.direction = 'forward'
        self.image = self.images['forward'][0]
        self.rect = self.image.get_rect()
        self.item_val = item_dict[item_id]
        self.name = self.item_val["NAME"]
        self.type = self.item_val["TYPE"]
        # self.load_spritesheet()

    def load_spritesheets(self, sprite_sheet, dimensions, sprite_data):
        item_sheet = pygame.image.load(os.path.join(DIR_SPRITES, sprite_sheet)).convert_alpha()
        frame_width = dimensions[0]
        frame_height = dimensions[1]
        scale = get_universal_scale()
        #Load all frames for each direction
        all_frames = collect_frames(item_sheet, sprite_data["total"], frame_width, frame_height, scale)
        # Splits the frames into forward, backward, right, and left directions
        self.images['forward'] = all_frames[0:1]
        self.images['backward'] = all_frames[0:1]
        self.images['right'] = all_frames[0:1]
        self.images['left'] = all_frames[0:1]


    def draw(self, screen):
        screen.blit(self.frames[self.name][0], (self.rect.x, self.rect.y))


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
            self.found_player.hp_update(self.item_val["VALUE"])
        self.found_player.lose_item(self)
        self.found_player = None

