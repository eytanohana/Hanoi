import pygame
import time
import sys

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


def init_pegs():
    pegs = []
    for i in range(1, 4):
        pegs.append(pygame.Rect(i * WIDTH // 4, PEG_HEIGHT, 5, board.top - PEG_HEIGHT))
        pygame.draw.rect(screen, Color.BLACK, pegs[-1])
    return pegs


def init_discs(n_discs, pegs):
    discs = []
    for i in range(n_discs, 0, -1):
        disc = pygame.Rect(0, 0, 0, 0)
        discs.append(disc)
        disc.width = 120 if i == n_discs else discs[-2].width * 0.9
        disc.height = 10
        disc.centerx = pegs[0].centerx
        disc.bottom = board.top if i == n_discs else discs[-2].top
        print(disc.bottom)
        pygame.draw.rect(screen, Color.DISC_COLORS[i % len(Color.DISC_COLORS)], disc)
        pygame.display.flip()
    return discs


def start_round(n_discs):
    pegs = init_pegs()
    discs = init_discs(n_discs, pegs)
    pygame.display.flip()
    return pegs, discs


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
    board = pygame.Rect(*BOARD_DIMS)
    running = True
    while running:
        print('running')
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(Color.WHITE)
        pygame.draw.rect(screen, Color.BLACK, board)
        start_round(n_discs)
        time.sleep(2)
