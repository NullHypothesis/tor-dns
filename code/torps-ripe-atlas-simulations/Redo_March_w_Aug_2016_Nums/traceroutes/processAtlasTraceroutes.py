import sys
import json
import shelve
from ripe.atlas.sagan import TracerouteResult
import requests
import pickle
import pyasn

'''
Make dictionary where
key = source AS as integer
value = another dictionary
    where
    key = destination IP address as string
    value = set of ASNs as ints (not strings)


    Usage: command-line args
    python processAtlasTraceroutes.py outPickleDictFileName asndb_file_name
    stdin: RIPE Atlas measurement ID(s)
    stdout: text version of output dictionary

Using Sagan:
Citation: http://ripe-atlas-sagan.readthedocs.io/en/latest/use.html
'''

def processMeasurement(mID, dic, asndb):
    #mID = '3703242' has two results in one measurement
    source = "https://atlas.ripe.net/api/v1/measurement-latest/" + mID
    response = requests.get(source).json()

    ip_set = set()
    
    for probe_id, result in response.items():
        result = result[0] # There's only one result for each probe
        parsed_result = TracerouteResult(result)

        source_ip = parsed_result.origin
        dest_ip = parsed_result.destination_address

        # convert source_ip to ASN
        (source_asn, source_prefix) = asndb.lookup(source_ip)
        if source_asn is None:
            continue        

        # get inner dict
        # create if it doesn't exist
        if source_asn not in dic:
            dic[source_asn] = {}

        inner_dic = dic[source_asn]

        # get ip set
        # create if it doesn't exist
        if dest_ip not in inner_dic:
            inner_dic[dest_ip] = set()

        as_path_set = inner_dic[dest_ip]
        ip_path_set = set()

        # Make set of IPs before converting to ASNs
        ip_path = parsed_result.ip_path
        for triple in ip_path:
            for ip in triple:
                if ip is not None:
                    ip_path_set.add(ip)


        # Explicity ADD source_ip and dest_ip to ip_path_set
        ip_path_set.add(source_ip)
        ip_path_set.add(dest_ip)

        # remove destination IP from IP set before converting
        #ip_path_set.discard(dest_ip)
        # remove source_ip from IP set
        #ip_path_set.discard(source_ip)

        # convert to AS and add ASes to set
        for ip in ip_path_set:
            (asn, prefix) = asndb.lookup(ip)
            #print asn
            if asn is not None:
                as_path_set.add(asn)       

        #print parsed_result.is_success # if traceroute completed successfully
        #print parsed_result.is_malformed
        #print parsed_result.is_error
        #print parsed_result.error_message


def main():
    # process command-line args
    dicFileName = sys.argv[1]
    dicFileName += '.pickle'

    asndb_file_name = sys.argv[2]
    asndb = pyasn.pyasn(asndb_file_name)
    
    # make empty dictionary
    dic = {}

    # Read in measurement IDs from stdin
    for mIDLine in sys.stdin:
        mID_str = mIDLine.rstrip()
        processMeasurement(mID_str, dic, asndb)

    print dic
    print len(dic)
    # pickle the dictionary
    with open(dicFileName, 'wb') as f:
        # Pickle the 'data' dictionary using the highest protocol available.
        pickle.dump(dic, f, pickle.HIGHEST_PROTOCOL)

        
if __name__ == '__main__':
    main()
