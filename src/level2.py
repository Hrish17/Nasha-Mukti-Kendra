import pygame
from pygame.locals import *
from pytmx.util_pygame import load_pygame
import player as character

class Image(pygame.sprite.Sprite):
    def __init__(self, x, y, image, width, height):
        super(Image, self).__init__()
        self.image = pygame.transform.scale(image, (width, height))
        self.rect = self.image.get_rect(topleft = (x, y))
        self.width = width
        self.height = height
        
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

class Key(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Key, self).__init__()
        original_image = pygame.image.load("assets/images/key.png").convert_alpha()
        scaled_image = pygame.transform.scale(original_image, (40, 40))
        rotated_image = pygame.transform.rotate(scaled_image, 90)
        self.image = rotated_image
        self.rect = self.image.get_rect(topleft=(x, y))

class Door(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Door, self).__init__()
        original_image = pygame.image.load("assets/images/door.jpg").convert_alpha()
        self.image = pygame.transform.scale(original_image, (60, 90))
        self.rect = self.image.get_rect(topleft=(x, y))

class Background(pygame.sprite.Sprite):
    def __init__(self,x,y,width,height,color):
        super(Background, self).__init__()
        self.surf = pygame.Surface((width, height))
        self.surf.fill(color)
        self.rect = self.surf.get_rect()
        self.rect.x = x
        self.rect.y = y

class Cigar(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Cigar, self).__init__()
        original_image = pygame.image.load("assets/images/cigar.png").convert_alpha()
        self.image = pygame.transform.scale(original_image, (50, 50))
        self.rect = self.image.get_rect(topleft=(x, y))

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

def create_level(blocks, tilewidth, tileheight):
    res = pygame.sprite.Group()
    for x,y,image in blocks.tiles():
        block = Block(x * tilewidth, y * tileheight, tilewidth, tileheight, image)
        res.add(block)
    return res

