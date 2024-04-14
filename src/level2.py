import pygame
from pygame.locals import *
from pytmx.util_pygame import load_pygame

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((30, 30))
        self.surf.fill((0, 0, 0))
        self.rect = self.surf.get_rect()

pygame.init()

# Set up the Pygame window
screen_width = 1024
screen_height = 680
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Tiled Map Demo")

# Load the Tiled map
tmxdata = load_pygame("assets/maps/untitled.tmx")

# Get the background layer
background_layer = tmxdata.get_layer_by_name("Background")

# Get the blocks layer
blocks_layer = tmxdata.get_layer_by_name("Blocks")

player = Player()

moving_left = False
moving_right = False
jumping = False

move_speed = 0.2
move_accumulator = 0
on_ground = True

og_gravity = 0.4
gravity = og_gravity
gravity_accumulator = 0

# Main game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
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
            # screen_offset_x -= int(move_accumulator)
            move_accumulator %= 1
    if moving_left:
        move_accumulator += move_speed
        if move_accumulator >= 1:
            player.rect.x -= int(move_accumulator)
            # screen_offset_x += int(move_accumulator)
            move_accumulator %= 1

    # for block in blocks:
    #     if player.rect.colliderect(block.rect):
    #         if jumping and player.rect.top < block.rect.bottom and player.rect.bottom > block.rect.top:
    #             player.rect.top = block.rect.bottom
    #             jumping = False
    #             on_ground = False
    #             gravity = 0.5
    #         elif player.rect.right > block.rect.left and player.rect.left < block.rect.left and (player.rect.bottom > block.rect.top + 1 and player.rect.top < block.rect.bottom):
    #             player.rect.right = block.rect.left
    #         elif player.rect.left < block.rect.right and player.rect.right > block.rect.right and (player.rect.bottom > block.rect.top + 1 and player.rect.top < block.rect.bottom):
    #             player.rect.left = block.rect.right
    #         else:
    #             player.rect.y = block.rect.y - player.rect.height
    #             on_ground = True
    #             jumping = False
    #             gravity = 0
    #     if player.rect.bottom == block.rect.top and on_ground:
    #         if player.rect.left >= block.rect.right or player.rect.right <= block.rect.left:
    #             on_ground = False
    #             gravity = og_gravity

    # Iterate through the blocks layer
    for x, y, image in blocks_layer.tiles():
        block_rect = pygame.Rect(x * tmxdata.tilewidth, y * tmxdata.tileheight, tmxdata.tilewidth, tmxdata.tileheight)
        if player.rect.colliderect(block_rect):
            # Collision detected, handle accordingly
            if jumping and player.rect.top < block_rect.bottom and player.rect.bottom > block_rect.top:
                # Player was jumping and collided with the top of the block
                player.rect.top = block_rect.bottom
                jumping = False
                on_ground = False
                gravity = 0.5
            elif player.rect.right > block_rect.left and player.rect.left < block_rect.left and (player.rect.bottom > block_rect.top + 1 and player.rect.top < block_rect.bottom):
                # Player collided with the right side of the block
                player.rect.right = block_rect.left
            elif player.rect.left < block_rect.right and player.rect.right > block_rect.right and (player.rect.bottom > block_rect.top + 1 and player.rect.top < block_rect.bottom):
                # Player collided with the left side of the block
                player.rect.left = block_rect.right
            else:
                # Player collided with the bottom of the block
                player.rect.y = block_rect.y - player.rect.height
                on_ground = True
                jumping = False
                gravity = 0

        if player.rect.bottom == block_rect.top and on_ground:
            if player.rect.left >= block_rect.right or player.rect.right <= block_rect.left:
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

    # Clear the screen
    screen.fill((0, 0, 0))

    # Render the background layer
    for x, y, image in background_layer.tiles():
        screen.blit(image, (x * tmxdata.tilewidth, y * tmxdata.tileheight))

    # Render the blocks layer
    for x, y, image in blocks_layer.tiles():
        screen.blit(image, (x * tmxdata.tilewidth, y * tmxdata.tileheight))

    screen.blit(player.surf, player.rect)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
