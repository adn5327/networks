import random
import queue


def random_seed(thresholder, size):
    actives = set(random.sample(range(0, len(thresholder.adj_lists)), size))
    return actives


def closeness_seed():
    pass


def degree_seed(thresholder, size):
    cur_q = queue.PriorityQueue()
    for node, node_list in thresholder.adj_lists.items():
        cur_q.put((-1*len(node_list), node))
    ret_set = set()
    for i in range(size):
        x = cur_q.get()
        ret_set.add(x[1])
    return ret_set
        
