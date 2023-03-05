from cell import Cell
from parse import parse

import curses
import math
import time


def floodfill(maze: list[list[Cell]], stdscr, delay=0.1) -> None:
    """Simulate the floodfill algo on a maze"""
    # TODO: figure out how to handle loops in the maze

    # move toward end of maze in next square that hasn't been covered
    # if blocked on all size, backtrack until reached new path
    # indicate backtracked with a double mark on the square
    cur_r = 0
    cur_c = 0
    for i, row in enumerate(maze):
        for j, cell in enumerate(row):
            if cell.start:
                cur_r = i
                cur_c = j
                break
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

        # check RIGHT
        if not cur.right and cur_c < 15:
            c = maze[cur_r][cur_c + 1]
            if not c.visited and (d := distance(cur_r, cur_c + 1)) < best_dist:
                best_way = cur_r, cur_c + 1
                best_dist = d

        # check DOWN
        if not cur.bottom and cur_r < 15:
            c = maze[cur_r + 1][cur_c]
            if not c.visited and (d := distance(cur_r + 1, cur_c)) < best_dist:
                best_way = cur_r + 1, cur_c
                best_dist = d

        # check LEFT
        if not cur.left and cur_c > 0:
            c = maze[cur_r][cur_c - 1]
            if not c.visited and (d := distance(cur_r, cur_c - 1)) < best_dist:
                best_way = cur_r, cur_c - 1
                best_dist = d
        
        # move to that cell mark cell visited
        if best_way is not None:
            cur_r, cur_c = best_way
            maze[cur_r][cur_c].visited = True
        else:
            # if no unvisited cell to go to
            #   backtrack and mark last cell backtracked
            cur.backtracked = True
            # find way to backtrack should only have one way to go back
            # check UP
            if not cur.top and not maze[cur_r - 1][cur_c].backtracked:
                cur_r, cur_c = cur_r - 1, cur_c
            # check RIGHT
            elif not cur.right and not maze[cur_r][cur_c + 1].backtracked:
                cur_r, cur_c = cur_r, cur_c + 1
            # check DOWN
            elif not cur.bottom and not maze[cur_r + 1][cur_c].backtracked:
                cur_r, cur_c = cur_r + 1, cur_c
            # check LEFT
            elif not cur.left and not maze[cur_r][cur_c - 1].backtracked:
                cur_r, cur_c = cur_r, cur_c - 1
            else:
                # got stuck ig
                print("got stuck")
                print(cur_r, cur_c, cur)
                break

        draw_maze(stdscr, maze)
        time.sleep(delay)


def distance(row, col) -> float:
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
