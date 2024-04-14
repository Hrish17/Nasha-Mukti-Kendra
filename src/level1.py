import pygame
from pygame.locals import *
pygame.init()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((30, 30))
        self.surf.fill((0, 0, 0))
        self.rect = self.surf.get_rect()

class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super(Block, self).__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((100, 100, 100))
        self.rect = self.image.get_rect(topleft=(x, y))
    
    def update(self):
        self.rect.move

class Key(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Key, self).__init__()
        original_image = pygame.image.load("assets/key.webp").convert_alpha()
        scaled_image = pygame.transform.scale(original_image, (40, 40))
        rotated_image = pygame.transform.rotate(scaled_image, 90)
        self.image = rotated_image
        self.rect = self.image.get_rect(topleft=(x, y))

class Door(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Door, self).__init__()
        self.width = 60
        self.height = 90
        self.surf = pygame.Surface((self.width, self.height))
        self.surf.fill((255, 255, 255))
        pygame.draw.rect(self.surf, (0, 0, 0), (0, 0, self.width, self.height), 4)
        self.rect = self.surf.get_rect(topleft=(x, y))

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


def create_level(level_data):
    blocks = pygame.sprite.Group()
    for block_data in level_data:
        x, y, width, height = block_data
        block = Block(x, y, width, height)
        blocks.add(block)
    return blocks

blocks1 = [(2270, 1525, 100, 20), (2440, 1465, 100, 20), (2610, 1405, 100, 20), (2780, 1345, 100, 20), (2950, 1285, 100, 20)]
key1 = (3100, 1220)
door1 = (3600, 1510)

def play(screen):
    map_width = 10000
    map_height = 2000
    player = Player()
    blocks = create_level(blocks1)
    ground = Block(0, 1600, map_width, map_height - 525)
    blocks.add(ground)
    key = Key(key1[0], key1[1])
    door = Door(door1[0], door1[1])

    screen_width = screen.get_width()
    screen_height = screen.get_height()

    level_width = 500
    level_height = 500
    game_surface = pygame.Surface((level_width, level_height))

    quit_button = Button(1150, 40, 100, 50, (0, 0, 0), 'Quit', pygame.font.Font(None, 36), (255, 255, 255))
    key_collected = False

    player.rect.x = 2100
    player.rect.y = 1500

    moving_left = False
    moving_right = False
    jumping = False

    move_speed = 0.2
    move_accumulator = 0
    on_ground = True

    og_gravity = 0.4
    gravity = og_gravity
    gravity_accumulator = 0

    screen_offset_x = -1700
    screen_offset_y = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
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
                elif event.key == pygame.K_UP or event.key == pygame.K_SPACE or event.key == pygame.K_w:
                    if not jumping and on_ground:
                        on_ground = False
                        jumping = True

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    moving_left = False
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    moving_right = False


        if moving_right:
            move_accumulator += move_speed
            if move_accumulator >= 1:
                player.rect.x += int(move_accumulator)
                screen_offset_x -= int(move_accumulator)
                move_accumulator %= 1
        if moving_left:
            move_accumulator += move_speed
            if move_accumulator >= 1:
                player.rect.x -= int(move_accumulator)
                screen_offset_x += int(move_accumulator)
                move_accumulator %= 1

        for block in blocks:
            if player.rect.colliderect(block.rect):
                if jumping and player.rect.top < block.rect.bottom and player.rect.bottom > block.rect.top:
                    player.rect.top = block.rect.bottom
                    jumping = False
                    on_ground = False
                    gravity = 0.5
                # elif jumping and player.rect.bottom < block.rect.top:
                #     print("2")
                #     player.rect.bottom = block.rect.top
                #     jumping = False
                #     gravity = og_gravity
                elif player.rect.right > block.rect.left and player.rect.left < block.rect.left and (player.rect.bottom > block.rect.top + 1 and player.rect.top < block.rect.bottom):
                    player.rect.right = block.rect.left
                elif player.rect.left < block.rect.right and player.rect.right > block.rect.right and (player.rect.bottom > block.rect.top + 1 and player.rect.top < block.rect.bottom):
                    player.rect.left = block.rect.right
                else:
                    player.rect.y = block.rect.y - player.rect.height
                    on_ground = True
                    jumping = False
                    gravity = 0
            if player.rect.bottom == block.rect.top and on_ground:
                if player.rect.left >= block.rect.right or player.rect.right <= block.rect.left:
                    on_ground = False
                    gravity = og_gravity

        if jumping:
            player.rect.y -= 0.51
            gravity -= 0.0045
            if gravity < -0.5:
                jumping = False
                gravity = og_gravity

        gravity_accumulator += gravity
        if gravity_accumulator >= 1.1:
            player.rect.y += int(gravity_accumulator)
            gravity_accumulator %= 1
        
        # if(player.rect.y > 500):
        #     on_ground = True
        #     player.rect.y = 500
        #     gravity = 0.5
        #     jumping = False

        if(player.rect.left > map_width - 30):
            player.rect.x = map_width - 30
        elif(player.rect.x < 0):
            player.rect.x = 0

        if player.rect.colliderect(key.rect):
            key_collected = True
        
        if player.rect.colliderect(door.rect) and key_collected:
            return True

        # screen.fill((170, 170, 170))
        # if not key_collected:
        #     screen.blit(key.image, key.rect)
        # screen.blit(door.surf, door.rect)
        # blocks.draw(screen)
        # screen.blit(player.surf, player.rect)
        # quit_button.draw(screen)
        # pygame.display.flip()
        if player.rect.y < screen.get_height() // 2:
            screen_offset_y = 0
        elif player.rect.y > screen.get_height() // 2:
            screen_offset_y = player.rect.y - screen.get_height() // 2
        block_offset_x = -player.rect.x

        screen.fill((170, 170, 170))
        
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

        door.rect.x += screen_offset_x
        door.rect.y -= screen_offset_y
        screen.blit(door.surf, door.rect)
        door.rect.x -= screen_offset_x
        door.rect.y += screen_offset_y

        player.rect.x += screen_offset_x
        player.rect.y -= screen_offset_y
        screen.blit(player.surf, player.rect)
        player.rect.x -= screen_offset_x
        player.rect.y += screen_offset_y

        quit_button.draw(screen)
        pygame.display.flip()
