import json
import urllib2
import time
import datetime

#for testing purposes
pid = 19810260
oid = 47290381

CALLS_PER_10S = 10
CALLS_PER_5M = 500
#extra delay when we're near the limit
EXTRA_DELAY = 0.1


class APICalls:
    """
    A class used to respect the API limits of Riot Games
    The constants PER10S and PER5M reflect how many calls can occur during the time period 
    If a call cannot be made, the program will halt until it can be made
    Each API call must being with a self._callCheck() and self._addCall()

    The public-facing interface involves the actual API calls
        getMatchHistory - gets the match history for all ranked queues for a given summoner        
    """
    def __init__(self,apikey):
        """
        Initializes the API calling mechanism with the given apikey
        """
        #ordered list of datetime objects which keep track of the most recent calls
        #pruned by _callCheck
        #added to by _addCall
        self._calls = [] 
        self._apikey = apikey
        self.idToChamp, self.champToID = self.getChampionIDDicts()

    def _callCheck(self,debug=False):
        """
        Waits for as long as needed to execute a call

        Begins by clearing the self._calls cache of anything that's been called more than 5 minutes ago
        Then checks if that is legal and, if not, waits until the call closest to 5m ago times out
        Then filters for <10s ago and checks if a call would be legal
            and again, if not, waits until the call closest to 10s ago times out
        Returns the amount of time waited
        """
        timeWaited = 0
        #pruning last 5 minutes
        currentTime = datetime.datetime.now()
        while len(self._calls) != 0:
            timeDelta = (currentTime - self._calls[0]).seconds
            #if the call occurred more than 5 minutes ago, remove it
            if timeDelta > 300:
                del self._calls[0]
            #otherwise we've eliminated all the oldest calls
            else:
                break

        #check how many calls have been made in 5 minutes
        if len(self._calls) >= CALLS_PER_5M:
            #the time we wait is 5 minutes minus the time we've already waited
            #plus a delay to make sure computation/transmission times don't screw things up
            timeWait = 300 - (currentTime - self._calls[0]).seconds + EXTRA_DELAY
            if debug:
                print "sleeping for {0} seconds until 5 minute restriction is up".format(timeWait)
            else:
                time.sleep(timeWait)
            timeWaited += timeWait

        #count how many calls have been made in 10 seconds
        last10sCalls = 0
        #the call which occurred closest to 10s ago (helps us decide how long to wait)
        closest10sCall = None
        #iterate through calls backwards
        for i in range(-1,-len(self._calls)-1,-1):
            if (currentTime - self._calls[i]).seconds < 10:
                last10sCalls += 1
                closest10sCall = self._calls[i]
            else:
                break

        #check if we can make more calls
        if last10sCalls >= CALLS_PER_10S:
            #the time we wait is 10 seconds minus the time we've already waited
            #plus a delay to make sure computation/transmission times don't screw things up
            timeWait = 10 - (currentTime-closest10sCall).seconds + EXTRA_DELAY
            if debug:
                print "sleeping for {0} seconds until 10 second restriction is up".format(timeWait)
            else:
                time.sleep(timeWait)
            timeWaited += timeWait

        return timeWaited

    def _addCall(self):
        """
        Adds the current call to the list of calls made
        """
        self._calls.append(datetime.datetime.now())

    def getMatchList(self,sid):
        self._callCheck(); self._addCall()
        fetchLink ="https://na.api.pvp.net/api/lol/na/v2.2/matchlist/by-summoner/{sid}?api_key={apikey}"\
                        .format(sid=sid,apikey=self._apikey)
        matchList = json.load(urllib2.urlopen(fetchLink))['matches']
        return matchList
    
    def getSID(self,name):
        self._callCheck(); self._addCall()
        fetchLink = "https://na.api.pvp.net/api/lol/na/v1.4/summoner/by-name/{name}?api_key={apikey}"\
                        .format(name=name,apikey=self._apikey)
        summonerInfo = json.load(urllib2.urlopen(fetchLink))[name]
        return summonerInfo['id']
    
    def getChampionIDDicts(self):
        #no need to run _callCheck() or _addCall() because static calls don't count
        fetchLink = "https://global.api.pvp.net/api/lol/static-data/na/v1.2/champion?api_key={apikey}"\
                        .format(apikey=self._apikey)
        champInfo = json.load(urllib2.urlopen(fetchLink))['data']
        idToChamp = {}
        champToID = {}
        for champ in champInfo:
            champToID[champ] = champInfo[champ]['id']
            idToChamp[champInfo[champ]['id']] = champ
        return idToChamp, champToID

    def getMatch(self,matchID):
        self._callCheck(); self._addCall()
        fetchLink = "https://na.api.pvp.net/api/lol/na/v2.2/match/{matchid}?includeTimeline=false&api_key={apikey}"\
                        .format(matchid=matchID,apikey=self._apikey)
        matchInfo = json.load(urllib2.urlopen(fetchLink))
        return matchInfo
