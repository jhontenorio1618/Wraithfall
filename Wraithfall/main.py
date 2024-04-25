import pygame
import mainmenu
import cutscenes
import game_window
import GameMapClass
import entity_classes
import overworld_functions
import textbox
import audio_mixer
import battle_menu
import view_spritesheets
import view_portraits
import GameClass

#Initialize pygame
pygame.init()

#Set up game window
game_window.setup()

#Initialize the audio mixer
audio_mixer.init()

#Load sprite sheets and portraits
view_spritesheets.load()
view_portraits.load()

#Start the main menu
mainmenu.run()

#Once the user starts the game, initialize game class
game = GameClass.Game()

#Run the main game loop
while game.running:
    #check for events
    events = pygame.event.get()
    
    #handle events
    game.handle_events(events)
    
    #Update the game state
    game.update()
    
    #Render the game
    
    game.render()
    
#Quite pygame when the game loop ends
pygame.quit()