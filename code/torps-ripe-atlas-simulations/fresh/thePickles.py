import pickle

def getPickledData(pFileName):
    with open(pFileName, 'rb') as f:
        # The protocol version used is detected automatically, so we do not
        # have to specify it.
        data = pickle.load(f)
        f.close()
        return data
