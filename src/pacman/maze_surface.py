import pygame
from enum import IntFlag
from utils import PacmanErrors
from mazegenerator import mazegenerator



class Wall(IntFlag):
    NORD = 1 << 0
    EST = 1 << 1
    SUD = 1 << 2
    OUEST = 1 << 3


class MazeManager:
    """Renders a maze from a hexadecimal grid using pygame."""

    def __init__(self, cell_size: int, levels_config: dict[str, dict], seed: int) -> None:
        self.levels_config: dict[str, dict] = levels_config
        self.grids: dict[str, list[list[int]]] = {}
        self.seed = seed
        self.rows: int = len(grid)
        self.cols: int = len(grid[0])
        self.cell_size: int = cell_size
        self.wall_color: tuple[int, int, int] = (0, 0, 255)
        self.bg_color:   tuple[int, int, int] = (0, 0, 0)
 
    def _get_maze_dim_level(self, level: int = 0) -> tuple[int, int]:
        """"""
        if not isinstance(level, int):
            raise PacmanErrors(
                'prog',
                'Level must be an int.',
                'parse_config.py'
                )
        if level >= len(self.levels):
            raise PacmanErrors(
                'prog',
                'Level out of range.',
                'parse_config.py'
                )
        dimension_data = self.levels_config[str(level)]
        return tuple(x for x in dimension_data.values())
    
    def generate_mazes(self) -> None:

        for lvl in self.levels_config:
            dim = self._get_maze_dim_level(lvl)
            maze = mazegenerator.MazeGenerator(
                    size=dim,
                    seed=config.seed
                )
            self.grids[lvl] = maze._maze
    
    def _get_rows(self, level: int | str) -> int:
        """"""
        if level is int:
            level = str(level)
        if not self.levels_config.get(level):
            raise PacmanErrors(
                'prog',
                f'{level} not a valid key',
                'maze_surface.py'
                )
        dim = self.levels_config[level]
        return dim['height']

    def _get_cols(self, level: int | str) -> int:
        """"""
        if level is int:
            level = str(level)
        if not self.levels_config.get(level):
            raise PacmanErrors(
                'prog',
                f'{level} not a valid key',
                'maze_surface.py'
                )
        dim = self.levels_config[level]
        return dim['width']

    def _draw_cell(
        self,
        surface: pygame.Surface,
        row: int,
        col: int,
        value: int,
    ) -> None:
        """Draw the walls of a single cell based on its bitmask value."""
        x = col * self.cell_size
        y = row * self.cell_size
        s = self.cell_size
        wall_t = 2

        if value & Wall.NORD:
            pygame.draw.line(
                surface, self.wall_color, (x, y), (x + s, y), wall_t
                )
        if value & Wall.EST:
            pygame.draw.line(
                surface, self.wall_color, (x + s, y), (x + s, y + s), wall_t
                )
        if value & Wall.SUD:
            pygame.draw.line(
                surface, self.wall_color, (x, y + s), (x + s, y + s), wall_t
                )
        if value & Wall.OUEST:
            pygame.draw.line(
                surface, self.wall_color, (x, y), (x, y + s), wall_t
                )

    def generate_surface(self, level: int) -> pygame.Surface:
        """Main pygame loop."""
        pygame.init()
        width = self._get_cols(level) * self.cell_size + 10
        height = self._get_rows(level) * self.cell_size + 10
        screen = pygame.display.set_mode((width, height)) # verifier car on ne veut pas set toute la fenetre juste l'espace du maze.
        pygame.display.set_caption("Pac-Man Maze")
        clock = pygame.time.Clock()

        screen.fill(self.bg_color)
        for row, line in enumerate(self.grid):
            for col, value in enumerate(line):
                self._draw_cell(screen, row, col, value)
        pygame.display.flip()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            clock.tick(30)

        pygame.quit()


# --- Exemple d'utilisation ---

GRID = [
    [11, 9, 3, 9, 1, 1, 5, 3, 9, 1, 1, 1, 1, 5, 3, 9, 3, 13, 1, 3],
    [10, 10, 8, 6, 8, 2, 11, 10, 14, 10, 8, 0, 6, 9, 6, 10, 8, 3, 8, 2],
    [8, 4, 2, 11, 8, 4, 2, 12, 5, 4, 2, 10, 9, 6, 9, 2, 8, 4, 6, 10],
    [10, 13, 4, 6, 8, 1, 4, 5, 5, 1, 6, 14, 8, 5, 2, 10, 12, 1, 3, 10],
    [8, 5, 5, 1, 2, 8, 5, 5, 3, 8, 5, 5, 4, 5, 2, 12, 3, 10, 12, 2],
    [8, 1, 7, 12, 6, 10, 15, 9, 6, 10, 15, 15, 15, 9, 4, 1, 4, 4, 5, 2],
    [10, 10, 9, 1, 3, 10, 15, 12, 5, 4, 5, 7, 15, 10, 9, 4, 3, 9, 5, 6],
    [10, 8, 2, 8, 4, 6, 15, 15, 15, 11, 15, 15, 15, 10, 8, 5, 2, 10, 9, 3],
    [10, 10, 12, 0, 1, 5, 5, 3, 15, 10, 15, 13, 5, 2, 12, 5, 0, 6, 10, 10],
    [10, 12, 5, 6, 12, 5, 1, 2, 15, 10, 15, 15, 15, 12, 5, 3, 8, 5, 2, 10],
    [8, 7, 9, 5, 5, 5, 2, 8, 1, 4, 3, 13, 1, 1, 3, 12, 4, 5, 4, 2],
    [10, 9, 2, 9, 1, 5, 2, 10, 8, 7, 12, 5, 6, 10, 12, 1, 3, 9, 5, 2],
    [10, 12, 4, 6, 8, 3, 12, 4, 4, 1, 5, 5, 7, 8, 1, 2, 12, 6, 11, 10],
    [10, 9, 1, 3, 10, 12, 1, 1, 1, 6, 9, 5, 1, 6, 12, 4, 5, 5, 4, 6],
    [12, 4, 4, 4, 4, 5, 4, 4, 4, 5, 4, 5, 4, 5, 5, 5, 5, 5, 5, 7]
    ]

if __name__ == "__main__":
    try:
        from utils.parse_config import parse_config
        config = parse_config()
        cell_size = config.cell_size
        maze = MazeManager(cell_size, GRID)
        maze.generate_surface()
    except Exception as e:
        print(e)