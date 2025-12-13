from __future__ import annotations

import argparse
from collections import defaultdict
from dataclasses import dataclass

import pygame

from hanoi import hanoi

FPS = 60

WIDTH = 600
HEIGHT = 400

BOARD_POS_LEFT = int(0.1 * WIDTH)
BOARD_POS_TOP = int(0.9 * HEIGHT)
BOARD_WIDTH = WIDTH - 2 * BOARD_POS_LEFT
BOARD_HEIGHT = int(0.02 * HEIGHT)
BOARD_DIMS = BOARD_POS_LEFT, BOARD_POS_TOP, BOARD_WIDTH, BOARD_HEIGHT

PEG_HEIGHT = HEIGHT // 2


class QuitGame(Exception):
    pass


class Color:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
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


@dataclass
class Settings:
    n_disks: int = 3
    speed: int = 6  # movement speed
    pause_after_solve_ms: int = 0


class Game:
    def __init__(self, settings: Settings):
        self.settings = settings
        pygame.init()
        pygame.display.set_caption("Towers of Hanoi")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.board = pygame.Rect(*BOARD_DIMS)
        self.pegs = self.init_pegs()
        self.disks = self.init_discs(self.settings.n_disks)

        self.peg_stacks = defaultdict(list)
        self.peg_stacks[1].extend(self.disks)

        self.print_spaces = len(str(2**self.settings.n_disks - 1))
        self.print_disk_spaces = len(str(self.settings.n_disks))
        self.clock = pygame.time.Clock()

    def init_pegs(self) -> list[pygame.Rect]:
        return [
            pygame.Rect(
                peg_num * WIDTH // 4, PEG_HEIGHT, 5, self.board.top - PEG_HEIGHT
            )
            for peg_num in range(1, 4)
        ]

    def init_discs(self, n_discs) -> list[pygame.Rect]:
        discs = []
        for i in range(n_discs, 0, -1):
            disc = pygame.Rect(0, 0, 0, 0)
            discs.append(disc)
            disc.width = 120 if i == n_discs else discs[-2].width * 0.9
            disc.height = 10
            disc.centerx = self.pegs[0].centerx
            disc.bottom = self.board.top if i == n_discs else discs[-2].top
        return discs

    @staticmethod
    def check_events():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise QuitGame

    def run(self):
        try:
            self.refresh()
            for i, (disc, from_, to) in enumerate(hanoi(self.settings.n_disks), 1):
                print(
                    f"{i:{self.print_spaces}}: Move disc {disc:{self.print_disk_spaces}} from peg {from_} to {to}."
                )
                self.move_disc(from_, to)
            else:
                print(f"\n{self.settings.n_disks} discs solved in {i} moves.")

            while True:
                self.check_events()
                self.refresh()
        except QuitGame:
            return

    def refresh(self):
        self.screen.fill(Color.WHITE)
        pygame.draw.rect(self.screen, Color.BLACK, self.board)
        for peg in self.pegs:
            pygame.draw.rect(self.screen, Color.BLACK, peg)
        for i, disc in enumerate(self.disks):
            pygame.draw.rect(
                self.screen, Color.DISC_COLORS[i % len(Color.DISC_COLORS)], disc
            )
        pygame.display.flip()
        self.clock.tick(FPS)

    def _step_towards(
        self,
        rect: pygame.Rect,
        *,
        x: int | None = None,
        y: int | None = None,
        bottom: int | None = None,
    ):
        speed = self.settings.speed

        def approach(current: int, target: int):
            if current == target or abs(target - current) <= speed:
                return target, True
            return (current + speed if target > current else current - speed), False

        done = True
        if x is not None:
            rect.centerx, ok = approach(rect.centerx, x)
            done &= ok
        if y is not None:
            rect.centery, ok = approach(rect.centery, y)
            done &= ok
        if bottom is not None:
            rect.bottom, ok = approach(rect.bottom, bottom)
            done &= ok
        return done

    def _animate_to(
        self,
        rect: pygame.Rect,
        *,
        x: int | None = None,
        y: int | None = None,
        bottom: int | None = None,
    ):
        while True:
            self.check_events()
            done = self._step_towards(rect, x=x, y=y, bottom=bottom)
            self.refresh()
            if done:
                return

    def move_disc(self, from_peg, to_peg):
        disc = self.peg_stacks[from_peg].pop()
        self._animate_to(disc, y=HEIGHT // 3)

        to_x = self.pegs[to_peg - 1].centerx
        self._animate_to(disc, x=to_x)

        try:
            top_disk = self.peg_stacks[to_peg][-1]
            to_y = top_disk.top
        except IndexError:
            to_y = self.board.top
        self._animate_to(disc, bottom=to_y)
        self.peg_stacks[to_peg].append(disc)


def parse_args() -> Settings:
    p = argparse.ArgumentParser(description="Animate Towers of Hanoi (pygame).")
    p.add_argument(
        "n_disks", nargs="?", type=int, default=3, help="number of disks (1..15)"
    )
    p.add_argument(
        "--speed", type=int, default=15, help="pixels per frame (movement speed)"
    )
    args = p.parse_args()

    n = args.n_disks
    if n < 1:
        n = 3
        print("Invalid number of disks. Using 3 disks instead.")
    if n > 10:
        n = 10
        print("Too many disks. Using 15 disks instead.")

    return Settings(n_disks=n, speed=max(10, args.speed))


def main():
    settings = parse_args()
    game = Game(settings)
    game.run()


if __name__ == "__main__":
    main()
