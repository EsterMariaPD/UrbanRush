import pygame
from code.const import WIN_HEIGHT

class Player(pygame.sprite.Sprite):
    def __init__(self, player_id, spritesheet_path, damage_sound=None):
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

        self.jump_speed = -11
        self.gravity = 0.9
        self.vel_y = 0
        self.is_jumping = False
        self.jump_timer = 0
        self.jump_max_time = 30

        self.health = 3
        self.damage_cooldown = 0  # frames para invulnerabilidade

        self.damage_sound = damage_sound  # som do dano recebido

        # Hitbox menor e centralizada
        hitbox_width = int(self.rect.width * 0.6)
        hitbox_height = int(self.rect.height * 0.8)
        self.hitbox = pygame.Rect(0, 0, hitbox_width, hitbox_height)
        self.hitbox.center = self.rect.center

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

        if self.rect.bottom >= WIN_HEIGHT - 10:
            self.rect.bottom = WIN_HEIGHT - 10
            self.is_jumping = False
            self.vel_y = 0

        # Atualiza hitbox centralizada
        self.hitbox.center = self.rect.center

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

    def take_damage(self):
        if self.damage_cooldown == 0 and self.health > 0:
            self.health -= 1
            self.damage_cooldown = 60  # 1 segundo invulnerável (60 FPS)
            if self.damage_sound:
                self.damage_sound.play()
            print(f"Player {self.id} levou dano! Vida restante: {self.health}")

    def draw(self, surface):
        # Piscar durante o cooldown de dano
        if self.damage_cooldown > 0:
            # Pisca a cada 4 frames
            if (self.damage_cooldown // 4) % 2 == 0:
                surface.blit(self.image, self.rect)
        else:
            surface.blit(self.image, self.rect)
