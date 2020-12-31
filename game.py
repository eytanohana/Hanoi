import pygame
import time
import random

WIDTH = 800
HEIGHT = 500

BOARD_POS_LEFT = int(0.1 * WIDTH)
BOARD_POS_TOP = int(0.9 * HEIGHT)
BOARD_WIDTH = WIDTH - 2 * BOARD_POS_LEFT
BOARD_HEIGHT = int(0.02 * HEIGHT)
BOARD_DIMS = BOARD_POS_LEFT, BOARD_POS_TOP, BOARD_WIDTH, BOARD_HEIGHT


class Color:
    BLACK = (0,) * 3
    WHITE = (255,) * 3
    RED = (168, 50, 50)
    ORANGE = (207, 138, 21)
    YELLOW = (201, 193, 26)
    GREEN = (70, 189, 19)
    BLUE = (19, 150, 194)
    PURPLE = (153, 13, 191)

    COLORS = [BLACK, WHITE, RED, ORANGE, YELLOW,
              GREEN, BLUE, PURPLE]

def display_pegs():
    for peg in pegs:
        pygame.draw.rect(screen, Color.BLACK, peg)

def start_round(n_discs=3):
    disc = pygame.Rect(pegs[0].centerx, board.top - 20, 120, 10)
    disc.centerx = pegs[0].centerx
    disc.bottom = board.top
    discs.append(disc)
    pygame.draw.rect(screen, Color.RED, disc)
    for i in range(n_discs-1, 0, -1):
        print(i, discs[n_discs-i-1])
        disc = pygame.Rect(discs[-1].left + 5, discs[-1].top-10, discs[-1].width-5*(i+1), 10)
        disc.centerx = discs[-1].centerx
        pygame.draw.rect(screen, random.choice(Color.COLORS), disc)
        discs.append(disc)


if __name__ == '__main__':
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
        pegs = [pygame.Rect(i * WIDTH // 4, HEIGHT // 2, 5, board.top - HEIGHT // 2)
                for i in range(1, 4)]
        display_pegs()
        discs = []
        start_round()

        pygame.display.flip()
        time.sleep(3)