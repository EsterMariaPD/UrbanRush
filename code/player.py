import pygame
from .const import WIN_WIDTH, WIN_HEIGHT

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

        # Hitbox menor (ajuste os valores para encaixar)
        self.hitbox = pygame.Rect(
            self.rect.left + 10,  # desloca 10px da esquerda
            self.rect.top + 10,   # desloca 10px de cima
            self.rect.width - 20, # reduz 20px na largura total
            self.rect.height - 15 # reduz 15px na altura total
        )

        self.frame_counter = 0
        self.animation_speed = 0.2

        self.jump_speed = -11
        self.gravity = 0.9
        self.vel_y = 0
        self.is_jumping = False
        self.jump_timer = 0
        self.jump_max_time = 30

        self.health = 3
        self.damage_cooldown = 0

        self.visible = True

        try:
            self.sound_damage = pygame.mixer.Sound('./assets/damage.wav')
        except pygame.error as e:
            print(f"Erro ao carregar som de dano: {e}")
            self.sound_damage = None

    def update(self, jump_pressed):
        if jump_pressed:
            if not self.is_jumping:
                self.is_jumping = True
                self.vel_y = self.jump_speed
                self.jump_timer = 0
            elif self.jump_timer < self.jump_max_time:
                self.vel_y += self.gravity / 3
                self.jump_timer += 1
            else:
                self.vel_y += self.gravity
        else:
            self.vel_y += self.gravity

        self.rect.y += self.vel_y

        # Atualiza a hitbox junto com o rect
        self.hitbox.topleft = (self.rect.left + 10, self.rect.top + 10)

        if self.rect.bottom >= WIN_HEIGHT - 10:
            self.rect.bottom = WIN_HEIGHT - 10
            self.is_jumping = False
            self.vel_y = 0

        if self.is_jumping:
            self.image = self.frames[3]
        else:
            self.frame_counter += self.animation_speed
            if self.frame_counter >= self.num_frames:
                self.frame_counter = 0
            self.current_frame = int(self.frame_counter)
            self.image = self.frames[self.current_frame]

        if self.damage_cooldown > 0:
            self.damage_cooldown -= 1
            if (self.damage_cooldown // 5) % 2 == 0:
                self.visible = False
            else:
                self.visible = True
        else:
            self.visible = True

    def take_damage(self):
        if self.damage_cooldown == 0 and self.health > 0:
            self.health -= 1
            self.damage_cooldown = 60
            if self.sound_damage:
                self.sound_damage.play()
            print(f"Player {self.id} levou dano! Life restante: {self.health}")

    def draw(self, surface):
        if self.visible:
            surface.blit(self.image, self.rect)
            # Debug: desenha hitbox em vermelho (apague ou comente depois)
            # pygame.draw.rect(surface, (255, 0, 0), self.hitbox, 1)