def play(screen):
    pygame.display.set_caption("NASHA MUKTI KENDRA")

    screen_number = 1
    level2 = Text(screen.get_width()/2, 100, 'LEVEL 2', pygame.font.Font(None, 80), (255, 255, 255))
    text1 = Text(screen.get_width()/2, 250, 'Smoking is injurious to health', pygame.font.Font(None, 50), (255, 0,0))
    text2 = Text(screen.get_width()/2, 300, 'Smoking kills', pygame.font.Font(None, 50), (255, 0, 0))
    begin_button = Button(screen.get_width()/2 - 75, 420, 150, 50, (70, 70, 70), 'BEGIN', pygame.font.Font(None, 36), (255, 255, 255), (100, 100, 100))

    #screen_number = 2
    tmxdata = load_pygame("assets/maps/level2.tmx")
    background_layer = tmxdata.get_layer_by_name("Background")
    blocks_layer = tmxdata.get_layer_by_name("Blocks")
    blocks1_layer = tmxdata.get_layer_by_name("Blocks1")

    quit_button = Button(20, 40, 100, 50, (0, 0, 0), 'Quit', pygame.font.Font(None, 36), (255, 255, 255), (43, 44, 48))

    blocks = create_level(blocks_layer, tmxdata.tilewidth, tmxdata.tileheight)
    blocks1 = create_level(blocks1_layer, tmxdata.tilewidth, tmxdata.tileheight)

    blocks2 = pygame.sprite.Group()
    for block in blocks:
        blocks2.add(block)
    for block in blocks1:
        blocks2.add(block)

    player = character.Player()
    all_sprites = pygame.sprite.Group(player)

    lowest_camera_y = player.rect.y


    key = Key(2250, 2300)
    door = Door(2600, 2470)

    cigar = Cigar(2000, 2380)

    moving_left = False
    moving_right = False
    right = True

    og_move_speed = 4
    move_speed = og_move_speed
    jumping = True

    og_jump_speed = 6
    jump_speed = 0
    max_fall_speed = 6

    gravity = 0.27

    screen_offset_x = -900
    screen_offset_y = 0

    key_collected = False
    reached = False

    running_cigar = False
    dist_cigar_moved = 0

    falling_blocks = False

    background = Background(200, 100, 700, 400, (43, 44, 48))
    gameover_text = Text(screen.get_width()/2, 200, 'GAME OVER', pygame.font.Font(None, 80), (255, 0, 0))
    main_menu_button = Button(screen.get_width()/2 - 75, 420, 150, 50, (70, 70, 70), 'Main Menu', pygame.font.Font(None, 36), (255, 255, 255), (100, 100, 100))
    retry_button = Button(screen.get_width()/2 - 75, 350, 150, 50, (70, 70, 70), 'Retry', pygame.font.Font(None, 36), (255, 255, 255), (100, 100, 100))
    gameover = False

    running = True
    clock = pygame.time.Clock()
    while running:
        clock.tick(60)
        if screen_number == 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return -1
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if begin_button.is_clicked(event.pos):
                        screen_number = 2
            screen.fill((43, 44, 48))
            level2.draw(screen)
            text1.draw(screen)
            text2.draw(screen)
            mouse_pos = pygame.mouse.get_pos()
            begin_button.draw(screen, mouse_pos, 1)
            pygame.display.flip()
        elif screen_number == 2:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return -1
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if quit_button.is_clicked(event.pos):
                        return -1
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        moving_left = True
                        moving_right = False
                        right = False
                        # player.action = "run_left"
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        moving_right = True
                        moving_left = False
                        right = True
                        # player.action = "run_right"
                    if event.key == pygame.K_UP or event.key == pygame.K_SPACE or event.key == pygame.K_w:
                        if not jumping:
                            jump_speed = og_jump_speed
                            jumping = True
                        # if right:    
                        #     player.action = "jump_right"
                        # else:
                        #     player.action = "jump_left"
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        moving_left = False
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        moving_right = False

            all_sprites.update()
            

            if jumping and not reached:
                player.rect.y -= jump_speed
                # screen_offset_y += jump_speed
                jump_speed -= gravity
                if jump_speed <= -max_fall_speed:
                    jump_speed = -max_fall_speed
                if not jumping:
                    jump_speed = 0

            on_a_block = False

            for block in blocks2:
                if player.rect.colliderect(block.rect):
                    if jumping and player.rect.top < block.rect.top and player.rect.bottom > block.rect.top:
                        player.rect.bottom = block.rect.top
                        jump_speed = 0
                        jumping = False
                    elif jumping and player.rect.top < block.rect.bottom and player.rect.bottom > block.rect.bottom:
                        player.rect.top = block.rect.bottom
                        jumping = True
                        jump_speed = 0
                    elif player.rect.right >= block.rect.left and player.rect.left < block.rect.left:
                        moving_right = False
                        player.rect.right = block.rect.left
                        screen_offset_x += 4
                        jumping = True
                        jump_speed = 0
                    elif player.rect.left <= block.rect.right and player.rect.right > block.rect.right:
                        moving_left = False
                        player.rect.left = block.rect.right
                        screen_offset_x -= 4
                        jumping = True
                        jump_speed = 0
                        
                if player.rect.bottom == block.rect.top and player.rect.left < block.rect.right and player.rect.right > block.rect.left:
                    on_a_block = True
            
            if not on_a_block:
                jumping = True

            if moving_right and not reached and not gameover:
                player.rect.x += move_speed
                screen_offset_x -= move_speed
            if moving_left and not reached and not gameover:
                player.rect.x -= move_speed
                screen_offset_x += move_speed

            keys_pressed = pygame.key.get_pressed()
            if not gameover:
                if not jumping:
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
            elif player.rect.y > screen.get_height() // 2:
                screen_offset_y = player.rect.y - screen.get_height() // 2 - 100

            if player.rect.y > lowest_camera_y:
                screen_offset_y = lowest_camera_y - screen.get_height() // 2 - 100

            if player.rect.colliderect(key.rect):
                key_collected = True
            
            #Moving cigar
            if player.rect.colliderect(cigar.rect):
                gameover = True
            
            if cigar.rect.x - player.rect.x < 200 and player.rect.y - cigar.rect.y < 100:
                running_cigar = True

            if running_cigar and dist_cigar_moved < 300 and not gameover:
                cigar.rect.x -= 5
                dist_cigar_moved += 5

            #Falling blocks
            for block in blocks1:
                if block.rect.x - player.rect.x < 30 and key_collected:
                    falling_blocks = True

            if falling_blocks:
                for block in blocks1:
                    block.rect.y += 6

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

            if key_collected:
                if abs(player.rect.center[0] - door.rect.center[0]) <= 4 and player.rect.center[1] > door.rect.top and player.rect.center[1] < door.rect.bottom:
                    reached = True
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

            cigar.rect.x += screen_offset_x
            cigar.rect.y -= screen_offset_y
            screen.blit(cigar.image, cigar.rect)
            cigar.rect.x -= screen_offset_x
            cigar.rect.y += screen_offset_y

            player.rect.x += screen_offset_x
            player.rect.y -= screen_offset_y
            all_sprites.draw(screen)
            player.rect.x -= screen_offset_x
            player.rect.y += screen_offset_y
            
            mouse_pos = pygame.mouse.get_pos()
            quit_button.draw(screen, mouse_pos, 1)

            if gameover:
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if main_menu_button.is_clicked(event.pos):
                            return -1
                        elif retry_button.is_clicked(event.pos):
                            return 0
                screen.blit(background.surf, background.rect)
                gameover_text.draw(screen)
                main_menu_button.draw(screen, mouse_pos, 1)
                retry_button.draw(screen, mouse_pos, 1)

            pygame.display.flip()