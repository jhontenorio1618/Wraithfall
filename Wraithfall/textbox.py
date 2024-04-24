#This is the textbox class that we will be able to call into different files to avoid redundancy
import game_window as WIN
import os
import pygame
import view_portraits

def get_image(sheet, frame, width, height, scale):
    image = pygame.Surface((width, height), pygame.SRCALPHA).convert_alpha()
    image.blit(sheet, (0, 0), ((frame * width), 0, width, height))
    image = pygame.transform.scale(image, (width * scale, height * scale))
    return image


# Dictionary mapping character names to portrait frames
character_portraits = {
    "MainCharacter": {
        "Neutral": get_image(view_portraits.mc_sheet, 0, 104, 111, 2),
        "Happy": get_image(view_portraits.mc_sheet, 1, 104, 111, 2),
        "Excited": get_image(view_portraits.mc_sheet, 2, 104, 111, 2),
        "Sad": get_image(view_portraits.mc_sheet, 3, 104, 111, 2),
        "Angry": get_image(view_portraits.mc_sheet, 4, 104, 111, 2)
    }
}


# Function to get the correct frame for a character's emotion
def get_character_frame(character_name, emotion):
    return character_portraits[character_name][emotion]
#Load font
def get_font(size):
    return pygame.font.Font(os.path.join(WIN.DIR_FONTS, "grand9kpixel.ttf"), size)


class SceneManager:
    def __init__(self, text_lines, sound_file):
        # Load the sound file
        pygame.mixer.init()
        self.sound = pygame.mixer.Sound(os.path.join(WIN.DIR_MUSIC, sound_file))
        self.initial_sound = True
        self.current_line_index = 0
        self.text_lines = text_lines
        self.current_text_line = None
        self.scene_ended = False #Keeps track scene ending

    def next_textbox(self):
        # Check if we have reached the end of text_lines
        if self.current_line_index == len(self.text_lines):
            #If so, indicate that the scene has ended and return false
            self.scene_ended = True
            return False
        
        self.current_text_line = self.text_lines[self.current_line_index]
        self.current_text_line.text_index = 0
        # Stop sound before playing again
        self.sound.stop()
        # Play sound when text is displayed
        self.sound.play()
        
        #Increment current_line_index
        self.current_line_index += 1
        
        #Return true to indicate that there are more textboxes to display
        return True

    def draw_textboxes(self, screen):
        #Check to see if the scene has ended
        if self.scene_ended:
            return
        if self.current_line_index < len(self.text_lines):  #Add condition to prevent index out of range
            self.current_text_line = self.text_lines[self.current_line_index]
        if self.initial_sound:
            # play sound and loop until text is finished
            self.sound.play()
            self.initial_sound = False
        self.current_text_line.draw(screen)

        # Update text index base on time
        self.current_text_line.update()

        # Stop sound once all text is displayed
        if self.current_text_line.text_index >= len(self.current_text_line.text):
            self.sound.stop()

    def reset_scene(self):
        """ Sets the scene back to the beginning. """
        self.current_line_index = 0

    def goto_scene(self, index):
        """ Allows access to a specific textbox. """
        self.current_line_index = index



class TextBox:
    def __init__(self, text, character, emotion):
        self.text = text
        self.character = character
        self.emotion = emotion
        self.font = get_font(20)
        self.text_index = 0
        self.text_delay = 0.1
        
    def draw(self, screen):
        #Define dimensions and position of the text box
        text_box_width = WIN.WIN_WIDTH - 40
        text_box_height = 120
        text_box_rect = pygame.Rect((20, WIN.WIN_HEIGHT - text_box_height - 20), (text_box_width, text_box_height))
    
        pygame.draw.rect(screen, "white", text_box_rect, 2)
    
        #Get character portrait for the current emotion
        portrait = get_character_frame(self.character, self.emotion)
        if portrait:
            portrait_rect = portrait.get_rect(topleft =(25, WIN.WIN_HEIGHT - text_box_height - 95))
            screen.blit(portrait, portrait_rect)
        
        #Center the text written in the text box
        text_surface = self.font.render(self.text[:self.text_index + 1], True, "white")
        text_rect = text_surface.get_rect(center=text_box_rect.center)
    
        #Blit the text surface onto the screen
        screen.blit(text_surface, text_rect)
        
    def update(self):
    #Delay the characters of the text before displaying them
        if pygame.time.get_ticks() % (self.text_delay * 40) == 0 and self.text_index < len(self.text):
            #Increment the index to display the next character
            self.text_index += 1
    
    