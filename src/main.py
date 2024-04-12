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
    info = pygame.display.Info()
    screen_width = info.current_w
    screen_height = info.current_h
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Qubi King")
    level_number = levels_completed + 1
    pygame.mouse.set_cursor(*pygame.cursors.tri_left)
    on_levels = False
    while True:
        if not on_levels:
            screen.fill((255, 255, 255))
            font_heading = pygame.font.Font(None, 60)
            heading = Heading(625, 200, 'QUBI KING', font_heading, (0, 0, 0))
            heading.draw(screen)
            button_font = pygame.font.Font(None, 36)
            play_button = Button(525, 500, 200, 50, (0, 0, 0), 'Play', button_font, (255, 255, 255))
            play_button.draw(screen)
            quit_button = Button(550, 600, 150, 50, (0, 0, 0), 'Quit', button_font, (255, 255, 255))
            quit_button.draw(screen)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    return
                elif event.type == MOUSEBUTTONDOWN:
                    if play_button.is_clicked(event.pos):
                        on_levels = True
                    elif quit_button.is_clicked(event.pos):
                        pygame.quit()
                        return
        else:
            screen.fill((255, 255, 255))
            font_levels_heading = pygame.font.Font(None, 48)
            levels_heading = Heading(625, 100, 'LEVELS', font_heading, (0, 0, 0))
            levels_heading.draw(screen)
            font_button = pygame.font.Font(None, 36)
            level_button = Button(100, 200, 50, 50, (0, 0, 0), '1', font_button, (255, 255, 255))
            level_button.draw(screen)
            back_button = Button(1150, 40, 100, 50, (0, 0, 0), 'Back', font_button, (255, 255, 255))
            back_button.draw(screen)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    return
                elif event.type == MOUSEBUTTONDOWN:
                    if level_button.is_clicked(event.pos):
                        level = __import__(f"level{level_number}")
                        level.play(screen)
                    elif back_button.is_clicked(event.pos):
                        on_levels = False

main()