import pygame
import os
from UI.component.button import Button
from UI.component.button_list import Button_list
from UI.component.input_box import Input_box
class Main_page():
    def __init__(self, UI_config):
        self.next_page = None
        self.UI_config = UI_config
        self.pull_height = self.UI_config["scale"]["pull_height"]
        self.pull_width = self.UI_config["scale"]["pull_width"]
        self.font = pygame.font.SysFont(self.UI_config["font_default"]["name"], self.UI_config["font_default"]["size"])
        self.pull_rect = pygame.Rect(0, 0, self.pull_width, self.pull_height)
        self.nopull_rect = pygame.Rect(0, 0, 50, self.pull_height)
        self.pullmain_rect = pygame.Rect(self.pull_width, 0, UI_config["scale"]["screen_width"] - self.pull_width, self.UI_config["scale"]["screen_height"])
        self.nopullmain_rect = pygame.Rect(50, 0, UI_config["scale"]["screen_width"] - 50, self.UI_config["scale"]["screen_height"])
        self.pull = False
        self.border_color = tuple(self.UI_config["rect_border"]["color_blue"])
        self.border_width = self.UI_config["rect_border"]["width"]
        self.pull_subsurface = None
        self.pull_mainsubsurface = None
        self.nopull_subsurface = None
        self.nopull_mainsubsurface = None
        self.word_color = []
        self.input_active = False
        self.color_active = (255, 255, 255)
        self.color_passive = (155, 155, 155)
        self.pull_chat_input_box = Input_box(50, 50, 200, 30, (128, 128, 128), self.color_active, self.color_passive, self.font)
        self.nopull_chat_input_box = Input_box(50, 50, 200, 30, (128, 128, 128), self.color_active, self.color_passive, self.font)
    def draw(self, screen):
        self.mouse_pos = pygame.mouse.get_pos()
        screen.fill("black")
        if self.pull:
            left = self.pull_rect
            right = self.pullmain_rect
        else:
            left = self.nopull_rect
            right = self.nopullmain_rect
        pygame.draw.rect(screen, "black", left)
        pygame.draw.rect(screen, "black", right)
        total_rect = left.union(right)
        pygame.draw.rect(screen, self.border_color, total_rect, self.border_width)
        pygame.draw.line(screen, self.border_color, (left.right, 0), (left.right, total_rect.height), self.border_width)

        if hasattr(self, "pull_list"):
            for count in range(0, self.pull_list.button_number):
                self.pull_list.button[count].word_color_change(self.color_passive)
            #兩個按鈕
            if self.pull_list.button[0].rect.collidepoint(self.mouse_pos):
                self.pull_list.button[0].word_color_change(self.color_active)
            elif self.pull_list.button[1].rect.collidepoint(self.mouse_pos):
                self.pull_list.button[1].word_color_change(self.color_active)

        if self.pull_subsurface == None:
            self.pull_subsurface = screen.subsurface(self.pull_rect)
            self.pull_list = Button_list(self.pull_subsurface, ["search mode", "setting"], (3, 3), (246, 50), (0, 0, 0), self.font, [self.color_passive, self.color_passive])
            
            self.pull_mainsubsurface = screen.subsurface(self.pullmain_rect)
            self.nopull_subsurface = screen.subsurface(self.nopull_rect)
            self.nopull_mainsubsurface = screen.subsurface(self.nopullmain_rect)
        
        if self.pull:
            self.pull_list.draw()

        #self.nopull_chat_input_box.draw(self.nopull_mainsubsurface)


        if self.mouse_pos[0] > left.width:
            self.pull = False
        else:
            self.pull = True

    def handle_event(self, event):
        pass