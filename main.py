import sys

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
    for i, (disc, from_, to) in enumerate(hanoi(int(sys.argv[1])), 1):
        print(f'{i:03} Move disc {disc} from {from_} to {to}.')
