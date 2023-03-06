# Floodfill Test
Test floodfill algorithm for micromouse. <br>
mazes from: https://github.com/micromouseonline/mazefiles

Run main.py in a shell that supports curses with color.
```python3 main.py [maze file path]```
- defaults to all ```./mazes``` in mazes directory


### Basic Algorithm

1. Search for directions of travel that aren't blocked by visited cells or walls
2. If there is at least one direction
   1. Move in the direction that minimizes distance to the end
   2. Mark the cell as visited from whichever direction is came from
3. If there are none you have to backtrack
   1. Follow the reverse of the direction current cell was visited from
   2. Mark cell as backtracked (not needed to solve the maze, but helps visualizing)
4. Repeat until the end is reached