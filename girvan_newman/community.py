import ast
import math
import operator
import random
import sys
import time

import networkx as nx

C = 5


class CommunityDetectionGraph:
    
    def __init__(self, filename, exact=True):
        self.graph = nx.Graph()
        self.num_edges_removed = 0
        self.graph_from_file(filename)
        self.exact = exact

    def graph_from_file(self, filename):
        with open(filename, 'r') as f:
            cur = f.readline().rstrip('\n')
            while cur:
                x = ast.literal_eval(cur)
                self.graph.add_edge(x[0], x[1])
                cur = f.readline().rstrip('\n')

    def stats(self, num_connected, cur_modularity):
        print('{}, {}, {:.9f}'.format(num_connected, self.num_edges_removed, cur_modularity))

    def remove_edge(self, i, j):
        self.graph.remove_edge(i,j)
        self.num_edges_removed +=1

    '''
    Referenced https://en.wikipedia.org/wiki/Modularity_%28networks%29 for modularity.
    '''
    def modularity(self):
        degrees = self.get_node_degrees()
        adj_mat = nx.adj_matrix(self.graph)
        m = float(len(self.graph.edges()))
        if m != self.m:
            print("NONONO {} -- {}".format(self.m, m))
        q = 0.
        list_of_lists = sorted(nx.connected_components(self.graph), key=len)
        # print(list_of_lists)
        for each in list_of_lists:
            for i in each:
                for j in each:
                    cur = adj_mat[i,j]
                    kikj = degrees[i] * degrees[j]
                    cur -= (kikj)/(2.0*m)
                    q += cur
        q = q/(2.0*m)
        return q
    
    def get_node_degrees(self):
        adj_mat = nx.adj_matrix(self.graph)
        node_list = self.graph.nodes()
        ret_dict = {}
        node_degrees = adj_mat.sum(axis=1)
        self.m = 0
        for i in range(len(node_list)):
            self.m += node_degrees[i,0]
            ret_dict[node_list[i]] = node_degrees[i,0]
        self.m /= 2
        return ret_dict
    
    '''
    Referenced http://algo.uni-konstanz.de/publications/b-fabc-01.pdf for betweenness.
    Referenced 3.6 in the Kleinberg textbook for betweenness.
    '''
    def setup_betweenness(self):
        betweenness = dict.fromkeys(self.graph, 0.0)
        betweenness.update(dict.fromkeys(self.graph.edges(), 0.0))
        return betweenness

    def exact_edge_betweenness(self):
        betweenness = self.setup_betweenness()

        for each in self.graph:
            explored, pred, sums = self.shortest_path(each)
            betweenness = self.edge_aggregate(betweenness, explored, pred, sums, each)

        self.cleanup(betweenness)

        for each in betweenness:
            betweenness[each] *= 0.5

        return betweenness

    def approx_edge_betweenness(self):
        used_set = set()
        betweenness = self.setup_betweenness()
        kcounter = dict.fromkeys(self.graph.edges(), 1.0)

        continue_flag = True 
        
        i=1
        while i < (len(self.graph.nodes())/10) and continue_flag is True:

            cur = random.randint(0,len(self.graph.nodes())-1)
            while cur in used_set:
                cur = random.randint(0,len(self.graph.nodes())-1)
            used_set.add(cur)

            explored, pred, sums = self.shortest_path(cur)
            betweenness = self.edge_aggregate(betweenness, explored, pred, sums, cur, kcounter, i)

            continue_flag = False
            # print('{} -- {}'.format(i, continue_flag))
            for key, val in betweenness.items():
                if type(key) is tuple:
                    if betweenness[key] < (C * len(self.graph.nodes())):
                        continue_flag = True 
                        # print('{} -- {} -- {}'.format(i, continue_flag, key))
                        break
            i+=1
        
        self.cleanup(betweenness)

        for each in betweenness:
            betweenness[each] *= (1.0/kcounter[each]) * len(self.graph.nodes()) * 0.5

        return betweenness
    
    def cleanup(self, betweenness):
        for n in self.graph:
            del betweenness[n]

    def shortest_path(self, s):
        explored = []
        sums= dict.fromkeys(self.graph, 0.0)    
        D = {}
        sums[s] = 1.0
        D[s] = 0
        queue = [s]

        pred = {}
        for v in self.graph:
            pred[v] = []

        while queue:   
            v = queue.pop(0)
            explored.append(v)
            for w in self.graph[v]:
                if w not in D:
                    queue.append(w)
                    D[w] = D[v] + 1
                if D[w] == D[v] + 1:   
                    sums[w] += sums[v]
                    pred[w].append(v)  
        return explored, pred, sums 

    def edge_aggregate(self, betweenness, explored, pred, sums, s, k_storer = None, cur_k = None):
        delta = dict.fromkeys(explored, 0)
        while explored:
            w = explored.pop()
            coeff = (1.0 + delta[w]) / sums[w]
            for v in pred[w]:
                c = sums[v] * coeff
                if (v, w) not in betweenness:
                    if k_storer is not None:
                        if(betweenness[(w,v)] < C * len(self.graph.nodes())):
                            betweenness[(w, v)] += c
                            k_storer[(w,v)] = cur_k
                    else:
                        betweenness[(w, v)] += c
                else:
                    if k_storer is not None:
                        if(betweenness[(v,w)] < C * len(self.graph.nodes())):
                            betweenness[(v, w)] += c
                            k_storer[(v,w)] = cur_k
                    else:
                        betweenness[(v, w)] += c
                        
                delta[v] += c
            if w != s:
                betweenness[w] += delta[w]
        return betweenness

    def girvan_newman_edge_removal(self):
        cur_connected = nx.number_connected_components(self.graph)
        num_connected = cur_connected
        while num_connected <= cur_connected:
            centrality = 0.
            if self.exact:
                centrality = self.exact_edge_betweenness()
            else:
                centrality = self.approx_edge_betweenness()
            max_node = max(centrality.items(), key=operator.itemgetter(1))[0]
            self.remove_edge(max_node[0], max_node[1])
            num_connected = nx.number_connected_components(self.graph)
        return num_connected

    def girvan_newman(self):
        self.orig_degrees = self.get_node_degrees()

        cur_mod = 0.
        num_connected = 1
        print('No of Communities, Cumulative Number of Edges Removed, Modularity')
        self.stats(num_connected, self.modularity())
        while num_connected < 5: 
            num_connected = self.girvan_newman_edge_removal()
            cur_mod = self.modularity()
            self.stats(num_connected, cur_mod)

