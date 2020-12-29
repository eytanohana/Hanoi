import pygame

WIDTH = 800
HEIGHT = 500

LEFT = int(0.1 * WIDTH)
TOP = int(0.9 * HEIGHT)

BOTTOM_BOARD_DIMS = LEFT, TOP, WIDTH - 2 * LEFT, 20


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
                         pygame.Rect(*BOTTOM_BOARD_DIMS))

        # pegs
        for i in range(1, 4):
            pos = i * (WIDTH - 2 * LEFT) // 3
            pygame.draw.rect(screen, Color.BLACK,
                             pygame.Rect(pos, HEIGHT//2, 5, TOP-250))
        pygame.display.flip()
