def getPosition(lane,role):
    """
    Gets the position that was played given the lane and role
    If it's not one of the positions we're interested in, return 'NONE'
    Otherwise, return the position
    """
    if lane == 'TOP' and role == 'SOLO':
        return 'TOP'
    if lane in ['MID','MIDDLE'] and role == 'SOLO':
        return 'MID'
    if lane in ['BOT','BOTTOM'] and role == 'DUO_CARRY':
        return 'ADC'
    if lane in ['BOT','BOTTOM'] and role == 'DUO_SUPPORT':
        return 'SUP'
    if lane == 'JUNGLE':
        return 'JG'
    else:
        return 'NONE'

def filterMatches(matches, positions=None, champs=None, timeRange=None):
    """
    Given the set of matches, returns the match IDs under restrictions of time, roles, and champions

        positions - TOP, ADC, SUP, MID, JG
            if None, no restriction

        champs - set of champion ids
            if None, no restriction

        time - filters out everything not in a certain time range

        Returns a list of matchIDs
    """
    matchIDs = []
    for match in matches:
        if positions != None:
            if getPosition(match['lane'],match['role']) not in positions:
                continue
        if champs != None:
            if match['champion'] not in champs:
                continue
        if timeRange != None:
            if not (timeRange[0] <= int(match['timestamp']) < timeRange[1]):
                continue
        matchIDs.append(match['matchId'])
    return matchIDs

def getWinrate(API,gameDict,matchIDs,sid):
    """
    Returns the average win rate across all the matches specified in matchIDs
    If a match has not already been looked up, an API call will be made to look it up
    """
    if len(matchIDs) == 0:
        return None
    wins = 0
    for matchID in matchIDs:
        if not gameDict[matchID]:
            gameDict[matchID] = API.getMatch(matchID)
        match = gameDict[matchID]
        participantInfo = getParticipant(sid,match)
        team = participantInfo['teamId']
        if match['teams'][0]['teamId'] == team and match['teams'][0]['winner'] == True or\
                match['teams'][1]['teamId'] == team and match['teams'][1]['winner'] == True:
            wins += 1
    return float(wins) / len(matchIDs)

def getParticipant(sid, match):
    """
    Returns the Participant structure of the player with a given sid

    First, we find the participantId based on the sid
    Then we return the Participant with that participantId
    """
    pid = None
    for participant in match['participantIdentities']:
        if participant['player']['summonerId'] == sid:
            pid = participant['participantId']
            break
    if pid == None:
        print "unsuccessful at identifying location of player"
        exit()
    for participant in match['participants']:
        if participant['participantId'] == pid:
            return participant
