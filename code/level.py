import pygame
import os
from code.const import WIN_WIDTH, WIN_HEIGHT

class Level:
    def __init__(self, level_number):
        self.level_number = level_number
        self.scroll = 0

        self.backgrounds = []
        self.scroll_speeds = []

        assets_folder = './assets/'

        i = 0
        while True:
            filename = f'Level{level_number}Bg{i}.png'
            filepath = os.path.join(assets_folder, filename)
            if os.path.isfile(filepath):
                img = pygame.image.load(filepath).convert_alpha()
                img = pygame.transform.scale(img, (WIN_WIDTH, WIN_HEIGHT))
                self.backgrounds.append(img)

                # Define velocidade de scroll por camada (ajuste conforme quiser)
                speed = 0.3 + i * 0.1
                self.scroll_speeds.append(speed)

                i += 1
            else:
                break

    def update(self):
        # Ajuste a velocidade geral conforme seu jogo
        self.scroll += 2

    def draw(self, surface):
        for i, bg in enumerate(self.backgrounds):
            speed = self.scroll_speeds[i]
            width = bg.get_width()
            x_pos = - (self.scroll * speed) % width
            surface.blit(bg, (x_pos, 0))
            surface.blit(bg, (x_pos - width, 0))

    def stop_music(self):
        pygame.mixer.music.stop()
