import sys
import time

import community


def timeit(func):
    def timed(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print('%r (%r, %r) %2.2f sec' %
              (func.__name__, args, kwargs, end - start))
        return result
    return timed


def main():
    print('Erdos Renyi -- Exact')
    runner('ErdosRenyi.txt', True)
    print('------------------')

    print('Erdos Renyi -- Approximate')
    runner('ErdosRenyi.txt', False)
    print('------------------')

    print('Barabassi -- Exact')
    runner('Barabasi.txt', True)
    print('------------------')

    print('Barabasi -- Approximate')
    runner('Barabasi.txt', False)
    print('------------------')
    
    print('WattsStogatz -- Exact')
    runner('WattsStrogatz.txt', True)
    print('------------------')

    print('WattsStrogatz -- Approximate')
    runner('WattsStrogatz.txt', False)
    print('------------------')


@timeit
def runner(one_graph, exact):
    x = community.CommunityDetectionGraph(one_graph, exact)
    x.girvan_newman()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if len(sys.argv) > 2:
            if sys.argv[2] == 'approximate':
                runner(sys.argv[1], False)
                sys.exit()
        runner(sys.argv[1], True)
        # runner(sys.argv[1], False)
    else:
        main()
