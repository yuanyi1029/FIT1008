from __future__ import annotations
from data_structures.referential_array import ArrayR
from layer_store import SetLayerStore

class Grid:
    DRAW_STYLE_SET = "SET"
    DRAW_STYLE_ADD = "ADD"
    DRAW_STYLE_SEQUENCE = "SEQUENCE"
    DRAW_STYLE_OPTIONS = (
        DRAW_STYLE_SET,
        DRAW_STYLE_ADD,
        DRAW_STYLE_SEQUENCE
    )

    DEFAULT_BRUSH_SIZE = 2
    MAX_BRUSH = 5
    MIN_BRUSH = 0

    def __init__(self, draw_style, x, y) -> None:
        """
        Initialise the grid object.
        - draw_style:
            The style with which colours will be drawn.
            Should be one of DRAW_STYLE_OPTIONS
            This draw style determines the LayerStore used on each grid square.
        - x, y: The dimensions of the grid.

        Should also intialise the brush size to the DEFAULT provided as a class variable.
        """

        # Initialise Draw Style
        if draw_style in self.DRAW_STYLE_OPTIONS:
            self.draw_style = draw_style
        else:
            raise ValueError("Invalid Draw Style")

        # Create Grid using Referential Array
        self.grid = ArrayR(y)
        for i in range(y):
            row = ArrayR(x)
            for j in range(x):
                set_layer_store = SetLayerStore()
                row[j] = set_layer_store
            self.grid[i] = row

        # Initialise Default Brush Size 
        self.brush_size = Grid.DEFAULT_BRUSH_SIZE

    def __getitem__(self, index):
        return self.grid[index]

    def increase_brush_size(self):
        """
        Increases the size of the brush by 1,
        if the brush size is already MAX_BRUSH,
        then do nothing.
        """
        if self.brush_size < Grid.MAX_BRUSH:
            self.brush_size += 1 

    def decrease_brush_size(self):
        """
        Decreases the size of the brush by 1,
        if the brush size is already MIN_BRUSH,
        then do nothing.
        """
        if self.brush_size > Grid.MIN_BRUSH:
            self.brush_size -= 1 

    def special(self):
        """
        Activate the special affect on all grid squares.
        """
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                self.grid[i][j].special()
        # raise NotImplementedError

if __name__ == "__main__":
    grid = Grid("SET", 10, 5)
    print(grid[4][9])
#     # print(k[11])