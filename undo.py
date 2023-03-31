from __future__ import annotations
from action import PaintAction
from grid import Grid
from data_structures.stack_adt import ArrayStack

class UndoTracker:
    MAX_ACTIONS = 10000


    def __init__(self):
        """
        Initialisation for an UndoTracker Object. 2 ArrayStacks are required to keep track
        of a User's actions. 1 ArrayStack for its history actions (self.actions) and 1 
        ArrayStack for actions that were undo'ed (self.parents) 
        
        Best Case Complexity: O(MAX_ACTIONS)
        Worst Case Complexity: O(MAX_ACTIONS)
        """        
        self.actions = ArrayStack(UndoTracker.MAX_ACTIONS)
        self.parents = ArrayStack(UndoTracker.MAX_ACTIONS)

    def add_action(self, action: PaintAction) -> None:
        """
        Adds an action to the undo tracker.
        If your collection is already full,
        feel free to exit early and not add the action.
        - action: PaintAction object

        Best Case Complexity: O(comp)
        Worst Case Complexity: O(comp)
        """
        # Push a PaintAction when to its history of actions 
        self.actions.push(action)

        # When called, clear all the undo'ed actions because a new action
        # is now a new branch, other branches should be removed
        if len(self.parents) != 0:
            self.parents.clear()

    def undo(self, grid: Grid) -> PaintAction|None:
        """
        Undo an operation, and apply the relevant action to the grid.
        If there are no actions to undo, simply do nothing.
        :return: The action that was undone, or None.
        - grid: Grid object

        Best Case Complexity: O(n)
        Worst Case Complexity: O(n)

        Where n is the time complexity of the erase() method used in the undo_apply()
        method. The erase() method has different complexities based on different 
        LayerStore objects
        """

        if len(self.actions) == 0:
            # Return None if there is no history
            return None
        else:
            # Pop the latest actions and get the action
            action = self.actions.pop()

            # Execute the undo_apply() method
            action.undo_apply(grid)
            # Push the latest actions to undo'ed actions (self.parents)
            self.parents.push(action)
            return action

    def redo(self, grid: Grid) -> PaintAction|None:
        """
        Redo an operation that was previously undone.
        If there are no actions to redo, simply do nothing.
        :return: The action that was redone, or None.
        - grid: Grid object

        Best Case Complexity: O(n)
        Worst Case Complexity: O(n)

        Where n is the time complexity of the add() method used in the redo_apply()
        method. The add() method has different complexities based on different 
        LayerStore objects
        """
        if len(self.parents) == 0:
            # Return None if there is undo'ed actions to redo
            return None
        else:
            # Pop the latest actions undo'ed action and get the action
            action = self.parents.pop()

            # Execute the redo_apply() method
            action.redo_apply(grid)
            # Push the latest actions back to history actions (self.actions)
            self.actions.push(action)
            return action
