from utils import PacManConfig, PacmanErrors, parse_config
from mazegenerator import mazegenerator

if __name__ == "__main__":
    try:
        config = parse_config()
        for level in config.levels:
            lvl = int([*level.keys()][0])
            dim = config._get_maze_dim_level(lvl)
            print(dim)
            maze = mazegenerator.MazeGenerator(
                size=dim,
                seed=config.seed
            )
            # maze._generate_maze()
            print(maze._maze)
            next = input('Next level ? (y/n)')
            if next.lower() == 'n':
                exit()
    except (Exception) as e:
        print(e)
