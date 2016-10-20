import sys
import pickle
from datetime import datetime
from ripe.atlas.cousteau import (
    Traceroute,
    AtlasSource,
    AtlasCreateRequest
)


'''
Performs UDP traceroutes to ip addresses from ddptr delegation path to nymity.ch
from a given set of exit ASes (exit ASes that have connected probes in RIPE)

    Usage: python prog_name exit_AS_set_pickle_file
    stdin: newline-separated IP addresses to go to
    stdout: is_success and measurement IDs
'''


def create_measurement(tr_list, source_list):
    ATLAS_API_KEY = "e2bb393f-b198-4bd0-96e3-fb5a5bc7fa22"
    atlas_request = AtlasCreateRequest(
        start_time=datetime.utcnow(),
        key=ATLAS_API_KEY,
        measurements=tr_list,
        sources=source_list,
        is_oneoff=True
    )
    (is_success, response) = atlas_request.create()
    
    print is_success
    print response


def main():
    # Handle command-line arguments
    exit_as_set_pickle_fname = sys.argv[1]


    with open(exit_as_set_pickle_fname, 'rb') as f:
        exit_as_set = pickle.load(f)

    source_list = []    
    for asn in exit_as_set:

        source = AtlasSource(
            type='asn',
            value='AS' + str(asn),
            requested=1
        )
        source_list.append(source)

    #print len(source_list)
    #print len(exit_as_set)
    #exit()

    the_port = 53
    tr_list = []

    for ip_line in sys.stdin:
        the_ip = ip_line.rstrip()
        
        traceroute = Traceroute(
            target=the_ip,
            af=4,
            timeout=4000,
            description='UDP Traceroute from exit ASes to ' + the_ip,
            protocol='UDP',
            resolve_on_probe=False,
            packets=3,
            size=48,
            first_hop=1,
            max_hops=32,
            port=the_port,
            paris=16,
            destination_option_size=0,
            hop_by_hop_option_size=0,
            dont_fragment=False,
            skip_dns_check=False
        )
    
        tr_list.append(traceroute)

    #print tr_list
    
    create_measurement(tr_list, source_list)
            
    
if __name__ == '__main__':
    main()
