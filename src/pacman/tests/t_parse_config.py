import pytest
from unittest.mock import patch, mock_open
from pydantic import ValidationError
from utils import parse_config, PacManConfig


# --- Fixtures ---

VALID_CONFIG = {
    "highscores_filename": "scores.json",
    "levels": [{"1": {"width": 10, "height": 10}}],
    "level_max_time": 60,
    "lives": 3,
    "nbr_pacgum": 42,
    "points_per_ghost": 300,
    "points_per_superpacgum": 100,
    "points_per_pacgum": 10,
    "seed": 42,
}


def make_config(**overrides) -> dict:
    return {**VALID_CONFIG, **overrides}


# --- Configuration (Pydantic model) ---

class TestConfiguration:

    @patch("parse_config.pth.getsize", return_value=100)
    @patch("parse_config.pth.isfile", return_value=True)
    def test_valid_config(self, mock_isfile, mock_getsize):
        config = PacManConfig(**VALID_CONFIG)
        assert config.lives == 3

    @patch("parse_config.pth.getsize", return_value=100)
    @patch("parse_config.pth.isfile", return_value=True)
    def test_invalid_highscores_filename(self, mock_isfile, mock_getsize):
        with pytest.raises(ValidationError):
            PacManConfig(**make_config(highscores_filename="scores.txt"))

    @patch("parse_config.pth.getsize", return_value=100)
    @patch("parse_config.pth.isfile", return_value=True)
    def test_lives_out_of_range(self, mock_isfile, mock_getsize):
        with pytest.raises(ValidationError):
            PacManConfig(**make_config(lives=0))
        with pytest.raises(ValidationError):
            PacManConfig(**make_config(lives=6))

    @patch("parse_config.pth.getsize", return_value=100)
    @patch("parse_config.pth.isfile", return_value=True)
    def test_points_order_not_respected(self, mock_isfile, mock_getsize):
        with pytest.raises(Exception, match="Points order not respected"):
            PacManConfig(**make_config(
                points_per_ghost=10,
                points_per_superpacgum=100,
                points_per_pacgum=5
            ))

    @patch("parse_config.pth.getsize", return_value=100)
    @patch("parse_config.pth.isfile", return_value=True)
    def test_too_many_pacgums(self, mock_isfile, mock_getsize):
        # 10x10 = 100 cases, max pacgum = 95, on en met 96
        with pytest.raises(Exception, match="Too many gums"):
            PacManConfig(**make_config(nbr_pacgum=96))

    @patch("parse_config.pth.getsize", return_value=0)
    @patch("parse_config.pth.isfile", return_value=True)
    def test_empty_highscores_file(self, mock_isfile, mock_getsize):
        with pytest.raises(Exception, match="is empty"):
            PacManConfig(**VALID_CONFIG)

    @patch("parse_config.pth.getsize", return_value=100)
    @patch("parse_config.pth.isfile", return_value=False)
    def test_highscores_file_not_found(self, mock_isfile, mock_getsize):
        with pytest.raises(Exception, match="No .* available"):
            PacManConfig(**VALID_CONFIG)


# --- parse_config() ---

class TestParseConfig:

    def test_missing_argument(self):
        with patch("sys.argv", ["prog"]):
            with pytest.raises(Exception, match="Missing"):
                parse_config()

    def test_too_many_arguments(self):
        with patch("sys.argv", ["prog", "a.json", "b.json"]):
            with pytest.raises(Exception, match="Too many"):
                parse_config()

    def test_file_not_found(self):
        with patch("sys.argv", ["prog", "missing.json"]):
            with patch("parse_config.pth.isfile", return_value=False):
                with pytest.raises(Exception, match="not found"):
                    parse_config()

    @patch("parse_config.pth.getsize", return_value=100)
    @patch("parse_config.pth.isfile", return_value=True)
    def test_valid_parse(self, mock_isfile, mock_getsize):
        import json
        with patch("sys.argv", ["prog", "scores.json"]):
            with patch("builtins.open", mock_open(
                read_data=json.dumps(VALID_CONFIG)
            )):
                config = parse_config()
                assert isinstance(config, PacManConfig)
                assert config.lives == 3
