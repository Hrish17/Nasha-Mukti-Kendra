import pygame
from pygame.locals import *

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

class Key(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Key, self).__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect(topleft=(x, y))

class Door(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Door, self).__init__()
        self.surf = pygame.Surface((60, 90))
        self.surf.fill((0, 255, 0))
        self.rect = self.surf.get_rect(topleft=(x, y))

def create_level(level_data):
    blocks = pygame.sprite.Group()
    for block_data in level_data:
        x, y, width, height = block_data
        block = Block(x, y, width, height)
        blocks.add(block)
    return blocks

def game(screen, level):
    player = Player()
    blocks = create_level(level[:-2])
    ground = Block(0, 525, 1250, 115)
    blocks.add(ground)
    key = Key(level[-2][0], level[-2][1])
    door = Door(level[-1][0], level[-1][1])
    gameOn = True

    key_collected = False

    player.rect.x = 100
    player.rect.y = 500

    moving_left = False
    moving_right = False
    jumping = False

    move_speed = 0.25
    move_accumulator = 0
    on_ground = True

    og_gravity = 0.5
    gravity = og_gravity
    gravity_accumulator = 0

    while gameOn:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_BACKSPACE:
                    gameOn = False
                elif event.key == K_LEFT or event.key == K_a:
                    moving_left = True
                    moving_right = False
                elif event.key == K_RIGHT or event.key == K_d:
                    moving_right = True
                    moving_left = False
                elif event.key == K_UP or event.key == K_SPACE or event.key == K_w:
                    if not jumping and on_ground:
                        on_ground = False
                        jumping = True

            elif event.type == KEYUP:
                if event.key == K_LEFT or event.key == K_a:
                    moving_left = False
                elif event.key == K_RIGHT or event.key == K_d:
                    moving_right = False

            elif event.type == QUIT:
                gameOn = False

        if moving_right:
            move_accumulator += move_speed
            if move_accumulator >= 1:
                player.rect.x += int(move_accumulator)
                move_accumulator %= 1
        if moving_left:
            move_accumulator += move_speed
            if move_accumulator >= 1:
                player.rect.x -= int(move_accumulator)
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
            gravity -= 0.005
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

        if(player.rect.left > screen.get_width() - 30):
            player.rect.x = screen.get_width() - 30
        elif(player.rect.x < 0):
            player.rect.x = 0

        if player.rect.colliderect(key.rect):
            key_collected = True


        screen.fill((170, 170, 170))
        if not key_collected:
            screen.blit(key.image, key.rect)
        screen.blit(door.surf, door.rect)
        blocks.draw(screen)
        screen.blit(player.surf, player.rect)
        pygame.display.flip()