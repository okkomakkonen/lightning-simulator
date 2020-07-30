"""
Simulates lightning
"""

from typing import List, Tuple, Optional, Generator
from queue import PriorityQueue
from random import randint

import numpy as np  # type: ignore
import imageio  # type: ignore


def trace_lightning(m: np.ndarray) -> Generator[np.ndarray, None, None]:
    """Return a sequence of images of a lightning

    The algorithm is based on the A* algorithm
    """

    im = np.zeros(m.shape, dtype=np.uint8)
    frame = 0

    visited = np.zeros(m.shape, dtype=np.bool)
    q: PriorityQueue[Tuple[float, float, int, int]] = PriorityQueue()

    start = randint(0, m.shape[1] - 1)
    q.put((0.0, 0.0, 0, start))

    stop = False

    while not stop:
        if frame % 20 == 0:
            yield im.copy()
        frame += 1
        im[im < 1] = 1
        im -= 1

        tq: List[Tuple[float, float, int, int]] = []

        # Loop over the 8 first in the priority queue
        for _ in range(8):
            if len(q.queue) == 0:
                break
            _, d, r, c = q.get()
            visited[r, c] = True
            im[r, c] = 255
            if r == m.shape[0] - 1:
                stop = True

            # Loop over all of the neighbours of the point
            for nr, nc in (
                (r + 1, c),
                (r - 1, c),
                (r, c + 1),
                (r, c - 1),
                (r + 1, c + 1),
                (r + 1, c - 1),
                (r - 1, c + 1),
                (r - 1, c - 1),
            ):
                if (
                    0 <= nr < m.shape[0]
                    and 0 <= nc < m.shape[1]
                    and not visited[nr, nc]
                ):
                    nd = d + m[nr, nc]
                    p = nd + 0.3 * (m.shape[0] - nr - 1)
                    tq.append((p, nd, nr, nc))

        for t in tq:
            q.put(t)


def generate_lightning(
    rows: int, cols: int, num: int = 1
) -> Generator[np.ndarray, None, None]:
    """Generates a gif of lightning"""

    for _ in range(num):
        m = np.random.rand(rows, cols)
        yield from trace_lightning(m)


if __name__ == "__main__":

    import random

    random.seed(2020)

    imageio.mimwrite(
        "media/lightning.gif",
        generate_lightning(500, 500, num=10),
        subrectangles=True,
        fps=30,
    )
