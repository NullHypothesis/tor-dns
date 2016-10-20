import pickle
import pyasn
import sys


'''
Make dict where key = TorPS sample #
value = another dict where
    key = timestamp
    value = intersection of ASes common to both entry path and exit AS of the Tor exit only
    if entry ip or exit ip not found, intersection = None
    if ASN conversion fails, None is returned for value
    if found and no intersection, return empty set
    
    Usage: command-line args
    python intersect.py guardTraceroutes.pickle nameOfOutPickleDict client_as asndb_file_name
    stdin: TorPS sim file
    stdout: text version of output pickle dict
'''


def get_intersection(client_as, guard_ip, exit_ip, guard_troutes_dic, asndb):
    # convert exit_ip to an ASN
    (exit_as, exit_prefix) = asndb.lookup(exit_ip)
    if exit_as is None:
        return None
        
    if client_as in guard_troutes_dic:
        guard_ip_dict = guard_troutes_dic[client_as]
        #dest_ip_dict = exit_dest_troutes_dic[exit_as]

        if guard_ip in guard_ip_dict:
            guard_as_set = guard_ip_dict[guard_ip]
            # new
            # guard_as_set.add(client_as) - REMOVED, should already be in there
            
            # exit AS set will contain AS of the Tor exit only
            exit_as_set = set()
            exit_as_set.add(exit_as)
            
            #print '--------------'
            return guard_as_set & exit_as_set
        else:
            #print '*************'
            return None
    else:
        #print '*************'
        return None
        


def parse_sim_str(sim_str):
    sim_list = sim_str.split()
    sample_num = int(sim_list[0])
    timestamp = float(sim_list[1]) # changed to float from int
    guard_ip = sim_list[2]
    exit_ip = sim_list[4]
    return (sample_num, timestamp, guard_ip, exit_ip)


def add_to_intersections_dict(sim_str, dic, guard_troutes_dic, client_as, asndb):
    (sample_num, timestamp, guard_ip, exit_ip) = parse_sim_str(sim_str)
    # print sample_num, timestamp, guard_ip, exit_ip
    
    # get inner dict
    # create if it doesn't exist
    if sample_num not in dic:
        dic[sample_num] = {}

    #inner_dict: key = timestamp, value = set of intersection of ASes common to both ends
    inner_dic = dic[sample_num]
    intersection_set = get_intersection(client_as, guard_ip, exit_ip, guard_troutes_dic, asndb)
    # Only add to dictionary if it's not None
    if intersection_set is not None: 
        inner_dic[timestamp] = intersection_set


def main():
    # process command-line args
    guard_troutes_fname = sys.argv[1]
    #exit_dest_troutes_fname = sys.argv[2]
    out_dic_fname = sys.argv[2]
    out_dic_fname += '.pickle'
    client_as = int(sys.argv[3]) # convert to int
    asndb_file_name = sys.argv[4]
    asndb = pyasn.pyasn(asndb_file_name)
    
    
    # open the two pickle files
    with open(guard_troutes_fname, 'rb') as f:
        # The protocol version used is detected automatically, so we do not
        # have to specify it.
        guard_troutes_dic = pickle.load(f)

    #print guard_troutes_dic.keys()
    #exit()

    #with open(exit_dest_troutes_fname, 'rb') as f:
    #    exit_dest_troutes_dic = pickle.load(f)

    #for val in exit_dest_troutes_dic.values():
    #    print val
    #exit()

    # make empty dictionary
    dic = {}

    # Read in TorPS sim from stdin
    # Need to skip the first line! TODO
    
    next(sys.stdin)
    for simLine in sys.stdin:
        sim_str = simLine.rstrip()
        add_to_intersections_dict(sim_str, dic, guard_troutes_dic, 
                                  client_as, asndb)

    print dic
    # pickle the dictionary
    with open(out_dic_fname, 'wb') as f:
        # Pickle the 'data' dictionary using the highest protocol available.
        pickle.dump(dic, f, pickle.HIGHEST_PROTOCOL)





if __name__ == '__main__':
    main()
