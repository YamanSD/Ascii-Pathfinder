import algorithms
from algorithms import *
from input import *


def process_main_input(map_name: str = None) -> None:
    while True:
        keyboard_input, mouse_input = process_input()

        if mouse_input != IDLE:
            draw_char(*mouse_input)  # Draws the given character, based on the mouse input.

        if keyboard_input == CLEAR:
            clear()  # Clear display

        elif keyboard_input == START:
            regress()
            algorithms.ALGORITHMS[input.current_function_index]()  # Call the pathfinding algorithm

        elif keyboard_input == BACK_SEARCH:
            regress()

        elif map_name is not None and keyboard_input == RESET:
            """  
            Reload map from the file.  
            Alternatively, we can save the configuration and reload it,  
            but this way it is more rewarding visually.       
            """

            load_map(map_name)


def main(map_name: str = None) -> None:
    # Sets a caption for the window
    set_caption(f"{config.algo_names[0]:}  |  {config.NODE_SYMBOLS[0]:}".center(25))

    if map_name is not None:
        # Load the map for the first time.

        process_input()
        load_map(map_name)

    process_main_input(map_name)


if __name__ == "__main__":
    main("basic_maze.txt")
