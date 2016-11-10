import networkx as nx
import random
import sys
import numpy as np
import matplotlib.pyplot as plt


def is_balanced(G, nodes):
    """
    Checks if a given graph G has a balanced triad between the three nodes provided in nodes
    """
    sum = 0
    x=G.edge[nodes[0]][nodes[1]]['weight']
    sum +=x
    y=G.edge[nodes[0]][nodes[2]]['weight']
    sum +=y
    z=G.edge[nodes[1]][nodes[2]]['weight']
    sum +=z

    if sum == -1 or sum == 3:
        return True
    return False

def flip_random_sign(G, nodes):
    """
    Flips the sign of a random edge between the triad represented by nodes
    """
    e1 = random.choice(nodes)
    e2 = e1
    while e2 == e1:
        e2 = random.choice(nodes)
    G.edge[e1][e2]['weight'] *= -1

def setup_graph(num_nodes):
    """
    Sets up a complete graph with num_nodes
    """
    G = nx.complete_graph(num_nodes)
    signs = [-1,1]
    for i in range(num_nodes):
        for j in range(i+1, num_nodes):
            G.add_edge(i, j, weight=random.choice(signs))
    return G

def three_nodes(num_nodes):
    """
    Selects num_nodes nodes at random
    """
    x = []
    x.append(random.randint(0,num_nodes - 1))
    while len(x) < 3:
        next_val = random.randint(0,num_nodes - 1)
        if next_val not in x:
            x.append(next_val)
    return x

def run_algo(num_nodes=10, num_iterations=1000000, num_graphs=100, num_averages=100):
    """
    Performs the actual dynamic processes algorithm and outputs a graph
    """
    total_balances = []
    for _ in range(num_graphs):
        G = setup_graph(num_nodes)
        # nx.write_weighted_edgelist(G, sys.stdout)

        num_balanced = []
        all_true_after = False
        for i in range(num_iterations):
            if not all_true_after:
                cur_nodes = three_nodes(num_nodes)
                if not is_balanced(G, cur_nodes):
                    flip_random_sign(G, cur_nodes)
            # below is used in case you only want to take averages every X number of iterations
            if i % num_averages == 0:
                iter_num_balanced = 0
                if not all_true_after:
                    for j in range(num_nodes):
                        for k in range(j+1, num_nodes):
                            for l in range(k+1, num_nodes):
                                if is_balanced(G, [j,k,l]):
                                    iter_num_balanced += 1
                    if iter_num_balanced == 120:
                        all_true_after = True
                else:
                    iter_num_balanced = 120
                num_balanced.append(iter_num_balanced)

        total_balances.append(num_balanced)

    x_axis = []
    averages = []
    for i in range(int(num_iterations/num_averages)):
        sum_val = 0.0
        for arr in total_balances:
            sum_val += arr[i]
        averages.append((sum_val / len(total_balances))/120)
        x_axis.append(i*num_averages)

    # print(averages[0:10])
    # print(len(averages))
    # print(num_iterations/num_averages)
    # print(x_axis[0:10])
    # print(len(x_axis))

    plt.semilogx(x_axis, averages)
    plt.ylim(0.5,1.1)
    plt.ylabel('Average fraction of balanced triads')
    plt.xlabel('Iteration number, log scaled')
    plt.title('Average fraction of balanced triads per iteration for {} networks'.format(num_graphs))
    plt.show()


if __name__ == '__main__':
    run_algo(num_iterations=1000000, num_graphs=100, num_averages=1)
