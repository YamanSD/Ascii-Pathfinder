from pygame.locals import K_ESCAPE, K_1, K_2, K_3, K_q, K_e, K_r, K_t, K_y, K_SPACE, \
    KEYDOWN, MOUSEMOTION, MOUSEBUTTONDOWN, MOUSEBUTTONUP


# Resolution of the screen in terms of the number of chars.
RES: tuple[int, int] = 100, 39

# 2D coordinates type
COORDS = tuple[int, int]

# Input timeout in milliseconds
IN_TIMEOUT: int = 5

# Input type from mouse
MOUSE_T = tuple[int, tuple[int, int]]

# Input type from keyboard & mouse
INPUT_T = tuple[int, MOUSE_T]

# Path type
PATH_T = list[tuple[int, int]]

# Color type.
COLOR = tuple[int, int, int]

# Font name, its size, whether it is bold, & whether it is italic. This is a backup font.
SYS_FONT: tuple[str, int, bool, bool] = ("Arial", 13, False, False,)

# Font file name and size.
FONT: tuple[str, int] = ('BaseFont.ttc', 13)

# List of keyboard controls signals, followed by mouse control signals.
CONTROLS: list[int] = [KEYDOWN, K_ESCAPE, K_1, K_2, K_3, K_q, K_e, K_r, K_t, K_y, K_SPACE,
                       MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION]

"""  
Tuple of possible characters.  
Must not change original order.  
If you want to add new nodes, must be between the hub [3] and search chars [4]. 
"""
NODE_SYMBOLS: tuple = ('S', 'E', '#', 'H', '*', '+', ' ',)

# Set of passable characters.
PASSABLE_CHARS: set[str] = {NODE_SYMBOLS[-1], NODE_SYMBOLS[3], NODE_SYMBOLS[1]}

# Coordinates of the start node in (x, y) format.
CHOSEN_START: tuple = ()

# Coordinates of the end node in (x, y) format.
CHOSEN_END: tuple = ()

# Signals a quit event.
QUIT_INPUT: INPUT_T = -1, (-2, (-1, -1))

# Signals that there is no input.
IDLE: INPUT_T = -1, (0, (-1, -1))

# Signals to clear the screen.
CLEAR: tuple[str, int] = NODE_SYMBOLS[-1], -1

# Signals a reset to default map.
RESET: tuple[str, int] = NODE_SYMBOLS[-1], -2

# Signals to start or pause an algorithm
START: tuple[str, int] = NODE_SYMBOLS[-1], -3

# Signlas to restore the grid to its state before aftivating the sorting algorithm.
BACK_SEARCH: tuple[str, int] = NODE_SYMBOLS[-1], -4

# RGB values for white.
WHITE: COLOR = (255, 255, 255)

# RGB values for black.
BLACK: COLOR = (0, 0, 0)

# RGB values for goldish.
GOLD: COLOR = (237, 176, 33)

# RGB values for cyan.
CYAN: COLOR = (33, 179, 171)

# RGB values for dark green.
DARK_GREEN: COLOR = (46, 140, 87)

# RGB values for green.
GREEN: COLOR = (0, 100, 0)

# RGB values for crimson.
CRIMSON: COLOR = (220, 20, 28)

# RGB values for deep blue.
BLUE: COLOR = (0, 191, 255)

# RGB values for orange.
ORANGE: COLOR = (255, 140, 0)

# Background color.
BACKGROUND_COLOR: COLOR = BLACK

# Colors for each node.
NODE_COLORS: dict[str: COLOR] = {
    NODE_SYMBOLS[0]: GOLD,
    NODE_SYMBOLS[1]: DARK_GREEN,
    NODE_SYMBOLS[2]: WHITE,
    NODE_SYMBOLS[3]: CYAN,
    NODE_SYMBOLS[4]: BLUE,
    NODE_SYMBOLS[5]: CRIMSON,
    NODE_SYMBOLS[-1]: BACKGROUND_COLOR,
    f"{NODE_SYMBOLS[3]}PASSED": ORANGE,
    f"{NODE_SYMBOLS[3]}FOUND": GREEN,
}

# Blank map.
BLANK_MAP: list[list[str]] = [[' ' for _ in range(RES[0])] for _ in range(RES[1])]

# 2D scaled map of the chars.
MAP: list[list[str]] = BLANK_MAP.copy()

# Algorithms count.
algo_count: int = 0

# Names of algorithms.
algo_names: list[str] = []

# Coordinates of the hubs on the grid, from oldest to newest in (x, y) format.
chosen_hubs: list[tuple[int, int]] = []
