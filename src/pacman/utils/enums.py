from enum import IntFlag, StrEnum


class Wall(IntFlag):
    """Bitmask representing the walls of a single maze cell."""
    NORD = 1 << 0
    EST = 1 << 1
    SUD = 1 << 2
    OUEST = 1 << 3


class Assets(StrEnum):
    """Bitmask representing the sprites of a single maze cell."""

    PACMAN_UP = 'src/pacman/assets/pacman/pac_man_up-sheet.png'
    PACMAN_DOWN = 'src/pacman/assets/pacman/pac_man_down-sheet.png'
    PACMAN_RIGHT = 'src/pacman/assets/pacman/pac_man_right-sheet.png'
    PACMAN_LEFT = 'src/pacman/assets/pacman/pac_man_left-sheet.png'


class Sprite(IntFlag):
    """Bitmask representing the sprites of a single maze cell."""
    PIXEL_DIM = 48
    SPEED = 500
