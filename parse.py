# Parse a mazefile into a maze array

from cell import Cell


MAZE_FILE = "mazes/maze1.txt"


def parse(lines: list[str]) -> list[list[Cell]]:
    """Parse a maze file into a 2d list of cells
    Expected 16x16 maze file with correct format otherwise behavior unknown"""
    maze = []
    for a, b, c in zip(lines[::2], lines[1::2], lines[2::2]):
        maze.append([])
        top_walls = [c == "-" for c in a[2::4]]
        right_walls = [c == "|" for c in b[4::4]]
        bottom_walls = [c == "-" for c in c[2::4]]
        left_walls = [c == "|" for c in b[:-1:4]]
        starts = [i // 4 for i, c in enumerate(b) if c == "S"]
        ends = [i // 4 for i , c in enumerate(b) if c == "G"]
        for t, r, b, l in zip(top_walls, right_walls, bottom_walls, left_walls):
            maze[-1].append(Cell(t, r, b, l))
        for s in starts:
            maze[-1][s].start = True
        for e in ends:
            maze[-1][e].end = True
    return maze
