import pygame, sys, os
import game_window as WIN
from button import Button
from pytmx.util_pygame import load_pygame
import pytmx
from pytmx.util_pygame import load_pygame
import pygame, sys, os
import entity_classes as ENTITY
from battle_menu import Battle
import pygame.event as EVENTS

# import mainmenu

'''
The 'GameClass' class serves as the central hub for managing the game's core functionalities.
 It encapsulates all the necessary components and behaviors required for running the game's main loop.
 This includes initializing the game window, preparing the screen for rendering, navigating through the main menu, starting the game itself, and handling game termination.

To utilize this class effectively, it must be instantiated and used within the main entry point of the game's codebase — typically the main function or the main game loop.
By doing so, this class orchestrates the flow of the game from start to finish,
 delegating responsibilities to specialized methods for each significant part of the game's lifecycle.
Each method within the 'PlayGame' class is designed to perform distinct actions:
- 'prepare_screen' readies the display for the game.
- 'main_menu' handles the logic for displaying and interacting with the game's main menu.
- 'start_game' kicks off the actual gameplay.
- 'quit_game' ensures a clean exit from the game.
Importing and using this class in the main function is essential for starting the game and tying together all the elements of gameplay.
'''

pygame.font.init()  # Initialize the font module specifically

SCREEN = pygame.display.set_mode (WIN.window_size ())
pygame.display.set_caption ("Menu")

MENU_TITLE = pygame.image.load (os.path.join (WIN.DIR_IMAGES, "WRAITHFALL_TITLE.png")).convert_alpha ()

# Background
BG = pygame.image.load (os.path.join (WIN.DIR_IMAGES, "menu_screen.jpeg")).convert ()

# Set size for image
DEFAULT_MENU_BACKGROUND_IMAGE_SIZE = (1280, 720)

# scale image
BG = pygame.transform.scale (BG, DEFAULT_MENU_BACKGROUND_IMAGE_SIZE)

# Set a position
DEFAULT_BACKGROUND_IMAGE_POSITION = (640, 360)


def get_font(size):
    return pygame.font.Font (os.path.join (WIN.DIR_FONTS, "grand9Kpixel.ttf"), size)
