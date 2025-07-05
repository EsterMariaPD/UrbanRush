import pygame
from code.const import WIN_WIDTH, WIN_HEIGHT
from code.menu import Menu
from code.level import Level
from code.player import Player


class Game:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        pygame.display.set_caption("Urban Rush")
        self.clock = pygame.time.Clock()
        self.running = True

        self.menu = Menu(self.window)
        self.state = "menu"

        self.player = None
        self.level = None

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

    def start_game(self, player):
        self.level = Level(level_number=1)

        # Define o caminho do spritesheet do player
        if player == 1:
            spritesheet_path = './assets/player_spritesheet.png'  # ajusta o caminho conforme seu arquivo
        else:
            spritesheet_path = './assets/player2_spritesheet.png'

        self.player = Player(player, spritesheet_path)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    self.running = False

            keys = pygame.key.get_pressed()
            self.player.handle_input(keys)

            self.level.update()
            self.window.fill((0, 0, 0))
            self.level.draw(self.window)
            self.player.draw(self.window)
            pygame.display.flip()
            self.clock.tick(60)

        self.level.stop_music()
        self.state = "menu"


if __name__ == "__main__":
    game = Game()
    game.run()
