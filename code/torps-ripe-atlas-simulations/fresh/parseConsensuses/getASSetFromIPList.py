import sys
import pyasn
import pickle


'''
Returns set of ASes as ints in pickle file from input file of IP addresses
using pyasn

    Usage: python progname out_pickle_file_name pyasn_database
    stdin: file of newline separated IP addresses
'''


def main():
    # process command-line args
    as_set_fname = sys.argv[1]
    as_set_fname += '.pickle'
    
    asndb_file_name = sys.argv[2]
    asndb = pyasn.pyasn(asndb_file_name)

    as_set = set()

    for ip_line in sys.stdin:
        ip = ip_line.rstrip()
        
        # convert to AS and add ASes to set
        (asn, prefix) = asndb.lookup(ip)
        if asn is not None:
            as_set.add(asn)
        else:
            print ip
            print 'ASN not found'

    # pickle the AS set
    with open(as_set_fname, 'wb') as f:
        pickle.dump(as_set, f, pickle.HIGHEST_PROTOCOL)

    print as_set
    print 'number of unique ASes = ' + str(len(as_set))


if __name__ == '__main__':
    main()
