from grid import Grid
from layers import black, lighten, rainbow, invert
from layer_store import SetLayerStore

if __name__ == "__main__":
    s = SetLayerStore()
    print(s)
    b = black
    print(b)
    s.add(black)

    print(s.get_color((0, 0, 0), 0, 1, 1))
    # grid = Grid("SET", 10, 5)
    # grid[4][9].add(black)
    # print(grid[4][9])
    