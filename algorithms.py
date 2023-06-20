from __future__ import annotations

from display import *
from typing import Optional, Callable
from queue import PriorityQueue
from collections import deque


class Node:
    def __init__(self, coords: tuple[int, int], parent: Optional[Node] = None,
                 cost: float = 0, heuristic: float = 0) -> None:
        """
        Create an instance of node.
        :param coords: In (y, x) format.
        :param parent: Node parent.
        """

        self.char: str = get_char_at(coords[::-1], True)
        self.coords: tuple[int, int] = coords
        self.parent: Node = parent

        self.display()

        self.cost: float = cost
        self.heuristic: float = heuristic

    def __lt__(self, other: Node) -> bool:
        """
        Returns True if the total cost of self is less than other
        :param other:
        :return:
        """

        return self.cost + self.heuristic < other.cost + other.heuristic

    def __eq__(self, other: Node) -> bool:
        """
        Returns True if the nodes are identical.
        :param other:
        :return:
        """

        return self.char == other.char and self.coords == other.coords

    def display_path(self) -> None:
        """
        Displays the node path from start.
        :return:
        """

        temp: Node = self

        while temp:
            draw_char(NODE_SYMBOLS[-2], temp.coords[::-1], unscale=True)
            temp = temp.parent

    def display(self) -> None:
        """
        Returns the node coords in (y, x) format.
        :return:
        """

        draw_char(NODE_SYMBOLS[-3], self.coords[::-1], unscale=True)


def __is_valid(coords: tuple[int, int]) -> bool:
    """
    Returns True if the coords in (y, x) format are valid.
    :param coords:
    :return:
    """

    return coords != (RES[1] - 1, RES[0] - 1) and 0 <= coords[0] < RES[1] and 0 <= coords[1] < RES[0]


def is_accessible(coords: tuple[int, int]) -> bool:
    """
    Returns True if the coords in (y, x) format are a valid space for searching.
    :param coords:
    :return:
    """

    return __is_valid(coords) and get_char_at(coords[::-1], True) in PASSABLE_CHARS


def manhattan_distance(A: tuple[int, int], B: tuple[int, int]) -> int:
    """
    Returns the Manhattan Distance between points A and B.
    :param A:
    :param B:
    :return:
    """

    return abs(A[0] - B[0]) + abs(A[1] - B[1])


def birds_eye_distance(A: tuple[int, int], B: tuple[int, int]) -> float:
    """
    Returns the birds eye distance between points A and B.
    :param A:
    :param B:
    :return:
    """

    return ((A[0] - B[0]) ** 2 + (A[1] - B[1]) ** 2) ** 0.5


def get_acc_coords(coords: tuple[int, int]) -> list[tuple[int, int]]:
    """
    Returns a list of possible chars with their coordinates in (y, x) format.
    :param coords:
    :return:
    """

    possible_coords: list[tuple[int, int]] = [
        (coords[0] + 1, coords[1]),
        (coords[0] - 1, coords[1]),
        (coords[0], coords[1] + 1),
        (coords[0], coords[1] - 1),
    ]

    return [c for c in possible_coords if is_accessible(c)]


def depth_first_search(*, left_pop: bool = False) -> None:
    """
    Depth First Search algorithm.
    Uninformed search.
    Does not guarantee shortest path.
    If left_pop is True, the algorithm becomes breadth first search.
    :return:
    """

    if not config.CHOSEN_START or not config.CHOSEN_END:
        return

    # Start Node.
    starting_node: Node = Node(config.CHOSEN_START[::-1])

    # End Node.
    end_node: Node = Node(config.CHOSEN_END[::-1])

    # Explored coords in (y, x) format.
    explored: set[tuple[int, int]] = {CHOSEN_START[::-1]}

    # Queue of the Nodes to be explored.
    frontier: deque[Node] = deque()
    frontier.append(starting_node)

    while frontier:
        current_node: Node = frontier.popleft() if left_pop else frontier.pop()

        if current_node == end_node:
            current_node.display_path()
            return

        for coords in get_acc_coords(current_node.coords):  # Explore unexplored viable children.
            if coords in explored:
                continue

            child_node: Node = Node(coords, current_node)  # Create node object.
            frontier.append(child_node)  # Add it to the frontier.

    return None


