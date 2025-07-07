import pygame
import random
from code.const import WIN_WIDTH, WIN_HEIGHT
from code.menu import Menu
from code.level import Level
from code.player import Player
from code.obstacle import Obstacle
from code.key import Key
from code.collision import Collision

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        pygame.display.set_caption("Urban Rush")
        self.clock = pygame.time.Clock()
        self.running = True

        self.font = pygame.font.SysFont(None, 36)
        self.pixel_font = pygame.font.Font('./assets/04B_30__.TTF', 30)

        self.menu = Menu(self.window)
        self.state = "menu"

        self.player = None
        self.level = None

        self.obstacles = pygame.sprite.Group()
        self.obstacle_timer = 0
        self.obstacle_interval = 1500

        self.keys = pygame.sprite.Group()
        self.key_timer = 0
        self.collected_keys = 0
        self.keys_to_collect = 3
        self.level_number = 1

        # Sons
        self.menu_music_path = './assets/Menu.wav'
        self.level_music_path = './assets/Level1.wav'
        self.game_over_sound = pygame.mixer.Sound('./assets/game_over.wav')
        self.key_sound = pygame.mixer.Sound('./assets/key_collect.wav')
        self.damage_sound = pygame.mixer.Sound('./assets/damage.wav')

        pygame.mixer.music.load(self.menu_music_path)
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

    def run(self):
        while self.running:
            if self.state == "menu":
                if not pygame.mixer.music.get_busy() or pygame.mixer.music.get_pos() == -1:
                    pygame.mixer.music.load(self.menu_music_path)
                    pygame.mixer.music.play(-1)

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
        self.level_number = 1
        self.level = Level(level_number=self.level_number)
        spritesheet_path = './assets/player_spritesheet.png' if player == 1 else './assets/player2_spritesheet.png'
        self.player = Player(player, spritesheet_path, damage_sound=self.damage_sound)

        self.obstacles.empty()
        self.keys.empty()
        self.obstacle_timer = pygame.time.get_ticks()
        self.key_timer = pygame.time.get_ticks()
        self.collected_keys = 0

        pygame.mixer.music.stop()
        pygame.mixer.music.load(self.level_music_path)
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

        running = True
        while running:
            dt = self.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    self.running = False

            keys_pressed = pygame.key.get_pressed()
            jump_pressed = keys_pressed[pygame.K_SPACE]
            self.player.update(jump_pressed)

            now = pygame.time.get_ticks()
            if now - self.obstacle_timer > self.obstacle_interval:
                self.spawn_obstacle()
                self.obstacle_timer = now

            if now - self.key_timer > 10000:
                self.spawn_key()
                self.key_timer = now

            self.obstacles.update()
            self.keys.update()

            Collision.check_obstacle_collision(self.player, self.obstacles)
            Collision.check_star_collection(self.player, self.keys, self.on_key_collected)

            for obs in self.obstacles:
                if obs.rect.right < 0:
                    self.obstacles.remove(obs)

            self.level.update()
            self.window.fill((0, 0, 0))
            self.level.draw(self.window)
            self.player.draw(self.window)
            self.obstacles.draw(self.window)
            self.keys.draw(self.window)
            self.draw_health()

            if self.player.health <= 0:
                pygame.mixer.music.stop()
                self.game_over_sound.play()
                self.display_game_over()
                pygame.time.delay(2000)
                running = False
                self.state = "menu"

            pygame.display.flip()

        self.level.stop_music()
        self.state = "menu"

    def on_key_collected(self, amount):
        self.collected_keys += amount
        self.key_sound.play()
        print(f"Chaves coletadas: {self.collected_keys}")

        if self.collected_keys >= self.keys_to_collect:
            print("Mudando para próximo nível!")
            self.level_number += 1
            self.level = Level(level_number=self.level_number)
            self.keys.empty()
            self.obstacles.empty()
            self.collected_keys = 0

    def spawn_obstacle(self):
        is_flying = random.random() < 0.3
        image_path = './assets/obstacle_flying.png' if is_flying else './assets/obstacle_ground.png'
        obstacle = Obstacle(image_path, is_flying)
        self.obstacles.add(obstacle)

    def spawn_key(self):
        x = WIN_WIDTH + 50
        y = random.choice([WIN_HEIGHT - 60, WIN_HEIGHT - 150])
        key = Key('./assets/key.png', x, y)
        self.keys.add(key)

    def draw_health(self):
        life_text = self.font.render(f"Life: {self.player.health}", True, (255, 255, 255))
        keys_text = self.font.render(f"Keys: {self.collected_keys}", True, (255, 255, 255))
        self.window.blit(life_text, (10, 10))
        self.window.blit(keys_text, (10, 40))

    def display_game_over(self):
        blink_timer = 0
        blink_duration = 2000
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
