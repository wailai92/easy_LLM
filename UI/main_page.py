import pygame
import os
from UI.component.button import Button
class Main_page():
    def __init__(self):
        self.next_page = None
        #self.font = pygame.font.SysFont(None, 36)
    def draw(self, screen):
        screen.fill("black")
    def handle_event(self, event):
        pass