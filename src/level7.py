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
        original_image = pygame.image.load("assets/images/door2.jpg").convert_alpha()
        self.image = pygame.transform.scale(original_image, (60, 90))
        self.rect = self.image.get_rect(center = (x, y))

class Cigar():
    def __init__(self, x, y):
        super(Cigar, self).__init__()
        original_image = pygame.image.load("assets/images/cigar.png").convert_alpha()
        self.image = pygame.transform.scale(original_image, (40, 40))
        self.rect = self.image.get_rect(topleft=(x,y))
        self.mask = pygame.mask.from_surface(self.image)

class Cherry(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Cherry, self).__init__()
        original_image = pygame.image.load("assets/images/cherries.png").convert_alpha()
        self.image = pygame.transform.scale(original_image, (50, 50))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.mask = pygame.mask.from_surface(self.image)

class Alcohol():
    def __init__(self, x, y):
        super(Alcohol, self).__init__()
        original_image = pygame.image.load("assets/images/alcohol.png").convert_alpha()
        self.image = pygame.transform.scale(original_image, (40, 40))
        self.rect = self.image.get_rect(topleft=(x,y))
        self.mask = pygame.mask.from_surface(self.image)

class Lemon():
    def __init__(self, x, y):
        super(Lemon, self).__init__()
        original_image = pygame.image.load("assets/images/lemon.png").convert_alpha()
        self.image = pygame.transform.scale(original_image, (40, 40))
        self.rect = self.image.get_rect(topleft=(x,y))
        self.mask = pygame.mask.from_surface(self.image)

class Cocaine():
    def __init__(self, x, y):
        super(Cocaine, self).__init__()
        original_image = pygame.image.load("assets/images/cocaine.png").convert_alpha()
        self.image = pygame.transform.scale(original_image, (170, 150))
        self.rect = self.image.get_rect(topleft=(x,y))
        self.mask = pygame.mask.from_surface(self.image)

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

def create_level(blocks, tilewidth, tileheight):
    res = pygame.sprite.Group()
    for x,y,image in blocks.tiles():
        block = Block(x * tilewidth, y * tileheight, tilewidth, tileheight, image)
        res.add(block)
    return res

