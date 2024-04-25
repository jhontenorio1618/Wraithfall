import pygame, sys, os
import game_window as WIN
import entity_classes as ENTITY
from battle_menu import Battle, item_menu, sword_menu, item_display_overworld
import pygame.event as EVENTS

from overworld_functions import check_player_death, entity_collision, \
    setup_sprite_groups, spawn_entity, spawn_player, get_sprite_groups

from audio_mixer import load_mixer, play_mixer, pause_mixer, unpause_mixer, stop_mixer

from cutscenes import play_scene, get_scene
from textbox import TextBox, SceneManager

pygame.init()
SCREEN = pygame.display.set_mode(WIN.window_size())
pygame.display.set_caption("debug: player actions")
clock = pygame.time.Clock()

# Sprite Groups

setup_sprite_groups()
"""game_sprites = pygame.sprite.Group()
mob_sprites = pygame.sprite.Group()
mob_vision_sprites = pygame.sprite.Group()
item_sprites = pygame.sprite.Group()
sword_sprite = pygame.sprite.Group()
gui_sprites = pygame.sprite.Group()
grandpa_sprites = pygame.sprite.Group()
sprite_groups = {"Game": game_sprites, "Mob": mob_sprites, "Mob Vision": mob_vision_sprites,
                 "Item": item_sprites, "Sword": sword_sprite, "GUI": gui_sprites, "Grandpa": grandpa_sprites}"""

"""
def spawn_entity(new_entity, entity_type, spawn_xy=(None, None)):
    sprite_groups[entity_type].add(new_entity)
    game_sprites.add(new_entity)
    new_entity.warp(x=spawn_xy[0], y=spawn_xy[1])
    return new_entity
"""

player = spawn_player()

"""
# Player Entity
player = ENTITY.Player()
player.warp(WIN.WIN_WIDTH/2, WIN.WIN_HEIGHT/2)
game_sprites.add(player)
"""

# Mob Entities
for i in range(5):
    dummy_wraith = spawn_entity(ENTITY.Mob(), "Mob")
    # dummy_box = spawn_entity(ENTITY.BoundingBox(bound_box_size=(225, 225)), "Mob Vision")
    # dummy_box.set_entity(dummy_wraith)
    dummy_wraith.set_speed(0, 0)
BOSS_wraith = spawn_entity(ENTITY.Mob(mob_id=1), "Mob", spawn_xy=(WIN.WIN_WIDTH/2, WIN.WIN_HEIGHT - 150), override_mob_vision=True)

# Sword Entity
sword = spawn_entity(ENTITY.Sword(), "Sword", spawn_xy=(WIN.WIN_WIDTH/2, WIN.WIN_HEIGHT/2 - 75))

# Grandpa
grandpa = spawn_entity(ENTITY.NPC(npc_id=0), "NPC", spawn_xy=(WIN.WIN_WIDTH/2, WIN.WIN_HEIGHT/2 - 35))
deer = spawn_entity(ENTITY.NPC(npc_id=1), "NPC", spawn_xy=(WIN.WIN_WIDTH/2, WIN.WIN_HEIGHT/2 + 70))

# Item Entities
for i in range(10):
    index = i % 7
    healing_item = spawn_entity(ENTITY.Item(item_id=index), "Item", spawn_xy=(WIN.WIN_WIDTH/2 + 30 + i*15, WIN.WIN_HEIGHT/2))

all_warps = pygame.sprite.Group()


sprite_groups = get_sprite_groups()



test_entity_text_lines = [
    TextBox("Let's practice safety training, Oliver. Press [ENTER] to start.", "Grandpa", "Happy"),
]
combat_menu_text_lines = [
    TextBox("Careful, Oliver.", "Grandpa", "Neutral"),
]
test_entity_scene = SceneManager(test_entity_text_lines, "text_sound.wav")
combat_menu_scene = SceneManager(combat_menu_text_lines, "text_sound.wav")


load_mixer("backgroundmusic1.wav")
play_mixer(-1)
# pygame.mixer.music.load(os.path.join(WIN.DIR_MUSIC, "backgroundmusic1.wav"))
# pygame.mixer.music.play(-1) #makes music continue to loop


