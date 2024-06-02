import json

def load_level(filename):
    with open(filename, 'r') as file:
        world_data = json.load(file)
    return world_data