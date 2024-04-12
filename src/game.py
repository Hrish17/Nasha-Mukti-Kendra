import pygame
from pygame.locals import *

class Square(pygame.sprite.Sprite):
    def __init__(self):
        super(Square, self).__init__()
        self.surf = pygame.Surface((25, 25))
        self.surf.fill((0, 0, 0))
        self.rect = self.surf.get_rect()

class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super(Block, self).__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((100, 100, 100))
        self.rect = self.image.get_rect(topleft=(x, y))

def create_level(level_data):
    blocks = pygame.sprite.Group()
    for block_data in level_data:
        x, y, width, height = block_data
        block = Block(x, y, width, height)
        blocks.add(block)
    return blocks

def game(screen, level):
    square1 = Square()
    blocks = create_level(level)
    ground = Block(0, 525, 1250, 115)
    blocks.add(ground)
    gameOn = True

    square1.rect.x = 100
    square1.rect.y = 500

    moving_left = False
    moving_right = False
    jumping = False

    move_speed = 0.35
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
                elif event.key == K_LEFT:
                    moving_left = True
                    moving_right = False
                elif event.key == K_RIGHT:
                    moving_right = True
                    moving_left = False
                elif event.key == K_UP:
                    if not jumping and on_ground:
                        on_ground = False
                        jumping = True

            elif event.type == KEYUP:
                if event.key == K_LEFT:
                    moving_left = False
                elif event.key == K_RIGHT:
                    moving_right = False

            elif event.type == QUIT:
                gameOn = False

        if moving_right:
            move_accumulator += move_speed
            if move_accumulator >= 1:
                square1.rect.x += int(move_accumulator)
                move_accumulator %= 1
        if moving_left:
            move_accumulator += move_speed
            if move_accumulator >= 1:
                square1.rect.x -= int(move_accumulator)
                move_accumulator %= 1

        for block in blocks:
            if square1.rect.colliderect(block.rect):
                if jumping and square1.rect.top < block.rect.bottom and square1.rect.bottom > block.rect.top:
                    square1.rect.top = block.rect.bottom
                    jumping = False
                    on_ground = False
                    gravity = 0.5
                # elif jumping and square1.rect.bottom < block.rect.top:
                #     print("2")
                #     square1.rect.bottom = block.rect.top
                #     jumping = False
                #     gravity = og_gravity
                elif square1.rect.right > block.rect.left and square1.rect.left < block.rect.left and (square1.rect.bottom > block.rect.top + 1 and square1.rect.top < block.rect.bottom):
                    square1.rect.right = block.rect.left
                elif square1.rect.left < block.rect.right and square1.rect.right > block.rect.right and (square1.rect.bottom > block.rect.top + 1 and square1.rect.top < block.rect.bottom):
                    square1.rect.left = block.rect.right
                else:
                    square1.rect.y = block.rect.y - square1.rect.height
                    on_ground = True
                    jumping = False
                    gravity = 0
            if square1.rect.bottom == block.rect.top and on_ground:
                if square1.rect.left >= block.rect.right or square1.rect.right <= block.rect.left:
                    on_ground = False
                    gravity = og_gravity

        if jumping:
            square1.rect.y -= 0.6
            gravity -= 0.006
            if gravity < -0.5:
                jumping = False
                gravity = og_gravity

        gravity_accumulator += gravity
        if gravity_accumulator >= 1:
            square1.rect.y += int(gravity_accumulator)
            gravity_accumulator %= 1
        
        # if(square1.rect.y > 500):
        #     on_ground = True
        #     square1.rect.y = 500
        #     gravity = 0.5
        #     jumping = False

        if(square1.rect.x > 1225):
            square1.rect.x = 1225
        elif(square1.rect.x < 0):
            square1.rect.x = 0

        screen.fill((170, 170, 170))
        screen.blit(square1.surf, square1.rect)
        blocks.draw(screen)
        pygame.display.flip()

pygame.init()
screen = pygame.display.set_mode((1250, 640))
level1 = [(320, 460, 100, 20), (200, 400, 50, 50)]  # Example level data with two blocks
game(screen, level1)