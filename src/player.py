import pygame


class Player(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()

        self.sprite_sheet = pygame.image.load("../assets/sprites/Amelia_32x32.png")
        self.image = self.get_image(0,0)

        self.images = {
            "down": self.get_image(96,20),
            "left": self.get_image(64,20),
            "right": self.get_image(0,20),
            "up": self.get_image(32,20)
        }

        self.position = [x, y]
        self.change_animation("down")
        self.rect = self.image.get_rect()
        self.speed = 5

        self.feet = pygame.Rect(0, 0, self.rect.width * 0.5, 8)
        self.old_position = self.position.copy()

    def save_location(self):
        self.old_position = self.position.copy()

    def run(self):
        self.speed = 20

    def walk(self):
        self.speed = 5

    def change_animation(self, name):
        self.image = self.images[name]
        self.image.set_colorkey([0,0,0])

    def move_right(self):
        self.save_location()
        #self.feet = pygame.Rect(0,0, 6, 4)
        self.change_animation("right")
        self.position[0] += self.speed

    def move_left(self):
        self.save_location()
        #self.feet = pygame.Rect(0,0, 16, 4)
        self.position[0] -= self.speed
        self.change_animation("left")

    def move_up(self):
        self.save_location()
        #self.feet = pygame.Rect(0,0, 4, 8)
        self.position[1] -= self.speed
        self.change_animation("up")

    def move_down(self):
        self.save_location()
        #self.feet = pygame.Rect(0,0, 4, 1)
        self.position[1] += self.speed
        self.change_animation("down")

    def update(self):
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

    def move_back(self):
        self.position = self.old_position
        self.update()

    def get_image(self, x, y):
        image = pygame.Surface([32,44])
        image.blit(self.sprite_sheet, (0, 0), (x, y, 32, 44))

        return image
