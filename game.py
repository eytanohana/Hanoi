import pygame

WIDTH = 800
HEIGHT = 500

LEFT = int(0.1 * WIDTH)
TOP = int(0.9 * HEIGHT)

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

        screen.fill('#ffffff')
        pygame.draw.rect(screen, (0, 0, 0),
                         pygame.Rect(LEFT, TOP, WIDTH - 2 * LEFT, 20))
        pygame.display.flip()
