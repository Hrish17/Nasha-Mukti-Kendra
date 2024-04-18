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

    def draw(self, screen, mouse_pos, hover):
        if self.rect.collidepoint(mouse_pos) and hover:
            pygame.draw.rect(screen, self.hover_color, self.rect)
        else:
            pygame.draw.rect(screen, self.color, self.rect)
        font_surface = self.font.render(self.text, True, self.text_color)
        font_rect = font_surface.get_rect(center=self.rect.center)
        screen.blit(font_surface, font_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)



class Text:
    def __init__(self, x, y, text, font, color):
        self.text = text
        self.font = font
        self.color = color
        self.rect = pygame.Rect(x, y, 0, 0)

    def draw(self, screen):
        font_surface = self.font.render(self.text, True, self.color)
        font_rect = font_surface.get_rect(center=self.rect.center)
        screen.blit(font_surface, font_rect)

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

def start_level(screen, level_number):
    level = __import__(f"level{6}")
    next = level.play(screen)
    if next == 1:
        level_number += 1
        level_number = start_level(screen, level_number)
    elif next == 0:
        level_number = start_level(screen, level_number)
    return level_number

def main():
    levels_unlocked = 1
    total_levels = 10
    pygame.init()
    screen_width = 1080
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("NASHA MUKTI KENDRA")
    logo = pygame.image.load('assets/images/logo.png')
    logo = Image(screen_width/2 - 250, 40, logo, 500, 400)
    logo_beer = pygame.image.load('assets/images/logo_beer.png')
    logo_beer = Image(screen_width/2 + 70, 380, logo_beer, 50, 50)

    button_font = pygame.font.Font(None, 50)
    play_button = Button(screen_width/2 - 60, 390, 120, 50, (43, 44, 48), 'PLAY', button_font, (255, 255, 255), (100, 100, 100))
    controls_button = Button(screen_width/2 - 115, 450, 230, 50, (43, 44, 48), 'CONTROLS', button_font, (255, 255, 255), (100, 100, 100))
    quit_button = Button(screen_width/2 - 60, 510, 120, 50, (43, 44, 48), 'QUIT', button_font, (255, 255, 255), (100, 100, 100))

    controls = Text(screen.get_width()/2, 100, 'CONTROLS', pygame.font.Font(None, 70), (255, 255, 255))
    controls_image = Image(screen.get_width()/2 - 400, 190, pygame.image.load("assets/images/controls.png"), 800, 300)

    font_heading = pygame.font.Font(None, 60)
    levels_heading = Heading(screen_width/2, 160, 'LEVELS', font_heading, (255, 255, 255))
    font_button = pygame.font.Font(None, 36)
    back_button = Button(screen_width/2 - 60, 490, 120, 50, (70, 70, 70), 'BACK', font_button, (255, 255, 255), (100, 100, 100))
    level_font_button = pygame.font.Font(None, 50)
    
    pygame.mouse.set_cursor(*pygame.cursors.tri_left)
    screen_number = 1
    clock= pygame.time.Clock()
    while True:
        if screen_number == 1:
            screen.fill((43, 44, 48))
            font_heading = pygame.font.Font(None, 60)
            screen.blit(logo.image, logo.rect)
            mouse_pos = pygame.mouse.get_pos()
            play_button.draw(screen, mouse_pos, 1)
            controls_button.draw(screen, mouse_pos, 1)
            quit_button.draw(screen, mouse_pos, 1)
            if play_button.rect.collidepoint(mouse_pos):
                logo_beer.rect.x = screen_width / 2 + 65
                logo_beer.rect.y = 390
                screen.blit(logo_beer.image, logo_beer.rect)
            elif controls_button.rect.collidepoint(mouse_pos):
                logo_beer.rect.x = screen_width/2 + 120
                logo_beer.rect.y = 450
                screen.blit(logo_beer.image, logo_beer.rect)
            elif quit_button.rect.collidepoint(mouse_pos):
                logo_beer.rect.x = screen_width/2 + 65
                logo_beer.rect.y = 510
                screen.blit(logo_beer.image, logo_beer.rect)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if play_button.is_clicked(event.pos):
                        screen_number = 3
                    elif controls_button.is_clicked(event.pos):
                        screen_number = 2
                    elif quit_button.is_clicked(event.pos):
                        pygame.quit()
                        return
        elif screen_number == 2:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if back_button.is_clicked(event.pos):
                        screen_number = 1
            screen.fill((43, 44, 48))
            controls.draw(screen)
            screen.blit(controls_image.image, controls_image.rect)
            mouse_pos = pygame.mouse.get_pos()
            back_button.draw(screen, mouse_pos, 1)
            pygame.display.flip()
        elif screen_number == 3:
            screen.fill((43, 44, 48))
            levels_heading.draw(screen)
            mouse_pos = pygame.mouse.get_pos()
            back_button.draw(screen, mouse_pos, 1)
            level_buttons = []
            for i in range(1, (total_levels // 6) + 2):
                for j in range(1, 7 if i <= (total_levels) // 6 else total_levels % 6 + 1):
                    level_button = Button(150 * j, 150 + 100 * i, 50, 50, (100, 100, 100), f'{6*(i-1) + j}', level_font_button, (255, 255, 255), (80, 80, 80))
                    level_buttons.append(level_button)
                    if 5*(i-1) + j > levels_unlocked:
                        level_button.color = (43, 44, 48)
                        level_button.draw(screen, mouse_pos, 0)
                    else:
                        level_button.draw(screen, mouse_pos, 1)
            pygame.display.flip()
            clock.tick(100)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if back_button.is_clicked(event.pos):
                        screen_number = 1
                    else:
                        for i in range(1, total_levels + 1):
                            if i > levels_unlocked:
                                continue
                            else:
                                level_button = level_buttons[i - 1]
                                if level_button.is_clicked(event.pos):
                                    l_number = start_level(screen, i)
                                    if l_number > levels_unlocked:
                                        levels_unlocked = l_number

main()