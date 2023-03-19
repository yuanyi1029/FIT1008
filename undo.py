from __future__ import annotations
from action import PaintAction
from grid import Grid
from data_structures.stack_adt import ArrayStack

class UndoTracker:
    def __init__(self):
        self.actions = ArrayStack(10000)
        self.parents = ArrayStack(10000)

    def add_action(self, action: PaintAction) -> None:
        """
        Adds an action to the undo tracker.

        If your collection is already full,
        feel free to exit early and not add the action.
        """
        self.actions.push(action)

        if len(self.parents) != 0:
            self.parents.clear()

    def undo(self, grid: Grid) -> PaintAction|None:
        """
        Undo an operation, and apply the relevant action to the grid.
        If there are no actions to undo, simply do nothing.

        :return: The action that was undone, or None.
        """
        pass
        if len(self.actions) == 0:
            return None
        else:
            action = self.actions.pop()

            action.undo_apply(grid)
            self.parents.push(action)
            return action

    def redo(self, grid: Grid) -> PaintAction|None:
        """
        Redo an operation that was previously undone.
        If there are no actions to redo, simply do nothing.

        :return: The action that was redone, or None.
        """
        if len(self.parents) == 0:
            return None
        else:
            action = self.parents.pop()

            action.redo_apply(grid)
            self.actions.push(action)
            return action
