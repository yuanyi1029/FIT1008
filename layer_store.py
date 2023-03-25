from __future__ import annotations
from abc import ABC, abstractmethod
from layer_util import Layer
from data_structures.queue_adt import CircularQueue
from data_structures.stack_adt import ArrayStack
from data_structures.bset import BSet
from data_structures.array_sorted_list import ArraySortedList
from data_structures.sorted_list_adt import ListItem 
from layer_util import get_layers


class LayerStore(ABC):

    def __init__(self) -> None:
        pass

    @abstractmethod
    def add(self, layer: Layer) -> bool:
        """
        Add a layer to the store.
        Returns true if the LayerStore was actually changed.
        """
        pass

    @abstractmethod
    def get_color(self, start: tuple[int, int, int], timestamp: int, x: int, y: int) -> tuple[int, int, int]:
        """
        Returns the colour this square should show, given the current layers.
        """
        return start

    @abstractmethod
    def erase(self, layer: Layer) -> bool:
        """
        Complete the erase action with this layer
        Returns true if the LayerStore was actually changed.
        """
        pass

    @abstractmethod
    def special(self):
        """
        Special mode. Different for each store implementation.
        """
        pass

class SetLayerStore(LayerStore):
    """
    Set layer store. A single layer can be stored at a time (or nothing at all)
    - add: Set the single layer.
    - erase: Remove the single layer. Ignore what is currently selected.
    - special: Invert the colour output.

    Best Case Complexity: O(1)
    Worst Case Complexity: O(1)
    """
    def __init__(self) -> None:
        """
        Initialisation for a SetLayerStore Object. 
        """
        # self.layer stores a single layer 
        self.layer = None
        self.is_special = False

    def add(self, layer: Layer) -> bool:
        """
        Adds a layer object to self.layer of SetLayerStore, returns True
        only if a layer has been changed  
        - layer: Layer object   

        Best Case Complexity: O(1)
        Worst Case Complexity: O(1)
        """
        try:
            # Check if previous layer is same with new layer 

            if self.layer is not None and self.layer.index == layer.index:
                # Same layer - No changes (return False)
                return False
            else:
                # Different layer - Update layer (return True)
                self.layer = layer
                return True
        except:    
            return False
    
    def get_color(self, start: tuple[int, int, int], timestamp: int, x: int, y: int) -> tuple[int, int, int]:
        """
        Returns an RGB value in tuple form based on the colour of the added layer.
        If self.is_special variable is True, returns an inverted RGB value instead 
        - start: initial RGB value
        - timestamp: a point of time
        - x: x coordinate
        - y: y coordinate 

        Best Case Complexity: O(1)
        Worst Case Complexity: O(n)

        Where n is the time complexity of the apply function of a layer. Some layer's
        apply function has a slower complexity than O(1) such as the sparkle layer's 
        apply function with a complexity of O(timestamp). Newer defined layers might 
        affect the Worst Case Complexity depending on how it is implemented.
        """
        # Check self.layer, if empty then return initial colour
        if self.layer is not None:

            # Obtain colour of the layer with apply() method
            colour_tuple = self.layer.apply(start, timestamp, x, y)

            # Invert colour if special() was called, subtract from 255 (maximum colour spectrum)
            if self.is_special:
                colour_tuple = (255-colour_tuple[0], 255-colour_tuple[1], 255-colour_tuple[2])

            # Return the RGB colour as a tuple 
            return colour_tuple
        
        else:
            return start

    def erase(self, layer: Layer) -> bool:
        """
        Removes a layer object from self.layer of SetLayerStore regardless of 
        the layer object parameter
        - layer: Layer object

        Best Case Complexity: O(1)
        Worst Case Complexity: O(1)
        """
        try:
            # Set self.layer to None (empty) return True because layer was changed
            self.layer = None
            return True
        except:
            return False

    def special(self):
        """
        Toggles on or off the self.is_special variable of a SetLayerStore
        to get a special effect when using the get_color() method

        Best Case Complexity: O(1)
        Worst Case Complexity: O(1)
        """
        # Toggle self.is_special variable 
        if self.is_special:
            self.is_special = False
        else:
            self.is_special = True


