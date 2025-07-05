import pygame
import os
from code.const import WIN_WIDTH, WIN_HEIGHT

class BackgroundLayer:
    def __init__(self, image, speed, position):
        self.image = pygame.transform.scale(image, (WIN_WIDTH, WIN_HEIGHT))
        self.speed = speed
        self.x = position

    def update(self):
        self.x -= self.speed
        if self.x <= -WIN_WIDTH:
            self.x += WIN_WIDTH * 2  # loop contínuo, assume 2 blocos

    def draw(self, surface):
        surface.blit(self.image, (self.x, 0))


class Level:
    def __init__(self, level_number: int, assets_path='./assets'):
        self.level_number = level_number
        self.assets_path = assets_path
        self.layers = []

        prefix = f"Level{level_number}Bg"
        self.music_path = os.path.join(assets_path, f"Level{level_number}.mp3")

        # Carrega imagens do fundo
        images = []
        for file in sorted(os.listdir(assets_path)):
            if file.startswith(prefix) and file.endswith('.png'):
                images.append(os.path.join(assets_path, file))

        # Cria camadas em pares para efeito parallax
        for i, img_path in enumerate(images):
            image = pygame.image.load(img_path).convert_alpha()
            speed = 1 + i  # velocidade aumenta conforme a camada (0 -> 1, 1 -> 2, ...)
            self.layers.append(BackgroundLayer(image, speed, 0))
            self.layers.append(BackgroundLayer(image, speed, WIN_WIDTH))

        # Inicializa o mixer de música
        try:
            pygame.mixer.music.load(self.music_path)
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.play(-1)
        except pygame.error as e:
            print(f"[WARN] Não foi possível carregar a música: {self.music_path} - {e}")

    def update(self):
        for layer in self.layers:
            layer.update()

    def draw(self, surface):
        for layer in self.layers:
            layer.draw(surface)

    def stop_music(self):
        pygame.mixer.music.stop()
