import pickle
import pyasn
import sys
#from enum import Enum


'''
Make dict where key = TorPS sample #
value = another dict where
    key = timestamp
    value = intersection of ASes common to both entry and exit paths
    if entry ip or exit ip not found, intersection = None
    if ASN conversion fails, None is returned for value
    if found and no intersection, return empty set

*** Tailored for ddptr
    
    Usage: command-line args
    python intersect.py guardTraceroutes.pickle exitTraceroutesToDestination.pickle--all_9_of_them nameOfOutPickleDict client_as asndb_file_name
    stdin: TorPS sim file
    stdout: text version of output pickle dict
'''


calendar_google = 0
docs_google = 1
facebook = 2
google = 3
instagram = 4
ixquick = 5
mail_google = 6
startpage = 7
twitter = 8


def get_intersection(client_as, guard_ip, exit_ip, guard_troutes_dic, exit_dest_troutes_dic, asndb):
    # convert exit_ip to an ASN
    (exit_as, exit_prefix) = asndb.lookup(exit_ip)
    if exit_as is None:
        return None
        
    if client_as in guard_troutes_dic and exit_as in exit_dest_troutes_dic:
        guard_ip_dict = guard_troutes_dic[client_as]
        dest_ip_dict = exit_dest_troutes_dic[exit_as]

        if guard_ip in guard_ip_dict:
            guard_as_set = guard_ip_dict[guard_ip]
            # new
            # guard_as_set.add(client_as)--removed, should be unnecessary
            
            # dest_ip_dict should have at most three keys
            # Join all the value sets together to make one giant set
            giant_dd_set = set()
            for s in dest_ip_dict.values():
                giant_dd_set = giant_dd_set | s
            #print giant_dd_set
            #print dest_ip_dict
            #print len(dest_ip_dict.values())
            #print dest_ip_dict.values()
            exit_as_set = giant_dd_set
            # new
            # exit_as_set.add(exit_as) -- removed, should be unnecessary
            
            #print exit_as_set
            #print '--------------'
            return guard_as_set & exit_as_set
        else:
            #print '*************'
            return None
    else:
        # NEW: Aug 2016 -- ISP fix/hack
        if client_as in guard_troutes_dic:
            guard_ip_dict = guard_troutes_dic[client_as]
            if guard_ip in guard_ip_dict:
                guard_as_set = guard_ip_dict[guard_ip]
                exit_as_set = set()
                exit_as_set.add(exit_as)
                return guard_as_set & exit_as_set
            else:
                return None
        else:
            return None

        #print '*************'
        return None
        


def parse_sim_str(sim_str):
    sim_list = sim_str.split()
    sample_num = int(sim_list[0])
    timestamp = float(sim_list[1]) # convert to float
    guard_ip = sim_list[2]
    exit_ip = sim_list[4]
    dest_ip = sim_list[5]
    return (sample_num, timestamp, guard_ip, exit_ip, dest_ip)



# Modified to handle 9 different websites, instead of 1
def add_to_intersections_dict(sim_str, dic, guard_troutes_dic, exit_site_dict, ip_to_site_dict, client_as, asndb):
    (sample_num, timestamp, guard_ip, exit_ip, dest_ip) = parse_sim_str(sim_str)
    # print sample_num, timestamp, guard_ip, exit_ip, dest_ip
    # NEW - had to actually add/use dest_ip
    # exit()

    # get inner dict
    # create if it doesn't exist
    if sample_num not in dic:
        dic[sample_num] = {}

    # NEW: Based on what the exit_ip is, pick the write exit_dest_troutes to pass to get_intersection function
    exit_dest_troutes_dic = exit_site_dict[ip_to_site_dict[dest_ip]]
    #print exit_dest_troutes_dic
    #print 'got over hurr'
    #exit()        

    #inner_dict: key = timestamp, value = set of intersection of ASes common to both ends
    inner_dic = dic[sample_num]
    intersection_set = get_intersection(client_as, guard_ip, exit_ip, guard_troutes_dic, exit_dest_troutes_dic, asndb)
    # Only add to dictionary if it's not None
    if intersection_set is not None:
        inner_dic[timestamp] = intersection_set


