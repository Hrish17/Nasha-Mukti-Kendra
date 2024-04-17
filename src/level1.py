import pygame
from pygame.locals import *
from pytmx.util_pygame import load_pygame

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
        self.rect = self.image.get_rect(topleft = (x, y))

class Door(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Door, self).__init__()
        original_image = pygame.image.load("assets/images/door.jpg").convert_alpha()
        self.image = pygame.transform.scale(original_image, (60, 90))
        self.rect = self.image.get_rect(topleft = (x, y))

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
    pygame.display.set_caption("AWARE US")

    screen_number = 1
    begin_button = Button(screen.get_width()/2 - 75, 500, 150, 50, (0, 0, 0), 'BEGIN', pygame.font.Font(None, 36), (255, 255, 255))
    controls = Text(screen.get_width()/2, 80, 'CONTROLS', pygame.font.Font(None, 60), (0, 0, 0))
    controls_image = Image(screen.get_width()/2 - 400, 150, pygame.image.load("assets/images/controls.png"), 800, 250)
    rule = Text(screen.get_width()/2, 450, 'Collect the key and reach the door to proceed to the next level', pygame.font.Font(None, 30), (67, 56, 165))

    #screen_number = 2
    tmxdata = load_pygame("assets/maps/level1.tmx")
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
    player.rect.y = 2532
    player_alpha = 255

    lowest_camera_y = player.rect.y

    key = Key(1850, 2300)
    door = Door(2600, 2470)

    moving_left = False
    moving_right = False

    move_speed = 4
    jumping = True

    og_jump_speed = 6
    jump_speed = 0
    max_fall_speed = 6

    gravity = 0.26

    screen_offset_x = -900
    screen_offset_y = 0

    key_collected = False
    reached = False

    falling_blocks = False

    running = True
    while running:
        if screen_number == 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if begin_button.is_clicked(event.pos):
                        screen_number = 2
            screen.fill((255, 255, 255))
            controls.draw(screen)
            screen.blit(controls_image.image, controls_image.rect)
            rule.draw(screen)
            begin_button.draw(screen)
            pygame.display.flip()

        elif screen_number == 2:
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
                # screen_offset_y += jump_speed
                jump_speed -= gravity
                if jump_speed <= -max_fall_speed:
                    jump_speed = -max_fall_speed
                if not jumping:
                    jump_speed = 0

            on_a_block = False

            # stopRight = False
            # stopLeft = False

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
                        # stopRight = True
                        player.rect.right = block.rect.left
                        screen_offset_x += 4
                        jumping = True
                        jump_speed = 0
                    elif player.rect.left <= block.rect.right and player.rect.right > block.rect.right:
                        moving_left = False
                        # stopLeft = True
                        player.rect.left = block.rect.right
                        screen_offset_x -= 4
                        jumping = True
                        jump_speed = 0
                # else:
                #     keys = pygame.key.get_pressed()
                #     if not stopRight and keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                #         moving_right = True
                #     elif not stopLeft and keys[pygame.K_LEFT] or keys[pygame.K_a]:
                #         moving_left = True

                if player.rect.bottom == block.rect.top and player.rect.left < block.rect.right and player.rect.right > block.rect.left:
                    on_a_block = True
            
            if not on_a_block:
                jumping = True

            if moving_right and not reached:
                player.rect.x += move_speed
                screen_offset_x -= move_speed
            if moving_left and not reached:
                player.rect.x -= move_speed
                screen_offset_x += move_speed


            if player.rect.y < screen.get_height() // 2:
                screen_offset_y = -100
            elif player.rect.y > screen.get_height() // 2 :
                screen_offset_y = player.rect.y - screen.get_height() // 2 - 100

            if player.rect.y > lowest_camera_y:
                screen_offset_y = lowest_camera_y - screen.get_height() // 2 - 100

            if player.rect.colliderect(key.rect):
                key_collected = True


            #Falling blocks
            for block in blocks1:
                if block.rect.x - player.rect.x < 30 and key_collected:
                    falling_blocks = True

            if falling_blocks:
                for block in blocks1:
                    block.rect.y += 6

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
                        player_alpha -= 6
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
