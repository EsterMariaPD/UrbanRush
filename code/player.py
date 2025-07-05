import pygame
from code.const import WIN_WIDTH, WIN_HEIGHT


class Player(pygame.sprite.Sprite):
    def __init__(self, player_id, spritesheet_path):
        super().__init__()
        self.id = player_id

        # Carrega o spritesheet
        self.spritesheet = pygame.image.load(spritesheet_path).convert_alpha()

        # Cada frame tem 48x48 px, total 6 frames
        self.frame_width = 48
        self.frame_height = 48
        self.num_frames = 6

        # Extrai os frames do spritesheet
        self.frames = []
        for i in range(self.num_frames):
            rect = pygame.Rect(i * self.frame_width, 0, self.frame_width, self.frame_height)
            frame_image = self.spritesheet.subsurface(rect)
            self.frames.append(frame_image)

        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect()

        # Posição inicial fixa para ambos os players
        self.rect.bottom = WIN_HEIGHT - 10
        self.rect.left = 50  # mesma posição para os dois

        self.speed = 5
        self.animation_speed = 0.2
        self.frame_counter = 0

    def handle_input(self, keys):
        moved = False

        if self.id == 1:
            if keys[pygame.K_LEFT]:
                self.rect.x -= self.speed
                moved = True
            if keys[pygame.K_RIGHT]:
                self.rect.x += self.speed
                moved = True
            if keys[pygame.K_UP]:
                self.rect.y -= self.speed
                moved = True
            if keys[pygame.K_DOWN]:
                self.rect.y += self.speed
                moved = True
        else:  # player 2 usa WASD
            if keys[pygame.K_a]:
                self.rect.x -= self.speed
                moved = True
            if keys[pygame.K_d]:
                self.rect.x += self.speed
                moved = True
            if keys[pygame.K_w]:
                self.rect.y -= self.speed
                moved = True
            if keys[pygame.K_s]:
                self.rect.y += self.speed
                moved = True

        # Limita dentro da tela
        self.rect.left = max(0, self.rect.left)
        self.rect.right = min(WIN_WIDTH, self.rect.right)
        self.rect.top = max(0, self.rect.top)
        self.rect.bottom = min(WIN_HEIGHT, self.rect.bottom)

        # Atualiza animação se moveu
        if moved:
            self.frame_counter += self.animation_speed
            if self.frame_counter >= self.num_frames:
                self.frame_counter = 0
            self.current_frame = int(self.frame_counter)
            self.image = self.frames[self.current_frame]
        else:
            self.image = self.frames[0]

    def draw(self, surface):
        surface.blit(self.image, self.rect)
