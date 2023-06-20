from os import environ

environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'                          # Disables the pygame initialization prompt

import config
import pygame
import input
from config import *
from pygcurse import PygcurseWindow
from pygame.font import Font, SysFont


pygame.init()                                                        # Initialize pygame.
pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLEBUFFERS, 3)     # Enables Anti-Aliasing
pygame.display.gl_set_attribute(pygame.GL_ACCELERATED_VISUAL, 1)     # Enables Pygame graphical acceleration

# Window object to display output.
try:
    window: PygcurseWindow = PygcurseWindow(*RES, fgcolor=WHITE, bgcolor=BACKGROUND_COLOR, font=Font(*FONT))

except FileNotFoundError:
    window: PygcurseWindow = PygcurseWindow(*RES, fgcolor=WHITE, bgcolor=BACKGROUND_COLOR, font=SysFont(*SYS_FONT))


def clear() -> None:
    """
    Clears the display.
    :return:
    """

    config.CHOSEN_END = ()                                    # Erase end node coordinates.
    config.CHOSEN_START = ()                                  # Erase starting node coordinates.
    config.MAP = [row.copy() for row in BLANK_MAP.copy()]     # Restart map values.
    config.chosen_hubs = []                                   # Resart hub values.

    window.fill(NODE_SYMBOLS[-1], fgcolor=config.NODE_COLORS[NODE_SYMBOLS[-1]], bgcolor=BACKGROUND_COLOR)


# Clear the window, must be done to avoid a bug with the library fill function.
clear()

# Adds a shadow around the window.
window.addshadow()


def __register_display(char: str, coords: tuple[int, int]) -> None:
    """
    Adds a drawn character into the MAP.
    Takes scaled coordinates.
    :param char:
    :param coords:
    :return:
    """

    try:
        config.MAP[coords[1]][coords[0]] = char

        if char == NODE_SYMBOLS[3]:
            config.chosen_hubs.append(coords)

    except TypeError:
        return


def __draw_char(char: str, coords: tuple[int, int],
                color: COLOR, bg_color: COLOR = BACKGROUND_COLOR,
                no_register: bool = False) -> None:
    """
    Draws the given char at the given 2D coordinates, and registers the char in the MAP.
    :param char:
    :param coords:
    :return:
    """

    # Actual coordinates on the screen.
    true_coordinates: tuple[int, int] = __scale_coordinates(coords)

    # Register the char in the map.
    __register_display(char, true_coordinates) if not no_register else ...

    # Displays the character at that given position.
    window.write(char, *true_coordinates, fgcolor=color, bgcolor=bg_color)


def visual_char_at(coords: tuple[int, int], scaled: bool = False) -> str:
    """
        Returns the character at the given on the screen coordinates in (x, y) format.
        :param scaled:
        :param coords:
        :return:
        """

    scaled_coords: tuple[int, int] = __scale_coordinates(coords) if not scaled else coords
    return window.getchar(*scaled_coords)


def get_char_at(coords: tuple[int, int], scaled: bool = False) -> str:
    """
    Returns the character at the given coordinates in (x, y) format.
    :param scaled:
    :param coords:
    :return:
    """

    scaled_coords: tuple[int, int] = __scale_coordinates(coords) if not scaled else coords
    return config.MAP[scaled_coords[1]][scaled_coords[0]]


def __scale_coordinates(coords: tuple[int, int]) -> tuple[int, int]:
    """
    Returns the scaled coordinates of the char in cells
    :param coords:
    :return:
    """

    return window.getcoordinatesatpixel(*coords) if coords else coords


def __unscale_coordinates(coords: tuple[int, int]) -> tuple[int, int]:
    """
    Returns the unscaled coordinates of the given cell coordinates.
    :param coords:
    :return:
    """

    return window.gettopleftpixel(*coords, onscreen=True) if coords else coords


