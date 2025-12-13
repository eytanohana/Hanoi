from __future__ import annotations

from hanoi.solver import hanoi


def test_move_count():
    for n in range(1, 9):
        moves = list(hanoi(n))
        assert len(moves) == 2 ** n - 1


def test_moves_are_legal_and_solve():
    n = 6
    pegs: dict[int, list[int]] = {1: list(range(n, 0, -1)), 2: [], 3: []}

    for disc, from_, to in hanoi(n):
        # disc must be top of from_ peg
        assert pegs[from_], 'moving from empty peg'
        assert pegs[from_][-1] == disc

        pegs[from_].pop()

        # cannot place on smaller disc
        if pegs[to]:
            assert pegs[to][-1] > disc
        pegs[to].append(disc)

    assert pegs[1] == []
    assert pegs[2] == []
    assert pegs[3] == list(range(n, 0, -1))
