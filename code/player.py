import pygame
from code.const import WIN_WIDTH, WIN_HEIGHT


class Player(pygame.sprite.Sprite):
    def __init__(self, player_id, spritesheet_path):
        super().__init__()
        self.id = player_id
        self.spritesheet = pygame.image.load(spritesheet_path).convert_alpha()

        self.frame_width = 48
        self.frame_height = 48
        self.num_frames = 6

        scale = 2
        self.frames = []
        for i in range(self.num_frames):
            rect = pygame.Rect(i * self.frame_width, 0, self.frame_width, self.frame_height)
            frame_image = self.spritesheet.subsurface(rect)
            frame_image = pygame.transform.scale(frame_image, (self.frame_width * scale, self.frame_height * scale))
            self.frames.append(frame_image)

        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect()

        self.rect.bottom = WIN_HEIGHT - 10
        self.rect.left = 50

        self.frame_counter = 0
        self.animation_speed = 0.2

        self.jump_speed = -11   # pulo maior para salto mais alto
        self.gravity = 0.9
        self.vel_y = 0
        self.is_jumping = False
        self.jump_timer = 0
        self.jump_max_time = 30  # pode segurar o pulo por mais tempo (frames)

    def update(self, jump_pressed):
        # Controle do pulo contínuo por pressão da tecla espaço
        if jump_pressed:
            if not self.is_jumping:
                # Inicia o pulo se não estiver pulando
                self.is_jumping = True
                self.vel_y = self.jump_speed
                self.jump_timer = 0
            elif self.jump_timer < self.jump_max_time:
                # Segura o pulo, desacelerando a gravidade enquanto segura a tecla
                self.vel_y += self.gravity / 3
                self.jump_timer += 1
            else:
                # Após tempo máximo, aplica gravidade normal
                self.vel_y += self.gravity
        else:
            # Soltou a tecla, aplica gravidade normal
            self.vel_y += self.gravity

        self.rect.y += self.vel_y

        # Checa o chão
        if self.rect.bottom >= WIN_HEIGHT - 10:
            self.rect.bottom = WIN_HEIGHT - 10
            self.is_jumping = False
            self.vel_y = 0

        # Animação: congela no frame 5 enquanto estiver pulando
        if self.is_jumping:
            self.image = self.frames[3]
        else:
            self.frame_counter += self.animation_speed
            if self.frame_counter >= self.num_frames:
                self.frame_counter = 0
            self.current_frame = int(self.frame_counter)
            self.image = self.frames[self.current_frame]

    def draw(self, surface):
        surface.blit(self.image, self.rect)
