import os.path
import pickle
CACHE_DIR = 'cache/{sid}.p'
def readCache(sid):
    """
    Attempts to read the cached results of summoner sid
    If there's no cache, returns None
    """
    fname = CACHE_DIR.format(sid=sid)
    if os.path.isfile(fname):
        return pickle.load(open(fname,'rb'))
    else:
        return None

def writeCache(sid,gameDict):
    """
    Writes the games of a given summoner to disk
    """
    fname = CACHE_DIR.format(sid=sid)
    pickle.dump(gameDict,open(fname,"wb"))
