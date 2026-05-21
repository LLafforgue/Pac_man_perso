import pygame
from pygame.locals import QUIT
from ui.screens.base_screen import BaseScreen
from ui.screens.main_menu import MainMenu


class Engine:
    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.states: dict[str, BaseScreen] = {
            "menu":      MainMenu(self),
            # "game":      GameView(self),
            # "pause":     PauseMenu(self),
            # "gameover":  GameOver(self),
            # "victory":   Victory(self),
            # "highscores": Highscores(self),
        }
        self.current_state: BaseScreen = self.states["menu"]
        self.running = False

    def set_state(self, name: str) -> None:
        self.current_state = self.states[name]

    def start_game(self) -> None:
        self.running = True
        clock = pygame.time.Clock()

        # Game loop
        while self.running:
            for event in pygame.event.get():
                self.current_state.handle_event(event)
                if event.type == QUIT:
                    self.running = False
                    return

            dt = clock.tick(60) / 1000.0  # delta time in seconds
            self.current_state.update(dt)
            self.current_state.draw(self.screen)
            pygame.display.flip()  # Push the surface to the monitor


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((1280, 920))
    pygame.display.set_caption('Pac-man')
    engine = Engine(screen)
    engine.start_game()


if __name__ == "__main__":
    main()
