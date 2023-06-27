from __future__ import annotations
from dataclasses import dataclass
from mountain import Mountain
from typing import TYPE_CHECKING, Union
from data_structures.linked_stack import LinkedStack

# Avoid circular imports for typing.
if TYPE_CHECKING:
    from personality import WalkerPersonality


@dataclass
class TrailSplit:
    """
    A split in the trail.

       ___path_top____
      /               \
    -<                 >-path_follow-
      \__path_bottom__/
    """

    path_top: Trail
    path_bottom: Trail
    path_follow: Trail

    def remove_branch(self) -> TrailStore:
        """
        Removes the branch, should just leave the remaining following trail.

        Complexity: O(1)
        """
        return self.path_follow.store


@dataclass
class TrailSeries:
    """
    A mountain, followed by the rest of the trail

    --mountain--following--
    """

    mountain: Mountain
    following: Trail

    def remove_mountain(self) -> TrailStore:
        """
        Removes the mountain at the beginning of this series.

        Complexity: O(1)
        """
        return self.following.store

    def add_mountain_before(self, mountain: Mountain) -> TrailStore:
        """
        Adds a mountain in series before the current one.

        Arguments:
            -mountain: Mountain object

        Complexity: O(1)
        """
        return TrailSeries(mountain, Trail(self))

    def add_empty_branch_before(self) -> TrailStore:
        """
        Adds an empty branch, where the current trail store is now the following path.

        Complexity: O(1)
        """
        return TrailSplit(Trail(None), Trail(None), Trail(self))

    def add_mountain_after(self, mountain: Mountain) -> TrailStore:
        """
        Adds a mountain after the current mountain, but before the following trail.

        Arguments:
            -mountain: Mountain object

        Complexity: O(1)
        """
        return TrailSeries(self.mountain, Trail(TrailSeries(mountain, self.following)))

    def add_empty_branch_after(self) -> TrailStore:
        """
        Adds an empty branch after the current mountain, but before the following trail.

        Complexity: O(1)
        """
        return TrailSeries(self.mountain, Trail(TrailSplit(Trail(None), Trail(None), self.following)))


TrailStore = Union[TrailSplit, TrailSeries, None]