# Game Loop
looping = True
combat_invul = False
invul_time = 0
playing_cutscene = True
current_cutscene = test_entity_scene
first_battle = True

""" Make trigger for cutscenes using collision. """
collide_to_cutscenes = []
cutscene_coordinates = [(50, 10), (100, 10), (150, 10), (200, 10), (250, 10),
                        (300, 10), (350, 10), (400, 10), (450, 10), (500, 10),
                        (550, 10)]
for i in range(11):
    cutscene_zone = spawn_entity(ENTITY.BoundingBox(bound_box_size=(10,10), fill_color="#FFFFFF"),
                                 "Scene", spawn_xy=cutscene_coordinates[i])
    scene_trigger = pygame.sprite.Group()
    scene_trigger.add(cutscene_zone)
    scene_id = i + 1
    collide_to_cutscenes.append([scene_trigger, scene_id])


def check_cutscene_trigger(player, collision_box_list):
    # scene_id = 1
    current_scene = None
    playing_cutscene = False
    for scene_collide, scene_index in collision_box_list:
        player_scene_collide = pygame.sprite.spritecollide(player, scene_collide, True)
        if player_scene_collide:
            current_scene = get_scene(scene_index)
            playing_cutscene = True
    return current_scene, playing_cutscene



while looping:
    # Updating reference to sprite groups
    sprite_groups = get_sprite_groups()
    clock.tick(WIN.get_fps())
    # Input Events
    for event in EVENTS.get():
        if event.type == pygame.KEYDOWN:
            # Escape Key
            if event.key == pygame.K_ESCAPE:
                WIN.game_exit()
            if not playing_cutscene:
                # Overworld Controls

                # G key
                if event.key == pygame.K_g:
                    # Access Sword Menu
                    if player.access_sword() is not None:
                        sword_menu(player)
                # Q key
                if event.key == pygame.K_q:
                    player.scroll_inv(-1)
                    if player.inventory:
                        # TODO printing to terminal is temp, only for debugging purposes
                        print(str(player.inventory_pointer) + ": " + str(player.inventory[player.inventory_pointer].get_name()))
                # E key
                if event.key == pygame.K_e:
                    player.scroll_inv(1)
                    if player.inventory:
                        # TODO printing to terminal is temp, only for debugging purposes
                        print(str(player.inventory_pointer) + ": " + str(player.inventory[player.inventory_pointer].get_name()))
                # F key
                if event.key == pygame.K_f:
                    selected_item = player.access_item()
                    if selected_item is not None:
                        selected_item.use_item()
            else:
                # Cutscene Controls

                # Enter key
                if event.key == pygame.K_RETURN:
                    playing_cutscene = not current_cutscene.next_textbox()

        # check click on window exit button
        if event.type == pygame.QUIT:
            WIN.game_exit()
    # Update game sprites
    if not playing_cutscene:
        sprite_groups["Game"].update()

        combat_invul, invul_time = entity_collision(player, sprite_groups, combat_invul=combat_invul, invul_time=invul_time,
                                                    combat_cutscene=combat_menu_scene)

    check_player_death(player, SCREEN)

    SCREEN.fill("#483b46")
    sprite_groups["Game"].draw(SCREEN)
    if not playing_cutscene:
        # TODO GUI code here
        item_display_overworld(player, sprite_groups["Game"], sprite_groups["GUI"])
        sprite_groups["GUI"].draw(SCREEN)

        # Seeing if player found a cutscene zone
        current_cutscene, playing_cutscene = check_cutscene_trigger(player, collide_to_cutscenes)


    playing_cutscene = play_scene(current_cutscene, playing_cutscene)
    if not playing_cutscene and current_cutscene is not None:
        current_cutscene = None
        
    if playing_cutscene or current_cutscene is not None:
        pause_mixer()
    else:
        unpause_mixer()
        
        
    # print(playing_cutscene)
    # update the display window...
    
    pygame.display.update()
    
    
stop_mixer()

