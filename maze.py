"""
Implements a simple Maze generator

TODO: remove recursion from maze generator
"""

from random import sample, choice
from enum import Enum
from typing import Tuple
import sys
import numpy as np


class Direction(Enum):
    """"Enum for directions in the maze"""

    UP, DOWN, LEFT, RIGHT = range(4)


class Maze:
    """Randomized maze generator class"""

    def __init__(self, rows: int, cols: int) -> None:
        """ Generates a maze randomly using a depth first search

        The algorithm moves through the array using a depth first search,
        where the direction is randomly chosen. It visits each point in the
        array exactly once.

        """
        self.rows, self.cols = rows, cols
        self.horizontal_walls = np.ones((rows + 1, cols), dtype=np.bool)
        self.vertical_walls = np.ones((rows, cols + 1), dtype=np.bool)

        sc = choice(range(self.cols))
        ec = choice(range(self.cols))

        self.horizontal_walls[0, sc] = 0
        self.horizontal_walls[self.rows, ec] = 0

        visited = np.zeros((rows, cols), dtype=np.bool)

        dirs = tuple(dir for dir in Direction)

        def visit(r: int, c: int) -> None:
            visited[r, c] = True

            for dir in sample(dirs, 4):
                if dir is Direction.UP:
                    nr, nc = r - 1, c
                if dir is Direction.DOWN:
                    nr, nc = r + 1, c
                if dir is Direction.LEFT:
                    nr, nc = r, c - 1
                if dir is Direction.RIGHT:
                    nr, nc = r, c + 1

                if 0 <= nr < self.rows and 0 <= nc < self.cols and not visited[nr, nc]:
                    self.make_open(r, c, dir)
                    visit(nr, nc)

        visit(0, sc)

    def is_open(self, r: int, c: int, dir: Direction) -> bool:
        """Returns true if the point (r, c) has a free path in the direction
        of dir
        """

        if dir is Direction.UP:
            return not self.horizontal_walls[r, c]
        if dir is Direction.DOWN:
            return not self.horizontal_walls[r + 1, c]
        if dir is Direction.LEFT:
            return not self.vertical_walls[r, c]
        if dir is Direction.RIGHT:
            return not self.vertical_walls[r, c + 1]
        return False

    def make_open(self, r: int, c: int, dir: Direction) -> None:
        """Removes a wall at the specified point"""

        if dir is Direction.UP:
            self.horizontal_walls[r, c] = 0
        if dir is Direction.DOWN:
            self.horizontal_walls[r + 1, c] = 0
        if dir is Direction.LEFT:
            self.vertical_walls[r, c] = 0
        if dir is Direction.RIGHT:
            self.vertical_walls[r, c + 1] = 0

    def __repr__(self) -> str:
        return f"<Maze object of size {(self.rows, self.cols)}>"

    def __str__(self) -> str:
        """Returns a string of the maze"""
        out = ""
        for r in range(self.rows + 1):
            # Print horizontal walls
            for c in range(self.cols):
                out += "+"
                if self.horizontal_walls[r, c]:
                    out += "--"
                else:
                    out += "  "
            out += "+"
            out += "\n"
            if r == self.rows:
                break
            # Print vertical walls
            for c in range(self.cols + 1):
                if self.vertical_walls[r, c]:
                    out += "|"
                else:
                    out += " "
                if c == self.cols:
                    break
                out += "  "
            out += "\n"

        return out


if __name__ == "__main__":

    if len(sys.argv) == 2:
        rows, cols = int(sys.argv[1]), int(sys.argv[1])
    elif len(sys.argv) == 3:
        rows, cols = int(sys.argv[1]), int(sys.argv[2])
    else:
        rows, cols = 20, 20

    m = Maze(rows, cols)

    print(m)
