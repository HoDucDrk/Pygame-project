import numpy as np

WIDTH = 1200
HEIGH = 675
FPS = 60
TILESIZE = 48

def load_map(path):
    return np.genfromtxt(path, delimiter=',', dtype=np.int32)

weapons_data = {
    'spear': {'cooldown': 100, 'damage': 15, 'graphic': '../Assets/Player/weapons/Frame/spear/'},
    'bow': {'cooldown': 400, 'damage': 10, 'graphic': '../Assets/Player/weapons/Frame/bow/'}
}
