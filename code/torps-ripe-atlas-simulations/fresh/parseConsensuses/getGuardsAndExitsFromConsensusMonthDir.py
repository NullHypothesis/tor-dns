from stem.descriptor import DocumentHandler, parse_file
import sys
import os
from getGuardsAndExistsFromConsensusFile import update_guard_and_exit_ip_sets


'''
Takes a consensus month dir, parses all the consensus files in it 
to get the set of IP addresses of the guards and exits
and outputs two files, one with newline-separated guard IP addys and the other with
newline-separated exit IP addys for the month

Prints out UNIQUE guard and exit ip addresses - no repeats!

Citation: https://stem.torproject.org/tutorials/examples/persisting_a_consensus.html

    Usage: python progname.py consensus_month_dir guard_ips_fname exit_ips_fname
'''


def loop_through_all_files(root_str, con_files_list, guard_ip_set, exit_ip_set):
    for consensus_fname in con_files_list:
        consensus_file = open(root_str + os.path.sep + consensus_fname, 'rb')
        consensus = next(parse_file(
            consensus_file,
            descriptor_type = 'network-status-consensus-3 1.0',
            document_handler = DocumentHandler.DOCUMENT,))
        consensus_file.close()

        if not consensus.is_consensus:
            print 'not a consensus file'
        else:
            update_guard_and_exit_ip_sets(consensus, guard_ip_set, exit_ip_set)


def main():
    # process command-line args
    consensus_dirname = sys.argv[1]

    guard_ips_fname = sys.argv[2]
    guard_ips_fname += '.txt'
    
    exit_ips_fname = sys.argv[3]
    exit_ips_fname += '.txt'

    guard_ip_set = set()
    exit_ip_set = set()

    # loop through all the files in the dir
    for root_str, dirs, files_list in os.walk(consensus_dirname):
        loop_through_all_files(root_str, files_list, guard_ip_set, exit_ip_set)
    
    # print to output files
    with open(guard_ips_fname, 'wb') as f:
        for ip in guard_ip_set:
            f.write(ip + '\n')
    
    with open(exit_ips_fname, 'wb') as f:
        for ip in exit_ip_set:
            f.write(ip + '\n')


if __name__ == '__main__':
    main()
