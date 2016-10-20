from stem.descriptor import DocumentHandler, parse_file
import stem
import sys



'''
Takes a consensus file, parses it to get the set of IP addresses of the guards and exits
and outputs two files, one with newline-separated guard IP addys and the other with
newline-separated exit IP addys

Prints out UNIQUE guard and exit ip addresses - no repeats!

Citation: https://stem.torproject.org/tutorials/examples/persisting_a_consensus.html

    Usage: python progname.py consensus_file guard_ips_fname exit_ips_fname
'''



def update_guard_and_exit_ip_sets(consensus, guard_ip_set, exit_ip_set):
    for fingerprint, relay in consensus.routers.items():
        if stem.Flag.GUARD in relay.flags:
            guard_ip_set.add(relay.address)
        if stem.Flag.EXIT in relay.flags:
            exit_ip_set.add(relay.address)


def main():
    # process command-line args
    consensus_fname = sys.argv[1]

    guard_ips_fname = sys.argv[2]
    guard_ips_fname += '.txt'
    
    exit_ips_fname = sys.argv[3]
    exit_ips_fname += '.txt'

    consensus_file = open(consensus_fname, 'rb')
    consensus = next(parse_file(
        consensus_file,
        descriptor_type = 'network-status-consensus-3 1.0',
        document_handler = DocumentHandler.DOCUMENT,))
    consensus_file.close()

    if not consensus.is_consensus:
        print 'not a consensus file'
        return

    guard_ip_set = set()
    exit_ip_set = set()

    update_guard_and_exit_ip_sets(consensus, guard_ip_set, exit_ip_set)
    
    #if stem.Flag.BADEXIT in relay.flags:
    #    print relay.nickname
    #    print relay.flags
    #print("%s: %s" % (fingerprint, relay.nickname))

    # print to output files
    with open(guard_ips_fname, 'wb') as f:
        for ip in guard_ip_set:
            f.write(ip + '\n')
    
    with open(exit_ips_fname, 'wb') as f:
        for ip in exit_ip_set:
            f.write(ip + '\n')


if __name__ == '__main__':
    main()
