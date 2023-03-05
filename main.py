import curses
import os
import time

from floodfill import floodfill
from parse import parse



# mazes directory should only have maze files otherwise chaos ensues

DELAY = 0.02



def main(stdscr):
    if curses.LINES < 34:
        stdscr.addstr(0, 0, "Increase the height of the shell to display the maze")
        stdscr.addstr(1, 0, "Press any key to continue...")
        stdscr.refresh()
        stdscr.getch()
        return
    if curses.COLS < 66:
        stdscr.addstr(0, 0, "Increase the width of the shell to display the maze")
        stdscr.addstr(1, 0, "Press any key to continue...")
        stdscr.refresh()
        stdscr.getch()
        return
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_GREEN)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_RED)

    for maze in os.listdir("mazes"):
        with open(f"mazes/{maze}") as f:
            maze = parse(f.readlines())
        floodfill(maze, stdscr, DELAY)
        time.sleep(1)
    stdscr.addstr(0, 67, "DONE")
    stdscr.getch()


curses.wrapper(main)