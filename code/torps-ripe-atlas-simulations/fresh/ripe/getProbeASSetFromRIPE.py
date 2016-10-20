import sys
import pickle


'''
Outputs pickle file with set of Asn_v4 (maybe) ASes as ints for probes in RIPE Atlas
For use in making measurements that don't error out
Skip the ABANDONED ones!
Revision: Only count the CONNECTED ones!

    Usage: python progname ripe_probe_as_set_fname
    stdin: text file dump from  ~/.local/bin/ripe-atlas probe-search --all > allprobes.txt
'''


def main():
    # process command-line args
    as_set_fname = sys.argv[1]
    as_set_fname += '.pickle'
    
    as_set = set()

    # get in position for regular lines by getting rid of first few lines
    for line in sys.stdin:
        if line.rstrip() == '===========================================':
            #print 'start'
            break

    for line in sys.stdin:
        l = line.rstrip()
        if l == '===========================================':
            #print 'end'
            break

        # dealing with regular line
        line_list = l.split()
        
        # if the word "Abandoned" appears in the list, skip it
        if 'Connected' in line_list:
            # *sigh* get the [1] element, see if it's an int
            # if it is an int, add it to as_set
            # I'm assuming there IS an [1] element
            potential_asn = line_list[1]
            if potential_asn.isdigit():
                as_set.add(int(potential_asn))    

    # pickle the AS set
    with open(as_set_fname, 'wb') as f:
        pickle.dump(as_set, f, pickle.HIGHEST_PROTOCOL)

    print as_set
    print 'number of unique ASes = ' + str(len(as_set))


if __name__ == '__main__':
    main()
