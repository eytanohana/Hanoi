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


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(Color.WHITE)
        # base board
        pygame.draw.rect(screen, Color.BLACK,
                         pygame.Rect(*BOARD_DIMS))

        # pegs
        for i in range(1, 4):
            pos = i * (WIDTH - 2 * BOARD_POS_LEFT) // 3
            pygame.draw.rect(screen, Color.BLACK,
                             pygame.Rect(pos, HEIGHT // 2, 5, BOARD_POS_TOP - 250))
        pygame.display.flip()
