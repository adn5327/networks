import numpy as np
import matplotlib.pyplot as plt

import graph
import seed


class LinearThresholding():
    def __init__(self, network_fname='network.txt', theta_fname='theta.txt'):
        self.setup(network_fname, theta_fname)
        pass

    def onealgo(self, func):
        totals = []
        for each in self.seed_sizes:
            num = self.call(func, each)
            totals.append(num)
        return totals
    
    def call(self, func, initial_set_size):
        seed_set = func(initial_set_size, len(self.adj_lists))
        num = self.threshold(seed_set)
        return num

    def setup(self, network_fname, theta_fname):
        self.adj_lists = graph.setup_graph(network_fname)
        self.theta_vals = graph.setup_thetas(theta_fname)
        self.seed_sizes = [5, 10, 20, 25, 30]

    def threshold(self, seed_set, num_steps=1000):
        for i in range(1, num_steps):
            new_actives = set()

            for node, node_list in self.adj_lists.items():
                if node not in seed_set:
                    total_neighbors = len(node_list)
                    total_active_neighbors = 0.
                    for each in node_list:
                        if each in seed_set:
                            total_active_neighbors += 1
                    if total_active_neighbors/total_neighbors >= self.theta_vals[node]:
                        new_actives.add(node)

            seed_set.update(new_actives)
        return len(seed_set)

    def runall(self):
        random_totals = self.onealgo(seed.random_seed)
        degree_totals = self.onealgo(seed.degree_seed)
        closeness_totals = self.onealg(seed.closeness_seed)

    def runall_print(self, seed_set_size=20):
        random_num = self.call(seed.random_seed, seed_set_size)
        degree_num = self.call(seed.degree_seed, seed_set_size)
        closeness_num = self.call(seed.closeness_seed, seed_set_size)
        print('RANDOM: {}'.format(random_num))
        print('DEGREE CENTRALITY: {}'.format(degree_num))
        print('CLOSENESS CENTRALITY: {}'.format(closeness_num))



if __name__ == "__main__":
    thresholder = LinearThresholding()
    random_totals = thresholder.onealgo(seed.random_seed)
    print(random_totals)