from cell import Cell
from parse import parse

import curses
import math
import time


# instead of simply marking that a cell has been visited
# track the direction it took to reach it
# so if you need to backtrack while on that cell, can just reverse that direction



def floodfill(maze: list[list[Cell]], stdscr, delay=0.1) -> None:
    """Simulate the floodfill algo on a maze"""
    # TODO: figure out how to handle loops in the maze
    # can track direction and turn around when stopped

    # move toward end of maze in next square that hasn't been covered
    # if blocked on all size, backtrack until reached new path
    # indicate backtracked with a double mark on the square
    cur_r, cur_c = find_start(maze)
    maze[cur_r][cur_c].visited = True

    draw_maze(stdscr, maze)
    time.sleep(delay)
    while not maze[cur_r][cur_c].end:
        # find next unvisited cell in direction of end (center)
        cur = maze[cur_r][cur_c]
        if cur.end:
            break
        best_way = None
        best_dist = 100000
        # check UP
        if not cur.top and cur_r > 0:
            c = maze[cur_r - 1][cur_c]
            if not c.visited and (d := distance(cur_r - 1, cur_c)) < best_dist:
                best_way = cur_r - 1, cur_c
                best_dist = d
                move_dir = "UP"

        # check RIGHT
        if not cur.right and cur_c < 15:
            c = maze[cur_r][cur_c + 1]
            if not c.visited and (d := distance(cur_r, cur_c + 1)) < best_dist:
                best_way = cur_r, cur_c + 1
                best_dist = d
                move_dir = "RIGHT"

        # check DOWN
        if not cur.bottom and cur_r < 15:
            c = maze[cur_r + 1][cur_c]
            if not c.visited and (d := distance(cur_r + 1, cur_c)) < best_dist:
                best_way = cur_r + 1, cur_c
                best_dist = d
                move_dir = "DOWN"

        # check LEFT
        if not cur.left and cur_c > 0:
            c = maze[cur_r][cur_c - 1]
            if not c.visited and (d := distance(cur_r, cur_c - 1)) < best_dist:
                best_way = cur_r, cur_c - 1
                best_dist = d
                move_dir = "LEFT"
        
        # move to that cell mark cell visited
        if best_way is not None:
            cur_r, cur_c = best_way
            maze[cur_r][cur_c].visited = move_dir
        else:
            # if no unvisited cell to go to
            #   backtrack and mark last cell backtracked
            cur.backtracked = True
            # find way to backtrack should only have one way to go back
            if cur.visited == "UP":
                cur_r, cur_c = cur_r + 1, cur_c
            elif cur.visited == "RIGHT":
                cur_r, cur_c = cur_r, cur_c - 1
            elif cur.visited == "DOWN":
                cur_r, cur_c = cur_r - 1, cur_c
            elif cur.visited == "LEFT":
                cur_r, cur_c = cur_r, cur_c + 1
            else:
                print("what the fuck bozo")

        draw_maze(stdscr, maze)
        time.sleep(delay)
    draw_final_path(stdscr, maze)
    stdscr.refresh()


def distance(row: int, col: int) -> float:
    """find the distance to the center of the maze"""
    return math.sqrt((row - 7.5) ** 2 + (col - 7.5) ** 2)


def draw_maze(stdscr, maze: list[list[Cell]]) -> None:
    """Draw the maze on a curses screen"""
    for i, row in enumerate(maze):
        for j, cell in enumerate(row):
            if cell.top:
                string = "o---o"
            else:
                string = "o   o"
            stdscr.addstr(i * 2, j * 4, string)

            if cell.left:
                string = "|"
            else:
                string = " "
            stdscr.addstr(i * 2 + 1, j * 4, string)

            if cell.backtracked:
                col = curses.color_pair(3)
            elif cell.visited:
                col = curses.color_pair(2)
            else:
                col = curses.color_pair(1)

            stdscr.addstr(i * 2 + 1, j * 4 + 1, "   ", col)

            if cell.right:
                string = "|"
            else:
                string = " "
            stdscr.addstr(i * 2 + 1, j * 4 + 4, string)

            if cell.bottom:
                string = "o---o"
            else:
                string = "o   o"
            stdscr.addstr(i * 2 + 2, j * 4, string)

            if cell.start:
                stdscr.addstr(i * 2 + 1, j * 4 + 2, "S", col)
            elif cell.end:
                stdscr.addstr(i * 2 + 1, j * 4 + 2, "G", col)
    stdscr.refresh()

def draw_final_path(stdscr, maze):
    """Draw the path without backtracks"""
    cur_r, cur_c = find_start(maze)
    path = [(cur_r, cur_c)]
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLUE)
    while not maze[cur_r][cur_c].end:
        stdscr.addstr(cur_r * 2 + 1, cur_c * 4 + 1, "   ", curses.color_pair(4))
        # find next unvisited cell in direction of end (center)
        cur = maze[cur_r][cur_c]
        if cur.end:
            break
        best_way = None
        best_dist = 100000
        # check UP
        if not cur.top and cur_r > 0 and (cur_r - 1, cur_c) not in path:
            c = maze[cur_r - 1][cur_c]
            if c.visited and not c.backtracked and (d := distance(cur_r - 1, cur_c)) < best_dist:
                best_way = cur_r - 1, cur_c
                best_dist = d

        # check RIGHT
        if not cur.right and cur_c < 15 and (cur_r, cur_c + 1) not in path:
            c = maze[cur_r][cur_c + 1]
            if c.visited and not c.backtracked and (d := distance(cur_r, cur_c + 1)) < best_dist:
                best_way = cur_r, cur_c + 1
                best_dist = d

        # check DOWN
        if not cur.bottom and cur_r < 15 and (cur_r + 1, cur_c) not in path:
            c = maze[cur_r + 1][cur_c]
            if c.visited and not c.backtracked and (d := distance(cur_r + 1, cur_c)) < best_dist:
                best_way = cur_r + 1, cur_c
                best_dist = d

        # check LEFT
        if not cur.left and cur_c > 0 and (cur_r, cur_c - 1) not in path:
            c = maze[cur_r][cur_c - 1]
            if c.visited and not c.backtracked and (d := distance(cur_r, cur_c - 1)) < best_dist:
                best_way = cur_r, cur_c - 1
                best_dist = d
        
        path.append(best_way)
        if best_way is not None:
            cur_r, cur_c = best_way
        else:
            break


def find_start(maze: list[list[Cell]]) -> tuple[int, int]:
    """Find the position of the start cell"""
    for i, row in enumerate(maze):
        for j, cell in enumerate(row):
            if cell.start:
                return i, j