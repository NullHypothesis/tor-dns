##### Process traces #####

# Turn trace streams with destination ip *.exit into resolve requests
# Filter out requests to same /24 and port within max_circuit_dirtiness/2
from pathsim import *
import cPickle as pickle
import sys


################
# Usage:
# python progname their_processed_tracefile my_modified_tracefile_name.pickle

################


their_procd_tracefile = sys.argv[1]
my_mod_tracefile = sys.argv[2]

with open(their_procd_tracefile) as f:
    obj = pickle.load(f)

models = ["facebook" , "gmailgchat", "gcalgdocs", "websearch", "irc",\
    "bittorrent"]

for key in models:
    print key
    print obj.trace[key]
    #print obj
    #print obj.trace


print ''
print obj.trace["irc"]
obj.trace["irc"] = [(0.0, '3.3.3.3', 0)]
print obj.trace["irc"]

# Fix bittorrent
print obj.trace["bittorrent"]
obj.trace["bittorrent"] = [(0.0, '4.4.4.4', 0)]

###########################################################################


# fix Facebook
print obj.trace["facebook"]
# facebook = 173.252.120.68  # from ripe atlas traceroutes
# instagram = 31.13.71.52
obj.trace["facebook"] = [(0.0, '173.252.120.68', 443), (195.720000029, '31.13.71.52', 443)]


# fix gdocs and gcal
print obj.trace["gcalgdocs"]
# gdocs = 172.217.3.14
# gcal = 209.85.232.101
obj.trace["gcalgdocs"] = [(0.0, '172.217.3.14', 443), (476.339999914, '209.85.232.101', 443)]
# Need separate IPs for each site


# Gmail and Twitter
print obj.trace["gmailgchat"]
# Gmail = 216.58.219.197
# twitter = 199.16.156.6
obj.trace["gmailgchat"] = [(0.0, '216.58.219.197', 443), (92.9600000381, '199.16.156.6', 443)]


# Finally, fix websearch category based on their traces
# www.ixquick.com, 443 = 64.71.134.54
# www.google.com, 443 = 209.85.232.105
# www.startpage.com, 443 = 64.71.134.46
obj.trace["websearch"] = [(0.0, '64.71.134.54', 443), (232.929999828, '209.85.232.105', 443), (684.399999857, '64.71.134.46', 443)]



# would like to add twitter and instagram to repace gdocs and gcal, move gcal to gmail
# so have gmail/gcal category
# and have twitter and instagram category


print 'AFTER MY MODS --------------------------------------------'
for key in models:
    print key
    print obj.trace[key]


with open(my_mod_tracefile, 'wb') as f:
    pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)
##########    