def play(screen):
    pygame.display.set_caption("NASHA MUKTI KENDRA")

    # screen number = 1
    screen_number = 1
    level4 = Text(screen.get_width()/2, 100, 'LEVEL 7', pygame.font.Font(None, 80), (255, 255, 255))
    text1 = Text(screen.get_width()/2, 230, 'Excessive alcohol exposure results in cerebellar ataxia', pygame.font.Font(None, 50), (255, 0, 0))
    text2 = Text(screen.get_width()/2, 300, 'and can lead to impaired postural stability and balance', pygame.font.Font(None, 50), (255, 0, 0))
    begin_button = Button(screen.get_width()/2 - 75, 420, 150, 50, (70, 70, 70), 'BEGIN', pygame.font.Font(None, 36), (255, 255, 255), (100, 100, 100))

    # screen number = 2
    heart1 = Image(screen, screen.get_width()/2 + 350, 30, 32, 32, 'assets/images/heart.png')
    heart2 = Image(screen, screen.get_width()/2 + 390, 30, 32, 32, 'assets/images/heart.png')
    heart3 = Image(screen, screen.get_width()/2 + 430, 30, 32, 32, 'assets/images/heart.png')
    heart4 = Image(screen, screen.get_width()/2 + 470, 30, 32, 32, 'assets/images/heart.png')
    heart5 = Image(screen, screen.get_width()/2 + 510, 30, 32, 32, 'assets/images/heart.png')
    hearts = [heart1, heart2, heart3, heart4, heart5]
    tmxdata = load_pygame("assets/maps/level7.tmx")
    background_layer = tmxdata.get_layer_by_name("Background")
    blocks_layer = tmxdata.get_layer_by_name("Blocks")

    player = character.Player()
    all_sprites = pygame.sprite.Group(player)

    quit_button = Button(20, 40, 100, 50, (0, 0, 0), 'Quit', pygame.font.Font(None, 36), (255, 255, 255), (43, 44, 48))

    blocks = create_level(blocks_layer, tmxdata.tilewidth, tmxdata.tileheight)

    lowest_camera_y = player.rect.y

    key = Key(3680, 2450)
    door = Door(5060, 2290)

    alcohol1 = Alcohol(2925, 2245)
    alcohol2 = Alcohol(3820, 2320)
    alcohol3 = Alcohol(3875, 2336)
    alcohol4 = Alcohol(3930, 2352)
    alcohol5 = Alcohol(3985, 2368)
    alcohols = [Alcohol(1670, 2520), Alcohol(1900, 2520), Alcohol(2590, 2200), Alcohol(2783, 2358), Alcohol(2813, 2358), Alcohol(2850, 2390), Alcohol(2880, 2390), alcohol1, Alcohol(2970, 2390), Alcohol(3000, 2390), Alcohol(3040, 2358), Alcohol(3070, 2358), Alcohol(3360, 2200), Alcohol(3840, 2200), alcohol2, alcohol3, alcohol4, alcohol5, Alcohol(4500, 2112), Alcohol(5540, 2270)]
    moving_alcohol = [alcohol2, alcohol3, alcohol4, alcohol5]
    moving_up = [False, False, False, False]
    naughty_alcohol = [alcohol1]
    alochol_naughty = False

    lemon = Lemon(4736, 2112)
    
    cherries = [Cherry(1795, 2510), Cherry(2925, 2390)]

    right = True    # face direction of player

    og_move_speed = 4
    move_speed = og_move_speed
    jumping = True

    og_jump_speed = 6
    jump_speed = 0
    max_fall_speed = 6

    gravity = 0.24

    screen_offset_x = -700
    screen_offset_y = 0


    key_collected = False
    reached = False

    background = Background(200, 100, 700, 400, (43, 44, 48))
    gameover_text = Text(screen.get_width()/2, 200, 'GAME OVER', pygame.font.Font(None, 80), (255, 0, 0))
    main_menu_button = Button(screen.get_width()/2 - 75, 420, 150, 50, (70, 70, 70), 'Main Menu', pygame.font.Font(None, 36), (255, 255, 255), (100, 100, 100))
    retry_button = Button(screen.get_width()/2 - 75, 350, 150, 50, (70, 70, 70), 'Retry', pygame.font.Font(None, 36), (255, 255, 255), (100, 100, 100))
    gameover = False

    bg_sound = pygame.mixer.Sound('./assets/sounds/bg.mp3')
    bg_played = False
    jump_sound = pygame.mixer.Sound('./assets/sounds/jump.mp3')
    key_sound = pygame.mixer.Sound('./assets/sounds/key.mp3')
    win_sound = pygame.mixer.Sound('./assets/sounds/win.mp3')
    win_sound_played = False
    gameover_sound = pygame.mixer.Sound('./assets/sounds/gameover.mp3')
    gameover_sound_played = False

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
            screen.fill((43, 44, 48))
            level4.draw(screen)
            text1.draw(screen)
            text2.draw(screen)
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
            if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and (not alochol_naughty):
                dx -= move_speed
                right = False
            elif (keys[pygame.K_LEFT] or keys[pygame.K_a]) and (alochol_naughty):
                dx += move_speed
                right = True
            if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and (not alochol_naughty):
                dx += move_speed
                right = True
            elif (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and (alochol_naughty):
                dx -= move_speed
                right = False
            
            all_sprites.update()

            if not reached:
                jump_speed -= gravity
                if jump_speed <= -max_fall_speed:
                    jump_speed = -max_fall_speed
            dy -= jump_speed

            for block in blocks:
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
                    elif (keys_pressed[pygame.K_LEFT] or keys_pressed[pygame.K_a]) and (not alochol_naughty):
                        player.action = "run_left"
                    elif (keys_pressed[pygame.K_RIGHT] or keys_pressed[pygame.K_d]) and (not alochol_naughty):
                        player.action = "run_right"
                    elif (keys_pressed[pygame.K_LEFT] or keys_pressed[pygame.K_a]) and (alochol_naughty):
                        player.action = "run_right"
                    elif (keys_pressed[pygame.K_RIGHT] or keys_pressed[pygame.K_d]) and (alochol_naughty):
                        player.action = "run_left"
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
            elif player.rect.y > screen.get_height() // 2:
                screen_offset_y = player.rect.y - screen.get_height() // 2 - 100

            if player.rect.y > lowest_camera_y:
                screen_offset_y = lowest_camera_y - screen.get_height() // 2 - 100

            if pygame.sprite.collide_mask(player, key):
                key_collected = True
                key_sound.play()
                key.rect.x = screen.get_width()/2 + 280
                key.rect.y = 20
                key.update()

            for cherry in cherries:
                if pygame.sprite.collide_mask(player, cherry):
                    cherry.rect.x = 0
                    cherry.rect.y = 0
                    player.update_health(1)

            for alcohol in naughty_alcohol:
                if pygame.sprite.collide_mask(player, alcohol):
                    alcohol.rect.x = 0
                    alcohol.rect.y = 0
                    alochol_naughty = not alochol_naughty
            for alcohol in alcohols:
                if pygame.sprite.collide_mask(player, alcohol):
                    alcohol.rect.x = 0
                    alcohol.rect.y = 0
                    player.update_health(-1)
            for i in range(4):
                alcohol = moving_alcohol[i]
                if (alcohol.rect.y == 2320):
                    moving_up[i] = False
                if (alcohol.rect.y == 2520):
                    moving_up[i] = True
                if not moving_up[i]:
                    alcohol.rect.y += 4
                if moving_up[i]:
                    alcohol.rect.y -= 4

            if pygame.sprite.collide_mask(player, lemon):
                lemon.rect.x = 0
                lemon.rect.y = 0
                alochol_naughty = not alochol_naughty

            if player.rect.y > 2800:
                gameover = True

            screen.fill((0, 0, 0))

            for x, y, image in background_layer.tiles():
                screen.blit(image, (x * tmxdata.tilewidth + screen_offset_x, y * tmxdata.tileheight - screen_offset_y))

            for block in blocks:
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
                    reached = True
                    bg_sound.stop()
                    if not win_sound_played:
                        win_sound.play()
                        win_sound_played = True
                    if player.alpha > 0:
                        player.alpha -= 5
                        player.image.set_alpha(player.alpha)
                    else:
                        return 1


            door.rect.x += screen_offset_x
            door.rect.y -= screen_offset_y
            screen.blit(door.image, door.rect)
            door.rect.x -= screen_offset_x
            door.rect.y += screen_offset_y

            for cherry in cherries:
                cherry.rect.x += screen_offset_x
                cherry.rect.y -= screen_offset_y
                screen.blit(cherry.image, cherry.rect)
                cherry.rect.x -= screen_offset_x
                cherry.rect.y += screen_offset_y

            for alcohol in alcohols:
                alcohol.rect.x += screen_offset_x
                alcohol.rect.y -= screen_offset_y
                screen.blit(alcohol.image, alcohol.rect)
                alcohol.rect.x -= screen_offset_x
                alcohol.rect.y += screen_offset_y

            lemon.rect.x += screen_offset_x
            lemon.rect.y -= screen_offset_y
            screen.blit(lemon.image, lemon.rect)
            lemon.rect.x -= screen_offset_x
            lemon.rect.y += screen_offset_y            

            player.rect.x += screen_offset_x
            player.rect.y -= screen_offset_y
            all_sprites.draw(screen)
            player.rect.x -= screen_offset_x
            player.rect.y += screen_offset_y
        
            mouse_pos = pygame.mouse.get_pos()
            quit_button.draw(screen, mouse_pos, 1)

            if player.health <= 0:
                gameover = True
            for i in range(0, player.health):
                hearts[i].draw()

            if gameover:
                bg_sound.stop()
                if not gameover_sound_played:
                    gameover_sound.play()
                    gameover_sound_played = True
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
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

            pygame.display.flip()