def breadth_first_search() -> None:
    """
    Depth first search, with pop_left set to True.
    Guarantees shortest path.
    :return:
    """

    return depth_first_search(left_pop=True)


def A_Star(distance_func: Callable = manhattan_distance, heuristic_func: Callable = lambda _: 1,
           chase_hubs: bool = False, starting_coords: tuple[int, int] = None,
           end_coords: tuple[int, int] = None, common_front: PriorityQueue = None,
           common_explored: dict = None) -> None:
    """
    A-Star algorithm.
    Informed search.
    Guarantees shortest path.
    Start and end coords are in (y, x) format.
    :return:
    """

    if not config.CHOSEN_START or not config.CHOSEN_END:
        return

    if starting_coords is None:
        starting_coords = config.CHOSEN_START[::-1]

    if end_coords is None:
        end_coords = config.CHOSEN_END[::-1]

    # Start Node.
    starting_node: Node = Node(starting_coords)

    # End Node.
    end_node: Node = Node(end_coords if end_coords else (-1, -1))

    if chase_hubs and starting_coords == config.CHOSEN_START[::-1]:

        target_hubs: list[tuple[int, int]] = [coords[::-1] for coords in config.chosen_hubs if visual_char_at(coords, True) == NODE_SYMBOLS[3]]

        target_hubs = [starting_coords] + target_hubs + ([end_node.coords] if end_node.coords != (-1, -1) else [])

        if len(target_hubs) == 1:
            A_Star(end_coords=target_hubs[0], heuristic_func=heuristic_func, distance_func=distance_func)

        else:
            for index, point in enumerate(target_hubs[:-1]):
                virtual_regress()

                A_Star(starting_coords=point, end_coords=target_hubs[index + 1],
                       distance_func=distance_func, heuristic_func=heuristic_func,
                       common_explored=common_explored, common_front=common_front)

        return

    # Explored coords in (y, x) format.
    explored: dict[tuple[int, int]: float] = {
        starting_coords: 0.0
    } if common_explored is None else common_explored

    # Queue of the Nodes to be explored.
    frontier: PriorityQueue[Node] = PriorityQueue() if common_front is None else common_front
    frontier.put(starting_node)

    while not frontier.empty():
        current_node: Node = frontier.get()

        if current_node == end_node or end_node.coords in explored:
            current_node.display_path()
            return

        adj_acc_coords: list[tuple[int, int]] = get_acc_coords(current_node.coords)

        for coords in adj_acc_coords:  # Explore unexplored viable children.
            new_cost: float = current_node.cost + heuristic_func(
                current_node.heuristic)  # 1 assumes a grid, needs a cost function for sophisticated apps.

            if coords not in explored or new_cost < explored[coords]:
                explored[coords] = new_cost

                child_node: Node = Node(coords, current_node, new_cost, distance_func(end_node.coords, coords))

                frontier.put(child_node)

    return


def A_Star_M() -> None:
    """
    A-Star but with a heuristic function.
    :return:
    """

    return A_Star(heuristic_func=lambda a: -1 / max(a, 1))


def A_Star_B() -> None:
    """
    A_Star_M, but passes through all hubs, then the end.
    :return:
    """

    return A_Star(chase_hubs=True, heuristic_func=lambda a: 1 / max(a, 1) ** 3)


def A_Star_T() -> None:
    """
    A_Star_B, but with a united front and explored.
    :return:
    """

    explored: dict = {
        config.CHOSEN_START[::-1]: 0
    }

    front: PriorityQueue = PriorityQueue()

    return A_Star(chase_hubs=True, common_explored=explored, common_front=front, heuristic_func=lambda a: 1 / max(a, 1))


def A_Star_BO() -> None:
    """
    A_Star_B but returns optimal path between nodes.
    :return:
    """

    return A_Star(chase_hubs=True)


# List of path finding algorithms.
ALGORITHMS: list[Callable[None: None]] = [
    depth_first_search,
    breadth_first_search,
    A_Star,
    A_Star_M,
    A_Star_B,
    A_Star_BO,
    A_Star_T,
]

# Change the number of algos.
config.algo_count = len(ALGORITHMS)

# Update the names of the algos in config.
config.algo_names = [a.__name__ for a in ALGORITHMS]
