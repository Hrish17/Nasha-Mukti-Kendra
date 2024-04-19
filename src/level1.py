import pygame
from pygame.locals import *
from pytmx.util_pygame import load_pygame
import player as character

class Image:
    def __init__(self, screen, x, y, width, height, image_path):
        self.screen = screen
        self.image = None
        self.rect = None
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()        

    def draw(self):
        self.rect.topleft = (self.x, self.y)
        self.screen.blit(self.image, self.rect)
        
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


class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image):
        super(Block, self).__init__()
        self.surf = pygame.Surface((width, height))
        self.surf.fill((0, 0, 0))
        self.rect = self.surf.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.image = image

class Background(pygame.sprite.Sprite):
    def __init__(self,x,y,width,height,color):
        super(Background, self).__init__()
        self.surf = pygame.Surface((width, height))
        self.surf.fill(color)
        self.rect = self.surf.get_rect()
        self.rect.x = x
        self.rect.y = y

class Key(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Key, self).__init__()
        original_image = pygame.image.load("./assets/images/key.png").convert_alpha()
        scaled_image = pygame.transform.scale(original_image, (80, 80))
        rotated_image = pygame.transform.rotate(scaled_image, -45)
        self.image = rotated_image
        self.rect = self.image.get_rect(topleft = (x, y))
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        original_image = pygame.image.load("./assets/images/key.png").convert_alpha()
        scaled_image = pygame.transform.scale(original_image, (50, 50))
        self.image = scaled_image

class Door(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Door, self).__init__()
        original_image = pygame.image.load("./assets/images/door.jpg").convert_alpha()
        self.image = pygame.transform.scale(original_image, (60, 90))
        self.rect = self.image.get_rect(topleft = (x, y))

