import pygame
from pygame.locals import *
from pytmx.util_pygame import load_pygame

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((28, 28))
        self.surf.fill((0, 0, 0))
        self.rect = self.surf.get_rect()

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
        self.rect = self.image.get_rect(topleft=(x,y))

class Door(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Door, self).__init__()
        original_image = pygame.image.load("assets/images/door.jpg").convert_alpha()
        self.image = pygame.transform.scale(original_image, (60, 90))
        self.rect = self.image.get_rect(center = (x, y))

class Cigar():
    def __init__(self, x, y):
        super(Cigar, self).__init__()
        original_image = pygame.image.load("assets/images/cigar.png").convert_alpha()
        self.image = pygame.transform.scale(original_image, (35, 35))
        self.rect = self.image.get_rect(topleft=(x,y))

class Money():
    def __init__(self, x, y):
        super(Money, self).__init__()
        original_image = pygame.image.load("assets/images/money.png").convert_alpha()
        self.image = pygame.transform.scale(original_image, (30, 30))
        self.rect = self.image.get_rect(topleft=(x,y))

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

def create_level(blocks, tilewidth, tileheight):
    res = pygame.sprite.Group()
    for x,y,image in blocks.tiles():
        block = Block(x * tilewidth, y * tileheight, tilewidth, tileheight, image)
        res.add(block)
    return res

