import json
import urllib2

#for testing purposes
pid = 19810260
oid = 47290381

apikey = None
def getMatchHistory(sid, apikey=None):
    if not apikey:
        apikey = open('apikey.txt').read().replace('\n','')
    fetchLink = "https://na.api.pvp.net/api/lol/na/v2.2/matchhistory/{sid}?api_key={apikey}".format(sid=sid,apikey=apikey)
    matchHistory = json.load(urllib2.urlopen(fetchLink))['matches']
    return matchHistory
