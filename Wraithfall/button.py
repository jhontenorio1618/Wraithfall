from game_window import get_font, scale_to_screen as stsc


class Button:
	def __init__(self, image, pos, text_input, font, base_color, hovering_color):
		# Intialize button attributes
		self.image = image # Button image
		self.x_pos = pos[0]
		self.y_pos = pos[1]
		self.font = font # font used for button
		self.base_color, self.hovering_color = base_color, hovering_color # base and hovering colors
		self.text_input = text_input
		self.text = self.font.render(self.text_input, True, self.base_color) # render button text
		if self.image is None:
			self.image = self.text # If not image is provided use rendered text as the image
		self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
		self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

	def update(self, screen):
		# update button appearance on screen
		if self.image is not None:
			screen.blit(self.image, self.rect)
		screen.blit(self.text, self.text_rect)

	def checkForInput(self, position):
		# check if the given position is within the buttons area
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			return True
		return False

	def changeColor(self, position):
		# change the color of the button when hovering over it
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			self.text = self.font.render(self.text_input, True, self.hovering_color)
		else:
			self.text = self.font.render(self.text_input, True, self.base_color)



