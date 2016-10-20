import pickle
import pyasn
import sys


'''
Make dict where key = TorPS sample #
value = another dict where
    key = timestamp
    value = intersection of ASes common to both entry and exit paths
    if entry ip or exit ip not found, intersection = None
    if ASN conversion fails, None is returned for value
    if found and no intersection, return empty set

*** Modified for handling 3rd party resolvers
*** FYI: the final_exit_ip_to_one_resolver_list_dict_pickle maps exit ips to resolvers
    Where key = value, it means that exit does its own resolution
    I don't explicitly check for that when I'm looking at dest_ip_dict
    because I never ran traceroutes to any of the exit IP addresses
    Otherwise, if key != value, value = a 3rd-party resolver that was randomly chosen

    Need to also supply the 8.8.8.8 database as a command-line arg because I excluded the 8.8.8.8 traceroutes
    because I didn't want to run them again
    The 8.8.8.8 traceroutes dict is added to the exitTraceroutesToDestination dict
    
    Usage: command-line args
    python intersect.py guardTraceroutes.pickle exitTraceroutesToDestination_3rd_party.pickle
           final_exit_ip_to_one_resolver_list_dict_pickle_fname
           forward_exit_ASes_to_8888_dict_fname forward_exit_ASes_ddptr_dict_fname_all_9_of_them
           nameOfOutPickleDict client_as asndb_file_name 
           
    stdin: TorPS sim file
    stdout: text repr. of output dict
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


def get_intersection(client_as, guard_ip, exit_ip, guard_troutes_dic, exit_dest_troutes_dic, asndb, 
                     final_exit_ip_to_one_resolver_list_dict, forward_exit_ASes_ddptr_dict):
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
            # guard_as_set.add(client_as) -- removed, should be unnecessary
            
            # *** New for 3rd party:
            if exit_ip in final_exit_ip_to_one_resolver_list_dict:
                #print exit_ip
                exit_resolver_ip_set = final_exit_ip_to_one_resolver_list_dict[exit_ip]
                # Safety check because exit_resolver_ip_set should have exactly one value
                if len(exit_resolver_ip_set) != 1:
                    raise ValueError('exit_resolver_ip_set should contain exactly 1 ip string')
                
                # Citation: http://stackoverflow.com/questions/1619514/how-to-extract-the-member-from-single-member-set-in-python
                (exit_resolver_ip,) = exit_resolver_ip_set
                
                if exit_resolver_ip in dest_ip_dict:
                    exit_as_set = dest_ip_dict[exit_resolver_ip]
                    # new
                    # exit_as_set.add(exit_as) -- removed, should be unnecessary
            
                    #print '--------------'
                    return guard_as_set & exit_as_set
                else:
                    # exit does its own resolution so key and value should match - this is the most likely
                    # reason to enter this block
                    # another reason could be that the traceroute is simply missing - RIPE Atlas didn't do it
                    #print exit_ip, exit_resolver_ip
                    #print '$$$$$$$$'

                    # *** New for whole enchilada
                    # Handle own resolution by incorporating ddptr results in here
                    if exit_ip == exit_resolver_ip:
                        # this exit does its own resolution
                        
                        #print exit_as
                        #if exit_as == 56322:
                        #    return None
                        #print 'getting to here!'
                        
                        # new: added this because of 56322
                        if exit_as not in forward_exit_ASes_ddptr_dict:
                            #print 'in here'
                            return None
                        #print 'getting to here!'
                        
                        dest_ip_ddptr_dict = forward_exit_ASes_ddptr_dict[exit_as]
                        # dest_ip_dict/dest_ip_ddptr_dict should have at most three keys (for nymity specifically)
                        # Join all the value sets together to make one giant set
                        #print len(dest_ip_ddptr_dict)
                        giant_dd_set = set()
                        for s in dest_ip_ddptr_dict.values():
                            giant_dd_set = giant_dd_set | s
                        #print len(dest_ip_ddptr_dict.values())
                        exit_as_set = giant_dd_set
                        # new
                        # exit_as_set.add(exit_as) -- removed, should be unnecessary

                        #print '=============='
                        return guard_as_set & exit_as_set
                    else:
                        return None
            else:
                # exit ip not in Philipp's mapping.py
                #print '******'
                return None
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
    timestamp = float(sim_list[1]) # changed to float from int
    guard_ip = sim_list[2]
    exit_ip = sim_list[4]
    dest_ip = sim_list[5]
    return (sample_num, timestamp, guard_ip, exit_ip, dest_ip)


def add_to_intersections_dict(sim_str, dic, guard_troutes_dic, exit_dest_troutes_dic, client_as, asndb, 
                              final_exit_ip_to_one_resolver_list_dict, 
                              exit_site_dict, ip_to_site_dict):
    (sample_num, timestamp, guard_ip, exit_ip, dest_ip) = parse_sim_str(sim_str)
    # print sample_num, timestamp, guard_ip, exit_ip
    
    # get inner dict
    # create if it doesn't exist
    if sample_num not in dic:
        dic[sample_num] = {}

    # NEW: Based on what the exit_ip is, pick the write ddptr routes to pass to get_intersection function
    forward_exit_ASes_ddptr_dict = exit_site_dict[ip_to_site_dict[dest_ip]]

    #inner_dict: key = timestamp, value = set of intersection of ASes common to both ends
    inner_dic = dic[sample_num]
    intersection_set = get_intersection(client_as, guard_ip, exit_ip, guard_troutes_dic, exit_dest_troutes_dic, asndb, 
                                            final_exit_ip_to_one_resolver_list_dict, forward_exit_ASes_ddptr_dict)
    # Only add to dictionary if it's not None
    if intersection_set is not None:
        inner_dic[timestamp] = intersection_set


# Changes first argument
def add_8888_trs_to_3rd_party_dict(exit_dest_troutes_dic, forward_exit_ASes_to_8888_dict):
    for asn_8888 in forward_exit_ASes_to_8888_dict:
        if asn_8888 in exit_dest_troutes_dic:
            exit_inner_dict = exit_dest_troutes_dic[asn_8888]
            eight_inner_dict = forward_exit_ASes_to_8888_dict[asn_8888]
            # Should only by one key, and that key should = '8.8.8.8'
            for eight_ip in eight_inner_dict:
                # Safety check - Should NEVER happen
                if eight_ip in exit_inner_dict:
                    raise ValueError('8.8.8.8 should NOT be in exit_inner_dict already')
                #print key
                # Add 8.8.8.8 trs AS set to exit_inner_dict
                exit_inner_dict[eight_ip] = eight_inner_dict[eight_ip]
        else:
            exit_dest_troutes_dic[asn_8888] = forward_exit_ASes_to_8888_dict[asn_8888]


def main():
    # process command-line args
    guard_troutes_fname = sys.argv[1]
    exit_dest_troutes_fname = sys.argv[2] #3rd-party traceroute results

    # new for 3rd party sitch
    final_exit_ip_to_one_resolver_list_dict_fname = sys.argv[3]
    forward_exit_ASes_to_8888_dict_fname = sys.argv[4]

    # ddptrs
    exit_calendar_google_troutes_fname = sys.argv[5]
    exit_docs_google_troutes_fname = sys.argv[6]
    exit_facebook_troutes_fname = sys.argv[7]
    exit_google_troutes_fname = sys.argv[8]
    exit_instagram_troutes_fname = sys.argv[9]
    exit_ixquick_troutes_fname = sys.argv[10]
    exit_mail_google_troutes_fname = sys.argv[11]
    exit_startpage_troutes_fname = sys.argv[12]
    exit_twitter_troutes_fname = sys.argv[13]

    out_dic_fname = sys.argv[14]
    out_dic_fname += '.pickle'
    client_as = int(sys.argv[15]) # convert to int
    asndb_file_name = sys.argv[16]
    asndb = pyasn.pyasn(asndb_file_name)
    
        
    # open all the pickle files
    with open(guard_troutes_fname, 'rb') as f:
        # The protocol version used is detected automatically, so we do not
        # have to specify it.
        guard_troutes_dic = pickle.load(f)

    with open(exit_dest_troutes_fname, 'rb') as f:
        exit_dest_troutes_dic = pickle.load(f)

    # Open the 9 ddptr files
    with open(exit_calendar_google_troutes_fname, 'rb') as f:
        exit_calendar_google_troutes_dic = pickle.load(f)

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


    # New for 3rd party sitch - open pickle file
    with open(final_exit_ip_to_one_resolver_list_dict_fname, 'rb') as f:
        final_exit_ip_to_one_resolver_list_dict = pickle.load(f)

    with open(forward_exit_ASes_to_8888_dict_fname, 'rb') as f:
        forward_exit_ASes_to_8888_dict = pickle.load(f)

    #print len(exit_dest_troutes_dic)
    #print len(forward_exit_ASes_to_8888_dict)

    # Specical for 3rd party sitch
    # Add forward_exit_ASes_to_8888_dict to exit_dest_troutes_dic
    add_8888_trs_to_3rd_party_dict(exit_dest_troutes_dic, forward_exit_ASes_to_8888_dict)
    #print exit_dest_troutes_dic
    #print len(exit_dest_troutes_dic)
    #exit()

    # make empty dictionary
    dic = {}

    # Read in TorPS sim from stdin
    # Need to skip the first line! TODO
    #count = 0
    next(sys.stdin)
    for simLine in sys.stdin:
        sim_str = simLine.rstrip()
        add_to_intersections_dict(sim_str, dic, guard_troutes_dic, exit_dest_troutes_dic, 
                                  client_as, asndb, final_exit_ip_to_one_resolver_list_dict, 
                                  exit_site_dict, ip_to_site_dict)
        #count += 1
        #if count == 10:
        #    break

    print dic
    # pickle the dictionary
    with open(out_dic_fname, 'wb') as f:
        # Pickle the 'data' dictionary using the highest protocol available.
        pickle.dump(dic, f, pickle.HIGHEST_PROTOCOL)


def test_code():
    # Test add_8888_trs_to_3rd_party_dicts function
    inner_dic1_a = {'blah': 4, 'nah': 6}
    inner_dic1_b = {'ok': 5}
    dic1 = {1:inner_dic1_a, 2:inner_dic1_b}
    print 'dic1 = '
    print dic1

    inner_dic2_a = {'8': 7}
    inner_dic2_b = {'8': 0}
    inner_dic2_c = {'8': 3}
    dic2 = {1:inner_dic2_a, 2:inner_dic2_b, 3:inner_dic2_c}
    print 'dic2 = '
    print dic2
    
    inner1 = {'blah': 4, 'nah':6, '8': 7}
    inner2 = {'ok': 5, '8':0}
    inner3 = inner_dic2_c
    print 'dic_I_expect'
    dic_I_expect = {1:inner1, 2:inner2, 3:inner3}
    print dic_I_expect
    
    add_8888_trs_to_3rd_party_dict(dic1, dic2)
    dic_I_got = dic1
    print 'dic_I_got'
    print dic_I_got
    


if __name__ == '__main__':
    #test_code()
    
    main()
