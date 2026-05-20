## pygame
- [x] Comprendre la notion de Surface
- [x] Comprendre le double buffer
- [ ] Comment integrer le maze (tableau de int) ?

## Folder Struct:
- [G] Makefile
    [G] Creation de Package pour steam et stich.io
- [ ] .env.example (dev/debug)
- [G] pyproject.toml
- [ ] README.md
- [G] .gitignore

- [G] highscore.json

- [L] config.json
- [ ] pac-man.py (exe)

- [ ] src/pacman/
    - [ ] __init__.py
    - [ ] main.py (boucle d'affichage et gestion des surfaces)
    - [ ] game/ (game state, scoring, cheat, levels, engine ?)
    - [ ] ui/ (`pygame` ui interface -> hud, screens/Main menu, pause menu, game_over, victor, highscores)
        - [G] highscores
        - [L] hud
        - [G] Main menu

    - [L] maze/ (external maze gen adapted)
    - [ ] entities/ (player, ghosts, gum)
        - [G] Entities (`pygame` => logique de creation/gestion de Surfaces ?)
            - [L] Player
            - [G] Ghost (Strategies)
        - [L] Object/Gum

    - [ ] utils/ (constants, errors)
        - [x] parse_config (`argparse` + `pydantic`)
           - inserer `argparse`
        - [x] pacman_errors

    - [ ] assets/ (fonts, sounds, images/sprites)
        - [L] sprites (Pac/Pac_killer; Ghost/G_feared; gum/super_gum)
- [ ] tests/ (config, scoring, player, ghost, maze, level...)
    - [L] parse config
    - [G]
- [ ] docs/ (preuves d'orga)

Libraries :
- `pathlib`
- `json`
- `dataclasses` (Pour classes qui n'ont pas besoin de regles strict)
- `enum`
- `typing`
- `logging` (Pour une meilleure experience et apprendre a log)
- `time` (time limit)
- `random`
- `argparse` (parsing + simple, et apprendre a l'utiliser)

External :
- `pygame` (for ui only ?)
- `pydantic` (config et highscore strict validation)
- `pytest` (Testing)