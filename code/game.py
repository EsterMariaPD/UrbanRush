import pygame
import random
from code.const import WIN_WIDTH, WIN_HEIGHT
from code.menu import Menu
from code.level import Level
from code.player import Player
from code.obstacle import Obstacle

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        pygame.display.set_caption("Urban Rush")
        self.clock = pygame.time.Clock()
        self.running = True

        self.font = pygame.font.SysFont(None, 36)
        self.pixel_font = pygame.font.Font('./assets/04B_30__.TTF', 60)  # Fonte menor para GAME OVER

        self.menu = Menu(self.window)
        self.state = "menu"

        self.player = None
        self.level = None

        self.obstacles = pygame.sprite.Group()
        self.obstacle_timer = 0
        self.obstacle_interval = 1500

    def run(self):
        while self.running:
            if self.state == "menu":
                choice = self.menu.run()
                if choice == "SAIR" or choice == "exit":
                    self.running = False
                elif choice == "JOGAR COM PLAYER 1":
                    self.start_game(player=1)
                elif choice == "JOGAR COM PLAYER 2":
                    self.start_game(player=2)
                elif choice == "SCORE":
                    print("Mostrar placar futuramente!")

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.clock.tick(60)

    def start_game(self, player):
        self.level = Level(level_number=1)
        spritesheet_path = './assets/player_spritesheet.png' if player == 1 else './assets/player2_spritesheet.png'
        self.player = Player(player, spritesheet_path)

        self.obstacles.empty()
        self.obstacle_timer = pygame.time.get_ticks()

        running = True
        while running:
            dt = self.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    self.running = False

            keys = pygame.key.get_pressed()
            jump_pressed = keys[pygame.K_SPACE]
            self.player.update(jump_pressed)

            now = pygame.time.get_ticks()
            if now - self.obstacle_timer > self.obstacle_interval:
                self.spawn_obstacle()
                self.obstacle_timer = now

            self.obstacles.update()

            # Colisão usando hitbox menor do player
            for obstacle in self.obstacles:
                if obstacle.rect.colliderect(self.player.hitbox):
                    self.player.take_damage()
                    break  # Evita múltiplos danos no mesmo frame

            for obs in self.obstacles:
                if obs.rect.right < 0:
                    self.obstacles.remove(obs)

            self.level.update()
            self.window.fill((0, 0, 0))
            self.level.draw(self.window)
            self.player.draw(self.window)
            self.obstacles.draw(self.window)
            self.draw_health()

            if self.player.health <= 0:
                self.display_game_over()
                pygame.time.delay(2000)
                running = False
                self.state = "menu"

            pygame.display.flip()

        self.level.stop_music()
        self.state = "menu"

    def spawn_obstacle(self):
        is_flying = random.random() < 0.3
        image_path = './assets/obstacle_flying.png' if is_flying else './assets/obstacle_ground.png'
        obstacle = Obstacle(image_path, is_flying)
        self.obstacles.add(obstacle)

    def draw_health(self):
        text = self.font.render(f"Life: {self.player.health}", True, (255, 255, 255))  # branco
        self.window.blit(text, (10, 10))

    def display_game_over(self):
        pygame.mixer.Sound('./assets/game_over.wav').play()

        blink_timer = 0
        blink_duration = 2000  # milissegundos
        show_text = True
        start_time = pygame.time.get_ticks()

        while pygame.time.get_ticks() - start_time < blink_duration:
            self.window.fill((0, 0, 0))

            overlay = pygame.Surface((WIN_WIDTH, WIN_HEIGHT))
            overlay.set_alpha(180)
            overlay.fill((0, 0, 0))
            self.window.blit(overlay, (0, 0))

            if show_text:
                game_over_text = self.pixel_font.render("GAME OVER", True, (255, 0, 0))
                rect = game_over_text.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2))
                self.window.blit(game_over_text, rect)

            pygame.display.flip()

            blink_timer += self.clock.tick(5)
            if blink_timer > 200:
                show_text = not show_text
                blink_timer = 0
