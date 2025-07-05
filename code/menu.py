# code/menu.py

import pygame
from code.const import WIN_WIDTH, WIN_HEIGHT, COLOR_TITLE_TEXT, COLOR_OPTION_TEXT_SELECTED, COLOR_OPTION_TEXT_NORMAL, \
    MENU_OPTIONS, COLOR_TEXT_SHADOW, COLOR_TEXT_HIGHLIGHT


class Menu:
    def __init__(self, window):
        self.window = window
        self.background = pygame.image.load('./assets/MenuBg.png').convert_alpha()
        self.background = pygame.transform.scale(self.background, (WIN_WIDTH, WIN_HEIGHT))
        self.rect = self.background.get_rect(topleft=(0, 0))

        try:
            pygame.mixer.init()
            pygame.mixer.music.load('./assets/Menu.wav')
            pygame.mixer.music.set_volume(0.5)
        except pygame.error as e:
            print(f"[AVISO] Erro ao carregar música: {e}")

        self.title_font_size = WIN_WIDTH // 15
        self.option_font_size = WIN_WIDTH // 35
        self.title_font = pygame.font.Font('./assets/04B_30__.TTF', self.title_font_size)
        self.option_font = pygame.font.Font('./assets/04B_30__.TTF', self.option_font_size)

    def run(self):
        menu_option = 0
        clock = pygame.time.Clock()

        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.play(-1)

        while True:
            self.window.blit(self.background, self.rect)

            # Título "URBAN RUSH" em lilás claro
            self.draw_text("URBAN", self.title_font, COLOR_TITLE_TEXT, (WIN_WIDTH // 2, WIN_HEIGHT // 6))
            self.draw_text("RUSH", self.title_font, COLOR_TITLE_TEXT, (WIN_WIDTH // 2, int(WIN_HEIGHT // 3.2)))

            # Opções do menu
            for i, option in enumerate(MENU_OPTIONS):
                color = COLOR_OPTION_TEXT_SELECTED if i == menu_option else COLOR_OPTION_TEXT_NORMAL
                y_pos = WIN_HEIGHT // 2 + i * (self.option_font_size * 2)
                self.draw_text(option, self.option_font, color, (WIN_WIDTH // 2, y_pos))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.mixer.music.stop()
                    return "exit"
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        menu_option = (menu_option + 1) % len(MENU_OPTIONS)
                    elif event.key == pygame.K_UP:
                        menu_option = (menu_option - 1) % len(MENU_OPTIONS)
                    elif event.key == pygame.K_RETURN:
                        pygame.mixer.music.stop()
                        return MENU_OPTIONS[menu_option]

            clock.tick(60)

    def draw_text(self, text, font, color, center_pos):
        # Sombra (preto, 2px para baixo e direita)
        shadow_surface = font.render(text, True, COLOR_TEXT_SHADOW)
        shadow_rect = shadow_surface.get_rect(center=(center_pos[0] + 2, center_pos[1] + 2))
        self.window.blit(shadow_surface, shadow_rect)

        # Luz (cinza claro, 1px para cima e esquerda)
        highlight_surface = font.render(text, True, COLOR_TEXT_HIGHLIGHT)
        highlight_rect = highlight_surface.get_rect(center=(center_pos[0] - 1, center_pos[1] - 1))
        self.window.blit(highlight_surface, highlight_rect)

        # Texto principal
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=center_pos)
        self.window.blit(text_surface, text_rect)
