import apiRequest
import getStats
import time

API = apiRequest.APICalls(open('apikey.txt').read())
name = 'penguin8r' sid = API.getSID(name) matches = API.getMatchList(sid)
gameDict = {}
for match in matches:
    gameDict[match['matchId']] = None
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

