from cell import Cell

import curses
import math
import time


def floodfill(maze: list[list[Cell]], stdscr, delay=0.1) -> None:
    """Simulate the floodfill algo on a maze"""
    # move toward end of maze in next square that hasn't been covered
    # if blocked on all size, backtrack until reached new path
    # backtrack by going reverse of the direction by which the cell was reached
    # indicate if a cell has been backtracked
    cur_r, cur_c = find_start(maze)
    maze[cur_r][cur_c].visited = True

    draw_maze(stdscr, maze)
    time.sleep(delay)
    while not maze[cur_r][cur_c].end:
        cur = maze[cur_r][cur_c]
        if cur.end:
            break
        # find next unvisited cell in direction of end (center)
        # if there are multiple choose closest to end
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
        # if no unvisited cell to go to
        #   backtrack and mark last cell as backtracked
        else:
            cur.backtracked = True

            # trace in reverse the way the current cell was reached
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
                return False

        draw_maze(stdscr, maze)
        time.sleep(delay)
    stdscr.refresh()
    return True


def distance(row: int, col: int) -> float:
    """find the distance to the center of the maze"""
    return math.sqrt((row - 7.5) ** 2 + (col - 7.5) ** 2)


def draw_maze(stdscr, maze: list[list[Cell]]) -> None:
    """Draw the maze on a curses screen"""
    for i, row in enumerate(maze):
        for j, cell in enumerate(row):
            draw_cell(stdscr, maze, i, j)
    stdscr.refresh()


def find_start(maze: list[list[Cell]]) -> tuple[int, int]:
    """Find the position of the start cell"""
    for i, row in enumerate(maze):
        for j, cell in enumerate(row):
            if cell.start:
                return i, j
            

def draw_cell(stdscr, maze: list[list[Cell]], row: int, col: int, color_override: int = None) -> None:
    """Draw a cell"""
    cell = maze[row][col]
    # upper border
    string = "█████" if cell.top else "█   █"
    color = curses.color_pair(1)
    if row > 0 and maze[row-1][col].visited:
        if cell.backtracked:
            color = curses.color_pair(3)
        elif cell.visited:
            if maze[row-1][col].backtracked:
                color = curses.color_pair(3)
            else:
                color = curses.color_pair(2)
    stdscr.addstr(row*2, col*4, string, color_override or color)

    # left border
    string = "█" if cell.left else " "
    color = curses.color_pair(1)
    if col > 0 and maze[row][col-1].visited:
        if cell.backtracked:
            color = curses.color_pair(3)
        elif cell.visited:
            if maze[row][col-1].backtracked:
                color = curses.color_pair(3)
            else:
                color = curses.color_pair(2)
    stdscr.addstr(row*2 + 1, col*4, string, color_override or color)

    # right border
    string = "█" if cell.right else " "
    color = curses.color_pair(1)
    if col < 15 and maze[row][col+1].visited:
        if cell.backtracked:
            color = curses.color_pair(3)
        elif cell.visited:
            if maze[row][col+1].backtracked:
                color = curses.color_pair(3)
            else:
                color = curses.color_pair(2)
    stdscr.addstr(row*2 + 1, col*4 + 4, string, color_override or color)

    # bottom border
    string = "█████" if cell.bottom else "█   █"
    color = curses.color_pair(1)
    if row < 15 and maze[row+1][col].visited:
        if cell.backtracked:
            color = curses.color_pair(3)
        elif cell.visited:
            if maze[row+1][col].backtracked:
                color = curses.color_pair(3)
            else:
                color = curses.color_pair(2)
    stdscr.addstr(row*2 + 2, col*4, string, color_override or color)

    # middle
    string = " S " if cell.start else " G " if cell.end else "   "
    if cell.backtracked:
        color = curses.color_pair(3)
    elif cell.visited:
        color = curses.color_pair(2)
    else:
        color = curses.color_pair(1)
    stdscr.addstr(row*2 + 1, col*4 + 1, string, color_override or color)
