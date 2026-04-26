from UI.component.button import Button

class Button_list():
    def __init__(self, screen, button_texts, start_pos, size, color, font, word_color):
        self.button_number = 0
        self.button = []
        self.x, self.y = start_pos
        self.width, self.height = size
        for text in button_texts:
            self.button.append(Button(screen, font, word_color[self.button_number], (self.x, self.y), size, color, text, False))
            self.y += self.height
            self.button_number += 1