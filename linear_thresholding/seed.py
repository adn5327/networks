import random


def random_seed(size, num_nodes):
    actives = set(random.sample(range(0, num_nodes), size))
    return actives

def closeness_seed():
    pass

def degree_seed():
    pass
