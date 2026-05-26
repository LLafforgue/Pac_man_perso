import pygame
from utils import PacManConfig, Wall, PacmanErrors, Sprite, Assets
import os.path as pth


class Player():
    """"""

    def __init__(
            self,
            config: PacManConfig,
            mazes: dict[str, list]) -> None:
        """"""
        self.__coord: tuple[int, int] = (0, 0)
        self.__mazes: dict[str, list] = mazes
        self.__lives: int = config.lives
        self.__step: int = config.cell_size
        self.SPEED: int = Sprite.SPEED
        self.orientation: str = 'south'
        self.__sprites: dict[str, str] = {'north': Assets.PACMAN_UP,
                                          'south': Assets.PACMAN_DOWN,
                                          'east': Assets.PACMAN_RIGHT,
                                          'west': Assets.PACMAN_LEFT}

    def generate_surfaces(self, nbr_frame: int
                          ) -> dict[str, list[pygame.Surface]]:
        """"""
        for key, path in self.__sprites.items():
            if not pth.isfile(path):
                raise PacmanErrors('Asset',
                                   f"No {path} available !",
                                   'player.py')
            image = pygame.image.load(path)

            frame_w = Sprite.PIXEL_DIM
            frame_h = Sprite.PIXEL_DIM

            def get_frame(img: pygame.Surface, index: int) -> pygame.Surface:
                """Extract a single frame from the sprite sheet."""
                rect = pygame.Rect(index * frame_w, 0, frame_w, frame_h)
                frame = pygame.Surface((frame_w, frame_h), pygame.SRCALPHA)
                frame.blit(img, (0, 0), rect)
                return pygame.transform.scale(
                    frame, (self.__step, self.__step))

            self.__sprites[key] = [get_frame(image, i)
                                   for i in range(nbr_frame)]
        return self.__sprites

    def move(self, level: str | int, key: int) -> None:
        """"""
        if isinstance(level, int):
            level = str(level)

        if key == pygame.K_UP and not self._chek_walls(level, "north"):
            self.__coord = (
                self.__coord[0] - 1,
                self.__coord[1]
                )
            self.orientation = 'north'

        if key == pygame.K_DOWN and not self._chek_walls(level, "south"):
            self.__coord = (
                self.__coord[0] + 1,
                self.__coord[1])
            self.orientation = 'south'

        if key == pygame.K_LEFT and not self._chek_walls(level, "west"):
            self.__coord = (
                self.__coord[0],
                self.__coord[1] - 1)
            self.orientation = 'west'

        if key == pygame.K_RIGHT and not self._chek_walls(level, "east"):
            self.__coord = (
                self.__coord[0],
                self.__coord[1] + 1)
            self.orientation = 'east'

    def _chek_walls(
            self,
            level: str,
            orientation: str,
            mode: str = "std"
            ) -> bool:
        """"""
        if level not in self.__mazes:
            raise PacmanErrors(
                'prog',
                f'{level} not a valid key',
                'player.py'
                )
        maze = self.__mazes[level]
        ln, col = self.__coord
        cell_value = maze[ln][col]
        if mode == "std":
            if orientation == "north" and cell_value & Wall.NORD:
                return True
            if orientation == "south" and cell_value & Wall.SUD:
                return True
            if orientation == "east" and cell_value & Wall.EST:
                return True
            if orientation == "west" and cell_value & Wall.OUEST:
                return True
        return False

    def _collision(self, entities: list[tuple[int, int]], mode: str = "std"):
        """"""

    def _set_lives(self) -> bool:
        """"""

    def get_lives(self) -> int:
        """"""
        return self.__lives

    def go_to(self):
        """"""

    def reset(self, level: str | int) -> None:
        """"""
        if isinstance(level, int):
            level = str(level)

        ln = len(self.__mazes[level]) // 2
        col = len(self.__mazes[level][0]) // 2

        while self.__mazes[level][ln][col] == 15:
            if self.__mazes[level][ln][col - 2] == 15:
                col -= 1
            else:
                col += 1
        self.__coord = (ln, col)

    def coord_to_position(self) -> tuple[int, int]:
        """"""
        h, w = tuple(x * self.__step + 20 for x in self.__coord)
        return (w, h)

    def get_surface(self) -> list[pygame.Surface]:
        """"""
        return self.__sprites[self.orientation]
