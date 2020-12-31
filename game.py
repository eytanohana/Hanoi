import pygame

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


def display_pegs():
    for peg in pegs:
        pygame.draw.rect(screen, Color.BLACK, peg)


def reset_globals(width, height):
    global WIDTH, HEIGHT, BOARD_POS_LEFT, BOARD_POS_TOP, \
        BOARD_WIDTH, BOARD_HEIGHT, BOARD_DIMS
    WIDTH = width
    HEIGHT = height

    BOARD_POS_LEFT = int(0.1 * WIDTH)
    BOARD_POS_TOP = int(0.9 * HEIGHT)
    BOARD_WIDTH = WIDTH - 2 * BOARD_POS_LEFT
    BOARD_HEIGHT = int(0.02 * HEIGHT)
    BOARD_DIMS = BOARD_POS_LEFT, BOARD_POS_TOP, BOARD_WIDTH, BOARD_HEIGHT


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    board = pygame.Rect(*BOARD_DIMS)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.VIDEORESIZE:
                reset_globals(event.w, event.h)
                screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

        screen.fill(Color.WHITE)
        pygame.draw.rect(screen, Color.BLACK, board)
        pegs = [pygame.Rect(i * WIDTH // 4, HEIGHT // 2, 5, board.top - HEIGHT // 2)
                for i in range(1, 4)]
        display_pegs()

        pygame.display.flip()
