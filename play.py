from grid import Grid
from layers import black, lighten, rainbow, invert, red, blue, green
from layer_store import SetLayerStore, AdditiveLayerStore
from data_structures.queue_adt import CircularQueue
from data_structures.array_sorted_list import ArraySortedList
from data_structures.sorted_list_adt import SortedList, ListItem

if __name__ == "__main__":
    # print(rainbow.index)
    # print(black.index)
    # print(lighten.index)
    # print(invert.index)
    # print(red.index)
    # print(blue.index)
    # print(green.index)

    ls = ArraySortedList(10)

    item = ListItem(rainbow, rainbow.index)
    item2 = ListItem(black, black.index)
    item3 = ListItem(red, red.index)

    ls.add(item3)
    ls.add(item2)
    ls.add(item)

    print(ls)
    
