import curses

from floodfill import floodfill
from parse import parse



# Put path to a maze file here
# the file should not have any extra lines or whitespace otherwise something might(?) not work properly

MAZE = "mazes/maze3.txt"



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

    with open(MAZE) as f:
        maze = parse(f.readlines())
    floodfill(maze, stdscr)
    stdscr.getch()


curses.wrapper(main)