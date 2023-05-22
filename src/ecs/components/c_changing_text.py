import pygame

class CChangingText:
    def __init__(self, text:str, font:pygame.font.Font, color: pygame.Color) -> None:
        self.font = font
        self.text = text
        self.color = color