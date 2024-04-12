import pygame
from pygame.locals import *

class Button:
    def __init__(self, x, y, width, height, color, text, font, text_color, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text
        self.font = font
        self.text_color = text_color
        self.action = action

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        font_surface = self.font.render(self.text, True, self.text_color)
        font_rect = font_surface.get_rect(center=self.rect.center)
        screen.blit(font_surface, font_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

class Heading:
    def __init__(self, x, y, text, font, color):
        self.text = text
        self.font = font
        self.color = color
        self.rect = pygame.Rect(x, y, 0, 0)

    def draw(self, screen):
        font_surface = self.font.render(self.text, True, self.color)
        font_rect = font_surface.get_rect(center=self.rect.center)
        screen.blit(font_surface, font_rect)

levels_completed = 0

def main():
    pygame.init()
    screen = pygame.display.set_mode((1250, 640))
    level_number = levels_completed + 1
    pygame.mouse.set_cursor(*pygame.cursors.tri_left)
    while True:
        screen.fill((255, 255, 255))
        font_heading = pygame.font.Font(None, 48)
        heading = Heading(625, 200, 'QUBI KING', font_heading, (0, 0, 0))
        heading.draw(screen)
        font_button = pygame.font.Font(None, 36)
        button = Button(525, 500, 200, 50, (0, 0, 0), 'Play', font_button, (255, 255, 255))
        button.draw(screen)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return
            elif event.type == MOUSEBUTTONDOWN:
                if button.is_clicked(event.pos):
                    level = __import__(f"level{level_number}")
                    level.play(screen)

main()