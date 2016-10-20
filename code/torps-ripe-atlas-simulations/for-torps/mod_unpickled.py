##### Process traces #####

# Turn trace streams with destination ip *.exit into resolve requests
# Filter out requests to same /24 and port within max_circuit_dirtiness/2
from pathsim import *
import cPickle as pickle
import sys

#if len(sys.argv) != 3: print "USAGE: " + sys.argv[0] + " in/users.traces.pickle out/users.traces.processed.pickle";sys.exit()

#in_tracefile = sys.argv[1]#'in/traces.pickle'
#out_tracefile = sys.argv[2]#'in/traces_processed.pickle'
with open('in/users2-processed.traces.pickle') as f:
    obj = pickle.load(f)


print obj

models = ["facebook" , "gmailgchat", "gcalgdocs", "websearch", "irc",\
    "bittorrent"]
max_circuit_dirtiness = 10*60
cover_time = float(max_circuit_dirtiness)/2
for key in models:
    model_trace = obj.trace[key]
    new_model_trace = []
    ip_port_seen = {}
    for stream in model_trace:
        if ('.exit' not in stream[1]):
            # remove streams that duplicate an ip/24:port seen recently
            ip_split = stream[1].split('.')
            ip_24 = '.'.join(ip_split[0:3])
            ip_port = ip_24 + ':' + str(stream[2])
            if (ip_port in ip_port_seen) and\
                (stream[0] - ip_port_seen[ip_port] < cover_time):
                continue
            else:
                ip_port_seen[ip_port] = stream[0]
                new_model_trace.append(stream)
        else:
            ip_split = stream[1].split('.')
            new_ip = '.'.join(ip_split[0:4])
            new_model_trace.append((stream[0], new_ip, 0))
    obj.trace[key] = new_model_trace



print 'facebook'
#print obj.trace["facebook"]
faceList = obj.trace["facebook"]
#for tup in faceList:
#    print tup[1]
print faceList
print ''

print 'gmailgchat'
gmailList =  obj.trace["gmailgchat"]
#for tup in gmailList:
#    print tup[1]
print gmailList
print ''

print 'gcalgdocs'
gcalList = obj.trace["gcalgdocs"]
#for tup in gcalList:
#    print tup[1]
print gcalList
print ''

print 'websearch'
websearchList =  obj.trace["websearch"]
#for tup in websearchList:
#    print tup[1]
print websearchList
print ''


exit()
# pickle ipSet up
with open('/u/laurar/myproj/fresh/typicalIPsToASes/setOfTypicalDestIPs.pickle', 'wb') as f:
    # Pickle the ipSet using the highest protocol available.
    pickle.dump(ipSet, f, pickle.HIGHEST_PROTOCOL)