@dataclass
class Trail:
    store: TrailStore = None

    def add_mountain_before(self, mountain: Mountain) -> Trail:
        """
        Adds a mountain before everything currently in the trail.

        Arguments:
            -mountain: Mountain object

        Complexity: O(1)
        """
        return Trail(TrailSeries(mountain, self))

    def add_empty_branch_before(self) -> Trail:
        """
        Adds an empty branch before everything currently in the trail.

        Complexity: O(1)
        """
        return Trail(TrailSplit(Trail(None), Trail(None), self))

    def follow_path(self, personality: WalkerPersonality) -> None:
        """
        Follow a path and add mountains according to a personality.

        Arguments:
            -personality: Walker's personality

        Best Complexity: O(n) when there is no trail splits encountered along the trail.
        Worst Complexity: O(n*m) when there is trail splits encountered along the trail.
        where n is the number of mountains traversed, and m is the number of trail splits in the trail.
        """
        trail_split_record: LinkedStack[TrailSplit] = LinkedStack()
        current_trail_store: TrailStore = self.store

        self._traverse_trail(current_trail_store, trail_split_record, personality)  # O(n)

        # Traverse through the current_trail_store trail, adding mountains encountered along the way, as well as
        # recording down trail splits into the trail_split_record stack and selecting the appropriate branch based on
        # the walker's personality.

        while not trail_split_record.is_empty():  # O(m)
            following_trail: TrailStore = trail_split_record.pop().remove_branch()

            if following_trail is not None:
                self._traverse_trail(following_trail, trail_split_record, personality)  # O(n)

        # Traverse through the trail_split_record stack to pop out any trail splits encountered while traversing the
        # current_trail_store trail. The trail splits that are popped out of the stack are then traversed through,
        # adding mountains encountered, as well as recording down inner trail splits back into the trail_split_record
        # stack and selecting the appropriate branch based on the walker's personality.

    @staticmethod
    def _traverse_trail(trail_store: TrailStore,
                        trail_record: LinkedStack[TrailSplit] | LinkedStack[TrailStore],
                        personality: WalkerPersonality = None, mountains_list: list[Mountain] = None) -> None:
        """
        Traverse a trail, adding and recording down encountered mountains and trail splits, and if personality is
        provided, the appropriate branch will be selected depending on the walker's personality.

        Arguments:
            -trail_store: Trail Store object
            -trail_record: Stack of trail records
            -personality: Walker's personality
            -mountains_list: List of Mountain object

        Complexity: O(n)
        where n is the number of mountains traversed
        """
        while trail_store is not None:  # O(n)
            if type(trail_store) is TrailSeries:

                if personality is not None:
                    personality.add_mountain(trail_store.mountain)

                else:
                    mountains_list.append(trail_store.mountain)

                trail_store = trail_store.remove_mountain()

            # Traverse through the trail_store trail. If the trail is a series, its mountain will be added,
            # and the trail_store will then traverse to the following mountain.

            elif type(trail_store) is TrailSplit:
                if personality is not None:
                    trail_record.push(trail_store)

                    if personality.select_branch(trail_store.path_top, trail_store.path_bottom):
                        trail_store = trail_store.path_top.store

                    else:
                        trail_store = trail_store.path_bottom.store

                else:
                    trail_record.push(trail_store.path_top.store)
                    trail_record.push(trail_store.path_bottom.store)
                    trail_store = trail_store.remove_branch()

            # If the trail is split, it will be pushed into the trail_record stack so that the path_follow trail of
            # the split may be retrieved and traversed afterwards. If personality is provided, the trail_store will
            # then traverse to the following mountain by selecting the appropriate branch based on the walker's
            # personality; else the trail_store will transverse to its following trail.

    def collect_all_mountains(self) -> list[Mountain]:
        """
        Returns a list of all mountains on the trail.

        Best Complexity: O(n) when there is no trail splits encountered along the trail.
        Worst Complexity: O(n*m) when there is trail splits encountered along the trail.
        where n is the number of mountains traversed, and m is the number of trail splits in the trail.
        """
        all_mountains: list[Mountain] = []
        current_trail_store: TrailStore = self.store
        branch_record: LinkedStack[TrailStore] = LinkedStack()

        self._traverse_trail(current_trail_store, branch_record, mountains_list=all_mountains)  # O(n)

        # Traverse through the current_trail_store trail, adding mountains encountered along the way, as well as
        # recording down trail splits by path top and bottom into the branch_record stack.

        while not branch_record.is_empty():  # O(m)
            branch: TrailStore = branch_record.pop()

            self._traverse_trail(branch, branch_record, mountains_list=all_mountains)  # O(n)

        # Traverse through the branch_record stack to pop out any trail splits encountered while traversing the
        # current_trail_store trail. The trail splits that are popped out of the stack are then traversed through,
        # adding mountains encountered, as well as recording down inner trail splits by path top and bottom back into
        # the branch_record stack.

        return all_mountains

    def length_k_paths(self, k) -> list[list[Mountain]]:  # Input to this should not exceed k > 50, at most 5 branches.
        """
        Returns a list of all paths of containing exactly k mountains.
        Paths are represented as lists of mountains.

        Paths are unique if they take a different branch, even if this results in the same set of mountains.

        Arguments:
            -k: Number of mountains that should be included in the returned paths

        Complexity: O(_length_k_paths_aux)
        where _length_k_paths_aux is the complexity of the _length_k_paths_aux() method of the Trail class
        """
        current_trail_store: TrailStore = self.store

        return self._length_k_paths_aux(k, current_trail_store)  # O(_length_k_paths_aux)

    def _length_k_paths_aux(self, k: int, trail_store: TrailStore,
                            trail_split_record: LinkedStack[TrailSplit] = LinkedStack(),
                            current_path: list[Mountain] = None,
                            k_paths: list[list[Mountain]] = None) -> list[list[Mountain]]:
        """
        Auxiliary function of length_k_paths() method of the Trail class.

        Arguments:
            -k: Number of mountains that should be included in the returned paths
            -trail_split_record: Stack of trail records
            -current_path: List of current path being traversed
            -k_paths: List of lists containing all the paths of length k

        Complexity: O(n^k)
        where n is the number of mountains in the trail
        """
        if current_path is None:
            current_path: list[Mountain] = []

        if k_paths is None:
            k_paths: list[list[Mountain]] = []

        # For the first iteration of the recursion, current_path and length_k_paths are created to record the
        # mountains that were traversed and the results for the output in length_k_path.

        if trail_store is None:
            if not trail_split_record.is_empty():
                following_trail: TrailStore = trail_split_record.pop().remove_branch()

                self._length_k_paths_aux(k, following_trail, trail_split_record, current_path, k_paths)

            elif len(current_path) == k:
                k_paths.append(current_path)

        # The base case is when trail_store is None, indicating that the trail has been traversed to the end. In this
        # instance, the trail_split_record stack will be traversed through to pop out any trail splits that were
        # encountered when traversing the trail_store trail. The trail splits that have been removed from the stack
        # are then travelled through, adding any mountains that are encountered and recording down any inner trail
        # splits back into the trail_split_record stack.

        # After traversing the trail_split_record, the length of the current_path is compared to k, and if they are
        # equal, the current path is appended to the length_k_paths list.

        if type(trail_store) is TrailSplit:
            trail_split_record.push(trail_store)
            trail_split_record_copy: LinkedStack[TrailSplit] = self._copy_stack(trail_split_record)

            self._length_k_paths_aux(k, trail_store.path_top.store, trail_split_record, current_path.copy(), k_paths)
            self._length_k_paths_aux(k, trail_store.path_bottom.store, trail_split_record_copy, current_path, k_paths)

        # Traverse through the trail_store trail. If the trail is split, it will be pushed into the
        # trail_split_record stack so that, when the base case is reached afterwards, the path_follow trail of the
        # split's top path may be traversed and combined.

        # Since the trail_split_record will be empty after travelling the top of the split path, a copy of it is made
        # to be used for the bottom of the split path. Also, because a series path may have previously been traversed
        # before reaching a split, a copy of the current path will be used for the path top of the split to avoid any
        # modifications from being made to the already traversed path when passing it through the bottom of the split.

        if type(trail_store) is TrailSeries:
            current_path.append(trail_store.mountain)

            self._length_k_paths_aux(k, trail_store.remove_mountain(), trail_split_record, current_path, k_paths)

        # If the trail is a series, its mountain will be appended to the current_path list, and the trail_store will
        # then traverse to the following mountain.

        return k_paths

    @staticmethod
    def _copy_stack(stack: LinkedStack[TrailSplit]) -> LinkedStack[TrailSplit]:
        """
        Creates a copy of a stack

        Arguments:
            -stack:

        Complexity: O(n)
        where n is the number of elements in the stack to be copied
        """
        copy: LinkedStack[TrailSplit] = LinkedStack()
        temp: LinkedStack[TrailSplit] = LinkedStack()

        while not stack.is_empty():
            temp.push(stack.pop())

        # All trail splits in the stack will be popped and pushed to the temp stack, transferring all trail splits
        # from the original stack to the temp stack in the reverse order.

        while not temp.is_empty():
            trail_split: TrailSplit = temp.pop()
            stack.push(trail_split)
            copy.push(trail_split)

        # All trail splits in the temp stack will be popped and pushed back to the original and copy stack,
        # which are both empty, transferring all reverse-ordered trail splits from the temp stack to the original and
        # copy stacks, which will then be turned to the correct order.

        return copy
