import pygame
from code.const import WIN_WIDTH, WIN_HEIGHT

class Key(pygame.sprite.Sprite):
    def __init__(self, image_path, x, y):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, speed=None):
        # Se receber velocidade, move a chave para a esquerda
        if speed is not None:
            self.rect.x -= speed
        else:
            # Caso não receba velocidade, usa um valor padrão
            self.rect.x -= 5

        # Remove a chave se ela sair da tela
        if self.rect.right < 0:
            self.kill()
