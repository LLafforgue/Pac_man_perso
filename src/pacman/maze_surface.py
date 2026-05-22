import pygame
from enum import IntFlag
from utils import PacmanErrors
from mazegenerator import mazegenerator


class Wall(IntFlag):
    """Bitmask representing the walls of a single maze cell."""
    NORD = 1 << 0
    EST = 1 << 1
    SUD = 1 << 2
    OUEST = 1 << 3


class MazeManager:
    """
    Handles the generation and rendering of one or more mazes using pygame.
    """

    def __init__(self,
                 cell_size: int,
                 levels_config: dict[str, dict],
                 seed: int
                 ) -> None:
        """Initialize MazeManager instance."""
        self.levels_config: dict[str, dict] = levels_config
        self.grids: dict[str, list[list[int]]] = {}
        self.seed = seed
        self.cell_size: int = cell_size
        self.wall_color: tuple[int, int, int] = (0, 0, 255)
        self.bg_color:   tuple[int, int, int] = (0, 0, 0)

    def _get_maze_dim_level(self, level: int | str = 0) -> tuple[int, int]:
        """Return the dimensions ``(width, height)`` of the requested level.

        Args:
            level (int | str): Level index, as an integer or numeric string.
                Defaults to ``0``.

        Returns:
            tuple[int, int]: Dimensions ``(width, height)`` extracted
                from ``levels_config``.

        Raises:
            PacmanErrors: If ``level`` is not an integer or numeric string,
                or if the level is absent from the configuration.
        """
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
        """Generate mazes for every level defined in ``levels_config``.

        Each grid is a 2D list of integers, where every integer is a
        ``Wall`` bitmask describing the walls of that cell.

        Returns:
            None
        """
        for lvl in self.levels_config:
            dim = self._get_maze_dim_level(lvl)
            maze = mazegenerator.MazeGenerator(
                    size=dim,
                    seed=self.seed
                )
            self.grids[lvl] = maze._maze

    def _get_rows(self, level: int | str) -> int:
        """Return the number of cols (height) for the given level.

        Args:
            level (int | str): Level index, as an integer or numeric string.

        Returns:
            int: Maze height expressed as a number of cells.

        Raises:
            PacmanErrors: If the level is absent from ``levels_config``.
        """
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
        """
        Return the number of columns (width) for the given level.

        Args:
            level (int | str): Level index, as an integer or numeric string.

        Returns:
            int: Maze width expressed as a number of cells.

        Raises:
            PacmanErrors: If the level is absent from ``levels_config``
        """
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
        """
        Draw the walls of a single cell onto the given surface.

        Args:
            surface (pygame.Surface): Target pygame surface to draw on.
            row (int): Row index of the cell within the grid.
            col (int): Column index of the cell within the grid.
            value (int): ``Wall`` bitmask describing which walls to draw.

        Returns:
            None
        """
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
        """
        Generate and return a ``pygame.Surface`` containing the rendered maze.

        Args:
            level (int | str): Index of the level to render.

        Returns:
            pygame.Surface: A surface ready to be blitted onto the display.
        """
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
        """
        Return the pygame window dimensions to fit the maze surface.

        Args:
        margin (int): Padding in pixels applied uniformly on all four
            sides of the window. Defaults to ``20``.

        Returns:
                tuple[width, height]: The new display window and the value
        """
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
