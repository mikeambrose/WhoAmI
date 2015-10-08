import apiRequest
import getStats
import time
import datetime
import caching
import visualizeStats

API = apiRequest.APICalls(open('apikey.txt').read())
name = 'fortis831'
sid = API.getSID(name)
matches = API.getMatchList(sid)
gameDict = {}
for match in matches:
    gameDict[match['matchId']] = None
cachedMatches = caching.readCache(sid)
if cachedMatches:
    for match in cachedMatches:
        assert match in gameDict
        gameDict[match] = cachedMatches[match]
def roleStats(sid,API,matches,gameDict):
    t = time.time()
    winrateDict = {}
    for role in ["TOP","MID","JG","ADC","SUP","NONE"]:
        roleGames = getStats.filterMatches(matches, positions=[role])
        winrateDict[role] = getStats.getWinrate(API,gameDict,roleGames,sid)
    print "{0} seconds elapsed for this query".format(time.time() - t)
    return winrateDict

def champStats(sid,API,matches,gameDict,minChampGames=10):
    t = time.time()
    winrateDict = {}
    for champId in API.idToChamp:
        champGames = getStats.filterMatches(matches,champs=[champId])
        if len(champGames)>minChampGames:
            winrateDict[API.idToChamp[champId]] = getStats.getWinrate(API,gameDict,champGames,sid)
    print "{0} seconds elapsed for this query".format(time.time() - t)
    return winrateDict

def timeStats(sid,API,matches,gameDict,buckets=4):
    timestamps = [match['timestamp'] for match in matches]     
    cutoffs = [i*(len(timestamps)-1)/buckets for i in range(buckets+1)][::-1]
    hist = {}
    #every cutoff but the last one has a histogram bucket
    for i in range(len(cutoffs)-1):
        cutoff,nextCutoff = timestamps[cutoffs[i]],timestamps[cutoffs[i+1]]
        histMatches = getStats.filterMatches(matches,timeRange=(cutoff,nextCutoff))
        hist[datetime.datetime.fromtimestamp(cutoff/1000.0)] = getStats.getWinrate(API,gameDict,histMatches,sid)
    return hist

timeHist = timeStats(sid,API,matches,gameDict,6)
#caching.writeCache(sid,gameDict)
visualizeStats.writeTimeOutput("output/testOutput.html",timeHist)
