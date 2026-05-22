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

    def __init__(self,
                 cell_size: int,
                 levels_config: dict[str, dict],
                 seed: int
                 ) -> None:
        self.levels_config: dict[str, dict] = levels_config
        self.grids: dict[str, list[list[int]]] = {}
        self.seed = seed
        self.cell_size: int = cell_size
        self.wall_color: tuple[int, int, int] = (0, 0, 255)
        self.bg_color:   tuple[int, int, int] = (0, 0, 0)

    def _get_maze_dim_level(self, level: int | str = 0) -> tuple[int, int]:
        """"""
        if not isinstance(level, int | str) or not level.isdigit():
            raise PacmanErrors(
                'prog',
                'Level must be an int or str.',
                'maze_surface.py'
                )
        if isinstance(level, int):
            level = str(level)
        if not self.levels_config.get(level):
            raise PacmanErrors(
                'prog',
                'Level out of range.',
                'maze_surface.py'
                )
        dimension_data = self.levels_config[level]
        return tuple(x for x in dimension_data.values())

    def generate_mazes(self) -> None:

        for lvl in self.levels_config:
            dim = self._get_maze_dim_level(lvl)
            maze = mazegenerator.MazeGenerator(
                    size=dim,
                    seed=self.seed
                )
            self.grids[lvl] = maze._maze

    def _get_rows(self, level: int | str) -> int:
        """"""
        if isinstance(level, int):
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
        if isinstance(level, int):
            print('level changed')
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

    def generate_surface(self, level: int | str) -> pygame.Surface:
        """Main pygame loop."""
        if isinstance(level, int):
            level = str(level)
        width = self._get_cols(level) * self.cell_size + 10
        height = self._get_rows(level) * self.cell_size + 10
        screen = pygame.Surface((width, height))

        screen.fill(self.bg_color)
        for row, line in enumerate(self.grids[level]):
            for col, value in enumerate(line):
                self._draw_cell(screen, row, col, value)
        self.screen = screen
        return screen

    def make_display_dim(self, margin: int = 20) -> tuple[int, int]:

        if not hasattr(self, 'screen'):
            raise PacmanErrors('Prog',
                               "Generate a surface first !",
                               "maze_surface.py")

        MARGIN = margin
        win_w = self.screen.get_width() + MARGIN * 2
        win_h = self.screen.get_height() + MARGIN * 2
        return (win_w, win_h)


if __name__ == "__main__":
    try:
        from utils.parse_config import parse_config
        config = parse_config()
        cell_size = config.cell_size
        maze = MazeManager(cell_size, config.levels, config.seed)
        maze.generate_mazes()
        pygame.init()
        curent_level = 0
        maze_surface = maze.generate_surface(0)
        display = pygame.display.set_mode(maze.make_display_dim())
        clock = pygame.time.Clock()
        running = True

        while running:

            pygame.display.set_caption(f"Maze — niveau {curent_level}")

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONUP:
                    curent_level = 0
                    while not (
                            isinstance(curent_level, str)
                            and curent_level.isdigit()):

                        curent_level = input(
                            'Which level do you want to print ?')

                        if not curent_level.isdigit():
                            print("\033[1;35mPlease\033[0m choose a digit")
                        if not maze.grids.get(curent_level):
                            print("\033[1;35mOut of range :\033[0m",
                                  '; '.join(
                                      [str(x) for x in range(len(maze.grids))]
                                      ))
                            curent_level = 0
                        if (isinstance(curent_level, str)
                           and curent_level.isdigit()):
                            maze_surface = maze.generate_surface(curent_level)
                            display = pygame.display.set_mode(
                                maze.make_display_dim())

            display.fill((0, 0, 0))
            display.blit(maze_surface, (20, 20))
            pygame.display.flip()
            clock.tick(60)

    except Exception as e:
        print(e)
