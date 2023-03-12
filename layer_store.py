from __future__ import annotations
from abc import ABC, abstractmethod
from layer_util import Layer

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
    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
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
        self.layer = None
        self.is_special = False

    def add(self, layer: Layer) -> bool:
        try:
            self.layer = layer
            return True
        except:    
            return False
    
    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        if self.layer:
            colour_tuple = self.layer.apply(start, timestamp, x, y)

            if self.is_special:
                colour_tuple = (255-colour_tuple[0], 255-colour_tuple[1], 255-colour_tuple[2])

            return colour_tuple
        else:
            return start

    def erase(self, layer: Layer) -> bool:
        try:
            self.layer = None
            return True
        except:
            return False

    def special(self):
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

    pass

class SequenceLayerStore(LayerStore):
    """
    Sequential layer store. Each layer type is either applied / not applied, and is applied in order of index.
    - add: Ensure this layer type is applied.
    - erase: Ensure this layer type is not applied.
    - special:
        Of all currently applied layers, remove the one with median `name`.
        In the event of two layers being the median names, pick the lexicographically smaller one.
    """

    pass