class AdditiveLayerStore(LayerStore):
    """
    Additive layer store. Each added layer applies after all previous ones.
    - add: Add a new layer to be added last.
    - erase: Remove the first layer that was added. Ignore what is currently selected.
    - special: Reverse the order of current layers (first becomes last, etc.)
    """
    def __init__(self) -> None:
        """
        Initialisation for an AdditiveLayerStore Object. 

        Best Case Complexity: O(????????)
        Worst Case Complexity: O(????????)
        """        
        # self.layers stores multiple layers orderly in a queue
        self.layers = CircularQueue(20 * 100)

    def add(self, layer: Layer) -> bool:
        """
        Adds a newest layer object to the end of self.layers of AdditiveLayerStore 
        - layer: Layer object 

        Best Case Complexity: O(1)
        Worst Case Complexity: O(1)
        """        
        try:
            # Add a layer to self.layers, return True because layer was changed
            self.layers.append(layer)
            return True
        except:
            return False
    
    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        """
        Returns an RGB value in tuple form based on all colours in the layers of
        AdditiveLayerStore.
        - start: initial RGB value
        - timestamp: a point of time
        - x: x coordinate
        - y: y coordinate 

        Best Case Complexity: O(len(self.layers))
        Worst Case Complexity: O(len(self.layers))

        Best and Worst Case Complexity is O(len(self.layers)) because this method
        loops through the number of layers in self.layers times to use each 
        layer's apply() method to get the colour_tuple.  
        """

        # Get initial colour tuple
        colour_tuple = start
        
        # Loop through oldest to newest layer
        for i in range(len(self.layers)):
            # Apply each layer's colour to colour tuple
            layer = self.layers.serve()
            colour_tuple = layer.apply(colour_tuple, timestamp, x, y)
            # Add the layer back to self.layers because it was served 
            self.layers.append(layer)

        # Return the RGB colour as a tuple 
        return colour_tuple


    def erase(self, layer: Layer) -> bool:
        """
        Removes the oldest added layer object from self.layers of 
        AdditiveLayerStore regardless of the layer object parameter
        - layer: Layer object

        Best Case Complexity: O(1)
        Worst Case Complexity: O(1)
        """        
        try:
            # Serve out oldest layer, return True because layer was changed
            self.layers.serve()
            return True
        except:
            return False

    def special(self):
        """
        Inverts the layers inside the layers Queue, in which the bottom 
        layer is now the top while the top layer is now at the bottom.
        Using the get_color() method will return a different RGB value now

        Best Case Complexity: O(len(self.layers))
        Worst Case Complexity: O(len(self.layers))

        Best and Worst Case Complexity is O(len(self.layers)) because this method
        loops through the number of layers in self.layers times to use each 
        layer's apply() method to get the colour_tuple.  
        """
        # Create a temporary Stack
        stack = ArrayStack(len(self.layers))

        # Get loop count from initial length of self.layers
        loop_count = len(self.layers)

        # Loop "loop_count" times, serve out each layer and push to stack
        for i in range(loop_count):
            stack.push(self.layers.serve())

        # Loop "loop_count" times, pop the newest added layer in stakc 
        # and append to self.layers queue
        for j in range(loop_count):
            self.layers.append(stack.pop())


class SequenceLayerStore(LayerStore):
    """
    Sequential layer store. Each layer type is either applied / not applied, and is applied in order of index.
    - add: Ensure this layer type is applied.
    - erase: Ensure this layer type is not applied.
    - special:
        Of all currently applied layers, remove the one with median `name`.
        In the event of two layers being the median names, pick the lexicographically smaller one.
    """
    def __init__(self) -> None:
        """
        Initialisation for an SequentialLayerStore Object. 

        ----------------------------------- IMPORTANT -----------------------------------
        Throughout the implementation of SequentialLayerStore, the index of each layer
        will be stored by an increased number of 1 due to the fact that a 0 index exists 
        in layers.py (Stored in BSet as 1). When retrieving the index of each layer, the
        returned indexes are all deducted by 1 to obtain the real index value of each 
        layer.
        ---------------------------------------------------------------------------------
        """        
        # self.layers stores the index of multiple layers orderly in a BinarySet
        self.layers = BSet()

    def add(self, layer: Layer) -> bool:
        """
        Adds layer object to self.layers of SequentialLayerStore only if it does 
        not already exist, layers objects are sorted based on its index from lowest
        to highest 
        - layer: Layer object 
        """
        try:
            # Check if the index of a layer is already in self.layers 
            if layer.index + 1 not in self.layers:
                # Not in self.layers - Add layer index (return True)
                self.layers.add(layer.index + 1)
                return True
            else:
                # Already in self.layers - No changes (return False)
                return False 
        except:
            return False 
    
    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        """
        Returns an RGB value in tuple form based on all colours in the layers of
        SequentialLayerStore.
        - start: initial RGB value
        - timestamp: a point of time
        - x: x coordinate
        - y: y coordinate 
        """
        # Get initial colour tuple
        colour_tuple = start

        # Get all the existing layers 
        all_layers = get_layers()

        # Create a duplicate copy of the self.layers BSet
        temp = BSet()
        temp = temp.union(self.layers)

        current = 1
        # Loop until duplicate BSet is empty
        while temp:
            # Determine the layer_index by checking temp, remove from temp if found
            if current in temp:
                layer_index = current - 1 
                temp.remove(current)
                
                # Determine each layer using layer_index and apply each colour to 
                # colour tuple
                layer = all_layers[layer_index]
                colour_tuple = layer.apply(colour_tuple, timestamp, x, y)

            current += 1

        # return colour_tuple
        return colour_tuple

    def erase(self, layer: Layer) -> bool:
        """
        Removes a layer object from self.layers of SequentialLayerStore that was 
        passed as a parameter
        - layer: Layer object
        """   
        try:
            # Remove the index of a layer given from self.layers
            self.layers.remove(layer.index + 1)
            return True
        except:
            return False

    def special(self):
        """
        Deletes the median layer object in self.layers based on lexicographical
        order, in which layers are arranged based on its name and the middle 
        layer will be deleted in self.layers.
        Using the get_color() method will return a different RGB value now
        """
        # Get all the existing layers 
        all_layers = get_layers()

        # Create a duplicate copy of the self.layers BSet
        tempbset = BSet()
        tempbset = tempbset.union(self.layers)

        # Create a temporary SortedList
        templist = ArraySortedList(len(self.layers))
        
        current = 1
        # Loop until duplicate BSet is empty
        while tempbset:
            # Determine the layer_index by checking tempbset, 
            # remove from tempbset if found
            if current in tempbset:
                layer_index = current - 1 
                tempbset.remove(current)

                # Determine each layer from layer_index and create a ListItem using
                # layer name as key, add it to templist
                layer = all_layers[layer_index]
                layer_list_item = ListItem(layer, layer.name)
                templist.add(layer_list_item)
                
            current += 1

        # Calculate the median value 
        median = (len(self.layers) - 1) // 2

        try:
            # Get index value from the median of templist, remove from self.layers
            index_to_delete = templist[median].value.index
            self.layers.remove(index_to_delete + 1)

        except:
            pass
