import dataclasses


@dataclasses.dataclass
class Cell:
    """A maze cell that stores whether there are walls in the 4 directions
    Also stores whether it is the start or end of the"""
    top: bool
    right: bool
    bottom: bool
    left: bool
    start: bool = False
    end: bool = False
    visited: bool = False
    backtracked: bool = False