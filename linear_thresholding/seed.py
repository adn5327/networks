import collections 
import queue
import random


def random_seed(thresholder, size):
    actives = set(random.sample(range(0, len(thresholder.adj_lists)), size))
    return actives


def closeness_seed(thresholder, size):
    cur_q = queue.PriorityQueue()

    for node, node_list in thresholder.adj_lists.items():
        cur_closeness = closeness(thresholder.adj_lists, node)
        cur_q.put((-1*cur_closeness, node))

    x = get_best(cur_q, size)
    return x


def closeness(adj_lists, root):
    bfs_dict = {}

    for cur_node, node_list in adj_lists.items():
        bfs_dict[cur_node] = len(adj_lists)
    
    q = queue.Queue()
    bfs_dict[root] = 0
    q.put(root)

    while not q.empty():
        cur = q.get()
        for each in adj_lists[cur]:
            if bfs_dict[each] == len(adj_lists):
                bfs_dict[each] = bfs_dict[cur] + 1
                q.put(each)
    sum = 0
    del(bfs_dict[root])
    for node, dist in bfs_dict.items():
        sum += 1.0/(dist)

    return sum


def degree_seed(thresholder, size):
    cur_q = queue.PriorityQueue()
    for node, node_list in thresholder.adj_lists.items():
        cur_q.put((-1*len(node_list), node))
    return get_best(cur_q, size)

def get_best(pq, size):
    ret_set = set()
    for i in range(size):
        x = pq.get()
        ret_set.add(x[1])
    return ret_set
