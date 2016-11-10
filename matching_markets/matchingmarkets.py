import csv
import sys
import time

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

from collections import deque
from networkx.algorithms import bipartite

NUM_HOMES = 100
PRICE = 'price'
BUYER = 'buyer'


def createGraph():
    B = nx.Graph()
    setupSellers(B)
    setupBuyers(B)
    return B
    
def setupSellers(B):
    #setup the nodes for the sellers 
    for i in range(NUM_HOMES):
        B.add_node(i, bipartite=0)
        B.node[i][PRICE] = 0
    # print(B.nodes(data=True))

def setupBuyers(B):
    #setup the nodes for the buyers
    with open('preference.csv', 'r') as csvfile:
        csvread = csv.reader(csvfile)
        for row in csvread:
            B.add_node(row[0], bipartite=1)
            for i in range(1,NUM_HOMES+1):
                B.add_edge(row[0], i-1, weight=int(row[i]))
            # print(','.join(row))
        # print(bipartite.sets(B))

def preferredSellerGraph(B,potential_energy):
    preferred_graph =  nx.Graph()
    cur_potential = 0
    for i in range(NUM_HOMES):
        preferred_graph.add_node(i, bipartite=0)
        preferred_graph.add_node(BUYER+str(i),bipartite=1)
    for i in range(NUM_HOMES):
        max_payoff = 0
        # cur_node = B.node[BUYER.join(str(i))]
        for dest_node, edge_info in B.edge[BUYER+ str(i)].items():
            cur_payoff = edge_info['weight'] - B.node[dest_node][PRICE]
            if  cur_payoff > max_payoff:
                max_payoff = cur_payoff
        cur_potential += max_payoff
        for dest_node, edge_info in B.edge[BUYER+str(i)].items():
            cur_payoff = edge_info['weight'] - B.node[dest_node][PRICE]
            if cur_payoff == max_payoff:
                preferred_graph.add_edge(BUYER+str(i), dest_node)
    for i in range(NUM_HOMES):
        cur_potential += B.node[i][PRICE]
    potential_energy.append(cur_potential)
    return preferred_graph

def findConstrictedSet(preferred_graph, max_match):
    start_pt = findNodeNotInMatch(preferred_graph, max_match)
    homes = []
    buyers = [start_pt]
    queue = deque([start_pt])
    # print(start_pt)
    bfs = nx.Graph()
    while len(queue) >0:
        cur_pt = queue.popleft()
        bfs.add_node(cur_pt)
        for key, val in preferred_graph.edge[cur_pt].items():
            if key not in bfs.node:
                if BUYER in str(key):
                    # only add if edge from cur_pt to key
                    # is in the max_match
                    if max_match[cur_pt] == key:
                        buyers.append(key)
                        bfs.add_node(key)
                        bfs.add_edge(cur_pt,key)
                        queue.append(key)
                else:
                    bfs.add_node(key)
                    bfs.add_edge(cur_pt, key)
                    queue.append(key)
                    homes.append(key)
    # print('\nconstricted')
    # print(start_pt)
    # print(homes)
    # print(len(homes))
    # print(buyers)
    # print(len(buyers))
    # print('-------\n')
    # construct BFS as a new graph
    # the neighbors are all the nodes that dont have buyer in it
    # traverse through all the nodes, and add all the homes to a list
    # never add a node twice
    return (buyers,homes) 

def findNodeNotInMatch(preferred_graph, max_match):
    for i in range(NUM_HOMES):
        if BUYER+str(i) not in max_match:
            return BUYER+str(i)

def maximalMatch(graph):
    match = bipartite.maximum_matching(graph)
    return match

def isMatchPerfect(graph,match):
    return len(match) == len(graph.node)
    
def reducePrices(B):
    min_price = sys.maxsize
    for i in range(NUM_HOMES):
        if B.node[i][PRICE] < min_price:
            min_price = B.node[i][PRICE]
    for i in range(NUM_HOMES):
        B.node[i][PRICE] -= min_price

def increasePrices(B,toIncrease):
    for each in toIncrease:
        B.node[each][PRICE] +=1

def plot(iterations, potential_energy):
    plt.plot(iterations, potential_energy)
    plt.title('Number of Iterations and Potential Energy of the Market')
    plt.xlabel('Iteration Number')
    plt.ylabel('Potential Energy')
    plt.show()

def market_clearing():
    B = createGraph()
    iterations = []
    potential_energy = []
    for i in range(100):
        iterations.append(i+1)
        preferred_sellers = preferredSellerGraph(B,potential_energy)
        max_match = maximalMatch(preferred_sellers)
        # print(max_match)
        # print(len(max_match))
        if isMatchPerfect(preferred_sellers, max_match):
            print('yay done')
            with open('market-clearing-{}.csv'.format(int(time.time())), 'w') as csvfile:
                writer = csv.writer(csvfile)
                # for i in range(NUM_HOMES):
                #     writer.writerow(['house'+str(i) , str(B.node[i]['price'])])
                for key,value in max_match.items():
                    if 'buyer' in str(key):
                        writer.writerow([key, 'house'+str(value), B.edge[key][value]['weight'] - B.node[value][PRICE]])
            plot(iterations, potential_energy)
            print(iterations)
            print(potential_energy)
            return
        constricted = findConstrictedSet(preferred_sellers,max_match)
        increasePrices(B,constricted[1])
        # print(B.nodes(data=True))
        reducePrices(B)
    
if __name__ == "__main__":
    market_clearing()
    # increasePrices(B, [0,1,2,3])
