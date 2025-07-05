import pygame
from code.const import WIN_WIDTH, WIN_HEIGHT
from code.menu import Menu


class Game:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        pygame.display.set_caption("Urban Rush")
        self.clock = pygame.time.Clock()
        self.running = True

        self.menu = Menu(self.window)
        self.state = "menu"

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
        # Tela temporária de carregamento
        self.window.fill((0, 0, 0))
        font = pygame.font.SysFont(None, 36)
        msg = f"Carregando Player {player}..."
        text = font.render(msg, True, (255, 255, 255))
        rect = text.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2))
        self.window.blit(text, rect)
        pygame.display.flip()
        pygame.time.delay(2000)

        # Depois volta pro menu por enquanto
        self.state = "menu"
