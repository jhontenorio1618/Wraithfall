import pygame
import game_window as WIN
import os
from textbox import TextBox, SceneManager, character_portraits
import sys

pygame.init()

# Set screen size using the dimensions in the window_size function in game_window
SCREEN = pygame.display.set_mode(WIN.window_size())
pygame.display.set_caption("Cutscenes")

# Load the sound file
pygame.mixer.init()

clock = pygame.time.Clock()

# TODO put "text_line" files all here with appropriate names corresponding to scene
# (note that i am importing "TextBox" straight from textbox.py so you'll want to remove that. this just looks nicer

#Text lines
scene1_text_lines = [
    TextBox("JOURNAL: \"June 18th, 2058: ", "MainCharacter", "Neutral"),
    TextBox("Dear Alice,", "MainCharacter", "Neutral"),
    TextBox("It's been six months, now, since the Rift appeared in the sky above the city.", "MainCharacter", "Sad"),
    TextBox("When Grandpa lets me go up on the roof of the cabin, I've got a perfect view of it", "MainCharacter", "Neutral"),
    TextBox("now, just past a few moutain peaks. It looks like the fabric of the sky is torn open.", "MainCharacter", "Neutral"),
    TextBox("The black smoke pours out constantly, covering the world in darkness.", "MainCharacter", "Neutral"),
    TextBox("They still don't know how to stop it; it's hidden the sun from everyone now.", "MainCharacter", "Sad"),
    TextBox("Just last week the UN declared a worldwide emergency, fearful of a new ice age.", "MainCharacter", "Neutral"),
    TextBox("It's supposed to be summer here, but it's still freezing.", "MainCharacter", "Sad"),
    TextBox("Grandpa thinks we'll never see the sun again...", "MainCharacter", "Sad"),
    TextBox("The wraiths are coming constantly from the Rift now, too.", "MainCharacter", "Neutral"),
    TextBox("Grandpa and I were attacked by one in the woods a few weeks ago; at this point,", "MainCharacter", "Neutral"),
    TextBox("it's barely safe to go out and hunt.", "MainCharacter", "Neutral"),
    TextBox("Two of them got our neighbor, Nellie, this week.", "MainCharacter", "Sad"),
    TextBox("I know it sounds stupid, but I've been researching the rift in my spare time.", "MainCharacter", "Neutral"),
    TextBox("I want to understand it. I want to figure out why it's here.", "MainCharacter", "Neutral"),
    TextBox("I'll be writing you to keep documenting my findings.", "MainCharacter", "Neutral"),
    TextBox("Who knows, maybe I'll actually figure something out.", "MainCharacter", "Excited"),
    TextBox("I know the city's destroyed now, but I hope you're alright.", "MainCharacter", "Happy"),
    TextBox("I'm not even sure if these letters ever get to you. If they do, write back, ok?", "MainCharacter", "Neutral"),
    TextBox("Eventually, I'll come find you.", "MainCharacter", "Happy"),
    TextBox("-   Oliver\"", "MainCharacter", "Neutral")
]

scene2_text_lines = [
    TextBox("Up and at'em, eh, Oliver?", "Grandpa", "Happy"), #Grandpa
    TextBox("Finally - it's already past dawn!", "Grandpa", "Neutral"), #Grandpa
    TextBox("Not that anyone can tell anymore...", "Grandpa", "Neutral"), #Grandpa
    TextBox("The wraiths have been quiet since last night.", "Grandpa", "Neutral"), #Grandpa
    TextBox("They left another pile of drained deer carcasses by the treeline.", "Grandpa", "Mad"), #Grandpa
    TextBox("It's a shame, all that tainted meat...", "Grandpa", "Mad"), #Grandpa
    TextBox("...Listen, Oliver.", "Grandpa", "Neutral"), #Grandpa
    TextBox("While I've got no desire to let you anywhere near those abominations...", "Grandpa", "Neutral"), #Grandpa
    TextBox("...I'm getting old, and hunting is hard on my bones. ", "Grandpa", "Neutral"), #Grandpa
    TextBox("Come out with me right now - I can show you the ropes, yeah?", "Grandpa", "Happy"), #Grandpa
]

scene3_text_lines = [
    TextBox("You know, I first taught your mom how to hunt in these mountains, too.", "Grandpa", "Happy"), #Grandpa
    TextBox("She'd be proud to see you out here today.", "Grandpa", "Happy"), #Grandpa
    TextBox("Here, this was hers. I've been using it as a good luck charm, but I want you to have it.", "Grandpa", "Happy"), #Grandpa
    TextBox("*Retrieves Grandpa's Gift*", "MainCharacter", "Neutral"), #Main Character
    TextBox("'...a gun?'", "MainCharacter", "Neutral"), #Main Character
    TextBox("*Obtained GUN*", "MainCharacter", "Neutral"), #Main Character
    TextBox("Handle it with care, okay?", "Grandpa", "Neutral"), #Grandpa
    TextBox("Why don't you pick those up, Oliver? They're a little bruised, but any food is good food...", "Grandpa", "Neutral"), #Grandpa
    TextBox("That bit of wisdom's stuck with me since my army days.", "Grandpa", "Neutral"), #Grandpa
    TextBox("...Quiet now", "Grandpa", "Neutral"), #Grandpa
    TextBox("Those things... if only someone could figure out what they are, why they're here terrorizing us.", "Grandpa", "Mad"), #Grandpa
    TextBox("...Hold on.", "Grandpa", "Neutral"), #Grandpa
    TextBox("There we go... you can tag the next one, alright, Oliver?", "Grandpa", "Neutral"), #Grandpa
    TextBox("Now, go and fetch the carcass for me, please.", "Grandpa", "Neutral"), #Grandpa
    TextBox("Oliver!!", "Grandpa", "Neutral"), #Grandpa
]

# TODO continue starting from Scene4.py

# ...

# TODO set up SceneManager for each scene

scene1 = SceneManager(scene1_text_lines, "pencilwriting.wav")
scene2 = SceneManager(scene2_text_lines, "text_sound.wav")
scene3 = SceneManager(scene3_text_lines, "text_sound.wav")

# TODO continue starting from Scene4.py

scene_dict = {1: scene1, 2: scene2, 3: scene3}

most_recent_scene_index = -1
next_scene_index = 1


def check_next_scene():
    if most_recent_scene_index == -1:
        next_scene_index = 1

    return most_recent_scene_index


def get_scene(id):
    return scene_dict[id]


def play_scene(scene, playing):
    if playing:
        ongoing_scene = True
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                # If enter key is pressed move to the next line
                if event.key == pygame.K_RETURN:
                    ongoing_scene = not scene.next_textbox()
                    print(ongoing_scene)

        scene.draw_textboxes(SCREEN)

        # Update the display
        pygame.display.flip()
        clock.tick(WIN.get_fps())
    else:
        ongoing_scene = False
    return ongoing_scene


def play_scene_with_loop(scene):
    """ Expects a SceneManager class """
    run = True
    end_of_scene = False
    while run:
        SCREEN.fill("black")

        for event in pygame.event.get():
            # If user closes the window exit the loop
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                # If enter key is pressed move to the next line
                if event.key == pygame.K_RETURN:
                    end_of_scene = scene.next_textbox()

        scene.draw_textboxes(SCREEN)

        # Update the display
        pygame.display.flip()
        clock.tick(WIN.get_fps())
        if end_of_scene:
            run = False


# play_scene_with_loop(get_scene(1))

