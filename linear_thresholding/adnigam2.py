import sys
import threshold

if __name__ == "__main__":
    if len(sys.argv) == 1:
        thresholder = threshold.LinearThresholding()
        thresholder.runall()
    elif len(sys.argv) == 2:
        thresholder = threshold.LinearThresholding(sys.argv[1])
        thresholder.runall_print()
    else:
        print('USAGE:')
        print('python adnigam2.py -- default')
        print('python adnigam2.py <filename> -- for different network file')
