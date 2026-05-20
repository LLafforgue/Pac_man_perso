import json
import sys
from os import path as pth
from pacman_errors import PacmanErrors
from pydantic import BaseModel, Field, model_validator
from typing_extensions import Self
from typing import Annotated


class Configuration(BaseModel):
    """Configure the pac_man game"""

    highscores_filename: str = Field(pattern=r"^.+\.json$")
    levels: list[
        dict[
            Annotated[str, Field(pattern=r"^\d+$")],
            dict[
                str,
                Annotated[int, Field(ge=3, le=100)]
                ]
                ]
            ]
    level_max_time: int = Field(ge=5, le=3600)
    lives: int = Field(ge=1, le=5)
    nbr_pacgum: int = Field(default=42, ge=4)
    points_per_ghost: int = Field(ge=50)
    points_per_pacgum: int = Field(ge=5)
    points_per_superpacgum: int = Field(ge=10)
    seed: int = Field(default=42)

    @model_validator(mode='after')
    def multi_validator(self) -> Self:

        if not pth.isfile(self.highscores_filename):
            raise PacmanErrors('Config',
                               f"No {self.highscores_filename} available !")
        if pth.getsize(self.highscores_filename) == 0:
            raise PacmanErrors('Config',
                               f'{self.highscores_filename} is empty.')

        def check_keys(level: dict) -> bool:
            """"""
            return [*level.values()][0].keys() == {"width", "height"}

        for level in self.levels:
            if not check_keys(level):
                raise PacmanErrors('config',
                                   ("Missing 'width' or 'height' "
                                    + "or unexpected key found"
                                    + f"in level {[*level.keys()][0]}"))

        def min_dimention(levels: list) -> int:
            mult: list = []
            for level in levels:
                dim = [*level.values()][0]
                mult.append(dim['width'] * dim['height'])
            return min(mult)

        min_dimensions = min_dimention(self.levels)
        if min_dimensions - 5 < self.nbr_pacgum:
            raise PacmanErrors('config',
                               f'Too many gums (max {min_dimensions})')

        if not (self.points_per_ghost >
                self.points_per_superpacgum >
                self.points_per_pacgum):
            raise PacmanErrors('config', ("Points order not respected:"
                                          + " ghost > superpacgum > pacgum"))

        return self


def parse_config() -> Configuration:
    """Parse and validate the Pac-Man config file passed as argument."""
    arg = sys.argv[1:]
    datas: dict = {}
    if len(arg) == 0:
        raise PacmanErrors(
            'arg',
            'Missing a config.json file in arguments !',
            'parse_config.py'
        )
    if len(arg) > 1:
        raise PacmanErrors(
            'arg',
            'Too many arguments !',
            'parse_config.py')
    if not pth.isfile(arg[0]):
        raise PacmanErrors(
            'arg', f'{arg[0]} not found !'
        )

    with open(arg[0], 'r') as f:
        datas = json.load(f)

    return Configuration(**datas)


if __name__ == "__main__":

    try:
        test = parse_config()
        print(test.levels)
    except (Exception, PacmanErrors) as e:
        print(e)
