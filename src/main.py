import pygame
from pygame.locals import *

class Button:
    def __init__(self, x, y, width, height, color, text, font, text_color, hover_color, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color  # New attribute for hover color
        self.text = text
        self.font = font
        self.text_color = text_color
        self.action = action

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        font_surface = self.font.render(self.text, True, self.text_color)
        font_rect = font_surface.get_rect(center=self.rect.center)
        screen.blit(font_surface, font_rect)

    def draw_with_hover(self, screen, mouse_pos):
        # Check if mouse is over the button
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, self.hover_color, self.rect)
        else:
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
        self.rect = self.font.render(self.text, True, self.color).get_rect(center=(x, y))

    def draw(self, screen):
        font_surface = self.font.render(self.text, True, self.color)
        screen.blit(font_surface, self.rect)

class Image(pygame.sprite.Sprite):
    def __init__(self, x, y, image, width, height):
        super(Image, self).__init__()
        self.image = pygame.transform.scale(image, (width, height))
        self.rect = self.image.get_rect(topleft = (x, y))
        self.width = width
        self.height = height

def main():
    levels_completed = 0
    total_levels = 7
    pygame.init()
    info = pygame.display.Info()
    screen_width = 1080
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("NASHA MUKTI KENDRA")
    logo = pygame.image.load('assets/images/logo.png')
    logo = Image(screen_width/2 - 250, 40, logo, 500, 400)
    logo_beer = pygame.image.load('assets/images/logo_beer.png')
    rotated_logo_beer = pygame.transform.rotate(logo_beer, 20)
    logo_beer = Image(screen_width/2 - 500, 80, rotated_logo_beer, 200, 150)

    button_font = pygame.font.Font(None, 50)
    play_button = Button(screen_width/2 - 100, 400, 200, 50, (43, 44, 48), 'PLAY', button_font, (255, 255, 255), (100, 100, 100))
    quit_button = Button(screen_width/2 - 100, 500, 200, 50, (43, 44, 48), 'QUIT', button_font, (255, 255, 255), (100, 100, 100))


    font_heading = pygame.font.Font(None, 48)
    levels_heading = Heading(screen_width/2, 100, 'LEVELS', font_heading, (0, 0, 0))
    font_button = pygame.font.Font(None, 36)
    back_button = Button(screen_width - 130, 40, 100, 50, (0, 0, 0), 'Back', font_button, (255, 255, 255), (100, 100, 100))
    
    level_number = levels_completed + 1
    pygame.mouse.set_cursor(*pygame.cursors.tri_left)
    on_levels = False
    clock= pygame.time.Clock()
    while True:
        if not on_levels:
            screen.fill((43, 44, 48))
            font_heading = pygame.font.Font(None, 60)
            screen.blit(logo.image, logo.rect)
            screen.blit(logo_beer.image, logo_beer.rect)
            mouse_pos = pygame.mouse.get_pos()
            play_button.draw_with_hover(screen, mouse_pos)
            quit_button.draw_with_hover(screen, mouse_pos)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if play_button.is_clicked(event.pos):
                        on_levels = True
                    elif quit_button.is_clicked(event.pos):
                        pygame.quit()
                        return
        else:
            screen.fill((255, 255, 255))
            levels_heading.draw(screen)
            mouse_pos = pygame.mouse.get_pos()
            back_button.draw_with_hover(screen, mouse_pos)
            level_buttons = []
            for i in range(1, (total_levels // 6) + 2):
                for j in range(1, 7 if i <= (total_levels) // 6 else total_levels % 6 + 1):
                    level_button = Button(150 * j, 100 + 100 * i, 50, 50, (0, 0, 0), f'{6*(i-1) + j}', font_button, (255, 255, 255), (100, 100, 100))
                    level_buttons.append(level_button)
                    if 5*(i-1) + j > levels_completed + 1:
                        level_button.color = (150, 150, 150)
                    level_button.draw(screen)
            pygame.display.flip()
            clock.tick(100)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if back_button.is_clicked(event.pos):
                        on_levels = False
                    else:
                        for i in range(1, total_levels + 1):
                            if i > levels_completed + 1:
                                continue
                            else:
                                level_button = level_buttons[i - 1]
                                if level_button.is_clicked(event.pos):
                                    level = __import__(f"level{i}")
                                    level_completed = level.play(screen)
                                    if level_completed and i == level_number:
                                        levels_completed += 1
                                        level_number += 1

main()