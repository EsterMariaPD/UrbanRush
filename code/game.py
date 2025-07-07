import pygame
import random
import os
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
        self.keys = pygame.sprite.Group()

        self.obstacle_timer = 0
        self.key_timer = 0

        self.obstacle_interval = 1500
        self.obstacle_speed = 6
        self.key_speed = 4

        self.collected_keys = 0
        self.keys_to_collect = 3
        self.level_number = 1

        self.menu_music_path = './assets/Menu.wav'
        self.game_over_sound = pygame.mixer.Sound('./assets/game_over.wav')
        self.key_sound = pygame.mixer.Sound('./assets/key_collect.wav')
        self.damage_sound = pygame.mixer.Sound('./assets/damage.wav')
        self.level_up_sound = pygame.mixer.Sound('./assets/level_up.wav')

        pygame.mixer.music.load(self.menu_music_path)
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

    def load_level_music(self, level_number):
        music_path = f'./assets/Level{level_number}.wav'
        try:
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)
            print(f"[INFO] Tocando música da fase {level_number}")
        except pygame.error as e:
            print(f"[ERRO] Música da fase {level_number} não encontrada: {e}")

    def run(self):
        while self.running:
            if self.state == "menu":
                if not pygame.mixer.music.get_busy() or pygame.mixer.music.get_pos() == -1:
                    pygame.mixer.music.load(self.menu_music_path)
                    pygame.mixer.music.play(-1)

                choice = self.menu.run()
                if choice == "EXIT":
                    self.running = False
                elif choice == "PLAYER 1":
                    self.start_game(player=1)
                elif choice == "PLAYER 2":
                    self.start_game(player=2)
                elif choice == "HOW TO PLAY":
                    self.display_how_to_play()

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

        self.obstacle_speed = 6
        self.key_speed = 4

        pygame.mixer.music.stop()
        self.load_level_music(self.level_number)

        self.running_game = True

        while self.running_game:
            dt = self.clock.tick(60)
            self.obstacle_speed += 0.001
            self.key_speed += 0.001

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running_game = False
                    self.running = False

            keys_pressed = pygame.key.get_pressed()
            jump_pressed = keys_pressed[pygame.K_SPACE]
            self.player.update(jump_pressed)

            now = pygame.time.get_ticks()
            if now - self.obstacle_timer > self.obstacle_interval:
                self.spawn_obstacle()
                self.obstacle_timer = now

            if now - self.key_timer > 2000:
                self.spawn_key()
                self.key_timer = now

            self.obstacles.update(self.obstacle_speed)
            self.keys.update(self.key_speed)

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
                self.running_game = False
                self.state = "menu"

            pygame.display.flip()

        self.level.stop_music()
        self.state = "menu"

    def on_key_collected(self, amount):
        self.collected_keys += amount
        self.key_sound.play()
        print(f"Chaves coletadas: {self.collected_keys}")

        if self.collected_keys >= self.keys_to_collect:
            self.level_number += 1

            next_level_bg_path = f'./assets/Level{self.level_number}Bg0.png'
            if not os.path.exists(next_level_bg_path):
                self.display_demo_warning()
                self.level.stop_music()
                pygame.mixer.music.load(self.menu_music_path)
                pygame.mixer.music.play(-1)

                self.running_game = False
                self.state = "menu"
                return

            print(f"Mudando para próximo nível: {self.level_number}")
            self.display_level_transition(f"LEVEL {self.level_number}")
            self.level = Level(level_number=self.level_number)
            self.keys.empty()
            self.obstacles.empty()
            self.collected_keys = 0
            self.player.health = 3
            self.obstacle_speed = 6
            self.key_speed = 4
            pygame.mixer.music.stop()
            self.load_level_music(self.level_number)

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

    def display_level_transition(self, text):
        blink_timer = 0
        blink_duration = 2000
        show_text = True
        start_time = pygame.time.get_ticks()
        self.level_up_sound.play()

        while pygame.time.get_ticks() - start_time < blink_duration:
            self.window.fill((0, 0, 0))

            overlay = pygame.Surface((WIN_WIDTH, WIN_HEIGHT))
            overlay.set_alpha(180)
            overlay.fill((0, 0, 0))
            self.window.blit(overlay, (0, 0))

            if show_text:
                level_text = self.pixel_font.render(text, True, (255, 255, 255))
                rect = level_text.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2))
                self.window.blit(level_text, rect)

            pygame.display.flip()

            blink_timer += self.clock.tick(5)
            if blink_timer > 300:
                show_text = not show_text
                blink_timer = 0

    def display_demo_warning(self):
        small_font = pygame.font.Font('./assets/04B_30__.TTF', 22)
        message1 = "LEVEL 3 - LOCKED"
        message2 = "This is a DEMO version of the game."
        message3 = "More levels coming soon!"
        prompt = "Press any key to return to menu"

        running = True
        show_text = True
        blink_timer = 0
        clock = pygame.time.Clock()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    running = False
                elif event.type == pygame.KEYDOWN:
                    running = False

            self.window.fill((0, 0, 0))
            overlay = pygame.Surface((WIN_WIDTH, WIN_HEIGHT))
            overlay.set_alpha(180)
            overlay.fill((0, 0, 0))
            self.window.blit(overlay, (0, 0))

            blink_timer += clock.tick(30)
            if blink_timer > 500:
                show_text = not show_text
                blink_timer = 0

            if show_text:
                text1 = small_font.render(message1, True, (255, 255, 0))
                text2 = small_font.render(message2, True, (255, 255, 255))
                text3 = small_font.render(message3, True, (200, 200, 200))
                prompt_text = small_font.render(prompt, True, (180, 180, 180))

                rect1 = text1.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2 - 50))
                rect2 = text2.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2 - 15))
                rect3 = text3.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2 + 20))
                rect_prompt = prompt_text.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2 + 70))

                self.window.blit(text1, rect1)
                self.window.blit(text2, rect2)
                self.window.blit(text3, rect3)
                self.window.blit(prompt_text, rect_prompt)

            pygame.display.flip()

    def display_how_to_play(self):
        font = pygame.font.Font('./assets/04B_30__.TTF', 17)
        lines = [
            "HOW TO PLAY:",
            "- Press SPACE to jump",
            "- Collect 3 keys to advance to the next level",
            "- Avoid ground and flying obstacles",
            "- You have 3 lives. If you lose all, it's Game Over.",
            "- Press any key to return to menu"
        ]

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    running = False
                elif event.type == pygame.KEYDOWN:
                    running = False

            self.window.fill((0, 0, 0))
            overlay = pygame.Surface((WIN_WIDTH, WIN_HEIGHT))
            overlay.set_alpha(180)
            overlay.fill((0, 0, 0))
            self.window.blit(overlay, (0, 0))

            for i, line in enumerate(lines):
                color = (255, 255, 255) if i == 0 else (200, 200, 200)
                text = font.render(line, True, color)
                rect = text.get_rect(center=(WIN_WIDTH // 2, 100 + i * 40))
                self.window.blit(text, rect)

            pygame.display.flip()
            self.clock.tick(30)
