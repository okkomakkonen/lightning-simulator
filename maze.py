"""
Implements a simple Maze generator

"""

import sys
from random import sample, randint
from enum import Enum
from typing import Tuple, Optional, Deque, Iterator
from collections import deque

import numpy as np
import imageio


class Direction(Enum):
    """"Enum for directions in the maze"""

    UP, DOWN, LEFT, RIGHT = range(4)


class Maze:
    """Randomized maze generator class"""

    def __init__(self, rows: int, cols: int, start_col: Optional[int] = None) -> None:
        """ Generates a maze randomly using a depth first search

        The algorithm moves through the array using a depth first search,
        where the direction is randomly chosen. It visits each point in the
        array exactly once.

        """
        self.rows, self.cols = rows, cols
        self.horizontal_walls = np.ones((rows + 1, cols), dtype=np.bool)
        self.vertical_walls = np.ones((rows, cols + 1), dtype=np.bool)

        if start_col is None:
            start_col = randint(0, cols - 1)
        else:
            end_col = randint(0, cols - 1)
            self.horizontal_walls[0, start_col] = False
            self.horizontal_walls[self.rows, end_col] = False

        visited = np.zeros((rows, cols), dtype=np.bool)

        dirs = tuple(dir for dir in Direction)

        class Frame:
            def __init__(self, r: int, c: int) -> None:
                self.r, self.c = r, c
                self.dirs: Optional[Iterator[Direction]] = None

            def __repr__(self) -> str:
                return f"<Frame {(self.r, self.c)}>"

        stack: Deque[Frame] = deque()
        stack.append(Frame(0, start_col))

        # Implements the call stack in the heap

        while stack:
            frame = stack[-1]
            visited[frame.r, frame.c] = True
            if frame.dirs is None:
                frame.dirs = iter(sample(dirs, 4))

            try:
                dir = next(frame.dirs)
                nr, nc = self.new_point(frame.r, frame.c, dir)

                if self.is_valid_point(nr, nc) and not visited[nr, nc]:
                    self.make_open(frame.r, frame.c, dir)
                    stack.append(Frame(nr, nc))

            except StopIteration:
                stack.pop()

    def new_point(self, r: int, c: int, dir: Direction) -> Tuple[int, int]:
        """Returns a new point in the specified direction"""
        if dir == Direction.UP:
            return r - 1, c
        if dir == Direction.DOWN:
            return r + 1, c
        if dir == Direction.LEFT:
            return r, c - 1
        if dir == Direction.RIGHT:
            return r, c + 1
        raise ValueError("dir has to be a valid direction")

    def is_valid_point(self, r: int, c: int) -> bool:
        return 0 <= r < self.rows and 0 <= c < self.cols

    def is_open(self, r: int, c: int, dir: Direction) -> bool:
        """Returns true if the point (r, c) has a free path in the direction
        of dir
        """

        if dir == Direction.UP:
            return not self.horizontal_walls[r, c]
        if dir == Direction.DOWN:
            return not self.horizontal_walls[r + 1, c]
        if dir == Direction.LEFT:
            return not self.vertical_walls[r, c]
        if dir == Direction.RIGHT:
            return not self.vertical_walls[r, c + 1]
        return False

    def make_open(self, r: int, c: int, dir: Direction) -> None:
        """Removes a wall at the specified point"""

        if dir == Direction.UP and r != 0:
            self.horizontal_walls[r, c] = False
        if dir == Direction.DOWN and r != self.rows - 1:
            self.horizontal_walls[r + 1, c] = False
        if dir == Direction.LEFT and c != 0:
            self.vertical_walls[r, c] = False
        if dir == Direction.RIGHT and c != self.cols - 1:
            self.vertical_walls[r, c + 1] = False

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

    def to_imagearray(
        self,
        cols: Optional[np.array] = None,
        line_width: int = 1,
        box_width: int = 3,
        col_line: Tuple[int, int, int] = (0, 0, 0),
        col_box: Tuple[int, int, int] = (255, 255, 255),
    ) -> np.array:
        """Returns an image of the maze"""
        # TODO: implement the colors for the boxes

        out = np.zeros(
            (
                (line_width + box_width) * self.rows + line_width,
                (line_width + box_width) * self.cols + line_width,
                3,
            ),
            dtype=np.uint8,
        )
        x = 0
        for r in range(self.rows + 1):
            # Print horizontal walls
            for _ in range(line_width):
                y = 0
                for c in range(self.cols):
                    out[x, y : y + line_width] = col_line
                    y += line_width
                    if self.horizontal_walls[r, c]:
                        out[x, y : y + box_width] = col_line
                    else:
                        # 0 <= r <= self.rows and 0 <= c < self.cols
                        if cols is None:
                            out[x, y : y + box_width] = col_box
                        else:
                            if r != self.rows:
                                out[x, y : y + box_width] = cols[r, c]
                            else:
                                out[x, y : y + box_width] = cols[r - 1, c]
                    y += box_width
                out[x, y : y + line_width] = col_line
                y += line_width
                x += 1

            if r == self.rows:
                break
            # Print vertical walls
            for _ in range(box_width):
                y = 0
                for c in range(self.cols + 1):
                    if self.vertical_walls[r, c]:
                        out[x, y : y + line_width] = col_line
                    else:
                        # 0 <= r < self.rows and 0 <= c <= self.cols
                        if cols is None:
                            out[x, y : y + line_width] = col_box
                        else:
                            if c != self.rows:
                                out[x, y : y + line_width] = cols[r, c]
                            else:
                                out[x, y : y + line_width] = cols[r, c - 1]
                    y += line_width
                    if c == self.cols:
                        break
                    # Color in the box
                    out[x, y : y + box_width] = (
                        cols[r, c] if cols is not None else col_box
                    )
                    y += box_width
                x += 1

        return out


if __name__ == "__main__":

    """Generates a maze, prints it and saves to an image."""

    import random

    random.seed(0)

    if len(sys.argv) == 2:
        rows, cols = int(sys.argv[1]), int(sys.argv[1])
    elif len(sys.argv) == 3:
        rows, cols = int(sys.argv[1]), int(sys.argv[2])
    else:
        rows, cols = 50, 50

    start = randint(0, cols - 1)

    m = Maze(rows, cols, start)

    if cols <= 50:
        print(m)

    imageio.imwrite("media/maze.png", m.to_imagearray())
