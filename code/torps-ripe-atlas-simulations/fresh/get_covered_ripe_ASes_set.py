import pickle
import sys


'''
Produces pickle file with ASes that I think RIPE covers
based on RIPE Magellan CLI --allprobes flag

Output the intersection of the two sets and pickle it

Usage: python progname as_set_pickle_fname ripe_as_set_pickle_fname covered_ases_pickle_fname
'''





def main():
    # Handle command-line args
    your_as_set_fname = sys.argv[1]
    ripe_as_set_fname = sys.argv[2]
    intersection_set_fName = sys.argv[3]
    intersection_set_fName += '.pickle'

    with open(your_as_set_fname, 'rb') as f:
        your_as_set = pickle.load(f)

    with open(ripe_as_set_fname, 'rb') as f:
        ripe_as_set = pickle.load(f)

    print 'your as set = ' + str(len(your_as_set))
    print 'ripe as set = ' + str(len(ripe_as_set))
    
    intersection_set = your_as_set & ripe_as_set
    print 'intersection set = ' + str(len(intersection_set))

    # pickle the intersection set up
    with open(intersection_set_fName, 'wb') as f:
        pickle.dump(intersection_set, f, pickle.HIGHEST_PROTOCOL)


if __name__ == '__main__':
    main()
