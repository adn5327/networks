import numpy as np
import matplotlib.pyplot as plt

import graph
import seed

NUM_RANDOM_ITERATIONS = 1000


class LinearThresholding():
    def __init__(self, network_fname='network.txt', theta_fname='theta.txt'):
        self.setup(network_fname, theta_fname)
        pass

    def onealgo(self, func):
        totals = []
        for each in self.seed_sizes:
            num = self.call(func, each)
            totals.append(num)
        return np.array(totals)

    def call(self, func, initial_set_size):
        seed_set = func(self, initial_set_size)
        num = self.threshold(seed_set)
        return num

    def setup(self, network_fname, theta_fname):
        self.adj_lists = graph.setup_graph(network_fname)
        self.theta_vals = graph.setup_thetas(theta_fname)
        self.seed_sizes = np.array([5, 10, 20, 25, 30])

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
            if not new_actives:
                break

            seed_set.update(new_actives)
        return len(seed_set)

    def runall(self):
        random_totals = np.zeros(len(self.seed_sizes))
        for i in range(NUM_RANDOM_ITERATIONS):
            cur_random_totals = self.onealgo(seed.random_seed)
            for j in range(len(cur_random_totals)):
                random_totals[j] += cur_random_totals[j]
        random_totals[:] = [ x/NUM_RANDOM_ITERATIONS for x in random_totals] 
        degree_totals = self.onealgo(seed.degree_seed)
        closeness_totals = self.onealgo(seed.closeness_seed)
        print(random_totals)
        print(degree_totals)
        print(closeness_totals)
        plt.plot(self.seed_sizes, random_totals, label='random')
        plt.plot(self.seed_sizes, degree_totals, label='degree centrality')
        plt.plot(self.seed_sizes, closeness_totals, label='closeness centrality')
        plt.xlabel('size of initial seed set')
        plt.ylabel('num nodes active after 1000 time steps')
        plt.legend(loc='best')
        plt.savefig('influence-result.png')

    def runall_print(self, seed_set_size=20):
        random_num_avg = 0.
        for i in range(NUM_RANDOM_ITERATIONS):
            random_num_avg += self.call(seed.random_seed, seed_set_size)
        random_num_avg = random_num_avg/NUM_RANDOM_ITERATIONS
        degree_num = self.call(seed.degree_seed, seed_set_size)
        closeness_num = self.call(seed.closeness_seed, seed_set_size)
        print('RANDOM: {}'.format(random_num_avg))
        print('DEGREE CENTRALITY: {}'.format(degree_num))
        print('CLOSENESS CENTRALITY: {}'.format(closeness_num))


if __name__ == "__main__":
    thresholder = LinearThresholding()
    random_totals = thresholder.onealgo(seed.closeness_seed)
    print(random_totals)
