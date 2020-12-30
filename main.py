import sys
import time


def hanoi(discs):
    def _hanoi(disc, from_, to, via):
        if disc <= 1:
            yield disc, from_, to
        else:
            yield from _hanoi(disc - 1, from_,via, to)
            yield disc, from_, to
            yield from _hanoi(disc - 1, via, to, from_)

    return _hanoi(discs, 1, 3, 2)


if __name__ == '__main__':
    discs = int(sys.argv[1])
    with open(f'hanoi-outputs/{discs}-discs.txt', 'w') as f:
        start = time.time()
        for i, (disc, from_, to) in enumerate(hanoi(discs), 1):
            f.write(f'{i:03} Move disc {disc:2} from {from_} to {to}.\n')
        end = time.time()
    print(f'Problem took {end - start:.2f} seconds to solve for {discs} discs.')