class GameClass:

    def __int__(self, screen):
        self.screen = screen

    # todo  main_menu and play -> this functions done by Madusin Crank
    def main_menu(self,func):
        self.func= func

        if func == 'menu':
            while True:
                SCREEN.blit (BG, (0, 0))
                MENU_MOUSE_POS = pygame.mouse.get_pos ()
                MENU_TEXT = get_font (150).render (" ", True, "#C2D7E7")
                MENU_RECT = MENU_TEXT.get_rect (center=(640, 100))

                SCREEN.blit (MENU_TITLE, (0, 0))  # Blit the title image
                SCREEN.blit (MENU_TEXT, MENU_RECT)

                PLAY_BUTTON = Button (image=None, pos=(640, 400),
                                      text_input="PLAY", font=get_font (75), base_color="#FFFFFF",
                                      hovering_color="#A90505")
                QUIT_BUTTON = Button (image=None, pos=(640, 500),
                                      text_input="QUIT", font=get_font (75), base_color="#FFFFFF",
                                      hovering_color="#A90505")
                SCREEN.blit (MENU_TEXT, MENU_RECT)
                for button in [PLAY_BUTTON, QUIT_BUTTON]:
                    button.changeColor (MENU_MOUSE_POS)
                    button.update (SCREEN)
                for event in pygame.event.get ():
                    if event.type == pygame.QUIT:
                        pygame.quit ()
                        sys.exit ()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if PLAY_BUTTON.checkForInput (MENU_MOUSE_POS):
                            self.start_game ('play')
                        if QUIT_BUTTON.checkForInput (MENU_MOUSE_POS):
                            pygame.quit ()
                            sys.exit ()
                pygame.display.update ()
        # mainmenu.main_menu ()

    # prepare screen -> load the file that contains the map and prepare it to the main function.
    def prepareMapScreen(self, tmxFile):
        self.tmxFile = tmxFile
        # the first map should be imported to this variable
        tmxFile = load_pygame (tmxFile)
        return tmxFile

    def draw_map(self,screenMap, tiled_map):
        self.screenMap = screenMap
        self.tiled_map=tiled_map
        # draw the map to the Pygame screen
        for layer in tiled_map.visible_layers:
            if isinstance (layer, pytmx.TiledTileLayer):
                for x, y, gid, in layer:
                    tile = tiled_map.get_tile_image_by_gid (gid)
                    if tile:
                        screenMap.blit (tile, (x * tiled_map.tilewidth, y * tiled_map.tileheight))

    # command such as play, Quit,  GameOVER, OR RESTART
    def start_game(self, command):


        self.command = command

        if command == 'play':
            paused = False
            pygame.init ()
            while True:
                PLAY_MOUSE_POSITION = pygame.mouse.get_pos ()
                screen = pygame.display.set_mode ((1200, 960))

                # tm = load_map ('Map/GameMap.tmx')
                tm = self.prepareMapScreen('Map/GameMap.tmx')
                # tm = load_map ('WraithFall Map/TSXFiles/GameMapLevelOne.tmx')
                clock = pygame.time.Clock ()
                running = True
                while running:
                    for event in pygame.event.get ():
                        if event.type == pygame.QUIT:
                            running = False

                    screen.fill ((0, 0, 0))

                    self.draw_map (screen, tm)
                    self.entities (screen=screen)

                    pygame.display.flip ()
                    clock.tick (60)
                pygame.quit ()
                # SCREEN.fill ("black")
                # PLAY_TEXT = get_font (45).render ("This is a place holder for the play screen", True, "White")
                # PLAY_RECT = PLAY_TEXT.get_rect (center=(640, 260))
                # SCREEN.blit (PLAY_TEXT, PLAY_RECT)
                #
                # PLAY_BACK = Button (image=None, pos=(640, 460),  # #A90505
                #                     text_input="BACK", font=get_font (75), base_color="#FFFFFF",
                #                     hovering_color="#A90505")
                # PLAY_BACK.changeColor (PLAY_MOUSE_POSITION)
                # PLAY_BACK.update (SCREEN)
                # for event in pygame.event.get ():
                #     if event.type == pygame.QUIT:
                #         pygame.quit ()
                #         sys.exit ()
                #     if event.type == pygame.MOUSEBUTTONDOWN:
                #         if PLAY_BACK.checkForInput (PLAY_MOUSE_POSITION):
                #             rtn_main_menu = self.main_menu()  # return to main menu
                #             rtn_main_menu.menu()
                #             # break #exit the play loop and go to main menu
                #             # main_me
                #
                #                 pygame.display.update ()
                #
                #     # def quit_game(self):
                #     #     passnu ()
    def entities(self, screen):
        # SCREEN = pygame.display.set_mode (WIN.window_size ())
        # pygame.display.set_caption ("debug: player actions")
        pygame.display.set_caption ("debug: player actions")
        clock = pygame.time.Clock ()

        # Sprite Groups
        game_sprites = pygame.sprite.Group ()
        mob_sprites = pygame.sprite.Group ()
        sword_sprite = pygame.sprite.Group ()

        # Player Entity
        player = ENTITY.Player ()
        game_sprites.add (player)

        # Mob Entities
        for i in range (5):
            dummy_wraith = ENTITY.Mob ()
            dummy_wraith.set_speed (0, 0)
            game_sprites.add (dummy_wraith)
            mob_sprites.add (dummy_wraith)

        # Sword Entity
        sword = ENTITY.Sword ()
        game_sprites.add (sword)
        sword_sprite.add (sword)

        tm = self.prepareMapScreen ('Map/GameMap.tmx')
        # Game Loop
        looping = True
        while looping:
            clock.tick (WIN.FPS)
            # Input Events
            for event in EVENTS.get ():
                if event.type == pygame.KEYDOWN:
                    # Escape Key
                    if event.key == pygame.K_ESCAPE:
                        WIN.game_exit ()
                    # G key
                    if event.key == pygame.K_g:
                        # Access Sword Menu
                        if player.access_sword () is not None:
                            access = Battle (player)
                            access.sword_menu ()
                # check click on window exit button
                if event.type == pygame.QUIT:
                    WIN.game_exit ()
            # 'updating' the game
            # update all game sprites
            game_sprites.update ()

            # Player and Mob collision
            player_mob_collide = pygame.sprite.spritecollide (player, mob_sprites, False)
            if player_mob_collide:
                combat = Battle (player, player_mob_collide)
                remaining_mob = combat.combat_screen ()
                if remaining_mob:
                    # Run away was chosen
                    # TODO make this invulnerability for a few seconds. changing position could lead to bugs
                    player.warp (player.rect.x - 10, player.rect.y - 10)
                else:
                    # Defeated mob, so remove mob from map
                    pygame.sprite.spritecollide (player, mob_sprites, True)
                # Recover HP at the end of combat
                player.set_stats ({"HP": player.get_stats ()["HP Max"]})

            # Player and Sword collision
            player_sword_collide = pygame.sprite.spritecollide (player, sword_sprite, False)
            if player_sword_collide:
                sword_ref = player_sword_collide[0]
                if sword_ref.verify () is None:
                    # Player picks up the sword
                    sword_ref.pickup (player)

            screen.fill ((0, 0, 0))
            self.draw_map (screen, tm)
            game_sprites.draw (screen)
            # update the display window...
            pygame.display.update ()



if __name__ == '__main__':
    play_game = GameClass()
    pygame.init ()
    play_game.main_menu(func='menu')

