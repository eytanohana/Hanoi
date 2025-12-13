from __future__ import annotations

import sys
import time
from collections.abc import Iterator

Move = tuple[int, int, int]


def hanoi(discs: int) -> Iterator[Move]:
    if discs < 1:
        return iter(())

    def _hanoi(disc: int, from_: int, to: int, via: int) -> Iterator[Move]:
        if disc == 1:
            yield disc, from_, to
        else:
            yield from _hanoi(disc - 1, from_, via, to)
            yield disc, from_, to
            yield from _hanoi(disc - 1, via, to, from_)

    return _hanoi(discs, 1, 3, 2)


if __name__ == "__main__":
    discs = int(sys.argv[1])
    with open(f"hanoi-outputs/{discs}-discs.txt", "w") as f:
        start = time.time()
        for i, (disc, from_, to) in enumerate(hanoi(discs), 1):
            # print(f'{i:03} Move disc {disc:2} from {from_} to {to}.')
            f.write(f"{i:03} Move disc {disc:2} from {from_} to {to}.\n")
        end = time.time()
    print(f"{discs} discs took {end - start:.2f} seconds to solve.")