def main():
    # process command-line args
    guard_troutes_fname = sys.argv[1]

    exit_calendar_google_troutes_fname = sys.argv[2]
    exit_docs_google_troutes_fname = sys.argv[3]
    exit_facebook_troutes_fname = sys.argv[4]
    exit_google_troutes_fname = sys.argv[5]
    exit_instagram_troutes_fname = sys.argv[6]
    exit_ixquick_troutes_fname = sys.argv[7]
    exit_mail_google_troutes_fname = sys.argv[8]
    exit_startpage_troutes_fname = sys.argv[9]
    exit_twitter_troutes_fname = sys.argv[10]

    out_dic_fname = sys.argv[11]
    out_dic_fname += '.pickle'
    client_as = int(sys.argv[12]) # convert to int
    asndb_file_name = sys.argv[13]
    asndb = pyasn.pyasn(asndb_file_name)

    
    # open the pickle files
    with open(guard_troutes_fname, 'rb') as f:
        # The protocol version used is detected automatically, so we do not
        # have to specify it.
        guard_troutes_dic = pickle.load(f)

    #print guard_troutes_dic.keys()
    #exit()

    # 9 more to go!

    with open(exit_calendar_google_troutes_fname, 'rb') as f:
        exit_calendar_google_troutes_dic = pickle.load(f)

    #for val in exit_dest_troutes_dic.values():
    #    print val
    #exit()

    with open(exit_docs_google_troutes_fname, 'rb') as f:
        exit_docs_google_troutes_dic = pickle.load(f)

    with open(exit_facebook_troutes_fname, 'rb') as f:
        exit_facebook_troutes_dic = pickle.load(f)

    with open(exit_google_troutes_fname, 'rb') as f:
        exit_google_troutes_dic = pickle.load(f)

    with open(exit_instagram_troutes_fname, 'rb') as f:
        exit_instagram_troutes_dic = pickle.load(f)

    with open(exit_ixquick_troutes_fname, 'rb') as f:
        exit_ixquick_troutes_dic = pickle.load(f)

    with open(exit_mail_google_troutes_fname, 'rb') as f:
        exit_mail_google_troutes_dic = pickle.load(f)

    with open(exit_startpage_troutes_fname, 'rb') as f:
        exit_startpage_troutes_dic = pickle.load(f)

    with open(exit_twitter_troutes_fname, 'rb') as f:
        exit_twitter_troutes_dic = pickle.load(f)

    # Make dictionary with key = global int from above
    # and corresponding dict as the value
    
    exit_site_dict = {}
    exit_site_dict[calendar_google] = exit_calendar_google_troutes_dic
    exit_site_dict[docs_google] = exit_docs_google_troutes_dic
    exit_site_dict[facebook] = exit_facebook_troutes_dic
    exit_site_dict[google] = exit_google_troutes_dic
    exit_site_dict[instagram] = exit_instagram_troutes_dic
    exit_site_dict[ixquick] = exit_ixquick_troutes_dic
    exit_site_dict[mail_google] = exit_mail_google_troutes_dic
    exit_site_dict[startpage] = exit_startpage_troutes_dic
    exit_site_dict[twitter] = exit_twitter_troutes_dic



    # Make IP - site name dict
    # key = ip address (the dest_ip above), value = global int from above
    # this mapping comes from final_model.py in torps dir
    ip_to_site_dict = {}

    ip_to_site_dict['209.85.232.101'] = calendar_google
    ip_to_site_dict['172.217.3.14'] = docs_google
    ip_to_site_dict['173.252.120.68'] = facebook
    ip_to_site_dict['209.85.232.105'] = google
    ip_to_site_dict['31.13.71.52'] = instagram
    ip_to_site_dict['64.71.134.54'] = ixquick
    ip_to_site_dict['216.58.219.197'] = mail_google
    ip_to_site_dict['64.71.134.46'] = startpage
    ip_to_site_dict['199.16.156.6'] = twitter
    
    # testing
    #print ip_to_site_dict
    #print exit_site_dict[ip_to_site_dict['216.58.219.197']]
    #exit()


    # make empty dictionary
    dic = {}

    # Read in TorPS sim from stdin
    # Need to skip the first line!
    #count = 0
    next(sys.stdin)
    for simLine in sys.stdin:
        sim_str = simLine.rstrip()
        add_to_intersections_dict(sim_str, dic, guard_troutes_dic, exit_site_dict, 
                                  ip_to_site_dict, 
                                  client_as, asndb)
        #count += 1
        #if count == 10:
        #    break
    
    print dic
    # pickle the dictionary
    with open(out_dic_fname, 'wb') as f:
        # Pickle the 'data' dictionary using the highest protocol available.
        pickle.dump(dic, f, pickle.HIGHEST_PROTOCOL)





if __name__ == '__main__':
    main()
