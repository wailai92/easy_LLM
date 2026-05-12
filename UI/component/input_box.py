import pygame

class Input_box():
    def __init__(self, x, y, w, h, rect_color, word_active_color, word_passive_color, font, text = ""):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.text = text
        self.rect_color = rect_color
        self.word_active_color = word_active_color
        self.word_passive_color = word_passive_color
        self.word_color = word_passive_color 
        self.font = font
        self.active = False
        self.input_rect = pygame.Rect(self.x, self.y, self.w, self.h)
        self.text_surface = self.font.render(self.text, True, self.word_color)
        self.text_rect = self.text_surface.get_rect(midleft=(self.input_rect.x + 5, self.input_rect.centery))

    def handle_event(self, event):
        if event.key == pygame.K_BACKSPACE:
            self.text = self.user_text[:-1]
        elif event.key == pygame.K_RETURN:
            self.text = ""
        else:
            self.text += event.unicode

    def activate(self):
        self.active = True
        self.word_color = self.word_active_color

    def inactivate(self):
        self.active = False
        self.word_color = self.word_passive_color

    def update(self):
        self.text_surface = self.font.render(self.text, True, self.word_color)
        self.input_rect.w = max(self.w, self.text_surface.get_width() + 10)
        self.text_rect = self.text_surface.get_rect(midleft=(self.input_rect.x + 5, self.input_rect.centery))

    def draw(self, screen):
        self.update()
        pygame.draw.rect(screen, self.rect_color, self.input_rect)
        screen.blit(self.text_surface, self.text_rect)