# Ascii Maze

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)


This is a pathfinding algorithms visualizer written in Python using the Pygame library. The program allows you to visualize various pathfinding algorithms on a map represented by ASCII characters. It supports both randomly generated maps and reading maps from files.

## Features

- ASCII Map Representation: The program uses ASCII characters to simply represent the map.
- Dynamic Map: You can add and delete elements of the ascii map.
- Map File Support: You can read maps from text files. 
- Pathfinding Algorithms:
  - Breadth-First Search (BFS)
  - Depth-First Search (DFS)
  - A-Star (A*)
  - Variations of A-Star that have different heuristics and/or support multiple targets instead of just one.

## Requirements

- Python 3.x
- See [requirements.txt](./requirements.txt) file for further information

## Installation & Usage

1. Clone the repository or download the source code.
2. Inside the repository file, execute `pip3 install -r requirements.txt`
3. Run [main.py](./main.py)

## Controls

- 1: Select start (S) or end (E) blocks, if possible
- 2: Select walls (#)
- 3: Select hubs (H)
- Q: Change to previous algorithm
- E: Change to next algorithm
- Space: Start search
- R: Clear map
- T: Reload map from file (basic_maze.txt)
- Y: Resets map to pre-search state
- ESC: Exit the program

## Background

-
