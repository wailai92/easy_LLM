import pygame

class Button():
    def __init__(self, screen, font, word_color = (255, 255, 255), pos = (0, 0), size = (0, 0), color="black", text="button", center=True):
        self.width, self.height = size
        self.x, self.y = pos
        self.name = text
        self.center = center
        self.screen = screen
        self.color = color
        self.font = font
        self.word_color = word_color


        if center:
            self.rect = pygame.Rect(0, 0, self.width, self.height)
            self.rect.center = pos
        else:
            self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        pygame.draw.rect(screen, color, self.rect)

        self.word = font.render(text, True, word_color)
        self.word_rect = self.word.get_rect(midleft=(self.rect.x + 10, self.rect.centery))
        screen.blit(self.word, self.word_rect)

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
        self.word = self.font.render(self.name, True, self.word_color)
        self.word_rect = self.word.get_rect(midleft=(self.rect.x + 10, self.rect.centery))
        self.screen.blit(self.word, self.word_rect)

    def color_change(self, color):
        self.color = color
    def word_color_change(self, color):
        self.word_color = color
        