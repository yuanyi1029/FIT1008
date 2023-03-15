from grid import Grid
from layers import black, lighten, rainbow, invert, red, blue, green
from layer_store import SetLayerStore, AdditiveLayerStore
from data_structures.queue_adt import CircularQueue

if __name__ == "__main__":
    ls = AdditiveLayerStore()

    ls.add(black)
    ls.add(red)
    ls.add(lighten)

    print(ls.get_color((0, 0, 0), 40, 0, 0))
    # print(list(ls.layers.array))

    # for i in range(len(ls.layers)):
    #     print(ls.layers.array[i])
    

    ls.special()

    print(ls.get_color((0, 0, 0), 40, 0, 0))
    # for i in range(len(ls.layers)):
    #     print(ls.layers.array[i])
    
