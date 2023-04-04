from __future__ import annotations
from action import PaintAction
from grid import Grid

from data_structures.referential_array import ArrayR
from data_structures.queue_adt import CircularQueue

class ReplayTracker:
    MAX_ACTIONS = 10000

    def __init__(self):
        """
        Initialisation for an ReplayTracker Object. an ArrayStacks is required to keep track
        of a User's actions. Another instance variable is required to keep track if the 
        ReplayTracker object should stop taking in PaintActions and start playing them back.
        
        Best Case Complexity: O(MAX_ACTIONS)
        Worst Case Complexity: O(MAX_ACTIONS)
        """   
        self.actions = CircularQueue(ReplayTracker.MAX_ACTIONS)
        self.end = False

    def start_replay(self) -> None:
        """
        Called whenever we should stop taking actions, and start playing them back.
        Useful if you have any setup to do before `play_next_action` should be called.

        Best Case Complexity: O(1)
        Worst Case Complexity: O(1)
        """
        self.end = True

    def add_action(self, action: PaintAction, is_undo: bool=False) -> None:
        """
        Adds an action to the replay.
        `is_undo` specifies whether the action was an undo action or not.
        Special, Redo, and Draw all have this is False.
        - action: PaintAction object
        - is_undo: Boolean to indentify if a PaintAction is an undo action. Defaults to False

        Best Case Complexity: O(comp)
        Worst Case Complexity: O(comp)
        """
        # Only proceed when ReplayTracker is still taking actions (self.end=False)
        if self.end is False:
            # Create an Array of length 2 to store a PaintAction and a is_undo boolean 
            action_array = ArrayR(2)
            action_array[0] = action
            action_array[1] = is_undo

            # Append the Array to self.actions
            self.actions.append(action_array)
        else:
            raise Exception("Unable to add action during replay")

    def play_next_action(self, grid: Grid) -> bool:
        """
        Plays the next replay action on the grid.
        Returns a boolean.
            - If there were no more actions to play, and so nothing happened, return True.
            - Otherwise, return False.
        - grid: Grid object

        Best Case Complexity: O(n)
        Worst Case Complexity: O(n)

        Where n is the time complexity of the add() or erase() method used in the redo_apply()
        and undo_apply() methods respectively. These methods have different complexities based
        on different LayerStore objects
        """
        try:
            # Get the latest PaintAction and is_undo status
            action_array = self.actions.serve()
            action = action_array[0]
            is_undo = action_array[1]

            if is_undo:
                # Execute undo_apply() if is_undo
                action.undo_apply(grid)
            else:
                # Execute redo_apply() if is_undo
                action.redo_apply(grid)
            
            # Return False because there are still actions
            return False
    

        # An error will occur in the "try" section if 
        # the replay is over (No actions left)
        except:
            # Therefore, set self.end to False to allow taking
            # actions again and return True
            self.end = False
            return True

if __name__ == "__main__":
    action1 = PaintAction([], is_special=True)
    action2 = PaintAction([])

    g = Grid(Grid.DRAW_STYLE_SET, 5, 5)

    r = ReplayTracker()
    # add all actions
    r.add_action(action1)
    r.add_action(action2)
    r.add_action(action2, is_undo=True)
    # Start the replay.
    r.start_replay()
    f1 = r.play_next_action(g) # action 1, special
    f2 = r.play_next_action(g) # action 2, draw
    f3 = r.play_next_action(g) # action 2, undo
    t = r.play_next_action(g)  # True, nothing to do.
    assert (f1, f2, f3, t) == (False, False, False, True)