class Button:
    def __init__(self, x, y, width, height, color, text, font, text_color, hover_color, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color  # New attribute for hover color
        self.text = text
        self.font = font
        self.text_color = text_color
        self.action = action
        self.click_sound = pygame.mixer.Sound('./assets/sounds/button_click.mp3')

    def draw(self, screen, mouse_pos, hover):
        if self.rect.collidepoint(mouse_pos) and hover:
            pygame.draw.rect(screen, self.hover_color, self.rect)
        else:
            pygame.draw.rect(screen, self.color, self.rect)
        font_surface = self.font.render(self.text, True, self.text_color)
        font_rect = font_surface.get_rect(center=self.rect.center)
        screen.blit(font_surface, font_rect)

    def is_clicked(self, pos):
        if self.rect.collidepoint(pos):
            self.click_sound.play()
            return True
        return False
    
class ButtonImage:
    def __init__(self, image_path, x, y, width, height):
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect = pygame.Rect()

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

def create_level(blocks, tilewidth, tileheight):
    res = pygame.sprite.Group()
    for x,y,image in blocks.tiles():
        block = Block(x * tilewidth, y * tileheight, tilewidth, tileheight, image)
        res.add(block)
    return res

def play(screen):
    pygame.display.set_caption("NASHA MUKTI KENDRA")

    screen_number = 1
    level1 = Text(screen.get_width()/2, 100, 'LEVEL 1', pygame.font.Font(None, 80), (255, 255, 255))
    rule = Text(screen.get_width()/2, 200, 'Collect the key and reach the door to proceed to the next level', pygame.font.Font(None, 50), (255, 255, 255))
    disclaimer = Text(screen.get_width()/2, 300, 'DISCLAIMER : This game contains elements of surprise!', pygame.font.Font(None, 50), (255, 0, 0))
    begin_button = Button(screen.get_width()/2 - 75, 420, 150, 50, (70, 70, 70), 'BEGIN', pygame.font.Font(None, 36), (255, 255, 255), (100, 100, 100))

    #screen_number = 2
    heart1 = Image(screen, screen.get_width()/2 + 350, 30, 32, 32, 'assets/images/heart.png')
    heart2 = Image(screen, screen.get_width()/2 + 390, 30, 32, 32, 'assets/images/heart.png')
    heart3 = Image(screen, screen.get_width()/2 + 430, 30, 32, 32, 'assets/images/heart.png')
    hearts = [heart1, heart2, heart3]
    tmxdata = load_pygame("./assets/maps/level1.tmx")
    background_layer = tmxdata.get_layer_by_name("Background")
    blocks_layer = tmxdata.get_layer_by_name("Blocks")
    blocks1_layer = tmxdata.get_layer_by_name("Blocks1")

    player = character.Player()
    all_sprites = pygame.sprite.Group(player)
    player.health = 1

    quit_button = Button(20, 40, 100, 50, (0, 0, 0), 'Quit', pygame.font.Font(None, 36), (255, 255, 255), (43, 44, 48))

    blocks = create_level(blocks_layer, tmxdata.tilewidth, tmxdata.tileheight)
    blocks1 = create_level(blocks1_layer, tmxdata.tilewidth, tmxdata.tileheight)

    blocks2 = pygame.sprite.Group()
    for block in blocks:
        blocks2.add(block)
    for block in blocks1:
        blocks2.add(block)

    lowest_camera_y = player.rect.y

    key = Key(1850, 2270)
    door = Door(2600, 2470)

    right = True

    move_speed = 4
    jumping = True

    og_jump_speed = 6
    jump_speed = 0
    max_fall_speed = 6

    gravity = 0.24

    screen_offset_x = -900
    screen_offset_y = 0

    key_collected = False
    reached = False

    falling_blocks = False

    background = Background(200, 100, 700, 400, (43, 44, 48))
    gameover_text = Text(screen.get_width()/2, 200, 'GAME OVER', pygame.font.Font(None, 80), (255, 0, 0))
    main_menu_button = Button(screen.get_width()/2 - 75, 420, 150, 50, (70, 70, 70), 'Main Menu', pygame.font.Font(None, 36), (255, 255, 255), (100, 100, 100))
    retry_button = Button(screen.get_width()/2 - 75, 350, 150, 50, (70, 70, 70), 'Retry', pygame.font.Font(None, 36), (255, 255, 255), (100, 100, 100))
    gameover = False
    nextlevel_text = Text(screen.get_width()/2, 200, 'YOU WON', pygame.font.Font(None, 80), (0, 255, 0))
    nextlevel_button = Button(screen.get_width()/2 + 125, 380, 150, 50, (70, 70, 70), 'Next Level', pygame.font.Font(None, 36), (255, 255, 255), (100, 100, 100))
    nextlevel_main_menu_button = Button(screen.get_width()/2 -75, 380, 150, 50, (70, 70, 70), 'Main Menu', pygame.font.Font(None, 36), (255, 255, 255), (100, 100, 100))
    nextlevel_retry_button = Button(screen.get_width()/2 - 275, 380, 150, 50, (70, 70, 70), 'Play Again', pygame.font.Font(None, 36), (255, 255, 255), (100, 100, 100))
    nextlevel = False

    bg_sound = pygame.mixer.Sound('./assets/sounds/bg.mp3')
    bg_played = False
    jump_sound = pygame.mixer.Sound('./assets/sounds/jump.mp3')

    running = True
    clock = pygame.time.Clock()
    while running:
        clock.tick(60)
        if screen_number == 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if begin_button.is_clicked(event.pos):
                        screen_number = 2
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        screen_number = 2
            screen.fill((43, 44, 48))
            level1.draw(screen)
            rule.draw(screen)
            disclaimer.draw(screen)
            mouse_pos = pygame.mouse.get_pos()
            begin_button.draw(screen, mouse_pos, 1)
            pygame.display.flip()

        elif screen_number == 2:
            if not bg_played:
                bg_sound.play()
                bg_played = True
            dx = 0
            dy = 0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    bg_sound.stop()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if quit_button.is_clicked(event.pos):
                        bg_sound.stop()
                        return -1

            keys = pygame.key.get_pressed()
            if (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]) and not jumping:
                jump_speed = og_jump_speed
                jumping = True
                jump_sound.play()
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                dx -= move_speed
                right = False
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                dx += move_speed
                right = True
            
            all_sprites.update()

            if not reached:
                jump_speed -= gravity
                if jump_speed <= -max_fall_speed:
                    jump_speed = -max_fall_speed
            dy -= jump_speed

            for block in blocks2:
                if block.rect.colliderect(player.rect.x + dx, player.rect.y, player.width, player.height):
                    dx = 0
                if block.rect.colliderect(player.rect.x, player.rect.y + dy, player.width, player.height):
                    if jump_speed > 0:
                        dy = block.rect.bottom - player.rect.top
                        jump_speed = 0
                    elif jump_speed <= 0:
                        dy = block.rect.top - player.rect.bottom
                        jump_speed = 0
                        jumping = False

            if not reached and not gameover:
                player.rect.x += dx
                screen_offset_x -= dx
                dy = dy//1
                player.rect.y += dy

            keys_pressed = pygame.key.get_pressed()
            if not gameover and not reached:
                if dy == 0:
                    if not keys_pressed[pygame.K_LEFT] and not keys_pressed[pygame.K_RIGHT] and not keys_pressed[pygame.K_a] and not keys_pressed[pygame.K_d]:
                        if right:
                            player.action = "idle_right"
                        else:
                            player.action = "idle_left"
                    elif keys_pressed[pygame.K_LEFT] or keys_pressed[pygame.K_a]:
                        player.action = "run_left"
                    elif keys_pressed[pygame.K_RIGHT] or keys_pressed[pygame.K_d]:
                        player.action = "run_right"
                else:
                    if right:
                        player.action = "jump_right"
                    else:
                        player.action = "jump_left"
            else:
                if right:
                    player.action = "idle_right"
                else:
                    player.action = "idle_left"
            


            if player.rect.y < screen.get_height() // 2:
                screen_offset_y = -100
            elif player.rect.y > screen.get_height() // 2 :
                screen_offset_y = player.rect.y - screen.get_height() // 2 - 100

            if player.rect.y > lowest_camera_y:
                screen_offset_y = lowest_camera_y - screen.get_height() // 2 - 100

            if pygame.sprite.collide_mask(player, key):
                key_collected = True
                key.rect.x = screen.get_width()/2 + 280
                key.rect.y = 20
                key.update()


            #Falling blocks
            for block in blocks1:
                if block.rect.x - player.rect.x < 30 and key_collected:
                    falling_blocks = True

            if falling_blocks:
                for block in blocks1:
                    block.rect.y += 6
            
            if player.rect.y > 2800:
                gameover = True
                bg_sound.stop()

            screen.fill((0, 0, 0))

            for x, y, image in background_layer.tiles():
                screen.blit(image, (x * tmxdata.tilewidth + screen_offset_x, y * tmxdata.tileheight - screen_offset_y))

            for block in blocks:
                block.rect.x += screen_offset_x
                block.rect.y -= screen_offset_y
                screen.blit(block.image, block.rect)
                block.rect.x -= screen_offset_x
                block.rect.y += screen_offset_y

            for block in blocks1:
                block.rect.x += screen_offset_x
                block.rect.y -= screen_offset_y
                screen.blit(block.image, block.rect)
                block.rect.x -= screen_offset_x
                block.rect.y += screen_offset_y

            if not key_collected:
                key.rect.x += screen_offset_x
                key.rect.y -= screen_offset_y
                screen.blit(key.image, key.rect)
                key.rect.x -= screen_offset_x
                key.rect.y += screen_offset_y
            else:
                screen.blit(key.image, key.rect)
                

            if key_collected:
                if abs(player.rect.center[0] - door.rect.center[0]) <= 4 and player.rect.center[1] > door.rect.top and player.rect.center[1] < door.rect.bottom:
                    bg_sound.stop()
                    reached = True
                    if player.alpha > 0:
                        player.alpha -= 5
                        player.image.set_alpha(player.alpha)
                    else:
                        nextlevel = True

            door.rect.x += screen_offset_x
            door.rect.y -= screen_offset_y
            screen.blit(door.image, door.rect)
            door.rect.x -= screen_offset_x
            door.rect.y += screen_offset_y

            player.rect.x += screen_offset_x
            player.rect.y -= screen_offset_y
            all_sprites.draw(screen)
            player.rect.x -= screen_offset_x
            player.rect.y += screen_offset_y
            
            mouse_pos = pygame.mouse.get_pos()
            quit_button.draw(screen, mouse_pos, 1)
            if (player.health <= 0):
                gameover = True
                bg_sound.stop()
            for i in range(0, player.health):
                hearts[i].draw()

            if gameover:
                for event in pygame.event.get():
                    if event.type == pygame.quit:
                        running = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if quit_button.is_clicked(event.pos):
                            return -1
                        elif main_menu_button.is_clicked(event.pos):
                            return -1
                        elif retry_button.is_clicked(event.pos):
                            return 0
                screen.blit(background.surf, background.rect)
                gameover_text.draw(screen)
                main_menu_button.draw(screen, mouse_pos, 1)
                retry_button.draw(screen, mouse_pos, 1)

            if nextlevel:
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if quit_button.is_clicked(event.pos):
                            return -1
                        elif nextlevel_main_menu_button.is_clicked(event.pos):
                            return -1
                        elif nextlevel_retry_button.is_clicked(event.pos):
                            return 2
                        elif nextlevel_button.is_clicked(event.pos):
                            return 1
                screen.blit(background.surf, background.rect)
                nextlevel_text.draw(screen)
                nextlevel_button.draw(screen, mouse_pos, 1)
                nextlevel_main_menu_button.draw(screen, mouse_pos, 1)
                nextlevel_retry_button.draw(screen, mouse_pos, 1)

            pygame.display.flip()
