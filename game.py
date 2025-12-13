from __future__ import annotations
import sys
from collections import defaultdict

import pygame

from hanoi import hanoi

WIDTH = 600
HEIGHT = 400

BOARD_POS_LEFT = int(0.1 * WIDTH)
BOARD_POS_TOP = int(0.9 * HEIGHT)
BOARD_WIDTH = WIDTH - 2 * BOARD_POS_LEFT
BOARD_HEIGHT = int(0.02 * HEIGHT)
BOARD_DIMS = BOARD_POS_LEFT, BOARD_POS_TOP, BOARD_WIDTH, BOARD_HEIGHT

PEG_HEIGHT = HEIGHT // 2


class Color:
    BLACK = (0,) * 3
    WHITE = (255,) * 3
    GREY = (143, 143, 143)
    RED = (168, 50, 50)
    ORANGE = (207, 138, 21)
    BURNT_ORANGE = (255, 132, 0)
    YELLOW = (201, 193, 26)
    GREEN = (70, 189, 19)
    BLUE = (19, 150, 194)
    LIGHT_BLUE = (42, 191, 250)
    PURPLE = (153, 13, 191)
    LIGHT_PURPLE = (207, 99, 190)

    DISC_COLORS = [
        RED,
        ORANGE,
        YELLOW,
        GREEN,
        BLUE,
        PURPLE,
        GREY,
        BURNT_ORANGE,
        LIGHT_BLUE,
        LIGHT_PURPLE,
    ]


def init_pegs() -> list[pygame.Rect]:
    return [pygame.Rect(peg_num * WIDTH // 4, PEG_HEIGHT, 5, board.top - PEG_HEIGHT) for peg_num in range(1, 4)]


def init_discs(n_discs) -> list[pygame.Rect]:
    discs = []
    for i in range(n_discs, 0, -1):
        disc = pygame.Rect(0, 0, 0, 0)
        discs.append(disc)
        disc.width = 120 if i == n_discs else discs[-2].width * 0.9
        disc.height = 10
        disc.centerx = pegs[0].centerx
        disc.bottom = board.top if i == n_discs else discs[-2].top
    return discs


def refresh():
    screen.fill(Color.WHITE)
    pygame.draw.rect(screen, Color.BLACK, board)
    for peg in pegs:
        pygame.draw.rect(screen, Color.BLACK, peg)
    for i, disc in enumerate(discs):
        pygame.draw.rect(screen, Color.DISC_COLORS[i % len(Color.DISC_COLORS)], disc)
    pygame.display.flip()


def move_disc(from_peg, to_peg):
    disc = peg_stacks[from_peg].pop()
    for y in range(disc.centery, HEIGHT // 3, -1):
        disc.centery = y
        refresh()
    to_x = pegs[to_peg - 1].centerx
    step = 1 if to_x > disc.centerx else -1
    for x in range(disc.centerx, pegs[to_peg - 1].centerx + step, step):
        disc.centerx = x
        refresh()

    try:
        top_disk = peg_stacks[to_peg][-1]
        to_y = top_disk.top
    except IndexError:
        to_y = board.top
    for y in range(disc.bottom, to_y + 1):
        disc.bottom = y
        refresh()

    peg_stacks[to_peg].append(disc)


def get_number_of_disks():
    try:
        n_disks = int(sys.argv[1])
        if n_disks < 1:
            n_disks = 3
            print(f"Invalid number of disks. Using {n_disks} disks instead.")
        if n_disks > 15:
            n_disks = 15
            print(f"Invalid number of disks. Using {n_disks} disks instead.")
    except IndexError:
        n_disks = 3
    return n_disks


if __name__ == "__main__":
    n_disks = get_number_of_disks()
    print_spaces = len(str(2**n_disks - 1))
    print_disk_spaces = len(str(n_disks))

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    board = pygame.Rect(*BOARD_DIMS)
    pegs = init_pegs()
    discs = init_discs(n_disks)

    peg_stacks = defaultdict(list)
    peg_stacks[1].extend(discs)

    for i, (disc, from_, to) in enumerate(hanoi(n_disks), 1):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                break

        print(f"{i:{print_spaces}}: Move disc {disc:{print_disk_spaces}} from peg {from_} to {to}.")
        move_disc(from_, to)
    else:
        print(f"\n{n_disks} discs solved in {i} moves.")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
