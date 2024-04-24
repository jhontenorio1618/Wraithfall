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
scene4_text_lines = [
    TextBox("...You held your own, Oliver. Good.", "Grandpa", "Happy"), #grandpa
    TextBox("'...What is this?'", "MainCharacter", "Neutral"), 
    TextBox("*Retrieves an item from the wraiths corpse*", "MainCharacter", "Neutral"), 
    TextBox("*Obtained WRAITH ESSENCE*", "MainCharacter", "Neutral"), 
    TextBox("'This could be useful to my research...'", "MainCharacter", "Neutral"), 
    TextBox("*Sigh*...That venison meat should be enough to keep us fed for the next week, at least.", "Grandpa", "Neutral"),
    TextBox("Let's go home, kid.", "Grandpa", "Happy")
]
scene5_text_lines = [
    TextBox("Now that was good...", "Grandpa", "Happy"), #grandpa
    TextBox("Y'know...", "Grandpa", "Happy"), #grandpa
    TextBox("We might not have fast food anymore, but nothing tastes better than meat you caught yourself.", "Grandpa", "Happy"), #grandpa
    TextBox("...", "Grandpa", "Neutral"), #grandpa
    TextBox("Hey, I'm really proud of you, Oliver.", "Grandpa", "Happy"), #grandpa
    TextBox("I know things got hard after you lost your mom...", "Grandpa", "Neutral"), #grandpa
    TextBox("And I know they got harder with this whole \"otherworldly apocalypse\" thing going on.", "Grandpa", "Neutral"), #grandpa
    TextBox("You're really growning into your own out here.", "Grandpa", "Happy"), #grandpa
    TextBox("...", "Grandpa", "Neutral"), #grandpa
    TextBox("You know--", "Grandpa", "Happy"), #grandpa
    TextBox("What the-?!", "MainCharacter", "Neutral"), #Maincharacter
    TextBox("...Now, I've seen plenty of strange things these past few months, but that was new.", "Grandpa", "Neutral"), #grandpa
    TextBox("Whatever came out of that rift just now, it landed on our mountain.", "Grandpa", "Mad"), #grandpa
    TextBox("...", "Grandpa", "Neutral"), #grandpa
    TextBox("...What, you want to go see what it is?", "Grandpa", "Neutral"), #grandpa
    TextBox("Kid, I feel like I don't need to explain to you why that's too dangerous.", "Grandpa", "Mad"), #grandpa
    TextBox("*Sigh*...Alright, fine. I know you're curious about the rift. ", "Grandpa", "Neutral"), #grandpa
    TextBox("Whatever it is, we don't get close, got it?", "Grandpa", "Neutral"), #grandpa
]
scene6_text_lines = [
    TextBox("I don't like the looks of this... stay quiet.", "Grandpa", "Mad"), #grandpa
]
scene7_text_lines = [
    TextBox("Incredible... like it's straight out of a fantasy novel.", "Grandpa", "Neutral"), #grandpa
]
scene8_text_lines = [
    TextBox("...We shouldn't touch it. Let's go, Oliver.", "Grandpa", "Mad"), #grandpa
    TextBox("It would be best to call it a night.", "Grandpa", "Neutral"), #grandpa
    TextBox("'Maybe I could use this for something...'", "MainCharacter", "Neutral"), #Maincharacter
    TextBox("...Oliver, that isn't wise...", "Grandpa", "Mad"), #grandpa
    TextBox("Oliver!!", "Grandpa", "Mad"), #grandpa
]
scene9_text_lines = [
    TextBox("No!!", "MainCharacter", "Sad"), #MainCharacter
]
scene10_text_lines = [
    TextBox("...", "Sword", "Neutral"), #sword
    TextBox("'Hold on, this thing's... blinking at me!'", "MainCharacter", "Neutral"), #MC
    TextBox("'Yeah, and this THING can hear you, too, kid.'", "Sword", "Mad"), #Sword
    TextBox("'Y-You can hear my thoughts?!'", "MainCharacter", "Neutral"), #MC
    TextBox("'Sure can. Call it a magical soul bond, if that floats your boat.'", "Sword", "Happy"), #Sword
    TextBox("'We got psychologically linked when you picked me up.'", "Sword", "Neutral"), #Sword
    TextBox("'Great... this isn't weird at all.'", "MainCharacter", "Neutral"), #MC
    TextBox("'We don't have time for this - can you just kill that giant wraith for me?!'", "MainCharacter", "Neutral"), #MC
    TextBox("'Woah, too good for introductions are we?'", "Sword", "Mad"), #Sword
    TextBox("'I'm Acheron, and you are...?'", "Sword", "Happy"), #Sword
    TextBox("'Oliver - now hurry up and do something! I've gotta help my Grandpa!'", "MainCharacter", "Angry"), #MC
    TextBox("'Sheesh - pushy are we?'", "Sword", "Mad"), #Sword
    TextBox("'Fine, fine. But we've gotta work together to get this done, alright?'", "Sword", "Neutral") #Sword
]
scene11_text_lines = [
    TextBox("No... please, no!", "MainCharacter", "Neutral"), #MC
    TextBox("He's all I have left!", "MainCharacter", "Sad"), #MC
    TextBox("Ugh... Oliver", "Grandpa", "Dead1"), #Grandpa
    TextBox("Kid...save your bandages...this is it for me...", "Grandpa", "Dead2"), #Grandpa
    TextBox("I meant it when I said that I was proud of you...", "Grandpa", "Dead1"), #Grandpa
    TextBox("...This world is dark and cruel, but keep pushing...", "Grandpa", "Dead2"), #Grandpa
    TextBox("...for me, ok?", "Grandpa", "Dead1"), #Grandpa
    TextBox("And for your mom...", "Grandpa", "Dead2"), #Grandpa
    TextBox("I'll finally get to be with my little girl again...", "Grandpa", "Dead1"), #Grandpa
    TextBox("Please...", "MainCharacter", "Sad"), #MC
    TextBox("I'm sorry I can't be there for you...Oliver...", "Grandpa", "Dead2"), #Grandpa
]


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