def draw_char(char: str, coords: tuple[int, int], unscale: bool = False) -> None:
    """
    Checks the char and coordinates, then
    draw the given char at the given 2D coordinates in form (x, y).
    Note that each condition has its own draw_char call, due to issues with pygame synchronization.
    :param unscale:
    :param char:
    :param coords:
    :return:
    """

    try:
        if unscale:
            coords = __unscale_coordinates(coords)

        char_at_coords: str = get_char_at(coords)

        if char == NODE_SYMBOLS[-1]:  # Empty space
            if char_at_coords == NODE_SYMBOLS[0]:  # Erase the starting node.
                config.CHOSEN_START = ()

            elif char_at_coords == NODE_SYMBOLS[1]:  # Erase the end node.
                config.CHOSEN_END = ()

            __draw_char(char, coords, NODE_COLORS[char])

        elif char_at_coords in NODE_SYMBOLS[:2]:
            return

        elif char == NODE_SYMBOLS[0]:  # Starting node
            input.selected_char = NODE_SYMBOLS[1 + bool(config.CHOSEN_END)]
            config.CHOSEN_START = __scale_coordinates(coords)

            __draw_char(char, coords, NODE_COLORS[char])

        elif char == NODE_SYMBOLS[1]:  # End node
            input.selected_char = NODE_SYMBOLS[2]
            config.CHOSEN_END = __scale_coordinates(coords)

            __draw_char(char, coords, NODE_COLORS[char])

        elif char == NODE_SYMBOLS[-3]:  # Search paths
            if char_at_coords == NODE_SYMBOLS[3]:
                __draw_char(NODE_SYMBOLS[3], coords, NODE_COLORS[f"{NODE_SYMBOLS[3]}FOUND"], no_register=True)

            elif visual_char_at(coords) != NODE_SYMBOLS[-2] and char_at_coords != NODE_SYMBOLS[-2]:
                __draw_char(char, coords, NODE_COLORS[char])

        elif char == NODE_SYMBOLS[-2]:  # Final path
            if char_at_coords == NODE_SYMBOLS[3]:  # Check if node is hub.
                __draw_char(NODE_SYMBOLS[3], coords, NODE_COLORS[f"{NODE_SYMBOLS[3]}PASSED"], no_register=True)

            else:
                __draw_char(char, coords, NODE_COLORS[char])

        elif char_at_coords == NODE_SYMBOLS[-1] or not NODE_SYMBOLS[-1]:  # Check if the space is empty, draw char if so.
            __draw_char(char, coords, NODE_COLORS[char])

    except TypeError:
        return


def __valid_line(line: str) -> bool:
    """
    Returns True if the characters in the given map are present in the possible_chars.
    :param line:
    :return:
    """

    has_end: bool = False
    has_start: bool = False

    for c in line:
        if c == NODE_SYMBOLS[1]:
            if has_end:
                return False

            has_end = True

        elif c == NODE_SYMBOLS[0]:
            if has_start:
                return False

            has_start = True

        elif c not in NODE_SYMBOLS:
            return False

    return True


def mark_cell(coords: tuple[int, int]) -> None:
    """
    Displays a search character at the given scaled coords.
    :param coords:
    :return:
    """

    draw_char(NODE_SYMBOLS[-3], coords, unscale=True)


def load_map(file_name: str) -> None:
    """
    Loads a map from a txt file.
    :param file_name:
    :return:
    """

    clear()

    with open(file_name, 'r') as file:
        for line_index in range(RES[1]):
            line: str = file.readline().rstrip()

            if line is None:
                break

            if not __valid_line(line):
                print("\033[31mIncompatible map with list of chars.\033[0m")
                clear()
                return

            for i, c in enumerate(line):
                if RES[0] <= i or line_index == RES[1] - 1 and i == RES[0] - 1:
                    break

                if c == NODE_SYMBOLS[0]:
                    config.CHOSEN_START = (line_index, i)

                elif c == NODE_SYMBOLS[1]:
                    config.CHOSEN_END = (line_index, i)

                draw_char(c, (i, line_index), unscale=True)


def regress() -> None:
    """
    Load given map content to display.
    :return:
    """

    chosen_hubs_copy: list[tuple[int, int]] = [coords for coords in config.chosen_hubs]
    config.chosen_hubs.clear()

    for row_index, row in enumerate(config.MAP):
        for column_index, column in enumerate(row):
            if row_index == RES[1] - 1 and column_index == RES[0] - 1:
                break

            char: str = visual_char_at((column_index, row_index), True)

            if char == NODE_SYMBOLS[-3] or char == NODE_SYMBOLS[-2]:
                draw_char(NODE_SYMBOLS[-1], (column_index, row_index), unscale=True)

            elif char == NODE_SYMBOLS[3]:
                draw_char(NODE_SYMBOLS[-1], (column_index, row_index), unscale=True)
                draw_char(NODE_SYMBOLS[3], (column_index, row_index), unscale=True)

    config.chosen_hubs = chosen_hubs_copy


def virtual_regress() -> None:
    """
    Clears the map without clearing the display.
    :return:
    """

    for row_index, row in enumerate(config.MAP):
        for column_index, column in enumerate(row):
            if row_index == RES[1] - 1 and column_index == RES[0] - 1:
                break

            char: str = get_char_at((column_index, row_index), True)

            if char == NODE_SYMBOLS[-3] or char == NODE_SYMBOLS[-2]:
                __register_display(NODE_SYMBOLS[-1], (column_index, row_index))
