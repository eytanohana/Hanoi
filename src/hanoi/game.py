from __future__ import annotations

from collections import defaultdict
from typing import Final

import pygame
from rich.console import Console

from hanoi import hanoi
from hanoi.cli import Settings

console = Console()

# -----------------------------
# Constants
# -----------------------------
FPS: Final[int] = 60

WIDTH: Final[int] = 800
HEIGHT: Final[int] = 400


BOARD_POS_LEFT: Final[int] = int(0.1 * WIDTH)
BOARD_POS_TOP: Final[int] = int(0.9 * HEIGHT)
BOARD_WIDTH: Final[int] = WIDTH - 2 * BOARD_POS_LEFT
BOARD_HEIGHT: Final[int] = int(0.02 * HEIGHT)


PEG_HEIGHT: Final[int] = HEIGHT // 2
PEG_WIDTH: Final[int] = 6

DISC_HEIGHT: Final[int] = 10
DISC_WIDTH: Final[int] = 120

LIFT_Y: Final[int] = HEIGHT // 3


class QuitGame(Exception):
    """Raised to stop the game loop cleanly when the window is closed."""


class ReturnToStartScreen(Exception):
    """Raised to return to the start screen from the game."""


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


class StartScreen:
    """Start screen for configuring game parameters before starting."""
    
    def __init__(self, screen: pygame.Surface, default_settings: Settings):
        self.screen = screen
        self.default_settings = default_settings
        
        # Current values
        self.n_disks = default_settings.n_disks
        self.speed = default_settings.speed
        
        # Input states
        self.active_field = 0  # 0: n_disks, 1: speed, 2: start button

        self.input_texts = [str(self.n_disks), str(self.speed)]
        self.editing = False
        
        # Fonts
        pygame.font.init()
        self.title_font = pygame.font.Font(None, 48)
        self.label_font = pygame.font.Font(None, 32)
        self.input_font = pygame.font.Font(None, 28)
        self.button_font = pygame.font.Font(None, 36)
        
        # Colors
        self.bg_color = Color.WHITE
        self.text_color = Color.BLACK
        self.active_color = Color.BLUE
        self.inactive_color = Color.GREY
        self.button_color = Color.GREEN
        self.button_hover_color = Color.LIGHT_BLUE
        
    def handle_event(self, event: pygame.event.Event) -> Settings | None:
        """Handle events. Returns Settings if start is pressed, None otherwise."""
        if event.type != pygame.KEYDOWN:
            return None
        
        if event.key == pygame.K_ESCAPE:
            raise QuitGame
        
        if event.key == pygame.K_UP or (event.key == pygame.K_TAB and (event.mod & pygame.KMOD_SHIFT)):
            self._navigate_up()
            return None
        
        if event.key in (pygame.K_TAB, pygame.K_DOWN):
            self._navigate_down()
            return None
        
        # Start game or toggle edit mode
        if event.key in (pygame.K_RETURN, pygame.K_SPACE):
            if self.active_field == 2:  # Start button
                return self._create_settings()
            self._toggle_edit_mode()
            return None
        
        # Handle text input
        if self.active_field < 3:
            # self._handle_text_input(event)
            if self.editing:
                self._handle_text_input(event)
            elif event.unicode.isdigit():
                # Start editing when typing a number
                self.editing = True
                self.input_texts[self.active_field] = event.unicode
        
        return None
    
    def _navigate_up(self) -> None:
        """Navigate to the previous field."""
        if self.editing and self.active_field < len(self.input_texts):
            self._commit_field()
        self.active_field = (self.active_field - 1) % (len(self.input_texts) + 1)
        self.editing = False
    
    def _navigate_down(self) -> None:
        """Navigate to the next field."""
        if self.editing and self.active_field < len(self.input_texts):
            self._commit_field()
        self.active_field = (self.active_field + 1) % (len(self.input_texts) + 1)
        self.editing = False
    
    def _toggle_edit_mode(self) -> None:
        """Toggle edit mode for the current field."""
        if self.editing:
            self._commit_field()
            self.editing = False
        else:
            self.editing = True
    
    def _handle_text_input(self, event: pygame.event.Event) -> None:
        """Handle text input when editing a field."""
        if event.key == pygame.K_BACKSPACE:
            if self.input_texts[self.active_field]:
                self.input_texts[self.active_field] = self.input_texts[self.active_field][:-1]
        elif event.unicode.isdigit():
            self.input_texts[self.active_field] += event.unicode
    
    def _commit_field(self) -> None:
        """Commit the current field value and validate it."""
        if self.active_field >= len(self.input_texts):
            return
        
        # Get and validate input
        input_text = self.input_texts[self.active_field].strip()
        if not input_text:
            # Empty input, reset to current value
            self._reset_field_display()
            return
        
        try:
            value = int(input_text)
        except ValueError:
            # Invalid input, reset to current value
            self._reset_field_display()
            return

        # Apply validation and update values
        if self.active_field == 0:  # n_disks
            self.n_disks = max(1, min(10, value))
            self.input_texts[0] = str(self.n_disks)
        else:  # self.active_field == 1:  # speed
            self.speed = max(1, value)
            self.input_texts[1] = str(self.speed)
    
    def _reset_field_display(self) -> None:
        """Reset the current field display to its committed value."""
        if self.active_field == 0:
            self.input_texts[0] = str(self.n_disks)
        elif self.active_field == 1:
            self.input_texts[1] = str(self.speed)

    def _create_settings(self) -> Settings:
        """Create Settings object from current values."""
        # Commit any field that's being edited
        return Settings(
            n_disks=self.n_disks,
            speed=self.speed,
            animate=True
        )
    
    def render(self) -> None:
        """Render the start screen."""
        self.screen.fill(self.bg_color)
        
        # Title
        self._render_title()
        
        # Configuration fields
        y_start = 140
        spacing = 60
        self._render_field(0, "Number of Disks (1-10):", self.input_texts[0], y_start)
        self._render_field(1, "Speed (pixels/frame):", self.input_texts[1], y_start + spacing)
        
        # Start button
        self._render_button(2, "Start Game", y_start + 2 * spacing + 20)
        
        # Instructions
        self._render_instructions()
        
        pygame.display.flip()
    
    def _render_title(self) -> None:
        """Render the title and subtitle."""
        title_text = self.title_font.render("Towers of Hanoi", True, self.text_color)
        title_rect = title_text.get_rect(center=(WIDTH // 2, 40))
        self.screen.blit(title_text, title_rect)
        
        subtitle_text = self.label_font.render("Configure Game Settings", True, self.inactive_color)
        subtitle_rect = subtitle_text.get_rect(center=(WIDTH // 2, 80))
        self.screen.blit(subtitle_text, subtitle_rect)
    
    def _render_instructions(self) -> None:
        """Render the instruction text."""
        inst_text = self._get_instruction_text()
        inst_surface = self.label_font.render(inst_text, True, self.inactive_color)
        inst_rect = inst_surface.get_rect(center=(WIDTH // 2, HEIGHT - 20))
        self.screen.blit(inst_surface, inst_rect)
    
    def _get_instruction_text(self) -> str:
        """Get the instruction text based on current state."""
        if self.active_field == 3:
            return "Press Enter or Space to start the game"
        elif self.editing:
            return "Type numbers, Enter to confirm, Tab/Arrow keys to navigate"
        else:
            return "Press Enter to edit, Tab/Arrow keys to navigate, Enter on Start to begin"
    
    def _render_field(self, index: int, label: str, value: str, y: int) -> None:
        """Render a labeled input field."""
        is_active = self.active_field == index
        is_editing = is_active and self.editing
        
        # Label
        label_color = self.active_color if is_active else self.text_color
        label_surface = self.label_font.render(label, True, label_color)
        label_rect = label_surface.get_rect(midright=(WIDTH // 2 - 20, y))
        self.screen.blit(label_surface, label_rect)
        
        # Input box
        input_color = self.active_color if is_active else self.inactive_color
        input_rect = pygame.Rect(WIDTH // 2 + 20, y - 15, 100, 30)
        border_width = 3 if is_editing else 2
        pygame.draw.rect(self.screen, input_color, input_rect, border_width)
        
        # Input text with cursor
        display_text = value if value else "0"
        if is_editing:
            display_text += "|"
        text_surface = self.input_font.render(display_text, True, self.text_color)
        text_rect = text_surface.get_rect(midleft=(input_rect.left + 5, input_rect.centery))
        self.screen.blit(text_surface, text_rect)
    
    def _render_button(self, index: int, text: str, y: int) -> None:
        """Render a button."""
        is_active = self.active_field == index
        button_color = self.button_hover_color if is_active else self.button_color
        button_rect = pygame.Rect(WIDTH // 2 - 100, y - 20, 200, 40)
        
        pygame.draw.rect(self.screen, button_color, button_rect)
        pygame.draw.rect(self.screen, self.text_color, button_rect, 2)
        
        text_surface = self.button_font.render(text, True, self.text_color)
        text_rect = text_surface.get_rect(center=button_rect.center)
        self.screen.blit(text_surface, text_rect)
    
    def run(self) -> Settings:
        """Run the start screen loop. Returns Settings when user starts the game."""
        clock = pygame.time.Clock()
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    raise QuitGame
                
                settings = self.handle_event(event)
                if settings is not None:
                    return settings
            
            self.render()
            clock.tick(FPS)


class Game:
    def __init__(self, settings: Settings):
        self.settings = settings
        # pygame.init() is called in run_pygame, so we don't need to call it here
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.board = pygame.Rect(BOARD_POS_LEFT, BOARD_POS_TOP, BOARD_WIDTH, BOARD_HEIGHT)
        self.pegs = self.init_pegs()
        self.disks = self.init_discs(self.settings.n_disks)

        self.peg_stacks = defaultdict(list)
        self.peg_stacks[1].extend(self.disks)

        self.print_spaces = len(str(2**self.settings.n_disks - 1))
        self.print_disk_spaces = len(str(self.settings.n_disks))
        self.clock = pygame.time.Clock()

        self.finished = False
        self.paused = False
        self.step_once = False

        # Initialize font for text display
        pygame.font.init()
        self.font = pygame.font.Font(None, 24)
        self.current_move_text = None

        self._update_caption()

    def init_pegs(self) -> list[pygame.Rect]:
        return [
            pygame.Rect(peg_num * WIDTH // 4, PEG_HEIGHT, PEG_WIDTH, self.board.top - PEG_HEIGHT)
            for peg_num in range(1, 4)
        ]

    def init_discs(self, n_discs) -> list[pygame.Rect]:
        discs = []
        for i in range(n_discs, 0, -1):
            width = DISC_WIDTH if i == n_discs else int(discs[-1].width * 0.9)
            disc = pygame.Rect(0, 0, width, DISC_HEIGHT)
            disc.centerx = self.pegs[0].centerx
            disc.bottom = self.board.top if i == n_discs else discs[-1].top
            discs.append(disc)
        return discs

    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise QuitGame
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_q):
                    raise QuitGame
                if event.key in (pygame.K_SPACE, pygame.K_p):
                    self.paused = not self.paused
                    if not self.paused:
                        # Resuming from pause - exit step mode to allow continuous running
                        self.step_once = False
                    self._update_caption()
                if event.key in (pygame.K_RIGHT, pygame.K_n):
                    self.step_once = True
                    if self.paused:
                        self.paused = False
                    self._update_caption()
                if event.key == pygame.K_r:
                    raise ReturnToStartScreen

    def _update_caption(self):
        caption = 'Towers of Hanoi'
        if not self.finished:
            if self.step_once:
                caption += '(Step)'
            elif self.paused:
                caption += ' (Paused)'
        pygame.display.set_caption(caption)

    def wait_if_paused(self):
        while self.paused:
            self.handle_events()
            self.refresh()

    def run(self):
        while True:
            self.refresh()
            move_iterator = enumerate(hanoi(self.settings.n_disks), 1)
            i = 0

            while True:
                self.handle_events()

                # If paused, wait (unless step_once is triggered, which will unpause)
                if self.paused and not self.step_once:
                    self.refresh()
                    continue

                # Execute next move
                try:
                    i, (disc, from_, to) = next(move_iterator)
                    move_text = (
                        f'{i:{self.print_spaces}}: Move disc {disc:{self.print_disk_spaces}} from peg {from_} to {to}.'
                    )
                    console.print(move_text)
                    self.current_move_text = move_text
                    self.move_disc(from_, to)

                    # If in step mode, pause after completing the move
                    if self.step_once:
                        self._update_caption()
                        self.paused = True
                        self.step_once = False
                except StopIteration:
                    self.finished = True
                    completion_text = f'{self.settings.n_disks} discs solved in {i} moves.'
                    console.print(f'\n[green]{completion_text}')
                    self.current_move_text = completion_text
                    while True:  # Wait for restart or quit
                        self.handle_events()
                        self.refresh()

    def refresh(self):
        self.screen.fill(Color.WHITE)
        pygame.draw.rect(self.screen, Color.BLACK, self.board)
        for peg in self.pegs:
            pygame.draw.rect(self.screen, Color.BLACK, peg)
        for i, disc in enumerate(self.disks):
            pygame.draw.rect(self.screen, Color.DISC_COLORS[i % len(Color.DISC_COLORS)], disc)

        # Display current move text
        if self.current_move_text:
            text_surface = self.font.render(self.current_move_text, True, Color.BLACK)
            text_rect = text_surface.get_rect()
            text_rect.centerx = WIDTH // 2
            text_rect.centery = HEIGHT // 5
            self.screen.blit(text_surface, text_rect)

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
        done = False
        while not done:
            self.handle_events()
            self.wait_if_paused()
            done = self._step_towards(rect, x=x, y=y, bottom=bottom)
            self.refresh()

    def move_disc(self, from_peg, to_peg):
        disc = self.peg_stacks[from_peg].pop()
        self._animate_to(disc, y=LIFT_Y)

        to_x = self.pegs[to_peg - 1].centerx
        self._animate_to(disc, x=to_x)

        try:
            top_disk = self.peg_stacks[to_peg][-1]
            to_y = top_disk.top
        except IndexError:
            to_y = self.board.top
        self._animate_to(disc, bottom=to_y)
        self.peg_stacks[to_peg].append(disc)


def run_pygame(settings: Settings):
    try:
        pygame.init()
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        current_settings = settings
        
        # Main loop: start screen -> game -> start screen (on restart)
        while True:
            # Show start screen
            start_screen = StartScreen(screen, current_settings)
            final_settings = start_screen.run()
            current_settings = final_settings
            
            # Create game with final settings (pygame already initialized)
            game = Game(final_settings)
            try:
                game.run()
            except ReturnToStartScreen:
                # Return to start screen with current settings
                continue
    except QuitGame:
        console.print('[blue]quitting game...')
    except KeyboardInterrupt:
        console.print('[yellow]interrupted, quitting game...')