def play(screen):
    pygame.display.set_caption("Nasha Mukti Kendra")
    tmxdata = load_pygame("assets/maps/level4.tmx")
    background_layer = tmxdata.get_layer_by_name("Background")
    blocks_layer = tmxdata.get_layer_by_name("Blocks")
    killing_blocks_layer = tmxdata.get_layer_by_name("KillerBlocks")

    quit_button = Button(20, 40, 100, 50, (0, 0, 0), 'Quit', pygame.font.Font(None, 36), (255, 255, 255))

    blocks = create_level(blocks_layer, tmxdata.tilewidth, tmxdata.tileheight)
    killing_blocks = create_level(killing_blocks_layer, tmxdata.tilewidth, tmxdata.tileheight)

    blocks2 = pygame.sprite.Group()
    for block in blocks:
        blocks2.add(block)
    for block in killing_blocks:
        blocks2.add(block)

    player = Player()
    player.rect.x = 1100
    player.rect.y = 2000
    player_alpha = 255


    key = Key(2500, 1900)
    door = Door(4500, 1940)

    # print(key.rect.x, key.rect.y)
    intial_cigar = Cigar(2290, 1940)
    cigar1 = Cigar(2450, 1700)
    cigar2 = Cigar(2550, 1700)
    cigar3 = Cigar(2650, 1700)
    cigars = [cigar1, cigar2, cigar3]

    moving_left = False
    moving_right = False

    og_move_speed = 4
    move_speed = og_move_speed
    jumping = True

    og_jump_speed = 6
    jump_speed = 0
    max_fall_speed = 6

    gravity = 0.25

    screen_offset_x = -900
    screen_offset_y = 2000

    key_collected = False
    reached = False

    # running_cigar = False
    # dist_cigar_moved = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if quit_button.is_clicked(event.pos):
                    return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    moving_left = True
                    moving_right = False
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    moving_right = True
                    moving_left = False
                if event.key == pygame.K_UP or event.key == pygame.K_SPACE or event.key == pygame.K_w:
                    if not jumping:
                        jump_speed = og_jump_speed
                        jumping = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    moving_left = False
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    moving_right = False
        

        if jumping and not reached:
            player.rect.y -= jump_speed
            jump_speed -= gravity
            if jump_speed <= -max_fall_speed:
                jump_speed = -max_fall_speed
            if not jumping:
                jump_speed = 0

        on_a_block = False

        for block in blocks:
            if player.rect.colliderect(block.rect):
                if jumping and player.rect.top < block.rect.top and player.rect.bottom > block.rect.top:
                    player.rect.bottom = block.rect.top
                    jump_speed = 0
                    jumping = False
                elif jumping and player.rect.top < block.rect.bottom and player.rect.bottom > block.rect.bottom:
                    player.rect.top = block.rect.bottom
                    jumping = True
                    jump_speed = 0
                elif player.rect.right >= block.rect.left and player.rect.left < block.rect.left and (player.rect.bottom > block.rect.top and player.rect.top < block.rect.bottom):
                    moving_right = False
                    player.rect.right = block.rect.left
                    screen_offset_x += 4
                    jumping = True
                    jump_speed = 0
                elif player.rect.left <= block.rect.right and player.rect.right > block.rect.right and (player.rect.bottom > block.rect.top and player.rect.top < block.rect.bottom):
                    moving_left = False
                    player.rect.left = block.rect.right
                    screen_offset_x -= 4
                    jumping = True
                    jump_speed = 0
                    
            if player.rect.bottom == block.rect.top and player.rect.left < block.rect.right and player.rect.right > block.rect.left:
                on_a_block = True

        for block in killing_blocks:
            if player.rect.colliderect(block.rect):
                return False
        
        if not on_a_block:
            jumping = True

        if moving_right and not reached:
            player.rect.x += move_speed
            screen_offset_x -= move_speed
        if moving_left and not reached:
            player.rect.x -= move_speed
            screen_offset_x += move_speed


        if player.rect.y < screen.get_height() // 2:
            screen_offset_y = 0
        elif player.rect.y > screen.get_height() // 2:
            screen_offset_y = player.rect.y - screen.get_height() // 2
        block_offset_x = -player.rect.x

        if player.rect.colliderect(key.rect):
            key_collected = True

        if player.rect.colliderect(intial_cigar.rect):
            intial_cigar.rect.x = 0
            intial_cigar.rect.y = 0
            # move_speed -= 0.2

        for cigar in cigars:
            if player.rect.colliderect(cigar.rect):
                # move_speed -= 0.2
                cigar.rect.x = 0
                cigar.rect.y = 0
            if (cigar.rect.x - player.rect.x) < 200:
                if cigar.rect.y < 1940:
                    cigar.rect.y += 4
        screen.fill((0, 0, 0))

        for x, y, image in background_layer.tiles():
            screen.blit(image, (x * tmxdata.tilewidth + screen_offset_x, y * tmxdata.tileheight - screen_offset_y))

        for block in blocks:
            block.rect.x += screen_offset_x
            block.rect.y -= screen_offset_y
            screen.blit(block.image, block.rect)
            block.rect.x -= screen_offset_x
            block.rect.y += screen_offset_y

        for block in killing_blocks:
            block.rect.x += screen_offset_x
            block.rect.y -= screen_offset_y
            screen.blit(block.image, block.rect)
            block.rect.x -= screen_offset_x
            block.rect.y += screen_offset_y

        if key_collected:
            if abs(player.rect.center[0] - door.rect.center[0]) <= 4 and player.rect.center[1] > door.rect.top and player.rect.center[1] < door.rect.bottom:
                reached = True
                if player_alpha > 0:
                    player_alpha -= 1
                else:
                    return True


        door.rect.x += screen_offset_x
        door.rect.y -= screen_offset_y
        screen.blit(door.image, door.rect)
        door.rect.x -= screen_offset_x
        door.rect.y += screen_offset_y

        intial_cigar.rect.x += screen_offset_x
        intial_cigar.rect.y -= screen_offset_y
        screen.blit(intial_cigar.image, intial_cigar.rect)
        intial_cigar.rect.x -= screen_offset_x
        intial_cigar.rect.y += screen_offset_y
        for cigar in cigars:
            cigar.rect.x += screen_offset_x
            cigar.rect.y -= screen_offset_y
            screen.blit(cigar.image, cigar.rect)
            cigar.rect.x -= screen_offset_x
            cigar.rect.y += screen_offset_y

        if not key_collected:
            key.rect.x += screen_offset_x
            key.rect.y -= screen_offset_y
            screen.blit(key.image, key.rect)
            key.rect.x -= screen_offset_x
            key.rect.y += screen_offset_y
            # print(key.rect.x, key.rect.y)

        player.rect.x += screen_offset_x
        player.rect.y -= screen_offset_y
        player.surf.set_alpha(player_alpha)
        screen.blit(player.surf, player.rect)
        player.rect.x -= screen_offset_x
        player.rect.y += screen_offset_y
        
        quit_button.draw(screen)

        pygame.display.flip()
