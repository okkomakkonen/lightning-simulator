# Lightning Simulator

This program can be used to visualize all kinds of mazes and path finding algorithms. The `maze.py` file can generate a random maze.

![Maze](media/maze.png)

The `path_finding_simulator.py` file can visualize breadth first search on a maze and output a gif of the process.

![Breadth first search of a maze](media/maze_path_bfs.gif) ![Depth first search of a maze](media/maze_path_dfs.gif)

The file `lightning.py` can be used to simulate a lightning strike.

![Lightning](media/lightning.gif)

## Usage
```bash
$ pipenv install
$ python maze.py
$ python path_finding_simulator.py
```

## TODO

* Lightning simulation using a different kind of maze generator and tracing algorithm
