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
        self.rect = self.image.get_rect(topleft=(x, y))

class Door(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Door, self).__init__()
        original_image = pygame.image.load("assets/images/door.jpg").convert_alpha()
        self.image = pygame.transform.scale(original_image, (60, 90))
        self.rect = self.image.get_rect(topleft=(x, y))

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
    tmxdata = load_pygame("assets/maps/level3.tmx")
    background_layer = tmxdata.get_layer_by_name("Background")
    blocks_layer = tmxdata.get_layer_by_name("Blocks")
    blocks1_layer = tmxdata.get_layer_by_name("Blocks1")

    quit_button = Button(20, 40, 100, 50, (0, 0, 0), 'Quit', pygame.font.Font(None, 36), (255, 255, 255))

    blocks = create_level(blocks_layer, tmxdata.tilewidth, tmxdata.tileheight)
    blocks1 = create_level(blocks1_layer, tmxdata.tilewidth, tmxdata.tileheight)

    blocks2 = pygame.sprite.Group()
    for block in blocks:
        blocks2.add(block)
    for block in blocks1:
        blocks2.add(block)

    player = Player()
    player.rect.x = 1100
    player.rect.y = 2000
    player_alpha = 255


    key = Key(2500, 2500)
    door = Door(2600, 2500)

    moving_left = False
    moving_right = False
    jumping = False

    standing_block = None

    og_move_speed = 1.5
    move_speed = og_move_speed
    move_accumulator = 0
    on_ground = True

    og_gravity = 2.0
    gravity = og_gravity
    gravity_accumulator = 0

    screen_offset_x = -900
    screen_offset_y = 2000

    key_collected = False
    reached = False

    running = True
    while running:
        # print ("yes")
        # screen_offset_x = min(-1000, max(screen_offset_x, -3500))
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
                    if not jumping and on_ground:
                        on_ground = False
                        jumping = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    moving_left = False
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    moving_right = False
        
        if moving_right and not reached:
            move_accumulator += move_speed
            if move_accumulator >= 1:
                player.rect.x += int(move_accumulator)
                # if screen_offset_x > -10000:
                screen_offset_x -= int(move_accumulator)
                move_accumulator %= 1
        if moving_left and not reached:
            move_accumulator += move_speed
            if move_accumulator >= 1:
                player.rect.x -= int(move_accumulator)
                # if screen_offset_x < 10000:
                screen_offset_x += int(move_accumulator)
                move_accumulator %= 1

        for block in blocks2:
            if player.rect.colliderect(block.rect):
                if jumping and player.rect.top < block.rect.bottom and player.rect.bottom > block.rect.top:
                    player.rect.top = block.rect.bottom
                    jumping = False
                    on_ground = False
                    gravity = 0.5
                elif player.rect.right > block.rect.left and player.rect.left < block.rect.left and (player.rect.bottom > block.rect.top + 1 and player.rect.top < block.rect.bottom):
                    player.rect.right = block.rect.left
                elif player.rect.left < block.rect.right and player.rect.right > block.rect.right and (player.rect.bottom > block.rect.top + 1 and player.rect.top < block.rect.bottom):
                    player.rect.left = block.rect.right
                else:
                    player.rect.y = block.rect.y - player.rect.height - 1
                    on_ground = True
                    standing_block = block
                    jumping = False
                    gravity = 0
            if player.rect.y == block.rect.y - player.rect.height - 1 and on_ground and block == standing_block:
                if player.rect.left >= block.rect.right or player.rect.right <= block.rect.left:
                    on_ground = False
                    gravity = og_gravity

        if jumping and not reached:
            move_speed = og_move_speed + 0.4
            player.rect.y -= 5
            gravity -= 0.05
            if gravity < -0.4:
                jumping = False
                gravity = og_gravity
                move_speed = og_move_speed

        gravity_accumulator += gravity
        if gravity_accumulator >= 1.1 and not reached:
            player.rect.y += int(gravity_accumulator)
            gravity_accumulator %= 1

        if on_ground:
            move_speed = og_move_speed

        if player.rect.y < screen.get_height() // 2:
            screen_offset_y = 0
        elif player.rect.y > screen.get_height() // 2:
            screen_offset_y = player.rect.y - screen.get_height() // 2
        block_offset_x = -player.rect.x

        if player.rect.colliderect(key.rect):
            key_collected = True


        #Falling blocks
        for block in blocks1:
            if block.rect.x - player.rect.x < 30 and block.rect.y < 1000 and key_collected:
                block.rect.y += 1

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
            if player.rect.center[0] == door.rect.center[0] and player.rect.center[1] > door.rect.top and player.rect.center[1] < door.rect.bottom:
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

        player.rect.x += screen_offset_x
        player.rect.y -= screen_offset_y
        player.surf.set_alpha(player_alpha)
        screen.blit(player.surf, player.rect)
        player.rect.x -= screen_offset_x
        player.rect.y += screen_offset_y
        
        quit_button.draw(screen)

        pygame.display.flip()
