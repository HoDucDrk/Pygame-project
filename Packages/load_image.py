from os import walk 

def load_image(path):
    name = ''
    for _, _, names in walk(path):
        name = names
    return name
