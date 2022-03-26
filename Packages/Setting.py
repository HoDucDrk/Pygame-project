import numpy as np

WIDTH = 1200
HEIGH = 675
FPS = 60
TILESIZE = 48

def load_map(path):
    return np.genfromtxt(path, delimiter=',', dtype=np.int32)
