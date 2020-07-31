"""
Simulating path finding algorithms
"""

COL_UNVISITED = (255, 255, 255)
COL_PVISITED = (146, 146, 183)
COL_VISITED = (30, 30, 153)

import sys
from random import randint
from collections import deque
from typing import Deque, Tuple, Optional, Iterator, Generator

import numpy as np  # type: ignore
import imageio  # type: ignore

from maze import Maze, Direction


def breadth_first_search(m: Maze, start: int) -> Generator[np.ndarray, None, None]:

    visited = np.zeros((m.rows, m.cols), dtype=np.bool)
    q: Deque[Tuple[int, int]] = deque()

    q.append((0, start))
    visited[0, start] = True

    im = np.ones((m.rows, m.cols, 3), dtype=np.uint8)
    im[:, :, :] = COL_UNVISITED

    while q:
        yield im.copy()
        ur, uc = q.popleft()
        for dir in Direction:
            if m.is_open(ur, uc, dir):
                vr, vc = m.new_point(ur, uc, dir)
                if m.is_valid_point(vr, vc) and not visited[vr, vc]:
                    visited[vr, vc] = True
                    q.append((vr, vc))
                    im[vr, vc] = COL_PVISITED
        im[ur, uc] = COL_VISITED

    yield im.copy()


def depth_first_search(m: Maze, start: int) -> Generator[np.ndarray, None, None]:
    class Frame:
        def __init__(self, r: int, c: int) -> None:
            self.r, self.c = r, c
            self.dirs: Optional[Iterator[Direction]] = None

    visited = np.zeros((m.rows, m.cols), dtype=np.bool)

    stack: Deque[Frame] = deque()
    stack.append(Frame(0, start))

    im = np.ones((m.rows, m.cols, 3), dtype=np.uint8)
    im[:, :, :] = COL_UNVISITED

    while stack:
        yield im.copy()
        frame = stack[-1]
        visited[frame.r, frame.c] = True
        im[frame.r, frame.c] = COL_PVISITED

        if frame.dirs is None:
            frame.dirs = iter(Direction)

        for dir in frame.dirs:
            if m.is_open(frame.r, frame.c, dir):
                nr, nc = m.new_point(frame.r, frame.c, dir)

                if m.is_valid_point(nr, nc) and not visited[nr, nc]:
                    stack.append(Frame(nr, nc))
                    break
        else:
            im[frame.r, frame.c] = COL_VISITED
            stack.pop()

    yield im.copy()


if __name__ == "__main__":

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

    ims = breadth_first_search(m, start)

    imageio.mimwrite(
        "media/maze_path_bfs.gif",
        map(m.to_imagearray, ims),
        fps=30,
        palettesize=4,
        subrectangles=True,
    )
