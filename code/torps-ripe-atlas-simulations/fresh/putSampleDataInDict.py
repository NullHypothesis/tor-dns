from thePickles import *

# read both path dicts in
asPathsFrom3320ToTorGuardsDict = getPickledData('./asPathsToTorGuardsForward/asPathsFrom3320ToTorGuards.pickle')
asPathsToTypDestsForwardDict = getPickledData('./asPathsToTypicalDestsForward/asPathsToTypDestsForwardDict.pickle')

# Need my IP 2 AS dicts in here
# In future, could rely on pyASN and do away with these
# compute on the fly
exitIP2ASDict = getPickledData('./exitIPsToASes/exitIP2ASDict.pickle')
guardIP2ASDict = getPickledData('./guardIPsToASes/guardIP2ASDict.pickle')
typIPToASDict = getPickledData('./typicalIPsToASes/typIPToASDict.pickle')


torps_filename = './torpsSims/typical_1000_December_15.txt'

# key = sample number, value = another dict with
# key = time, value = tuple (forwardASPathEntrySet, forwardASPathExitSet)
samplesDict = {}


sample_index = 0
timestamp_index = 1
guard_ip_index = 2
exit_ip_index = 4
dest_ip_index = 5


samplesFile = open(torps_filename)
# skip the first line in the file
next(samplesFile)

count = 0
guard_error_count = 0
exit_error_count = 0
times_through = 0
exit_ip_count = 0
no_destIP_inTypIP_dict = 0

for line in samplesFile:
    times_through += 1
    #print line
    lineList = line.split()
    sample = lineList[sample_index]
    timestamp = lineList[timestamp_index]
    guard_ip = lineList[guard_ip_index]
    exit_ip = lineList[exit_ip_index]
    dest_ip = lineList[dest_ip_index]
    #print sample, timestamp, guard_ip, exit_ip, dest_ip


    # if first time, make new dict as value
    if sample not in samplesDict:
        samplesDict[sample] = {}
        count += 1

    # now insert tuple as value: index 0 = guard path, index 1 = exit AS path
    innerDict = samplesDict[sample]
    guardASPath = set()
    try:
        guardASPath = asPathsFrom3320ToTorGuardsDict[guardIP2ASDict[guard_ip]]
    except KeyError as e:
        #print "Key error in guardIP2ASDict"
        guard_error_count += 1
    #print guardASPath
    #print typIPToASDict[dest_ip]
    exitASPath = set()

    try:
        exitAS = exitIP2ASDict[exit_ip]
        try:
            typDestAS = typIPToASDict[dest_ip]

            try:
                dictTwo = asPathsToTypDestsForwardDict[exitAS]

                try:
                    #print typDestAS
                    #print str(typDestAS)
                    exitASPath = dictTwo[str(typDestAS)]
                except KeyError as e:
                    print 'did not find typDestAS in dictTwo'

            except KeyError as e:
                print 'did not find exitAS in asPathsToTypDestsForwardDict'
            

        except KeyError as e:
            print 'did not find dest IP in typIPToASDict'
            no_destIP_inTypIP_dict += 1

    except KeyError as e:
        print 'did not find exit IP in exitIP2ASDict'
        exit_ip_count += 1
        
    innerDict[timestamp] = (guardASPath, exitASPath)
    #break

print samplesDict
print len(samplesDict)
print count

print times_through, guard_error_count, exit_error_count
print no_destIP_inTypIP_dict, exit_ip_count
