import json
from os import path as pth
from pacman_errors import PacmanErrors
from pydantic import BaseModel, Field, model_validator
from typing_extensions import Self
from typing import Annotated, Literal


class Configuration(BaseModel):
    """Configure the pac_man game"""

    highscores_file: str = Field(pattern=r"^.+\.json$")
    levels: list[
        dict[
            Annotated[str, Field(pattern=r"^\d+$")],
            dict[
                Literal["width", "height"],
                Annotated[int, Field(ge=3, le=100)]
                ]
                ]
            ]
    level_max_time: int = Field(ge=5, le=3600)
    lives: int = Field(default=42, ge=1, le=5)
    nbr_pacgum: int = Field(ge=4)
    pts_ghost: int = Field(ge=50)
    pts_pacgum: int = Field(ge=5)
    pts_superpacgum: int = Field(ge=10)
    seed: int = Field(default=42)

    @model_validator(mode='after')
    def multi_validator(self) -> Self:

        if not pth.isfile(self.highscores_file):
            raise PacmanErrors('Config',
                               f"No {self.highscores_file} available !")
        if pth.getsize(self.highscores_file) == 0:
            raise PacmanErrors('Config',
                               f'{self.highscores_file} is empty.')
  
        if not self.pts_ghost > self.pts_superpacgum > self.pts_pacgum:
            raise PacmanErrors('config', ("Points order not respected:"
                                          + " ghost > superpacgum > pacgum"))
        return self


# Model validator pour vérifier que width et height sont présents.

if __name__ == "__main__":

    try:
        test = Configuration(
            highscores_file="highscore.json",
            levels=[
                {"0": {"width": 15, "height": 15}},
                {"1": {"width": 20, "height": 15}}
            ],
            lives=3,
            level_max_time=25,
            nbr_pacgum=10,
            pts_ghost=200,
            pts_pacgum=20,
            pts_superpacgum=10
        )
        print(test.levels)
    except (Exception, PacmanErrors) as e:
        print(e)
