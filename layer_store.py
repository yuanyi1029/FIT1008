from __future__ import annotations
from abc import ABC, abstractmethod
from layer_util import Layer
from data_structures.queue_adt import CircularQueue
from data_structures.stack_adt import ArrayStack
from data_structures.array_sorted_list import ArraySortedList
from data_structures.sorted_list_adt import ListItem 


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
        """
        # Check self.layer, if empty then return initial colour
        if self.layer is not None:

            # Obtain colour of the layer, invert if special() was called
            colour_tuple = self.layer.apply(start, timestamp, x, y)

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
        """        
        # self.layers stores multiple layers orderly in a queue
        self.layers = CircularQueue(20 * 100)

    def add(self, layer: Layer) -> bool:
        """
        Adds a newest layer object to the end of self.layers of AdditiveLayerStore 
        - layer: Layer object 
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
        """

        # Get initial colour tuple
        colour_tuple = start
        
        # Loop through oldest to newest layer
        for i in range(len(self.layers)):
            # Apply each layer's colour to colour tuple
            layer = self.layers.serve()
            colour_tuple = layer.apply(colour_tuple, timestamp, x, y)
            self.layers.append(layer)

        # Return the RGB colour as a tuple 
        return colour_tuple


    def erase(self, layer: Layer) -> bool:
        """
        Removes the oldest added layer object from self.layers of 
        AdditiveLayerStore regardless of the layer object parameter
        - layer: Layer object
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
        """
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
        """        
        # self.layers stores multiple layers orderly in a SortedList based on index
        self.layers = ArraySortedList(20 * 100)

    def add(self, layer: Layer) -> bool:
        """
        Adds layer object to self.layers of SequentialLayerStore only if it does 
        not already exist, layers objects are sorted based on its index from lowest
        to highest 
        - layer: Layer object 
        """       
        try:
            # Create a ListItem for the sorted list
            item = ListItem(layer, layer.index)

            # Check if the ListItem is already in self layers 
            if item not in self.layers:
                # Not in self.layers - Add layer (return True)
                self.layers.add(item)
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

        # Loop through self.layers from smallest to largest index
        for i in range(len(self.layers)):
            # Apply each layer's colour to colour tuple
            layer = self.layers[i].value
            colour_tuple = layer.apply(colour_tuple, timestamp, x, y)

        # Return the RGB colour as a tuple 
        return colour_tuple

    def erase(self, layer: Layer) -> bool:
        """
        Removes a layer object from self.layers of SequentialLayerStore that was 
        passed as a parameter
        - layer: Layer object
        """   
        try:
            # Create a temporary ListItem, gets its index in self.layers and delete it 
            self.layers.delete_at_index(self.layers.index(ListItem(layer, layer.index)))
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

        # Create a temporary SortedList
        temp = ArraySortedList(len(self.layers))

        # Loop through self.layers, create ListItem but use layer name as a key, 
        # add it to the temporary Sorted List
        for i in range(len(self.layers)):
            temp_layer = ListItem(self.layers[i].value, self.layers[i].value.name)
            temp.add(temp_layer)

        # Calculate the median value 
        median = (len(self.layers) - 1) // 2

        # Get the median layer, create a ListItem for it, find it in self.layers 
        # and delete it
        try:
            item_to_delete = ListItem(temp[median].value, temp[median].value.index)
            self.layers.remove(item_to_delete)

        except:
            pass
    

            