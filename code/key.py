import pygame
from code.const import WIN_WIDTH, WIN_HEIGHT

class Key(pygame.sprite.Sprite):
    def __init__(self, image_path, x, y):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = 4  # mesma velocidade do obstáculo terrestre

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill()
