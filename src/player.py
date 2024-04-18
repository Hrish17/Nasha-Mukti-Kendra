import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        images_path = 'assets/images/character/'
        new_width = 40
        new_height = 85
        # self.idle_images = [pygame.image.load(images_path + 'Idle' + str(i) + '.png').convert_alpha() for i in range(1, 7)]
        # self.run_images = [pygame.image.load(images_path + 'Run' + str(i) + '.png').convert_alpha() for i in range(1, 9)]
        # self.jump_images = [pygame.image.load(images_path + 'Jump' + str(i) + '.png').convert_alpha() for i in range(1, 11)]
        self.idle_right_images = [pygame.transform.scale(pygame.image.load(images_path + 'Idle' + str(i) + '.png').convert_alpha(), (new_width, new_height)) for i in range(1, 7)]
        self.run_right_images = [pygame.transform.scale(pygame.image.load(images_path + 'Run' + str(i) + '.png').convert_alpha(), (new_width, new_height)) for i in range(1, 9)]
        self.jump_right_images = [pygame.transform.scale(pygame.image.load(images_path + 'Jump' + str(i) + '.png').convert_alpha(), (new_width, new_height)) for i in range(1, 11)]
        
        self.idle_left_images = [pygame.transform.scale(pygame.image.load(images_path + 'flip_Idle' + str(i) + '.png').convert_alpha(), (new_width, new_height)) for i in range(1, 7)]
        self.run_left_images = [pygame.transform.scale(pygame.image.load(images_path + 'flip_Run' + str(i) + '.png').convert_alpha(), (new_width, new_height)) for i in range(1, 9)]
        self.jump_left_images = [pygame.transform.scale(pygame.image.load(images_path + 'flip_Jump' + str(i) + '.png').convert_alpha(), (new_width, new_height)) for i in range(1, 11)]

        self.alpha = 255

        self.image = self.idle_right_images[0]
        self.rect = self.image.get_rect()
        self.rect.x = 1100
        self.rect.y = 2500

        self.action = "idle_right"

        self.animation_index = 0
        self.animation_speed = 5
        self.animation_counter = 0

        self.image.set_alpha(self.alpha)

    def update(self):
        if self.action == "idle_right":
            self.animate(self.idle_right_images)
        elif self.action == "run_right":
            self.animate(self.run_right_images)
        elif self.action == "jump_right":
            self.animate(self.jump_right_images)
        elif self.action == "idle_left":
            self.animate(self.idle_left_images)
        elif self.action == "run_left":
            self.animate(self.run_left_images)
        elif self.action == "jump_left":
            self.animate(self.jump_left_images)

    def animate(self, images):
        if self.action == "idle":
            self.animation_speed = 10
        else:
            self.animation_speed = 5
        self.animation_counter += 1
        if self.animation_counter >= self.animation_speed:
            self.animation_counter = 0
            self.animation_index = (self.animation_index + 1) % len(images)
            self.image = images[self.animation_index]