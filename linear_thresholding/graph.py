import csv


def setup_graph(fname):
    adj_list = {}
    with open(fname, 'r') as f:
        reader = csv.reader(f, delimiter='\t')
        for row in reader:
            src = int(row[0])
            dest = int(row[1])
            new_edge(adj_list, src, dest)
    return adj_list


def new_edge(adj_list, src, dest):
    if src not in adj_list:
        adj_list[src] = set() 
    if dest not in adj_list:
        adj_list[dest] = set() 
    adj_list[src].add(dest)
    adj_list[dest].add(src)


def setup_thetas(fname):
    theta_list = {}
    with open(fname, 'r') as f:
        reader = csv.reader(f, delimiter='\t')
        for row in reader:
            theta_list[int(row[0])] = float(row[1])
    return theta_list
