from collections import defaultdict
from main import hanoi
import time
import sys
import pygame


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

    DISC_COLORS = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE,
                   GREY, BURNT_ORANGE, LIGHT_BLUE, LIGHT_PURPLE]

def init_board():
    board = pygame.Rect(*BOARD_DIMS)
    return board

def init_pegs():
    pegs = []
    for i in range(1, 4):
        pegs.append(pygame.Rect(i * WIDTH // 4, PEG_HEIGHT, 5, board.top - PEG_HEIGHT))
    return pegs


def init_discs(n_discs):
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
    for y in range(disc.centery, HEIGHT//3, -1):
        disc.centery = y
        refresh()
    to_x = pegs[to_peg-1].centerx
    step = 1 if to_x > disc.centerx else -1
    for x in range(disc.centerx, pegs[to_peg-1].centerx+step, step):
        disc.centerx = x
        refresh()

    try:
        top_disk = peg_stacks[to_peg][-1]
        to_y = top_disk.top
    except IndexError:
        to_y = board.top
    for y in range(disc.bottom, to_y+1):
        disc.bottom = y
        refresh()

    peg_stacks[to_peg].append(disc)


if __name__ == '__main__':
    try:
        n_discs = int(sys.argv[1])
        if n_discs < 1:
            n_discs = 3
        if n_discs > 15:
            n_discs = 15
    except IndexError:
        n_discs = 3

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    board = init_board()
    pegs = init_pegs()
    discs = init_discs(n_discs)

    peg_stacks = defaultdict(list)
    peg_stacks[1].extend(discs)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        refresh()
        time.sleep(2)
        for i, (disc, from_, to) in enumerate(hanoi(n_discs), 1):
            print(f'{i:03} Move disc {disc:2} from {from_} to {to}.')
            move_disc(from_, to)

        print(f'{n_discs} discs solved in {i} moves.')
        running = False
        time.sleep(5)
