"""
Simulating path finding algorithms
"""

COL_UNVISITED = (255, 255, 255)
COL_PVISITED = (146, 146, 183)
COL_VISITED = (30, 30, 153)

import sys
from random import randint
from collections import deque
from typing import Deque, Tuple, List

import numpy as np
import imageio

from maze import Maze, Direction


def breadth_first_search(m: Maze, start: int) -> List[np.ndarray]:

    visited = np.zeros((m.rows, m.cols), dtype=np.bool)
    q: Deque[Tuple[int, int]] = deque()

    q.append((0, start))
    visited[0, start] = True

    ims: List[np.array] = []
    im = np.ones((m.rows, m.cols, 3), dtype=np.uint8)
    im[:, :, :] = COL_UNVISITED

    while q:
        ims.append(im.copy())
        ur, uc = q.popleft()
        for dir in Direction:
            if m.is_open(ur, uc, dir):
                vr, vc = m.new_point(ur, uc, dir)
                if m.is_valid_point(vr, vc) and not visited[vr, vc]:
                    visited[vr, vc] = True
                    q.append((vr, vc))
                    im[vr, vc] = COL_PVISITED
        im[ur, uc] = COL_VISITED

    return ims


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

    imageio.mimwrite("media/maze_path.gif", map(m.to_imagearray, ims), fps=10)
