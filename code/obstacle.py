import pygame
from code.const import WIN_WIDTH, WIN_HEIGHT

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, image_path, is_flying):
        super().__init__()
        self.is_flying = is_flying

        if self.is_flying:
            spritesheet = pygame.image.load(image_path).convert_alpha()
            self.frame_width = 96
            self.frame_height = 96
            self.num_frames = 4
            self.frames = []

            for i in range(self.num_frames):
                rect = pygame.Rect(i * self.frame_width, 0, self.frame_width, self.frame_height)
                frame = spritesheet.subsurface(rect)
                frame = pygame.transform.scale(frame, (int(self.frame_width * 1.5), int(self.frame_height * 1.5)))
                self.frames.append(frame)

            self.current_frame = 0
            self.animation_speed = 0.2
            self.frame_counter = 0
            self.image = self.frames[self.current_frame]
            self.rect = self.image.get_rect()
            self.rect.bottom = WIN_HEIGHT - 150
            self.speed = 6
        else:
            image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(image, (60, 60))
            self.rect = self.image.get_rect()
            self.rect.bottom = WIN_HEIGHT - 10
            self.speed = 4

        self.rect.left = WIN_WIDTH

    def update(self, speed=None):
        if speed is not None:
            self.rect.x -= speed
        else:
            self.rect.x -= self.speed

        if self.is_flying:
            self.frame_counter += self.animation_speed
            if self.frame_counter >= self.num_frames:
                self.frame_counter = 0
            self.current_frame = int(self.frame_counter)
            self.image = self.frames[self.current_frame]

    def draw(self, surface):
        surface.blit(self.image, self.rect)
