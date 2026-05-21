from __future__ import annotations

from typing import TYPE_CHECKING
import pygame

from .base_screen import BaseScreen

if TYPE_CHECKING:
    from pacman.main import Engine


class MainMenu(BaseScreen):
    def __init__(self, engine: Engine) -> None:
        self.engine = engine

        self.font_title = pygame.font.Font(None, 64)
        self.font_btn = pygame.font.Font(None, 28)

        self.title_surface = self.font_title.render(
            "PAC MAN", True, (250, 250, 250)
        )
        self.title_rect = self.title_surface.get_rect(center=(400, 100))

        self.buttons = [
            ("Start Game", "game"),
            ("Highscores", "highscores"),
            ("Instructions", "instructions"),
            ("Exit", None),
        ]

        self.btn_rects = [
            pygame.Rect(300, 220 + i * 80, 200, 50)
            for i in range(len(self.buttons))
        ]

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for i, rect in enumerate(self.btn_rects):
                if rect.collidepoint(event.pos):
                    _, target = self.buttons[i]
                    if target is None:
                        pygame.quit()
                        raise SystemExit
                    self.engine.set_state(target)

    def update(self, dt: float) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        # Fill background
        background = pygame.Surface(surface.get_size())
        background = background.convert()
        surface.fill((0, 0, 0))

        # Draw title
        surface.blit(self.title_surface, self.title_rect)

        # Draw a line
        pygame.draw.line(surface, (255, 215, 0), (150, 165), (650, 165), 2)

        # Draw buttons
        mouse_pos = pygame.mouse.get_pos()
        for i, rect in enumerate(self.btn_rects):
            # Hover highlight
            is_hovered = rect.collidepoint(mouse_pos)
            bg_color = (255, 215, 0) if is_hovered else (30, 30, 60)
            txt_color = (10, 10, 26) if is_hovered else (255, 215, 0)

            pygame.draw.rect(surface, bg_color, rect, border_radius=8)
            pygame.draw.rect(surface, (255, 215, 0), rect, 2, border_radius=8)

            btn_name, _ = self.buttons[i]
            btn_surf = self.font_btn.render(btn_name, True, txt_color)
            btn_rect = btn_surf.get_rect(center=rect.center)
            surface.blit(btn_surf, btn_rect)
