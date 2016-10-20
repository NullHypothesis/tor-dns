import sys
import time
from datetime import datetime
from ripe.atlas.cousteau import (
    Traceroute,
    AtlasSource,
    AtlasCreateRequest
)


'''
Performs UDP traceroutes 
to a given set of IP addresses from client five, new client ASes

    Usage: python prog_name
    stdin: ip_address_text_file
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
    our_as_with_own_probe = '7922'
    client_as_list = ('42610', '3320', '3215') # '2856')

    source_list = []

    # add Philipp's probe as a source
    source = AtlasSource(
        type="probes",
        value='11090',
        requested=1
    )
    source_list.append(source)

    # add British one separate for AS 2856
    # because the one it uses doesn't work
    source = AtlasSource(
        type="probes",
        value='14274',
        requested=1
    )
    source_list.append(source)

    # the rest
    for cli_as in client_as_list:
        source = AtlasSource(
            type="asn",
            value="AS" + cli_as,
            requested=1
        )
        source_list.append(source)


    tor_default_port = 9001 # useless now because not doing TCP traceroutes anymore
    limit = 85
    
    tr_list = []
    count = 0
    
    # Need to do traceroutes to all IPs
    for ip_line in sys.stdin:
        ip_str = ip_line.rstrip()

        traceroute = Traceroute(
            target=ip_str,
            af=4,
            timeout=4000,
            description='Traceroute from client AS to ' + ip_str,
            protocol="UDP",
            resolve_on_probe=False,
            packets=3,
            size=48,
            first_hop=1,
            max_hops=32,
            port=tor_default_port,
            paris=16,
            destination_option_size=0,
            hop_by_hop_option_size=0,
            dont_fragment=False,
            skip_dns_check=False
        )
        
        tr_list.append(traceroute)
        count += 1
        create_measurement(tr_list, source_list)
        # reset the tr_list
        tr_list = []
        
        if count == limit:
            # sleep for 15 minutes
            # 60 seconds * 15
            time.sleep(900)
            # reset the count
            count = 0
            
    
if __name__ == '__main__':
    main()
