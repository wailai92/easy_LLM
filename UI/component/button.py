import pygame

class Button():
    def __init__(self, screen, font, word_color = (255, 255, 255), pos = (0, 0), size = (0, 0), color="black", text="button", center=True):
        width, height = size
        x, y = pos
        self.name = text

        if center:
            self.rect = pygame.Rect(0, 0, width, height)
            self.rect.center = pos
        else:
            self.rect = pygame.Rect(x, y, width, height)

        pygame.draw.rect(screen, color, self.rect)

        word = font.render(text, True, word_color)
        word_rect = word.get_rect(midleft=(self.rect.x + 10, self.rect.centery))
        screen.blit(word, word_rect)