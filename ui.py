import pygame
from core.config import WIDTH, HEIGHT

class GameUI:
    def __init__(self, screen):
        self.screen = screen
        # self.state = state
        self.title_font = pygame.font.SysFont('Arial', 32, bold=True)
        self.ui_font = pygame.font.SysFont('Arial', 20)
        self.small_font = pygame.font.SysFont('Arial', 16)
        
        self.instructions_x = WIDTH - 280

    def draw(self):
        # self.draw_background()
        self.draw_title()
        self.draw_instructions()
        self.draw_debug()

        # pygame.display.flip()

    # def draw_background(self):
    #     for y in range(HEIGHT):
    #         color = 240 - int(y / HEIGHT * 40)
    #         pygame.draw.line(self.screen, (color, color, color), (0, y), (WIDTH, y))

    def draw_title(self):
        # self.screen.blit(self.title_font.render("Jogo", True, (30, 30, 60)), (30, 15))
        # self.screen.blit(self.small_font.render("Input Buffer System", True, (80, 80, 120)), (35, 50))
        pass
    
    def draw_instructions(self):
        # panel_rect = pygame.Rect(self.instructions_x - 10, 15, 270, 150)
        # pygame.draw.rect(self.screen, (60, 60, 35, 10), panel_rect, border_radius=8)
        # pygame.draw.rect(self.screen, (100, 100, 120), panel_rect, 2, border_radius=8)

        instructions = [
            # "CONTROLS:",
            # "Arrow keys - Add actions",
            # "Space - Toggle pause",
            # "L - Load sequence",
            # "C - Clear buffer",
            # "ESC - Quit"
        ]

        for i, text in enumerate(instructions):
            color = (255, 220, 150) if i == 0 else (220, 220, 220)
            surface = self.ui_font.render(text, True, color)
            self.screen.blit(surface, (self.instructions_x, 30 + i * 25))

    def draw_debug(self):
        # info = self.state.debug_info
        # lines = [
        #     f"P1 Frame: {info.get('current_frame_p1', 0)}",
        #     f"P1 Buffer: {info.get('buffer_size_p1', 0)}",
        #     f"P1 Priority: {info.get('priority_size_p1', 0)}",
        #     info.get('last_frame_action_p1', ''),
        #     "",
        #     f"P2 Frame: {info.get('current_frame_p2', 0)}",
        #     f"P2 Buffer: {info.get('buffer_size_p2', 0)}",
        #     f"P2 Priority: {info.get('priority_size_p2', 0)}",
        #     info.get('last_frame_action_p2', '')
        # ]
        # for i, text in enumerate(lines):
        #     if text:
        #         surface = self.small_font.render(text, True, (50, 50, 50))
        #         self.screen.blit(surface, (30, HEIGHT - 20 - i * 18))
        pass