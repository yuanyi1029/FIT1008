from __future__ import annotations
from data_structures.referential_array import ArrayR
from layers import lighten
from layer_store import SetLayerStore, AdditiveLayerStore, SequenceLayerStore


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
        self.x = x 
        self.y = y

        # Initialise Draw Style
        if draw_style in self.DRAW_STYLE_OPTIONS:
            self.draw_style = draw_style
        else:
            raise ValueError("Invalid Draw Style")
        
        # Initialise Default Brush Size 
        self.brush_size = Grid.DEFAULT_BRUSH_SIZE

        # Create Grid using Referential Array
        self.grid = ArrayR(self.y)

        # Loop through y times (Numbers of rows)
        for i in range(self.y):
            # Create row of size x (Number of pixels in a row)
            row = ArrayR(self.x)
            # Loop through x times (Number of pixels), create LayerStore for each pixel
            for j in range(self.x):
                if self.draw_style == self.DRAW_STYLE_OPTIONS[0]:
                    row[j] = SetLayerStore()
                    row[j].add(lighten)
                elif self.draw_style == self.DRAW_STYLE_OPTIONS[1]:
                    row[j] = AdditiveLayerStore()
                elif self.draw_style == self.DRAW_STYLE_OPTIONS[2]:
                    row[j] = SequenceLayerStore()
            # Add each LayerStore to the row 
            self.grid[i] = row

    def __getitem__(self, index):
        """
        Magic method for a Grid object allow indexing
        to obtain a certain grid pixel 
        """
        return self.grid[index]

    def increase_brush_size(self):
        """
        Increases the size of the brush by 1,
        if the brush size is already MAX_BRUSH,
        then do nothing.
        """
        # Check if current brush size does not exceed max size
        if self.brush_size < Grid.MAX_BRUSH:
            self.brush_size += 1 

    def decrease_brush_size(self):
        """
        Decreases the size of the brush by 1,
        if the brush size is already MIN_BRUSH,
        then do nothing.
        """
        # Check if current brush size is above minimum size
        if self.brush_size > Grid.MIN_BRUSH:
            self.brush_size -= 1 

    def special(self):
        """
        Activate the special affect on all grid squares.
        """
        # Loops through each row 
        for i in range(len(self.grid)):
            # Loops through each LayerStore 
            for j in range(len(self.grid[i])):
                # Activate special() method 
                self.grid[i][j].special()
